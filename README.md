<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0f1e,35:1a0533,70:4c1d95,100:7c3aed&height=230&section=header&text=Ultimate%20Interview%20Prep&fontSize=46&fontColor=ffffff&fontAlignY=38&desc=AI-Powered%20FAANG%20Interview%20Simulator%20%E2%80%A2%20Real-Time%20Code%20Execution%20%E2%80%A2%20Personalized%20Feedback&descAlignY=58&descSize=15&animation=fadeIn" />

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&duration=2500&pause=800&color=A78BFA&center=true&vCenter=true&width=760&lines=AI+Question+Generator+%E2%80%94+Easy+%7C+Medium+%7C+Hard+%F0%9F%A7%A0;Live+Python+Sandbox+with+Time-Complexity+Analysis+%E2%9A%A1;Smart+Code+Analyst+powered+by+Gemini+2.5+Flash+%F0%9F%A4%96;Resume+Analyzer+%E2%80%94+FAANG-Targeted+Critique+%F0%9F%93%84;Local+SQLite+Progress+Tracker+%E2%80%94+Offline+Ready+%F0%9F%93%8A" />

<br/><br/>

[![GitHub](https://img.shields.io/badge/GitHub-Ultimate--Interview--prep--platform-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Bhogi123-T/Ultimate-Interview-prep-platform)
[![Author](https://img.shields.io/badge/Author-Bhogeswara%20Rao%20T-7c3aed?style=for-the-badge)](https://github.com/Bhogi123-T)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini%202.5%20Flash-AI%20Engine-4285F4?style=flat-square&logo=google&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3%20Glassmorphic-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

</div>

---

## 📌 Overview

**Ultimate AI Interview Prep Platform** is a full-stack, locally-running interview preparation system that simulates FAANG-style technical interviews from start to finish. Powered by **Google Gemini 2.5 Flash**, it generates fresh DSA questions on demand, lets you write and run Python code in the browser, analyzes your code with AI, critiques your resume for top-tier company standards, and tracks your progress over time — all offline-capable with a local SQLite database.

---

## ✨ Platform Features

<table>
<tr>
<td width="50%" valign="top">

### 🧠 AI Question Generator
- Generates customized DSA questions across any topic
- Three difficulty tiers — **Easy · Medium · Hard**
- Deduplication logic ensures no repeated questions per session
- Powered by Gemini 2.5 Flash with structured prompting

</td>
<td width="50%" valign="top">

### ⚡ Interactive Python Sandbox
- Write & execute Python code directly in the browser
- Real-time output, error detection & traceback display
- **Time-complexity estimates** powered by AI analysis
- Safe sandboxed execution environment

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🔍 Smart Code Analyst
- Instant AI explanation of your code logic
- Identifies failing test cases & edge cases
- **Hint mode** — nudges you without spoiling the answer
- Logic efficiency review with improvement suggestions

</td>
<td width="50%" valign="top">

### 📄 Resume Analyzer
- Upload your professional profile for instant critique
- FAANG-targeted feedback:
  - **3 missing skills** to add
  - **2 areas to improve**
- Benchmarked against top tech company standards

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📊 Local Progress Tracker
- Offline SQLite database — no cloud needed
- Tracks problems solved & overall accuracy
- Identifies your **weak topics** automatically
- Persists across sessions

</td>
<td width="50%" valign="top">

### 🎨 Glassmorphic UI
- Premium frosted-glass design language
- Smooth, distraction-free coding environment
- Fully responsive across screen sizes
- Dark-mode optimized interface

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python · Flask |
| **AI Engine** | Google Generative AI SDK — Gemini 2.5 Flash |
| **Database** | SQLite3 (local, offline-first) |
| **Frontend** | Vanilla HTML5 · CSS3 (Glassmorphic) · JavaScript |
| **Auth / Config** | python-dotenv · `.env` based API key management |

---

## 🏗️ Project Structure

```
Ultimate-Interview-prep-platform/
├── app.py                  # Flask backend — routes, AI calls, SQLite logic
├── requirements.txt        # Python dependencies
├── .env                    # 🔐 Your API key (gitignored — never commit this)
├── .env.example            # Template for environment setup
├── .gitignore
│
├── static/
│   ├── css/                # Glassmorphic stylesheets
│   └── js/                 # Frontend logic — sandbox, question UI, progress
│
└── templates/
    └── index.html          # Main app UI
```

---

## 🚀 Local Setup

### Prerequisites

- Python **3.9+**
- A **Google Gemini API key** — get one free at [aistudio.google.com](https://aistudio.google.com)

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Bhogi123-T/Ultimate-Interview-prep-platform.git
cd Ultimate-Interview-prep-platform
```

---

### Step 2 — Install Dependencies

```bash
pip install flask requests python-dotenv google-generativeai
```

---

### Step 3 — Configure Your API Key

Create a `.env` file in the root directory:

```bash
# Create the file
touch .env   # or manually create it on Windows
```

Add your Gemini API key:

```env
GEMINI_API_KEY="your_actual_gemini_key_here"
```

> ⚠️ **Important:** The `.env` file is listed in `.gitignore`. **Never push your API key to GitHub.**  
> Get your free key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

### Step 4 — Run the Server

```bash
python app.py
```

---

### Step 5 — Open in Browser

Navigate to:

```
http://localhost:8000
```

The platform is now running fully locally. 🎉

---

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini Developer API Key | ✅ Yes |

> All other configuration is handled automatically by the app.

---

## 🗺️ How It Works

```
User selects topic & difficulty
           ↓
Gemini 2.5 Flash generates unique DSA question
           ↓
User writes Python solution in browser sandbox
           ↓
Code executed server-side → output returned
           ↓
Smart Code Analyst reviews logic, hints, and efficiency
           ↓
Result logged to SQLite (accuracy + weak topic analysis)
           ↓
Progress dashboard updates automatically
```

---

## 🎯 Who Is This For?

| Profile | How AQUA Helps |
|---------|---------------|
| 🎓 CS Students | Structured DSA practice with AI guidance |
| 💼 Job Seekers | FAANG-style simulation before real interviews |
| 🔁 Career Switchers | Resume critique + coding fundamentals together |
| 🏆 Competitive Programmers | Rapid question generation across all topics |

---

## 🤝 Contributing

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/your-feature-name

# 3. Commit your changes
git commit -m "feat: describe your change"

# 4. Push and open a Pull Request
git push origin feature/your-feature-name
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7c3aed,50:4c1d95,100:0a0f1e&height=130&section=footer&animation=fadeIn" />

**Developed & Designed by [Bhogeswara Rao T](https://github.com/Bhogi123-T) · Chennai, India**

*"Design with purpose. Code with impact."* 🚀

</div>
