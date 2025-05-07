import pandas as pd
import os
from utils.prompt_templates import LINEAGE_SUMMARY_PROMPT
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
def get_changes(csv_paths):
    """
    Dynamically processes all CSV files uploaded by the user, and generates lineage summaries based on relationships.
    """
    # Load all CSVs dynamically based on uploaded files
    dataframes = {}
    for file_name, file_df in csv_paths.items():
        dataframes[file_name] = file_df

    # Assuming all dataframes have a 'LoanNumber' column to merge on
    merged_df = dataframes[list(dataframes.keys())[0]]  # Start with the first dataframe

    # Merge all dataframes on 'LoanNumber'
    for file_name, df in dataframes.items():
        if "LoanNumber" in df.columns:
            merged_df = merged_df.merge(df, on="LoanNumber", how="left")

    # Derive lineage commentary
    comments = []
    for _, row in merged_df.iterrows():
        comment = f"Loan {row['LoanNumber']}: "
        # Dynamically determine which columns to check
        if 'RiskSegment' in row and row['RiskSegment'] == 'High' and 'ApprovedAmount' in row and row['ApprovedAmount'] < row.get('RequestedAmount', 0):
            comment += "Approved lower than requested due to high risk. "
        elif 'RiskSegment' in row and row['RiskSegment'] == 'Medium':
            comment += "Moderate risk adjustment applied. "
        else:
            comment += "Full or near-full approval granted. "

        if 'DisbursedAmount' in row and row['DisbursedAmount'] < row.get('ApprovedAmount', 0):
            comment += "Deductions before disbursement. "

        if 'EMIStatus' in row and (row['EMIStatus'] == 'Delayed' or row['EMIStatus'] == 'Missed'):
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
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
