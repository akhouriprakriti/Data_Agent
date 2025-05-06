# File: main.py

import streamlit as st
import pandas as pd
from utils.file_loader import load_csv_paths
from agents.lineage_agent import get_changes, summarize_lineage_with_llm
from agents.quality_agent import run_dq_checks, summarize_dq_with_llm

st.set_page_config(page_title="Agentic AI: Loan Lineage + DQ", layout="wide")
st.title("📊 Agentic AI: Loan Data Lineage and Data Quality Analyzer")

# Load CSVs from data folder
try:
    csv_paths = load_csv_paths("data")
    merged_df = get_changes(csv_paths)
    st.success("CSV files loaded and lineage processed.")

    st.subheader("Lineage Mapping")
    st.dataframe(merged_df[["LoanNumber", "LineageSummary"]])

    if st.button("Generate LLM Summary for Lineage"):
        lineage_summary = summarize_lineage_with_llm(merged_df['LineageSummary'].tolist())
        st.markdown("### 🧠 Lineage Summary via LLM")
        st.write(lineage_summary)

    # Data Quality Checks
    st.subheader("Run Data Quality Checks")
    cleaned_df, dq_report = run_dq_checks(merged_df)
    st.dataframe(cleaned_df[["LoanNumber", "DQ_Report"]])

    if st.button("Generate LLM Summary for DQ Issues"):
        dq_summary = summarize_dq_with_llm(dq_report)
        st.markdown("### 🩺 Data Quality Summary via LLM")
        st.write(dq_summary)

except FileNotFoundError as e:
    st.error(str(e))
except Exception as ex:
    st.error(f"Something went wrong: {ex}")
