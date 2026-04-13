# Resume Knight

**Resume Knight** is an AI-powered resume analyzer built with **Streamlit** and **FastAPI**. Upload your resume, optionally provide a job description, and receive AI-backed resume feedback plus an ATS-style score.

---

## Features
- Upload resume (PDF or TXT)
- AI-generated strengths and weaknesses
- ATS-style score (0–100)
- Job role and job description support
- Clean Streamlit UI with FastAPI backend

---

## Tech Stack
- Python
- Streamlit
- FastAPI
- OpenAI API
- PyPDF2
- Requests
- python-dotenv

---

## Setup

```bash
git clone https://github.com/Dishant2609/Resume-Knight.git
cd Resume-Knight
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## Run Locally

Start the FastAPI backend:

```bash
uvicorn api:app --reload
```

In a second terminal, start the Streamlit frontend:

```bash
streamlit run app.py
```

Open the app in your browser at:

```text
http://localhost:8501
```

Open API docs at:

```text
http://localhost:8000/docs
```

---

## Notes
- Keep your real API key in `.env` only.
- Don’t commit `.env` or `.venv/` to the repo.
- The frontend expects the backend at `http://localhost:8000`.

---

## Optional files
- `.gitignore` already excludes `.env`, `.venv/`, and `__pycache__/`
- `.env.example` can be used as a template for your environment variables


