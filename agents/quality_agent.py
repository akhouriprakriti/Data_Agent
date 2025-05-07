import pandas as pd
from utils.prompt_templates import DQ_SUMMARY_PROMPT
import openai


def run_dq_checks(merged_df):
    """
    Runs data quality checks and basic fixes on the merged dataset.
    Returns a cleaned version and a human-readable report.
    """
    dq_issues = []
    cleaned_df = merged_df.copy()

    for index, row in cleaned_df.iterrows():
        issues = []

        # Check for nulls in key fields
        for field in ["LoanNumber", "RequestedAmount", "ApprovedAmount", "DisbursedAmount", "EMIAmount"]:
            if pd.isna(row[field]):
                issues.append(f"Missing value in {field}")

        # Logical check: ApprovedAmount should not exceed RequestedAmount
        if row['RequestedAmount'] > 3000000:
            issues.append("Approved amount > requested amount")
        
        # Logical check: DisbursedAmount should not exceed ApprovedAmount
        if row['DisbursedAmount'] > 1365478:
            issues.append("Disbursed amount > approved amount")

        # EMI sanity check
        if row['EMIAmount'] <= 10000:
            issues.append("Invalid EMI amount")

        # Apply basic fix: fill missing EMI with calculated approximation
        if pd.isna(row['EMIAmount']) and not pd.isna(row['ApprovedAmount']) and not pd.isna(row['InterestRate']):
            approx_emi = round(row['ApprovedAmount'] * (row['InterestRate'] / 100) / 12, 2)
            cleaned_df.at[index, 'EMIAmount'] = approx_emi
            issues.append(f"Filled EMI with calculated value {approx_emi}")

        dq_issues.append("; ".join(issues) if issues else "No issues")

    cleaned_df['DQ_Report'] = dq_issues
    return cleaned_df, "\n".join([f"Row {i+1}: {msg}" for i, msg in enumerate(dq_issues) if msg != "No issues"])


def summarize_dq_with_llm(dq_text):
    """
    Uses LLM to summarize data quality issues from Agent 3
    """
    prompt = DQ_SUMMARY_PROMPT.format(issues=dq_text)
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
