import streamlit as st
from PyPDF2 import PdfReader

# Load role-based skills
def load_role_skills():
    roles = {}
    current_role = None

    with open("skills.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                current_role = line[1:-1]
                roles[current_role] = []
            elif current_role:
                roles[current_role].append(line)

    return roles

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
        if skill.lower() in text:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    score = int((len(found_skills) / len(skills)) * 100)
    return score, found_skills, missing_skills

# ---------------- UI ---------------- #

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer 🚀")

st.write("Analyze your resume based on job roles and get instant feedback!")

# Load roles
roles = load_role_skills()

# Dropdown for role selection
selected_role = st.selectbox("🎯 Select Job Role", list(roles.keys()))

# Upload file
uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    text = extract_text(uploaded_file)
    skills = roles[selected_role]

    score, found, missing = analyze_resume(text, skills)

    st.subheader(f"📊 {selected_role} Resume Score: {score}%")
    st.progress(score)

    st.write("### ✅ Skills Found")
    st.write(found)

    st.write("### ❌ Missing Skills")
    st.write(missing)

    # Feedback
    if score < 50:
        st.warning("⚠️ Add more relevant skills to improve your resume!")
    elif score >= 80:
        st.success("🔥 Excellent Resume!")

else:
    st.info("📌 Please upload a resume to get analysis.")