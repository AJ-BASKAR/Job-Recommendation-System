import string
import numpy as np
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st  # required for caching


# -------------------------------
# 🔒 Load and cache the transformer model
# -------------------------------
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer("paraphrase-MiniLM-L6-v2")


# -------------------------------
# 🔄 Preprocess job data and cache embeddings
# -------------------------------
@st.cache_data(show_spinner="🔄 Generating job embeddings...")
def preprocess_jobs(jobs_csv, _model):
    jobs_df = pd.read_csv(jobs_csv)
    jobs_df.fillna("", inplace=True)

    # Combine multiple fields into one searchable text block
    jobs_df["job_text"] = (
        jobs_df["workplace"].astype(str) + " "
        + jobs_df["working_mode"].astype(str) + " "
        + jobs_df["position"].astype(str) + " "
        + jobs_df["job_role_and_duties"].astype(str) + " "
        + jobs_df["requisite_skill"].astype(str)
    )

    # Encode job descriptions
    jobs_texts = jobs_df["job_text"].tolist()
    embeddings = _model.encode(jobs_texts, convert_to_numpy=True).astype(np.float32)

    # Create FAISS index for efficient similarity search
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    return jobs_df, jobs_texts, embeddings, index, dim


# -------------------------------
# 🚀 Job Recommendation System
# -------------------------------
class JobRecommendationSystem:
    def __init__(self, jobs_csv):
        self.model = load_model()
        (
            self.jobs_df,
            self.jobs_texts,
            self.job_embeddings,
            self.index,
            self.dim
        ) = preprocess_jobs(jobs_csv, self.model)

    def clean_text(self, text):
        """Lowercase, remove punctuation, and strip spaces."""
        return text.lower().translate(str.maketrans("", "", string.punctuation)).strip()

    def filter_top_jobs(self, resume_text, top_n=100):
        """Use TF-IDF to find top N jobs that match resume before semantic search."""
        vectorizer = TfidfVectorizer()
        job_vectors = vectorizer.fit_transform(self.jobs_texts)
        resume_vector = vectorizer.transform([resume_text])
        similarity_scores = (job_vectors @ resume_vector.T).toarray().flatten()
        top_indices = np.argsort(similarity_scores)[-top_n:]
        return (
            [self.jobs_texts[i] for i in top_indices],
            self.jobs_df.iloc[top_indices].reset_index(drop=True),
            self.job_embeddings[top_indices]
        )

    def recommend_jobs(self, resume_text, top_n=20, use_tfidf_filter=True):
        """Return top N recommended jobs based on the resume content."""
        resume_text = self.clean_text(resume_text)

        if use_tfidf_filter:
            filtered_texts, filtered_df, filtered_embeddings = self.filter_top_jobs(resume_text)
            temp_index = faiss.IndexFlatIP(self.dim)
            temp_index.add(filtered_embeddings)
            df_to_use = filtered_df
            index_to_use = temp_index
        else:
            df_to_use = self.jobs_df
            index_to_use = self.index

        # Generate embedding for resume
        resume_embedding = self.model.encode([resume_text], convert_to_numpy=True).astype(np.float32)

        # Search in FAISS index
        distances, indices = index_to_use.search(resume_embedding, top_n)
        recommended_jobs = df_to_use.iloc[indices[0]].to_dict(orient="records")

        return {
            "recommended_jobs": recommended_jobs
        }
