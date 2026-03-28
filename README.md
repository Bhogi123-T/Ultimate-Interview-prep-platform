# Ultimate AI Interview Prep Platform 🚀

A comprehensive, AI-powered tech interview preparation platform designed to simulate FAANG-style interviews, provide real-time code execution, and offer personalized feedback using the Google Gemini ecosystem.

## Features ✨
* **AI Question Generator:** Automatically generates customized Data Structures & Algorithms questions (Easy, Medium, Hard) tailored to specific tech topics, ensuring questions don't duplicate.
* **Interactive Python Sandbox:** Execute your Python code safely with real-time feedback, error detection, and time-complexity estimates directly in the browser.
* **Smart Code Analyst:** Uses AI to instantly explain logic, spot failing test cases, provide hints (without revealing the full answer), and review logic efficiency.
* **Resume Analyzer:** Upload your professional details to get rapid critiques geared towards top tech companies (3 missing skills, 2 areas to improve).
* **Local Progress Tracking:** Offline SQLite database dynamically logs the number of problems you solve, overall accuracy, and analyzes weak topics.

## Tech Stack 🛠️
* **Backend:** Python, Flask, SQLite3
* **Frontend:** Vanilla HTML5, CSS3 (Glassmorphic UI), JavaScript
* **AI Engine:** Native Google Generative AI SDK (Gemini 2.5 Flash)




## Local Setup 💻
1. Clone the repository.
   ```bash
   git clone https://github.com/Bhogi123-T/Ultimate-Interview-prep-platform.git
   ```
2. Ensure you have Python 3.9+ installed.
3. Install the required Python dependencies:
   ```bash
   pip install flask requests python-dotenv google-generativeai
   ```
4. Create a `.env` file in the root directory and add your Google Gemini Developer Key:
   ```env
   GEMINI_API_KEY="your_actual_key_here"
   ```
5. Run the backend server:
   ```bash
   python app.py
   ```
6. Open your browser and navigate to the local server shown in the console (`http://localhost:8000`).

## Environment Variables 🔐
Because the `.env` file is safely ignored via our `.gitignore`, do **not** upload your keys to GitHub.

---
*Developed & Designed by Bhogi123-T*

