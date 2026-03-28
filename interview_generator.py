import os
import json
import re
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import random

load_dotenv()

app = FastAPI(title="Interview Question Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FALLBACK_QUESTIONS = [
    {"id": 1, "difficulty": "Easy", "question": "Reverse a Linked List", "hint": "Use three pointers (prev, curr, next).", "solution": "Iterate through the list, setting each node's next pointer to the previous node."},
    {"id": 2, "difficulty": "Medium", "question": "Find the longest palindromic substring", "hint": "Expand around center of every character.", "solution": "Loop through each character and try to expand outwards to check for palindromes."},
    {"id": 3, "difficulty": "Hard", "question": "Design a URL shortener like TinyURL", "hint": "Think about hashing and base62 encoding.", "solution": "Use a database to store long URLs mapped to short hashes (base62 encoding of an auto-incremented ID)."}
]

class GenerationRequest(BaseModel):
    topic: str
    difficulty: str = "All"

@app.post("/api/generate")
async def generate_questions(request: GenerationRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_google_gemini_api_key_here":
        print("Warning: GEMINI_API_KEY is not set or invalid. Using fallback questions.")
        return {"questions": FALLBACK_QUESTIONS}

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro")

    difficulty_prompt = f" Generate questions of {request.difficulty} difficulty level." if request.difficulty != "All" else " Include a mix of Easy, Medium, and Hard difficulties."

    prompt = (
        f"Generate exactly 5 technical interview questions for the topic: '{request.topic}'."
        f"{difficulty_prompt}\n"
        f"Return ONLY a strictly valid JSON array of objects. Do not write any markdown blocks (like ```json), just raw JSON.\n"
        f"Each object must have these exact keys:\n"
        f'- "id" (a unique integer)\n'
        f'- "difficulty" (string: "Easy", "Medium", or "Hard")\n'
        f'- "question" (string: the interview problem statement)\n'
        f'- "hint" (string: a short nudge without revealing the answer)\n'
        f'- "solution" (string: a concise, clear explanation of the approach)'
    )

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean up markdown output
        if text.startswith("```json"): text = text[7:]
        if text.startswith("```"): text = text[3:]
        if text.endswith("```"): text = text[:-3]
        text = text.strip()

        questions = json.loads(text)
        return {"questions": questions}

    except Exception as e:
        print(f"Error generation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch from Gemini API.")

# Make sure static directory exists
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("interview_generator:app", host="127.0.0.1", port=8000, reload=True)