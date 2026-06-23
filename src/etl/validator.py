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
# DQ-05
# OPM Cross Check
# =====================================================

def dq05_opm_crosscheck(pl_df):

    valid_rows = pl_df[
        (pl_df["sales"] > 0)
        & (pl_df["opm_percentage"].notna())
        & (pl_df["opm_percentage"] >= -100)
        & (pl_df["opm_percentage"] <= 100)
    ].copy()

    valid_rows["calc_opm"] = (
        valid_rows["operating_profit"]
        / valid_rows["sales"]
        * 100
    )

    valid_rows["diff"] = abs(
        valid_rows["calc_opm"]
        - valid_rows["opm_percentage"]
    )

    failures = valid_rows[
        valid_rows["diff"] > 2
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-05",
            "severity": "WARNING",
            "table": "profitandloss",
            "company": row["company_id"],
            "message": (
                f"OPM mismatch. "
                f"Expected={row['calc_opm']:.2f}, "
                f"Actual={row['opm_percentage']}"
            )
        })


# =====================================================
# DQ-06
# Positive Sales
# =====================================================

def dq06_positive_sales(pl_df):

    failures = pl_df[
        pl_df["sales"] < 0
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-06",
            "severity": "WARNING",
            "table": "profitandloss",
            "company": row["company_id"],
            "message": "Negative sales value"
        })


# =====================================================
# DQ-07
# Net Cash Flow Check
# =====================================================

def dq07_net_cashflow(cf_df):

    calc = (
        cf_df["operating_activity"]
        + cf_df["investing_activity"]
        + cf_df["financing_activity"]
    )

    failures = cf_df[
        abs(calc - cf_df["net_cash_flow"]) > 1
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-07",
            "severity": "WARNING",
            "table": "cashflow",
            "company": row["company_id"],
            "message": f"Net cash flow mismatch ({row['year']})"
        })


# =====================================================
# DQ-08
# Tax Rate Validation
# =====================================================

def dq08_tax_rate(pl_df):

    failures = pl_df[
        (pl_df["tax_percentage"] < 0)
        | (pl_df["tax_percentage"] > 100)
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-08",
            "severity": "WARNING",
            "table": "profitandloss",
            "company": row["company_id"],
            "message": f"Invalid tax rate {row['tax_percentage']}"
        })


# =====================================================
# DQ-09
# Dividend Payout Validation
# =====================================================

def dq09_dividend_payout(pl_df):

    failures = pl_df[
        (pl_df["dividend_payout"] < 0)
        | (pl_df["dividend_payout"] > 100)
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-09",
            "severity": "WARNING",
            "table": "profitandloss",
            "company": row["company_id"],
            "message": f"Invalid dividend payout {row['dividend_payout']}"
        })


# =====================================================
# DQ-10
# EPS Sign Check
# =====================================================

def dq10_eps_sign(pl_df):

    failures = pl_df[
        (
            (pl_df["net_profit"] > 0)
            & (pl_df["eps"] < 0)
        )
        |
        (
            (pl_df["net_profit"] < 0)
            & (pl_df["eps"] > 0)
        )
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-10",
            "severity": "WARNING",
            "table": "profitandloss",
            "company": row["company_id"],
            "message": "EPS sign inconsistent with net profit"
        })


# =====================================================
# DQ-11
# Documents FK Validation
# =====================================================

def dq11_documents_fk(doc_df, valid_company_ids):

    failures = doc_df[
        ~doc_df["company_id"].isin(valid_company_ids)
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-11",
            "severity": "CRITICAL",
            "table": "documents",
            "company": row["company_id"],
            "message": "Company not found in master table"
        })


# =====================================================
# DQ-12
# Analysis FK Validation
# =====================================================

def dq12_analysis_fk(analysis_df, valid_company_ids):

    failures = analysis_df[
        ~analysis_df["company_id"].isin(valid_company_ids)
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-12",
            "severity": "CRITICAL",
            "table": "analysis",
            "company": row["company_id"],
            "message": "Company not found in master table"
        })


# =====================================================
# DQ-13
# ProsCons FK Validation
# =====================================================

def dq13_proscons_fk(pc_df, valid_company_ids):

    failures = pc_df[
        ~pc_df["company_id"].isin(valid_company_ids)
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-13",
            "severity": "CRITICAL",
            "table": "prosandcons",
            "company": row["company_id"],
            "message": "Company not found in master table"
        })


# =====================================================
# DQ-14
# URL Validation
# =====================================================

def dq14_url_validation(doc_df):

    failures = doc_df[
        ~doc_df["Annual_Report"]
        .astype(str)
        .str.startswith(
            ("http://", "https://")
        )
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-14",
            "severity": "WARNING",
            "table": "documents",
            "company": row["company_id"],
            "message": "Invalid annual report URL"
        })


# =====================================================
# DQ-15
# Duplicate Reports
# =====================================================

def dq15_duplicate_reports(doc_df):

    failures = doc_df[
        doc_df.duplicated(
            subset=["company_id", "Year"],
            keep=False
        )
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-15",
            "severity": "WARNING",
            "table": "documents",
            "company": row["company_id"],
            "message": f"Duplicate annual report {row['Year']}"
        })


# =====================================================
# DQ-16
# Missing Values
# =====================================================

def dq16_missing_values(companies_df):

    failures = companies_df[
        companies_df.isnull().any(axis=1)
    ]

    for _, row in failures.iterrows():

        validation_failures.append({
            "rule_id": "DQ-16",
            "severity": "WARNING",
            "table": "companies",
            "company": row["id"],
            "message": "Missing mandatory field"
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
    analysis = load_core_file("analysis.xlsx")
    documents = load_core_file("documents.xlsx")
    prosandcons = load_core_file("prosandcons.xlsx")

    valid_company_ids = set(
        companies["id"]
    )

    print("Running validations...")

    # DQ-01
    dq01_company_pk_uniqueness(
        companies
    )

    # DQ-02
    dq02_company_year_uniqueness(
        profitandloss
    )

    # DQ-03
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

    # DQ-04
    dq04_balance_sheet_balance(
        balancesheet
    )

    # DQ-05
    dq05_opm_crosscheck(
        profitandloss
    )

    # DQ-06
    dq06_positive_sales(
        profitandloss
    )

    # DQ-07
    dq07_net_cashflow(
        cashflow
    )

    # DQ-08
    dq08_tax_rate(
        profitandloss
    )

    # DQ-09
    dq09_dividend_payout(
        profitandloss
    )

    # DQ-10
    dq10_eps_sign(
        profitandloss
    )

    # DQ-11
    dq11_documents_fk(
        documents,
        valid_company_ids
    )

    # DQ-12
    dq12_analysis_fk(
        analysis,
        valid_company_ids
    )

    # DQ-13
    dq13_proscons_fk(
        prosandcons,
        valid_company_ids
    )

    # DQ-14
    dq14_url_validation(
        documents
    )

    # DQ-15
    dq15_duplicate_reports(
        documents
    )

    # DQ-16
    dq16_missing_values(
        companies
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
        f"\nValidation complete. "
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
        print(
            "No validation failures found."
        )