import streamlit as st
from PyPDF2 import PdfReader

# Page configuration
st.set_page_config(
    page_title="Smart Resume Analyzer",
    layout="centered"
)

# Sidebar
st.sidebar.title("About")

st.sidebar.info("""
This project analyzes resumes based on selected job roles
and provides ATS-style scoring and suggestions.
""")

# Main title
st.title("📄 Smart Resume Analyzer")

st.markdown("""
Upload your resume and analyze it based on job-specific skills.
""")

# Job role selection
role = st.selectbox(
    "Select Job Role",
    ["Software Developer", "Data Analyst"]
)

# Required skills based on role
if role == "Software Developer":
    required_skills = [
        "python",
        "java",
        "data structures",
        "algorithms",
        "git"
    ]

else:
    required_skills = [
        "python",
        "sql",
        "excel",
        "data analysis",
        "statistics"
    ]

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):

    pdf_reader = PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text

# Resume analysis function
def analyze_resume(text):

    text = text.lower()

    found = []
    missing = []

    for skill in required_skills:

        if skill in text:
            found.append(skill)

        else:
            missing.append(skill)

    score = int((len(found) / len(required_skills)) * 100)

    return found, missing, score

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

resume_text = ""

if uploaded_file is not None:

    resume_text = extract_text_from_pdf(uploaded_file)

    st.success("✅ Resume uploaded successfully!")

# Analyze Button
if st.button("Analyze"):

    if resume_text == "":
        st.error("Please upload a resume first.")

    else:

        found, missing, score = analyze_resume(resume_text)

        # ATS Score
        ats_score = score

        if "github" in resume_text.lower():
            ats_score += 10

        if "linkedin" in resume_text.lower():
            ats_score += 10

        if len(resume_text) > 1000:
            ats_score += 10

        if ats_score > 100:
            ats_score = 100

        # ATS Score display
        st.subheader("ATS Compatibility Score")

        st.progress(ats_score / 100)

        st.write(f"ATS Score: {ats_score}%")

        # Resume Score
        st.subheader("Resume Match Score")

        st.progress(score / 100)

        st.write(f"Match Score: {score}%")

        # Skills Found
        st.success(f"✅ Skills Found: {', '.join(found)}")

        # Missing Skills
        st.error(f"❌ Missing Skills: {', '.join(missing)}")

        # Feedback
        if score < 50:
            st.warning("Your resume needs improvement for this role.")

        else:
            st.success("Good skill match for this role.")

        # Suggestions
        st.subheader("Suggestions")

        if "python" not in found:
            st.write("👉 Learn Python basics")

        if "data structures" not in found:
            st.write("👉 Practice DSA on LeetCode")

        if "sql" not in found:
            st.write("👉 Learn SQL for data handling")

        if "git" not in found and role == "Software Developer":
            st.write("👉 Learn Git and GitHub basics")

        if "excel" not in found and role == "Data Analyst":
            st.write("👉 Improve Excel skills for analytics")

# Footer
st.markdown("---")
st.caption("Built using Python, Streamlit and PyPDF2")