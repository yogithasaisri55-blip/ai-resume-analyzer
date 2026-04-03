import streamlit as st
from PyPDF2 import PdfReader

# Load skills
def load_skills():
    with open("skills.txt", "r") as f:
        skills = f.read().splitlines()
    return skills

# Extract text from PDF
def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# Analyze resume
def analyze_resume(text, skills):
    found_skills = []
    missing_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    score = int((len(found_skills) / len(skills)) * 100)
    return score, found_skills, missing_skills

# UI
st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    text = extract_text(uploaded_file)
    skills = load_skills()

    score, found, missing = analyze_resume(text, skills)

    st.subheader(f"Resume Score: {score}%")
    st.progress(score)

    st.write("### ✅ Skills Found")
    st.write(found)

    st.write("### ❌ Missing Skills")
    st.write(missing)

    if score < 50:
        st.warning("⚠️ Add more skills to improve your resume")
    elif score > 80:
        st.success("🔥 Excellent Resume!")