# utils/prompt_templates.py

# Prompt for summarizing Data Quality issues from Agent 3
DQ_SUMMARY_PROMPT = """
You are a data quality analyst reviewing loan processing pipeline issues.
Summarize the problems detected below in a clear, actionable manner for business stakeholders.

Issues Detected:
{issues}

Respond with:
1. Key categories of issues
2. Potential risks if unaddressed
3. Suggested next steps to improve data quality
"""

# Prompt for summarizing lineage commentary from Agent 2
LINEAGE_SUMMARY_PROMPT = """
You are a business analyst reviewing how loans evolved across their lifecycle.
Below is a summary for each loan. Present a high-level report with key trends and exceptions.

Lineage Summary:
{lineage}

Respond with:
- Major observations
- Highlighted anomalies
- Any business rule violations or patterns
"""

# Prompt for explaining EMI calculation to a non-financial user
EMI_EXPLAINER_PROMPT = """
You are a loan officer explaining EMI calculation in plain English.

Loan Amount: ₹{amount}
Interest Rate: {rate}%

Please explain:
- How EMI is calculated
- Why it's important to monitor
- What happens if it's miscalculated or delayed
"""
