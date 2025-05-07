import streamlit as st
import pandas as pd
import openai
from agents.lineage_agent import get_changes, summarize_lineage_with_llm
from agents.quality_agent import run_dq_checks, summarize_dq_with_llm
from dotenv import load_dotenv
import os

# Load OpenAI API key from environment
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit configuration
st.set_page_config(page_title="Agentic AI: Loan Lineage + DQ", layout="wide")
st.title("📊 Agentic AI: Loan Data Lineage and Data Quality Analyzer")

# File Upload Section (Dynamic)
st.subheader("Upload CSV Files for Loan Processing")
uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)

if uploaded_files:
    # Check if files are uploaded
    st.write(f"Total {len(uploaded_files)} files uploaded")

    # Read the uploaded files and store them as DataFrames
    csv_paths = {}
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_df = pd.read_csv(uploaded_file)
        csv_paths[file_name] = file_df
        st.write(f"Loaded file: {file_name}")
        
    try:
        # Process lineage or data quality on the uploaded files
        merged_df = get_changes(csv_paths)
        st.success("CSV files uploaded and lineage processed.")

        # Ensure 'LoanNumber' is displayed as a string without commas
        merged_df['LoanNumber'] = merged_df['LoanNumber'].astype(str)

        # User input for loan number(s)
        loan_numbers_input = st.text_input("Enter one or more Loan Numbers (comma-separated):")
        if loan_numbers_input:
            loan_numbers = [ln.strip() for ln in loan_numbers_input.split(",")]
            filtered_df = merged_df[merged_df["LoanNumber"].isin(loan_numbers)]
            if not filtered_df.empty:
                st.subheader("Lineage Mapping for Selected Loan Numbers")

                # Display Lineage Summary in Markdown
                lineage_comments = filtered_df["LineageSummary"].tolist()
                for comment in lineage_comments:
                    st.markdown(f"**Lineage for Loan {filtered_df['LoanNumber'].iloc[lineage_comments.index(comment)]}:**")
                    st.markdown(f"- {comment}")

            else:
                st.warning("No matching Loan Numbers found.")

        # Lineage Summary Button
        if st.button("Generate LLM Summary for Lineage"):
            lineage_summary = summarize_lineage_with_llm(filtered_df['LineageSummary'].tolist())
            st.markdown("### 🧠 Lineage Summary via LLM")
            st.markdown(f"**Summary:** {lineage_summary}")
        # Check if the 'RequestedAmount_x' or 'RequestedAmount_y' exists
        # and use the one that is correct for your use case
        if 'RequestedAmount_x' in merged_df.columns:
            merged_df['RequestedAmount'] = merged_df['RequestedAmount_x']
        elif 'RequestedAmount_y' in merged_df.columns:
            merged_df['RequestedAmount'] = merged_df['RequestedAmount_y']
        else:
            st.error("'RequestedAmount' column is missing in the uploaded data.")
        
        # Data Quality Checks
        st.subheader("Run Data Quality Checks")
        # Pass the merged DataFrame (not csv_paths) to the data quality agent
        cleaned_df, dq_report = run_dq_checks(merged_df)  # Corrected this part

        # Ensure that 'LoanNumber' column is not missing for quality checks
        if 'LoanNumber' in cleaned_df.columns:
            st.dataframe(cleaned_df[["LoanNumber", "DQ_Report"]])
        else:
            st.warning("'LoanNumber' column is missing from the processed data.")

        # Generate LLM Summary for Data Quality Issues
        if st.button("Generate LLM Summary for DQ Issues"):
            dq_summary = summarize_dq_with_llm(dq_report)
            st.markdown("### 🩺 Data Quality Summary via LLM")
            st.markdown(f"**Summary:** {dq_summary}")

    except Exception as ex:
        st.error(f"Something went wrong: {ex}")

else:
    st.warning("Please upload CSV files to proceed.")
