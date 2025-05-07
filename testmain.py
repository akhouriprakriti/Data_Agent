import pandas as pd
from agents.quality_agent import run_dq_checks, summarize_dq_with_llm   
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Sample data (replace this with your actual merged_df)
data = {
    'LoanNumber': [123, 456, 789],
    'RequestedAmount': [10000, 20000, 15000],
    'ApprovedAmount': [9000, 20000, 14000],
    'DisbursedAmount': [9000, 19500, 13500],
    'EMIAmount': [300, None, 350],
    'InterestRate': [5, 4.5, 5]
}

merged_df = pd.DataFrame(data)

# Run data quality checks
cleaned_df, dq_report = run_dq_checks(merged_df)

# Check the cleaned data and the report
print(cleaned_df)  # This should display the dataframe with DQ_Report
print(dq_report)   # This should display the summary of data quality issues


# Test summarize_dq_with_llm
dq_summary = summarize_dq_with_llm(dq_report)
print(dq_summary)  # This will print the LLM summary of the data quality issues
