import pandas as pd
import streamlit as st
import requests

st.set_page_config(page_title="JD ↔ Resume Matcher", layout="wide")
st.title("📄 JD ↔ Resume Matcher")

with st.expander("🔍 Upload Files", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        jd_file = st.file_uploader("Job Description", type=["txt", "pdf", "docx"], key="jd")
    with col2:
        resume_files = st.file_uploader("Resumes", type=["txt", "pdf", "docx"], accept_multiple_files=True, key="resumes")


with st.expander("Select parameters", expanded=True):

    col1, col2 = st.columns(2)
    with col1:
        # Matching method selection
        matching_method = st.radio(
            "🧠 Select Matching Method",
            options=["AI Matching", "Traditional Matching", "Both"],
            index=1,
            help="AI Matching uses semantic similarity (e.g., GPT), Traditional Matching uses keyword-based TF-IDF.",
            horizontal=True
        )
    with col2:
        # Adding keyword input
        keywords = st.text_input("🔑 Must have keywords in the resume (comma-separated)",
                                 help="Enter keywords separated by commas")

    method_map = {
        "AI Matching": "ai",
        "Traditional Matching": "traditional",
        "Both": "both"
    }
    selected_methods = [method_map[matching_method]]

    col1, col2 = st.columns(2)
    with col1:
        threshold = st.slider("🎯 Min Match %", min_value=0, max_value=100, value=40)
    with col2:
        alpha = st.slider("⚖️ TF-IDF vs Semantic", 0.0, 1.0, 0.5, 0.05)


if st.button("🔍 Match"):
    if not jd_file or not resume_files:
        st.warning("Please upload both JD and at least one resume.")
    elif not selected_methods:
        st.warning("Please select at least one matching method.")
    else:
        with st.spinner("Matching in progress..."):
            files = [("jd_file", (jd_file.name, jd_file, jd_file.type))]
            for f in resume_files:
                files.append(("resumes", (f.name, f, f.type)))

            params = {
                "alpha": alpha,
                "methods": ",".join(selected_methods),
                "keywords": keywords
            }

            response = requests.post("http://localhost:5000/match", files=files, params=params)

        if response.status_code == 200:
            data = response.json()
            st.write(f"### ✅ {data.get('total_resumes', 0)} Resumes Processed")
            with st.expander("📦 Full Response Data", expanded=False):
                st.write(data)

            if "ai_results" in data:
                st.subheader("🤖 AI Matching Results")
                st.dataframe([
                    {
                        "Resume #": r["resume_index"] + 1,
                        "Filename":r["resume_name"],
                        "Accepted by OpenAI": r["accepted_by_openai"],
                        "Reason": r["reason"]
                    }
                    for r in data["ai_results"]
                ])

            if "traditional_results" in data:
                st.subheader("📘 Traditional Matching Results")
                df = pd.DataFrame([
                    {
                        "Resume #": r["resume_index"] + 1,
                        "Filename":r["resume_name"],
                        "Match % (Higher the better)": round(r["tfidf_score"], 2) * 100,
                        "Semantic Score": round(r["semantic_score"], 2),
                        "Reason": r["reason"],
                        "Accepted by rule": r["accepted_by_rule"],
                        "ATS Compliance Report": r["ats_compliance_report"]
                    }
                    for r in data["traditional_results"]
                    if round(r["tfidf_score"] * 100) >= threshold
                ])
                st.dataframe(df)

                # Function to display DataFrame with word wrap
                def display_dataframe_with_word_wrap(df):
                    st.markdown(
                        """
                         <style>
                         .dataframe thead th {
                         text-align: center;
                         }
                         .dataframe tbody tr td {
                         word-wrap: break-word;
                         white-space: normal;
                         }
                         </style>
                        """,
                        unsafe_allow_html=True
                    )
                    st.write(df.to_html(escape=False), unsafe_allow_html=True)

                display_dataframe_with_word_wrap(df)

        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
