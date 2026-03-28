import sys
import subprocess
import os
import json
import sqlite3
import tempfile

# ── Auto-install missing packages ──────────────────────────────────────────────
try:
    from flask import Flask, request, jsonify, send_from_directory
    import requests as http
    from dotenv import load_dotenv
    import google.generativeai as genai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "flask", "requests", "python-dotenv", "google-generativeai"])
    from flask import Flask, request, jsonify, send_from_directory
    import requests as http
    from dotenv import load_dotenv
    import google.generativeai as genai

# Use absolute path so .env is always found regardless of working directory
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(_BASE_DIR, ".env"), override=True)

app = Flask(__name__, static_folder='static')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ── Database Setup ────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("session_history.db")
    cur  = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS seen_questions (
                       id            INTEGER PRIMARY KEY AUTOINCREMENT,
                       question_text TEXT UNIQUE)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS user_progress (
                       id             INTEGER PRIMARY KEY,
                       problems_solved INTEGER DEFAULT 0,
                       accuracy        REAL    DEFAULT 0.0,
                       weak_topics     TEXT    DEFAULT 'System Design, Graphs')''')
    cur.execute("INSERT OR IGNORE INTO user_progress (id) VALUES (1)")
    conn.commit()
    conn.close()

init_db()

# ── Gemini Helper ─────────────────────────────────────────────────────────────
def ask_ai(messages, json_mode=False):
    """Call Google Gemini and return the assistant's reply text. Raises on error."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in your .env file.")

    system_msg = next((m["content"] for m in messages if m["role"] == "system"), None)
    prompt = "\n".join(m["content"] for m in messages if m["role"] != "system")

    model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=system_msg)
    
    generation_config = {"response_mime_type": "application/json"} if json_mode else None
    resp = model.generate_content(prompt, generation_config=generation_config)
    
    return resp.text

# ── Routes: Static Pages ──────────────────────────────────────────────────────
@app.route("/")
def landing():
    return send_from_directory("static", "landing.html")

@app.route("/app")
def main_app():
    return send_from_directory("static", "index.html")

# ── API: Diagnostic Test ──────────────────────────────────────────────────────
@app.route("/api/test")
def api_test():
    try:
        reply = ask_ai([{"role": "user", "content": "Say 'API connected!' and nothing else."}])
        return jsonify({"status": "✅ SUCCESS", "key_prefix": GEMINI_API_KEY[:15] + "...", "reply": reply})
    except Exception as e:
        return jsonify({"status": "❌ FAILED", "error": str(e), "key_set": bool(GEMINI_API_KEY)})

# ── API: Generate Questions ───────────────────────────────────────────────────
@app.route("/api/generate", methods=["POST"])
def generate_questions():
    data       = request.get_json()
    topic      = data.get("topic",      "Data Structures")
    difficulty = data.get("difficulty", "All")
    language   = data.get("language",   "Python")

    conn = sqlite3.connect("session_history.db")
    cur  = conn.cursor()
    cur.execute("SELECT question_text FROM seen_questions ORDER BY id DESC LIMIT 50")
    seen = [r[0] for r in cur.fetchall()]

    diff_hint = (f" Only {difficulty} difficulty." if difficulty != "All"
                 else " Mix Easy, Medium, Hard.")
    seen_hint = (f"\nDO NOT repeat: {json.dumps(seen)}\n" if seen else "")

    system_msg = ("You are a tech-interview question generator. "
                  "Output ONLY valid JSON — no markdown, no prose. "
                  "Root key must be 'questions', an array of 5 objects.")
    user_msg   = (
        f"Generate 5 FAANG-style questions on: '{topic}'.{diff_hint}{seen_hint}"
        " Each object needs: id (int), difficulty ('Easy'|'Medium'|'Hard'), "
        "question (str), is_most_repeated (bool), hint (str), "
        f"logic_suggestion (str), solution (str with {language} code in ```{language.lower()} blocks)."
    )

    try:
        raw = ask_ai(
            [{"role": "system", "content": system_msg},
             {"role": "user",   "content": user_msg}],
            json_mode=True
        )
        # Strip any accidental markdown fences
        clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        parsed = json.loads(clean)
        questions = parsed.get("questions", parsed) if isinstance(parsed, dict) else parsed

        for q in questions:
            if "question" in q:
                try:
                    cur.execute("INSERT INTO seen_questions (question_text) VALUES (?)", (q["question"],))
                except sqlite3.IntegrityError:
                    pass
        conn.commit()
        conn.close()
        return jsonify({"questions": questions})

    except Exception as e:
        conn.close()
        return jsonify({"detail": f"Failed to fetch from Gemini API. Error: {e}"}), 500

# ── API: Run Python Code (Sandbox) ────────────────────────────────────────────
@app.route("/api/run_code", methods=["POST"])
def run_code():
    data     = request.get_json()
    language = data.get("language", "Python")
    code     = data.get("code", "")
    tests    = data.get("test_cases", "")

    if language.lower() != "python":
        return jsonify({"output": "Only Python sandbox is supported currently.", "error": True})

    src = code + "\n\n" + tests
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8") as f:
        f.write(src)
        tmp = f.name

    try:
        import subprocess as sp
        result = sp.run([sys.executable, tmp], capture_output=True, text=True, timeout=5)
        complexity = "O(N) or worse" if ("for " in code or "while " in code) else "O(1)"
        return jsonify({"output": result.stdout, "error": result.stderr, "complexity": complexity})
    except sp.TimeoutExpired:
        return jsonify({"output": "", "error": "Time Limit Exceeded (TLE) — infinite loop?", "complexity": "TLE"})
    finally:
        os.remove(tmp)

# ── API: Wrong Answer Analyzer ────────────────────────────────────────────────
@app.route("/api/analyze_wrong_answer", methods=["POST"])
def analyze_wrong():
    d = request.get_json()
    prompt = (f"Problem: {d.get('problem')}\n\nCode:\n{d.get('code')}\n\n"
              f"Error:\n{d.get('error')}\n\n"
              "As a tech interview coach: 1) Why did it fail? 2) Hint to fix (no full solution).")
    try:
        return jsonify({"analysis": ask_ai([{"role": "user", "content": prompt}])})
    except Exception as e:
        return jsonify({"analysis": f"AI Coach Error: {e}"})

# ── API: Code Explainer ───────────────────────────────────────────────────────
@app.route("/api/explain_code", methods=["POST"])
def explain_code():
    code = request.get_json().get("code", "")
    prompt = (f"Explain this code step-by-step, show a dry run, and give time/space complexity:\n\n{code}")
    try:
        return jsonify({"explanation": ask_ai([{"role": "user", "content": prompt}])})
    except Exception as e:
        return jsonify({"explanation": f"AI Coach Error: {e}"})

# ── API: Resume Analyzer ──────────────────────────────────────────────────────
@app.route("/api/resume_analyzer", methods=["POST"])
def resume_analyzer():
    text   = request.get_json().get("resume_text", "")
    prompt = (f"Analyze this candidate for FAANG SWE roles:\n{text}\n\n"
              "Give: 3 missing skills to learn, 2 areas to improve.")
    try:
        return jsonify({"feedback": ask_ai([{"role": "user", "content": prompt}])})
    except Exception as e:
        return jsonify({"feedback": f"AI Coach Error: {e}"})

# ── API: Progress Dashboard ───────────────────────────────────────────────────
@app.route("/api/progress")
def get_progress():
    conn = sqlite3.connect("session_history.db")
    cur  = conn.cursor()
    cur.execute("SELECT problems_solved, accuracy, weak_topics FROM user_progress WHERE id=1")
    row  = cur.fetchone()
    conn.close()
    if row:
        return jsonify({"problems_solved": row[0], "accuracy": row[1],
                        "weak_topics": [t.strip() for t in row[2].split(",")]})
    return jsonify({"problems_solved": 0, "accuracy": 0, "weak_topics": []})

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n✅  AI Interview Coach — Flask + Gemini")
    print("   Landing  → http://127.0.0.1:8000")
    print("   App      → http://127.0.0.1:8000/app")
    print("   API Test → http://127.0.0.1:8000/api/test\n")
    app.run(host="127.0.0.1", port=8000, debug=True)
