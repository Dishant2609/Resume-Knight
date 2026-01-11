<<<<<<< HEAD
import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv
import re


load_dotenv()

st.set_page_config(
    page_title="Resume Knight",
    page_icon="🦇",
    layout="centered"
)

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://i.postimg.cc/D09gCmFC/batman-5120x2880-26326.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


st.title("🦇 Resume Knight")
st.markdown("Upload your resume and get **AI powered concise feedback and ATS score!**")


with st.sidebar:
    creativity = st.slider(" Creativity (temperature)", 0.0, 1.0, 0.7)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role (optional)")


analyze = st.button(" Analyze Resume")


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return "\n".join([page.extract_text() for page in pdf_reader.pages])

def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

def extract_score(text):
    match = re.search(r"(\d{1,3})\s*/?\s*100", text)
    return int(match.group(1)) if match else None

def get_jobdesc_text(file, textarea):
    if file:
        return extract_text(file)
    return textarea.strip() if textarea.strip() else None


if analyze and uploaded_file:
    try:
        resume_text = extract_text(uploaded_file)
        if not resume_text.strip():
            st.error(" Resume has no readable content.")
            st.stop()

        analysis_prompt = f"""
                            You are ResumeSherlock, a resume detective.
                            Provide a short, concise, bullet-point style analysis** (step-by-step CoT) for the resume:

                            1. List Strengths
                            2. List Weaknesses
                            3. Give Overall Score (1-10)
                            4. Short Recommendations for {job_role if job_role else 'general job'}

                            Resume content:
                            {resume_text}
                            """
        with st.spinner(" Analyzing resume..."):
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
        st.markdown(" Resume Analysis (Concise)")
        st.markdown(analysis_result)
 
        ats_prompt = f"""
                        You are an ATS simulation tool.
                        Provide a **short, bullet-point ATS evaluation** (step-by-step Cot):

                        1. Section-wise score (Formatting, Skills, Experience, Contact Info)
                        2. Overall ATS score (0-100)
                        3. Short recommendations

                        Resume content:
                        {resume_text}
                        """
        with st.spinner("Calculating ATS Score..."):
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
        st.markdown(" ATS Score")
        if ats_score:
            st.metric("ATS Score", f"{ats_score}/100")
            st.progress(ats_score / 100)
        st.markdown(ats_result)

        
    except Exception as e:
        st.error(f" Error: {str(e)}")

=======
import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv
import re

 
load_dotenv()



load_dotenv()


st.set_page_config(
    page_title="Resume Knight",
    page_icon="🦇",
    layout="centered"
)


page_bg_img = """
                <style>
                [data-testid="stAppViewContainer"] {
                    background-image: url("https://i.postimg.cc/D09gCmFC/batman-5120x2880-26326.jpg");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                }
                [data-testid="stHeader"] { background: rgba(0,0,0,0); }
                </style>
                """
st.markdown(page_bg_img, unsafe_allow_html=True)


st.title("🦇 Resume Knight")
st.markdown("Upload your resume and get **feedback and ATS score!**")

with st.sidebar:
    creativity = st.slider("Creativity (temperature)", 0.0, 1.0, 0.7)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI API key not found.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)


uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role (optional)")
analyze = st.button("🔍 Analyze Resume")


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return "\n".join(page.extract_text() or "" for page in pdf_reader.pages)

def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

def extract_score(text):
    match = re.search(r"(\d{1,3})\s*/?\s*100", text)
    return int(match.group(1)) if match else None


if analyze and uploaded_file:
    try:
        resume_text = extract_text(uploaded_file)

        if not resume_text.strip():
            st.error("Resume has no readable content.")
            st.stop()

        
        if len(resume_text) > 5000:
            st.warning("Resume too long. Please upload a concise version.")
            st.stop()

       
        prompt = f"""
                    Review the resume below and respond concisely with:

                    1. Strengths (bullet points)
                    2. Weaknesses (bullet points)
                    3. ATS score (0–100)
                    4. 3 practical improvement suggestions for {job_role or "general roles"}

                    Resume:
                    {resume_text}
                    """

        with st.spinner("Analyzing resume..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a resume reviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )

        result = response.choices[0].message.content

        st.markdown("### Resume Review")
        st.markdown(result)

        
        ats_score = extract_score(result)
        if ats_score:
            st.metric("ATS Score", f"{ats_score}/100")
            st.progress(ats_score / 100)

    except Exception as e:
        st.error(f"Error: {str(e)}")
>>>>>>> 8d80355 (refactor: clean up app.py and improve resume analysis logic)
