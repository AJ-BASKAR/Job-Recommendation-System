🤖 AI-Powered Job Recommendation System
🚀 Developed by AJ Baskar
🧠 Overview
The AI-Powered Job Recommendation System is an intelligent web application built by AJ Baskar that helps job seekers discover the most suitable career opportunities based on their resume content. By combining Natural Language Processing, semantic similarity, and vector search, this system goes beyond keyword matching and delivers smart, contextual job recommendations.

It’s ideal for recent graduates, professionals changing fields, or anyone looking for personalized job insights.

🌟 Highlighted Features
📄 Upload Resume (PDF): Automatically reads and analyzes your resume.

🔍 AI-Driven Job Matching: Uses SentenceTransformer for contextual understanding.

⚡ FAISS Indexing: Enables lightning-fast similarity search across thousands of job descriptions.

🧠 TF-IDF Filtering: Narrows down to the most relevant job categories before semantic matching.

🌐 Interactive UI with Streamlit: Provides a responsive and intuitive interface.

📊 Real-time Recommendations: See top job matches instantly after uploading your resume.

💼 Keyword Skill Highlighting: Skills in your resume are matched with job requirements.

📥 Download Matching Jobs (Planned): Export recommendations in PDF format.

🧰 Tech Stack
Technology	Purpose
Python	Core logic, NLP, and data processing
Streamlit	Web interface
FAISS	Approximate nearest neighbor search
SentenceTransformer	Text embeddings for semantic comparison
PyMuPDF (fitz)	Extracts raw text from PDF resumes
scikit-learn	TF-IDF filtering and preprocessing
pandas & NumPy	Data manipulation and structuring

🧪 How It Works
Resume Ingestion

The user uploads a .pdf file.

PyMuPDF parses and extracts the content.

Preprocessing

Important keywords and skills are extracted.

TF-IDF reduces irrelevant job roles.

Semantic Search

The filtered jobs and resume text are embedded using SentenceTransformer.

FAISS identifies the closest job matches based on cosine similarity.

Result Display

Top 5–10 most relevant job roles are shown.

Option to view job descriptions and matched skill highlights.

📂 Dataset Details
JobsFE.csv includes:

Job Titles

Job Descriptions

Required Skills

Company Info (optional)

Work Type (remote/on-site)

Tip: You can update this dataset to match different industries (e.g., Data Science, Web Dev, etc.)

🚀 Getting Started
bash
Copy
Edit
# 1. Clone the repo
git clone https://github.com/AJBaskar/job-recommendation-system-ai.git
cd job-recommendation-system-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run streamlit.py
Make sure you have Python ≥ 3.8 installed and a stable internet connection for model loading.

🔮 Future Roadmap
✅ Resume support for .docx and .txt

✅ Filter jobs by location, salary, or domain

✅ Integration with real-time APIs (LinkedIn, Indeed)

✅ Personalized job alerts via email

✅ PDF report of recommended jobs

✅ Admin dashboard to update jobs dataset via UI

✅ Skill-gap analysis and suggestions for upskilling

📸 Screenshots (Optional)
Add screenshots of the Streamlit app: Upload Section, Top Job Matches, UI Preview, etc.

📌 Why This Project?
As a Data Science and AI enthusiast, AJ Baskar wanted to solve a real-world problem faced by many job seekers—finding jobs that actually match their unique skillset. Traditional keyword-matching job boards fail to understand context. This project fills that gap by using semantic AI to connect candidates with ideal job opportunities.

