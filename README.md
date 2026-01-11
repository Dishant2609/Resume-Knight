<<<<<<< HEAD
# Resume Knight

**Resume Knight** is an AI-powered resume analyzer built with **Streamlit** that provides **concise feedback and an ATS-style score** for uploaded resumes.

---

## Features
- Upload resume (PDF or TXT)
- AI-generated strengths & weaknesses
- ATS-style score (0–100)
- Job-role based recommendations
- Clean, minimal UI

---

## Tech Stack
- Python
- Streamlit
- OpenAI API
- PyPDF2
- dotenv

---

## Run Locally

```bash
git clone https://github.com/Dishant2609/Resume-Knight.git
cd Resume-Knight

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt


Create .env file:

OPENAI_API_KEY=your_api_key


Run the app:

streamlit run app.py
=======
# 🦇 Resume Knight

AI-powered "Resume Inspector". Upload your resume (PDF/TXT) and get "AI feedback + ATS score" instantly.  

Features
- Upload resume (PDF or TXT)  
- AI feedback: strengths, weaknesses, and suggestions  
- ATS scoring (0–100)
>>>>>>> 8d80355 (refactor: clean up app.py and improve resume analysis logic)
