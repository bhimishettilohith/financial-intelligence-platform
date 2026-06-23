from pathlib import Path
import pandas as pd


RAW_DATA_PATH = Path("data/raw")
OUTPUT_PATH = Path("output")

OUTPUT_PATH.mkdir(exist_ok=True)

validation_failures = []


def load_core_file(file_name):
    """
    Load Excel file using header=1
    """
    return pd.read_excel(
        RAW_DATA_PATH / file_name,
        header=1
    )


# =====================================================
# DQ-01
# Company PK uniqueness
# =====================================================

def dq01_company_pk_uniqueness(companies_df):

    duplicates = companies_df[
        companies_df["id"].duplicated()
    ]

    for _, row in duplicates.iterrows():

        validation_failures.append({
            "rule_id": "DQ-01",
            "severity": "CRITICAL",
            "table": "companies",
            "company": row["id"],
            "message": "Duplicate company id"
        })


# =====================================================
# DQ-02
# (company_id, year) uniqueness
# =====================================================

def dq02_company_year_uniqueness(pl_df):

    duplicates = pl_df[
        pl_df.duplicated(
            subset=["company_id", "year"],
            keep=False
        )
    ]

    for _, row in duplicates.iterrows():

        validation_failures.append({
            "rule_id": "DQ-02",
            "severity": "CRITICAL",
            "table": "profitandloss",
            "company": row["company_id"],
            "message": f"Duplicate year record: {row['year']}"
        })


# =====================================================
# DQ-03
# FK Integrity
# =====================================================

def dq03_fk_integrity(df, table_name, valid_company_ids):

    invalid_rows = df[
        ~df["company_id"].isin(valid_company_ids)
    ]

    for _, row in invalid_rows.iterrows():

        validation_failures.append({
            "rule_id": "DQ-03",
            "severity": "CRITICAL",
            "table": table_name,
            "company": row["company_id"],
            "message": "Foreign key not found in companies table"
        })


# =====================================================
# DQ-04
# Balance Sheet Balance Check
# Assets ≈ Liabilities (within 1%)
# =====================================================

def dq04_balance_sheet_balance(bs_df):

    valid_rows = bs_df[
        bs_df["total_assets"] > 0
    ].copy()

    valid_rows["diff_pct"] = (
        abs(
            valid_rows["total_assets"]
            - valid_rows["total_liabilities"]
        )
        / valid_rows["total_assets"]
        * 100
    )

    failures = valid_rows[
        valid_rows["diff_pct"] > 1
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-04",
            "severity": "WARNING",
            "table": "balancesheet",
            "company": row["company_id"],
            "message": f"Balance sheet mismatch {row['diff_pct']:.2f}%"
        })


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print("Loading datasets...")

    companies = load_core_file("companies.xlsx")
    profitandloss = load_core_file("profitandloss.xlsx")
    balancesheet = load_core_file("balancesheet.xlsx")
    cashflow = load_core_file("cashflow.xlsx")

    valid_company_ids = set(
        companies["id"]
    )

    print("Running validations...")

    dq01_company_pk_uniqueness(companies)

    dq02_company_year_uniqueness(
        profitandloss
    )

    dq03_fk_integrity(
        profitandloss,
        "profitandloss",
        valid_company_ids
    )

    dq03_fk_integrity(
        balancesheet,
        "balancesheet",
        valid_company_ids
    )

    dq03_fk_integrity(
        cashflow,
        "cashflow",
        valid_company_ids
    )

    dq04_balance_sheet_balance(
        balancesheet
    )

    failures_df = pd.DataFrame(
        validation_failures,
        columns=[
            "rule_id",
            "severity",
            "table",
            "company",
            "message"
        ]
    )

    output_file = (
        OUTPUT_PATH /
        "validation_failures.csv"
    )

    failures_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Validation complete. "
        f"Failures: {len(failures_df)}"
    )

    print(
        f"Output file: {output_file}"
    )

    print("\nValidation Summary:")

    if len(failures_df) > 0:
        print(
            failures_df["rule_id"]
            .value_counts()
        )
    else:
        print("No validation failures found.")