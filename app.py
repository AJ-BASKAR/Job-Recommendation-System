import streamlit as st
import fitz  # PyMuPDF for PDF extraction
import pandas as pd
import requests
from model import JobRecommendationSystem
from streamlit_lottie import st_lottie
from fpdf import FPDF

# -------------------------------
# 🔄 Lottie Animation Loader
# -------------------------------
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        st.error(f"❌ Animation load failed: {e}")
    return None

# -------------------------------
# 📄 PDF Generator
# -------------------------------
def generate_pdf(jobs):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Top Job Recommendations", ln=True, align="C")
    pdf.ln(10)

    for i, job in enumerate(jobs, start=1):
        pdf.multi_cell(0, 10, txt=f"""
Job {i}: {job['position']}
Company: {job['workplace']}
Mode: {job['working_mode']}
Duties: {job['job_role_and_duties']}
Required Skills: {job['requisite_skill']}
------------------------------
""")
    return pdf.output(dest='S').encode('latin-1')


# -------------------------------
# 🌠 Lottie Animations
# -------------------------------
lottie_resume = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_touohxv0.json")
lottie_processing = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_sF2D1M.json")

# -------------------------------
# 🎨 Custom Styles
# -------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');

html, body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.stApp {
    background-image: url("https://www.transparenttextures.com/patterns/stardust.png");
    background-size: cover;
    animation: stars 60s linear infinite;
}

@keyframes stars {
  0% { background-position: 0 0; }
  100% { background-position: 1000px 1000px; }
}

.title {
    font-size: 3em;
    text-align: center;
    margin-bottom: 0.5em;
    color: #F9FAFB;
    text-shadow: 0 0 20px rgba(255,255,255,0.3);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🧠 Load Recommender
# -------------------------------
st.markdown('<div class="title">🚀 AI-Powered Job Recommendation System</div>', unsafe_allow_html=True)
st.write("📄 Upload your **PDF Resume** and discover **20 tailored job opportunities** using intelligent matching.")

recommender = JobRecommendationSystem("JobsFE.csv")

# -------------------------------
# 📤 Upload Resume
# -------------------------------
uploaded_file = st.file_uploader("📤 Upload your resume (PDF only)", type=["pdf"])

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text.strip()

resume_text = ""
job_results = []

if uploaded_file:
    with st.spinner("📄 Extracting resume content..."):
        if lottie_resume:
            st_lottie(lottie_resume, height=200, key="upload")
        resume_text = extract_text_from_pdf(uploaded_file)

# -------------------------------
# 🔍 Recommend Button
# -------------------------------
if st.button("🔍 Recommend Jobs"):
    if resume_text:
        with st.spinner("🤖 Analyzing your resume and finding best job matches..."):
            if lottie_processing:
                st_lottie(lottie_processing, height=200, key="process")
            recommendations = recommender.recommend_jobs(resume_text, top_n=20)
            job_results = recommendations["recommended_jobs"]

        st.success(f"✅ Found {len(job_results)} job recommendations for you!")

        for i, job in enumerate(job_results, start=1):
            st.markdown(f"""
                <div style="padding:1em; border-radius:12px; background-color:rgba(255,255,255,0.07); margin-bottom:1em;">
                    <h3 style="color:#FFD700;">🚀 Job {i}: {job['position']}</h3>
                    <p><strong>🏢 Company:</strong> {job['workplace']}</p>
                    <p><strong>💻 Mode:</strong> {job['working_mode']}</p>
                    <p><strong>🧾 Duties:</strong> {job['job_role_and_duties']}</p>
                    <p><strong>🛠 Required Skills:</strong> {job['requisite_skill']}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please upload a valid PDF resume before proceeding.")

# -------------------------------
# 📄 PDF Download Button
# -------------------------------
if job_results:
    pdf_bytes = generate_pdf(job_results)
    st.download_button(
        label="📥 Download Job Recommendations (PDF)",
        data=pdf_bytes,
        file_name="job_recommendations.pdf",
        mime="application/pdf"
    )
