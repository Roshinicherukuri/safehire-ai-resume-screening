import io
import re
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Extend this domain vocabulary for the roles your team recruits for.
SKILLS = {
    "python", "java", "c++", "javascript", "typescript", "sql", "mysql", "postgresql",
    "mongodb", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "machine learning",
    "deep learning", "nlp", "natural language processing", "tf-idf", "spacy", "nltk",
    "flask", "django", "fastapi", "streamlit", "rest api", "api development",
    "html", "css", "react", "node.js", "git", "docker", "kubernetes", "aws", "azure",
    "linux", "power bi", "tableau", "excel", "data analysis", "data visualization",
    "statistics", "communication", "project management", "agile", "spring boot",
}

def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_skills(text: str) -> set[str]:
    normalized = _normalize(text)
    found = set()
    for skill in SKILLS:
        # Word boundaries avoid matching short skills inside unrelated words.
        pattern = r"(?<![a-z0-9+#.])" + re.escape(skill) + r"(?![a-z0-9+#.])"
        if re.search(pattern, normalized):
            found.add(skill)
    return found

def extract_text(file_bytes: bytes, filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".txt":
        return file_bytes.decode("utf-8", errors="ignore")
    if suffix == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        from docx import Document
        document = Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in document.paragraphs)
    raise ValueError("Unsupported file type. Upload PDF, DOCX or TXT.")

def evaluate_resume(filename: str, resume_text: str, job_description: str) -> dict:
    resume = _normalize(resume_text)
    job = _normalize(job_description)
    if not resume:
        raise ValueError("No readable text found in this file.")

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([job, resume])
    similarity = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])

    job_skills = extract_skills(job)
    resume_skills = extract_skills(resume)
    matched = sorted(job_skills & resume_skills)
    missing = sorted(job_skills - resume_skills)
    skill_score = len(matched) / len(job_skills) if job_skills else 0.0

    # Transparent weighted score: 70% TF-IDF similarity + 30% skill coverage.
    ats_score = round((0.70 * similarity + 0.30 * skill_score) * 100)
    return {
        "candidate": Path(filename).stem,
        "ats_score": ats_score,
        "similarity": round(similarity * 100, 1),
        "matched_skills": ", ".join(matched),
        "missing_skills": ", ".join(missing),
    }
