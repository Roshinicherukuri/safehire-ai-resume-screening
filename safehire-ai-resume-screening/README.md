# SafeHire — AI Resume Screening & Candidate Matching

SafeHire is a small, explainable resume-screening prototype. It converts uploaded resumes into text, detects skills, compares each resume with a job description using TF-IDF cosine similarity, and ranks candidates with a transparent ATS-style score.

## Features

- Upload multiple PDF, DOCX and TXT resumes
- Extract text from resumes
- Detect skills using an editable keyword vocabulary
- Compare resume text with a job description using TF-IDF
- Calculate an ATS-style score and rank candidates
- Show matched and missing skills
- Export results to CSV

## Tech stack

Python · Streamlit · Scikit-learn · TF-IDF · Pandas · NLP · pypdf · python-docx

## Run locally

```bash
git clone https://github.com/<your-username>/safehire-ai-resume-screening.git
cd safehire-ai-resume-screening

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`).

## Scoring method

The prototype uses this weighted formula:

`ATS score = (0.70 × TF-IDF similarity + 0.30 × skill coverage) × 100`

- **TF-IDF similarity:** cosine similarity between the job description and resume text.
- **Skill coverage:** number of detected job-description skills also found in the resume, divided by the number of detected job-description skills.

The skill vocabulary is in `src/matcher.py`. Add role-specific skills there to improve coverage for your target jobs.

## Project structure

```text
safehire-ai-resume-screening/
├── app.py
├── src/
│   ├── __init__.py
│   └── matcher.py
├── data/
│   ├── sample_job_description.txt
│   └── sample_resumes/
│       ├── python_candidate.txt
│       └── data_candidate.txt
├── requirements.txt
├── .gitignore
└── README.md
```

## Limitations and responsible use

- This is a portfolio/learning prototype, not a production hiring system.
- Keyword matching can miss synonyms, context and transferable skills.
- TF-IDF measures textual overlap; it does not establish competence or job performance.
- Scanned/image-only PDFs may need OCR, which is not included.
- Do not use protected characteristics or proxies for them in ranking.
- Keep a human reviewer in the loop. Validate the system for disparate impact, explainability, privacy and local employment-law requirements before any real hiring use.
- Do not upload confidential candidate information to an unapproved environment.

## Future improvements

- Add OCR for scanned resumes
- Add semantic embeddings for synonym-aware matching
- Add configurable skill weights by role
- Add unit tests and evaluation metrics on a consented, representative dataset
- Add database storage and recruiter authentication
