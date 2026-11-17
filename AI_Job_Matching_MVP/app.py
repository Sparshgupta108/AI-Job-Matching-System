import streamlit as st
import fitz
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Job Matching System", page_icon="🎯", layout="wide")

SKILLS = ["python", "java", "c++", "javascript", "react", "node.js", "html", "css",
          "sql", "mongodb", "mysql", "machine learning", "deep learning", "nlp",
          "data analysis", "pandas", "numpy", "scikit-learn", "tensorflow",
          "flask", "django", "fastapi", "express", "git", "aws", "docker"]

JOBS = [
    {"title": "Python Developer", "company": "TechNova",
     "description": "Python SQL REST API Flask Django Git backend development"},
    {"title": "Frontend Developer", "company": "WebWorks",
     "description": "JavaScript React HTML CSS responsive design REST API Git"},
    {"title": "Machine Learning Intern", "company": "DataMind",
     "description": "Python machine learning pandas numpy scikit-learn NLP data analysis"},
    {"title": "Full Stack Developer", "company": "BuildStack",
     "description": "JavaScript React Node.js Express MongoDB HTML CSS REST API"},
    {"title": "Data Analyst", "company": "InsightHub",
     "description": "SQL Python Excel data analysis pandas statistics visualization"}
]

def extract_pdf_text(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in pdf)

def detect_skills(text):
    found = []
    for skill in SKILLS:
        if re.search(r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])", text, re.I):
            found.append(skill)
    return found

def recommend_jobs(resume):
    docs = [resume] + [job["description"] for job in JOBS]
    vectors = TfidfVectorizer(stop_words="english").fit_transform(docs)
    scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    return sorted(zip(JOBS, scores), key=lambda x: x[1], reverse=True)

st.title("🎯 AI-Powered Candidate Job Matching System")
st.caption("Academic MVP using Python, PDF text extraction, TF-IDF and Cosine Similarity.")

candidate_tab, recruiter_tab, about_tab = st.tabs(
    ["Candidate: Find Jobs", "Recruiter: Rank Candidates", "About the Project"])

with candidate_tab:
    st.subheader("Upload your resume")
    file = st.file_uploader("Upload a text-based PDF resume", type=["pdf"])
    if file:
        try:
            resume = extract_pdf_text(file)
            if not resume.strip():
                st.warning("No selectable text found. Scanned PDFs need OCR, which is not included.")
            else:
                skills = detect_skills(resume)
                st.write("**Detected skills:**", ", ".join(skills) if skills else "No listed skills found")
                st.subheader("Recommended jobs")
                for job, score in recommend_jobs(resume):
                    with st.container(border=True):
                        st.markdown(f"**{job['title']}** — {job['company']}")
                        st.progress(float(score))
                        st.write(f"Text similarity: **{score * 100:.1f}%**")
                        st.caption(job["description"])
                st.info("Similarity is not a probability of getting hired or a final suitability decision.")
        except Exception as error:
            st.error(f"Could not read this PDF: {error}")

with recruiter_tab:
    st.subheader("Compare candidate profiles")
    description = st.text_area("Job description", placeholder="Required skills and experience...")
    profiles = [st.text_area(f"Candidate {i} profile", key=f"profile{i}",
                             placeholder="Paste candidate skills, education and experience...")
                for i in range(1, 4)]
    if st.button("Rank candidates", type="primary"):
        active = [(f"Candidate {i+1}", p) for i, p in enumerate(profiles) if p.strip()]
        if not description.strip() or not active:
            st.warning("Enter a job description and at least one candidate profile.")
        else:
            docs = [description] + [p[1] for p in active]
            vectors = TfidfVectorizer(stop_words="english").fit_transform(docs)
            scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
            for name, score in sorted(zip([p[0] for p in active], scores),
                                      key=lambda x: x[1], reverse=True):
                st.write(f"**{name}: {score * 100:.1f}% text similarity**")
                st.progress(float(score))
            st.caption("This is a ranking aid for demonstration, not an automated hiring decision.")

with about_tab:
    st.subheader("How it works")
    st.markdown("""
    1. Candidate uploads a PDF resume.
    2. PyMuPDF extracts selectable text.
    3. A predefined keyword list detects technical skills.
    4. TF-IDF converts resume and job descriptions into numerical vectors.
    5. Cosine Similarity compares the vectors and ranks sample jobs.
    6. Recruiters can compare pasted candidate profiles with a job description.

    **Current limitations**
    - Sample job descriptions are stored in the code.
    - Skill extraction uses a fixed keyword dictionary.
    - No login, live job posting, OCR, or persistent database is included.
    - This MVP uses Python + Streamlit. React + Node.js + MongoDB can be a later full-stack phase.
    """)

st.divider()
st.caption("Academic project prototype")
