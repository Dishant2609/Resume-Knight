from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import io
import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Resume Knight API")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


class AnalysisRequest(BaseModel):
    resume_text: str
    job_role: str = ""
    job_description: str = ""
    creativity: float = 0.7


class AnalysisResponse(BaseModel):
    analysis: str
    ats_evaluation: str
    ats_score: int


def extract_text_from_pdf(pdf_bytes):
    """Extract text from PDF"""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    return "\n".join([page.extract_text() for page in pdf_reader.pages])


def extract_score(text):
    """Extract numerical score from text"""
    match = re.search(r"(\d{1,3})\s*/?\s*100", text)
    return int(match.group(1)) if match else 0


@app.get("/")
def root():
    return {"message": "Resume Knight API - AI-powered resume analyzer"}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze_resume(request: AnalysisRequest):
    """Analyze resume and return feedback + ATS score"""
    
    resume_text = request.resume_text
    job_role = request.job_role
    job_description = request.job_description
    creativity = request.creativity

    if not resume_text.strip():
        return {
            "analysis": "Error: Resume has no readable content.",
            "ats_evaluation": "",
            "ats_score": 0
        }

    # Resume Analysis
    target_info = []
    if job_role:
        target_info.append(f"Job role: {job_role}")
    if job_description:
        target_info.append(f"Job description:\n{job_description}")

    analysis_prompt = f"""
    You are ResumeSherlock, a resume detective.
    Provide a short, concise, bullet-point style analysis (step-by-step CoT) for the resume.
    Tailor the recommendations using the following role information:
    {"\n".join(target_info) if target_info else 'No target role information provided.'}

    1. List Strengths
    2. List Weaknesses
    3. Give Overall Score (1-10)
    4. Short Recommendations for the candidate

    Resume content:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert resume reviewer. Keep feedback concise."},
            {"role": "user", "content": analysis_prompt}
        ],
        temperature=creativity,
        max_tokens=600
    )
    analysis_result = response.choices[0].message.content

    # ATS Evaluation
    ats_prompt = f"""
    You are an ATS simulation tool.
    Provide a **short, bullet-point ATS evaluation** (step-by-step CoT):

    1. Section-wise score (Formatting, Skills, Experience, Contact Info)
    2. Overall ATS score (0-100)
    3. Short recommendations

    Resume content:
    {resume_text}
    """

    ats_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an ATS evaluation tool. Keep it short."},
            {"role": "user", "content": ats_prompt}
        ],
        temperature=0.3,
        max_tokens=400
    )
    ats_result = ats_response.choices[0].message.content
    ats_score = extract_score(ats_result)

    return {
        "analysis": analysis_result,
        "ats_evaluation": ats_result,
        "ats_score": ats_score
    }


@app.post("/extract-text")
def extract_text_endpoint(file: UploadFile = File(...)):
    """Extract text from uploaded PDF or TXT file"""
    try:
        content = file.file.read()
        
        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(content)
        else:
            text = content.decode("utf-8")
        
        return {"text": text}
    except Exception as e:
        return {"error": str(e), "text": ""}
