

Welcome! This is your **friendly AI-powered assistant** for quickly screening resumes.  
Upload a **Job Description** and candidate resumes, and it’ll help you **find the best matches** — just like having a real HR partner by your side! 💼✨


- **Upload Job Description** (TXT file)  
- **Upload Resumes** in two ways:
  - CSV dataset (must have a column called **Resume**)  
  - Multiple PDF files (we’ll extract text automatically!)  
- **Rank candidates** using AI (TF-IDF + Cosine Similarity)  
- **Friendly dashboard** that guides you step by step  
- **Download results** to share with your team or for records  
## 🛠️ Built With
- **Python 3.12+** – core programming  
- **Streamlit** – interactive, easy-to-use dashboard  
- **Pandas** – organize and handle data  
- **Scikit-learn** – calculate resume-job similarity  
- **PyMuPDF (fitz)** – read PDF resumes  
## 📂 How The Project Is Organized
ResumeScreeningAI/
│── app.py # Main interactive app
│── requirements.txt # Libraries needed
│── README.md # This friendly guide
│── sample_resumes/ # Example resumes (optional)
│── job_description.txt # Example Job Description (optional)
│── .gitignore # Files to ignore in Git

pip install -r requirements.txt
streamlit run app.py
