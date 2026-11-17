import re
import streamlit as st
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Job Matching", page_icon="💼", layout="wide")
st.title("💼 AI-Powered Candidate Job Matching")
st.caption("Resume analysis • Job recommendations • Recruiter candidate ranking")
st.info("Academic MVP: TF-IDF + Cosine Similarity measures text similarity. It is not a validated probability of job suitability.")

JOBS = [
 {"title":"Python Developer","company":"DemoTech","location":"Noida","description":"Python backend development, REST APIs, SQL, Git, testing and debugging.","skills":"Python, REST API, SQL, Git"},
 {"title":"Frontend Developer","company":"WebWorks","location":"Remote","description":"Responsive websites using HTML, CSS, JavaScript, React, APIs and Git.","skills":"HTML, CSS, JavaScript, React, Git"},
 {"title":"Machine Learning Intern","company":"DataLab","location":"Bengaluru","description":"Python, machine learning, pandas, scikit-learn, NLP, statistics and model evaluation.","skills":"Python, Machine Learning, pandas, scikit-learn, NLP"},
 {"title":"Full Stack Developer Intern","company":"BuildIt","location":"Greater Noida","description":"React, JavaScript, Node.js, Express, MongoDB, REST APIs and Git.","skills":"React, JavaScript, Node.js, Express, MongoDB"}
]
SKILLS = ["python","java","javascript","react","node.js","express","mongodb","sql","mysql","html","css","machine learning","deep learning","nlp","scikit-learn","pandas","numpy","tensorflow","pytorch","git","rest api","flask","fastapi","data analysis","docker","c++"]

def pdf_text(data):
    with fitz.open(stream=data, filetype="pdf") as pdf:
        return "\n".join(page.get_text() for page in pdf)

def found_skills(text):
    low = text.lower()
    return sorted({s for s in SKILLS if re.search(r"(?<!\w)"+re.escape(s)+r"(?!\w)", low)})

def job_scores(candidate, jobs):
    docs = [candidate] + [j["title"]+" "+j["description"]+" "+j["skills"] for j in jobs]
    mat = TfidfVectorizer(stop_words="english", ngram_range=(1,2)).fit_transform(docs)
    return cosine_similarity(mat[0:1], mat[1:]).flatten()

mode = st.sidebar.radio("Choose role", ["Candidate", "Recruiter"])
if mode == "Candidate":
    st.subheader("Candidate: get job recommendations")
    file = st.file_uploader("Upload resume PDF", type=["pdf"])
    text = st.text_area("Or paste resume/profile text", height=160,
                        placeholder="Python, SQL, React, projects, education, experience...")
    if st.button("Analyze and recommend", type="primary"):
        try:
            resume = (text or "").strip()
            if file:
                resume += "\n" + pdf_text(file.getvalue())
            if len(resume.strip()) < 20:
                st.warning("Upload a text-based PDF or paste more profile details.")
            else:
                skills = found_skills(resume)
                scores = job_scores(resume, JOBS)
                ranked = sorted(zip(JOBS, scores), key=lambda x:x[1], reverse=True)
                st.markdown("### Extracted skills (dictionary-based demo)")
                st.write(", ".join(skills) if skills else "No listed skills detected; expand SKILLS in app.py.")
                st.markdown("### Recommended jobs")
                for job, score in ranked:
                    with st.container(border=True):
                        a,b = st.columns([4,1])
                        a.markdown(f"**{job['title']} — {job['company']}**")
                        a.caption(f"{job['location']} · Skills: {job['skills']}")
                        a.write(job["description"])
                        b.metric("Text match", f"{score*100:.1f}%")
                        b.progress(min(1.0, float(score)))
        except Exception as e:
            st.error(f"Could not process the resume: {e}")
else:
    st.subheader("Recruiter: rank candidates for a job")
    labels = [f"{j['title']} — {j['company']}" for j in JOBS]
    idx = labels.index(st.selectbox("Select job", labels))
    job = JOBS[idx]
    st.write("**Requirements:**", job["description"])
    profiles = st.text_area("Enter candidate profiles, one per line", height=180,
        placeholder="Candidate A: Python, SQL, REST APIs, Git\nCandidate B: React, JavaScript, CSS\nCandidate C: Python, pandas, NLP, machine learning")
    if st.button("Rank candidates", type="primary"):
        candidates = [x.strip() for x in profiles.splitlines() if len(x.strip()) > 5]
        if not candidates:
            st.warning("Enter at least one candidate profile.")
        else:
            docs = [job["title"]+" "+job["description"]+" "+job["skills"]] + candidates
            mat = TfidfVectorizer(stop_words="english", ngram_range=(1,2)).fit_transform(docs)
            scores = cosine_similarity(mat[0:1], mat[1:]).flatten()
            for rank,(candidate,score) in enumerate(sorted(zip(candidates,scores), key=lambda x:x[1], reverse=True),1):
                with st.container(border=True):
                    a,b=st.columns([5,1])
                    a.markdown(f"**#{rank} Candidate**")
                    a.write(candidate)
                    b.metric("Text match", f"{score*100:.1f}%")
st.divider()
st.caption("Demo data only. Do not use text-similarity scores as the sole basis for hiring decisions.")
