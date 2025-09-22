
import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Page Config ---
st.set_page_config(page_title="AI Resume Screening", page_icon="🧑‍💼", layout="wide")

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🧑‍💼 Smart Resume Screening Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Upload a job description and resumes. I’ll help you find the best matches, just like a hiring assistant would!</p>", unsafe_allow_html=True)
st.write("---")

# --- Job Description Upload ---
st.sidebar.header("📌 Step 1: Job Description")
jd_file = st.sidebar.file_uploader("Upload JD (TXT file)", type=["txt"])

# --- Resume Upload Options ---
st.sidebar.header("📌 Step 2: Resumes")
option = st.sidebar.radio("Choose Resume Format", ["CSV Dataset", "PDF Files"])

resume_texts, resume_names = [], []

if option == "CSV Dataset":
    resume_file = st.sidebar.file_uploader("Upload CSV file (must contain 'Resume' column)", type=["csv"])
    if resume_file:
        df = pd.read_csv(resume_file)
        if "Resume" not in df.columns:
            st.error("❌ The CSV must have a column named 'Resume'")
        else:
            resume_texts = df["Resume"].astype(str).tolist()
            resume_names = df.index.astype(str).tolist()

elif option == "PDF Files":
    pdf_files = st.sidebar.file_uploader("Upload multiple PDF resumes", type=["pdf"], accept_multiple_files=True)
    for pdf in pdf_files:
        try:
            doc = fitz.open(stream=pdf.read(), filetype="pdf")
            text = "".join([page.get_text("text") for page in doc])
            resume_texts.append(text)
            resume_names.append(pdf.name)
        except Exception as e:
            st.error(f"⚠️ Error reading {pdf.name}: {e}")

# --- Processing ---
if jd_file and resume_texts:
    job_description = jd_file.read().decode("utf-8")

    # Vectorization
    vectorizer = TfidfVectorizer(stop_words="english")
    resume_vectors = vectorizer.fit_transform(resume_texts)
    jd_vector = vectorizer.transform([job_description])

    # Similarity scores
    similarities = cosine_similarity(jd_vector, resume_vectors).flatten()

    # Results
    results = pd.DataFrame({
        "Candidate": resume_names,
        "Match %": (similarities * 100).round(2),
        "Extracted Resume": resume_texts
    }).sort_values(by="Match %", ascending=False)

    # --- Display Results ---
    st.success("✅ Screening complete! Here are the top matches:")
    st.subheader("🏆 Top Candidates")

    for idx, row in results.head(5).iterrows():
        st.markdown(
            f"""
            <div style="border:1px solid #ddd; border-radius:10px; padding:15px; margin-bottom:10px;">
                <h4>👤 {row['Candidate']}</h4>
                <p><b>Match Score:</b> {row['Match %']}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- Download Option ---
    st.write("---")
    st.info("💾 Download full ranking for HR records:")
    csv = results.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Full Results (CSV)",
        data=csv,
        file_name="resume_screening_results.csv",
        mime="text/csv",
    )

else:
    st.warning("👆 Please upload both a Job Description and at least one Resume input to get started.")



