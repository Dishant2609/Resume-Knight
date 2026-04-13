import streamlit as st
import requests
import io

API_BASE_URL = "http://localhost:8000"

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
    creativity = st.slider("Creativity (temperature)", 0.0, 1.0, 0.7)

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role (optional)")
job_description = st.text_area("Paste the job description (optional)", height=170)

analyze = st.button("Analyze Resume")

if analyze and uploaded_file:
    try:
        with st.spinner("Extracting text from resume..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            extract_response = requests.post(f"{API_BASE_URL}/extract-text", files=files)
            extract_response.raise_for_status()
            resume_text = extract_response.json()["text"]

        if not resume_text.strip():
            st.error("Resume has no readable content.")
            st.stop()

        with st.spinner("Analyzing resume with AI..."):
            analysis_payload = {
                "resume_text": resume_text,
                "job_role": job_role,
                "job_description": job_description,
                "creativity": creativity
            }
            api_response = requests.post(f"{API_BASE_URL}/analyze", json=analysis_payload)
            api_response.raise_for_status()
            result = api_response.json()

        st.markdown("### Resume Analysis")
        st.markdown(result["analysis"])

        st.markdown("### ATS Score")
        ats_score = result["ats_score"]
        if ats_score:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("Score", f"{ats_score}/100")
            with col2:
                st.progress(ats_score / 100)

        st.markdown(result["ats_evaluation"])

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Make sure FastAPI server is running:\n`uvicorn api:app --reload`")
    except Exception as e:
        st.error(f"Error: {str(e)}")
