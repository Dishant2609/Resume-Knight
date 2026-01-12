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

---


