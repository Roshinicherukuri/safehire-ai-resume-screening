import streamlit as st
import pandas as pd
from src.matcher import extract_text, evaluate_resume

st.set_page_config(page_title="SafeHire | AI Resume Screener", page_icon="🧑‍💼", layout="wide")
st.title("🧑‍💼 SafeHire")
st.caption("AI-assisted resume screening and candidate-to-job matching")
st.info("Decision-support prototype: scores are estimates, not hiring decisions. Review every candidate manually.")

job_description = st.text_area(
    "Paste the job description",
    value="Python developer with experience in Python, SQL, Pandas, Scikit-learn, NLP, REST APIs and machine learning.",
    height=170,
)
uploads = st.file_uploader(
    "Upload resumes (PDF, DOCX or TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

if st.button("Screen resumes", type="primary", disabled=not job_description.strip() or not uploads):
    results = []
    progress = st.progress(0)
    for i, uploaded in enumerate(uploads):
        try:
            text = extract_text(uploaded.getvalue(), uploaded.name)
            result = evaluate_resume(uploaded.name, text, job_description)
            results.append(result)
        except Exception as exc:
            st.error(f"Could not process {uploaded.name}: {exc}")
        progress.progress((i + 1) / len(uploads))

    if results:
        df = pd.DataFrame(results).sort_values("ats_score", ascending=False)
        st.subheader("Candidate ranking")
        st.dataframe(
            df[["candidate", "ats_score", "similarity", "matched_skills", "missing_skills"]],
            use_container_width=True,
            hide_index=True,
        )
        st.download_button(
            "Download results as CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="safehire_screening_results.csv",
            mime="text/csv",
        )
        st.subheader("Candidate details")
        for row in df.to_dict("records"):
            with st.expander(f"{row['candidate']} — ATS score: {row['ats_score']}/100"):
                st.write(f"**Matched skills:** {row['matched_skills'] or 'None detected'}")
                st.write(f"**Missing job skills:** {row['missing_skills'] or 'None detected'}")
                st.write(f"**Text similarity:** {row['similarity']}%")
                st.caption("The score is based on text similarity and detected skills only. It does not assess candidate quality, personality, or protected characteristics.")
