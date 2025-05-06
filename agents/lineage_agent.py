# File: agent2_lineage.py (in agents/)

import pandas as pd
import os
from utils.prompt_templates import LINEAGE_SUMMARY_PROMPT
import openai


def get_changes(csv_paths):
    """
    Reads 5 CSVs representing loan processing stages and maps lineage
    for each LoanNumber. Outputs a summary DataFrame showing evolution.
    """
    # Load CSVs
    app_df = pd.read_csv(csv_paths['application'])
    credit_df = pd.read_csv(csv_paths['credit'])
    approval_df = pd.read_csv(csv_paths['approval'])
    disbursement_df = pd.read_csv(csv_paths['disbursement'])
    repayment_df = pd.read_csv(csv_paths['repayment'])

    # Merge all based on LoanNumber
    merged_df = app_df
    merged_df = merged_df.merge(credit_df, on='LoanNumber', how='left')
    merged_df = merged_df.merge(approval_df, on='LoanNumber', how='left')
    merged_df = merged_df.merge(disbursement_df, on='LoanNumber', how='left')
    merged_df = merged_df.merge(repayment_df, on='LoanNumber', how='left')

    # Derive lineage commentary
    comments = []
    for _, row in merged_df.iterrows():
        comment = f"Loan {row['LoanNumber']}: "
        if row['RiskSegment'] == 'High' and row['ApprovedAmount'] < row['RequestedAmount']:
            comment += "Approved lower than requested due to high risk. "
        elif row['RiskSegment'] == 'Medium':
            comment += "Moderate risk adjustment applied. "
        else:
            comment += "Full or near-full approval granted. "

        if row['DisbursedAmount'] < row['ApprovedAmount']:
            comment += "Deductions before disbursement. "

        if row['EMIStatus'] == 'Delayed' or row['EMIStatus'] == 'Missed':
            comment += f"Repayment not on track: {row['EMIStatus']}"
        else:
            comment += f"EMIs are on schedule."

        comments.append(comment)

    merged_df['LineageSummary'] = comments
    return merged_df


def summarize_lineage_with_llm(lineage_comments):
    """
    Uses LLM to generate a summary of lineage observations.
    """
    prompt = LINEAGE_SUMMARY_PROMPT.format(lineage="\n".join(lineage_comments))
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()