import os

def load_csv_paths(base_dir="data"):
    """
    Validates and returns the full paths to required CSVs from the data folder.
    Expects files with these exact names:
    - 01_application.csv
    - 02_credit_check.csv
    - 03_approval.csv
    - 04_disbursement.csv
    - 05_repayment.csv
    """
    expected_files = {
        "application": "01_application.csv",
        "credit": "02_credit_check.csv",
        "approval": "03_approval.csv",
        "disbursement": "04_disbursement.csv",
        "repayment": "05_repayment.csv"
    }

    csv_paths = {}
    for key, filename in expected_files.items():
        full_path = os.path.join(base_dir, filename)
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"Missing required file: {filename}")
        csv_paths[key] = full_path

    return csv_paths
