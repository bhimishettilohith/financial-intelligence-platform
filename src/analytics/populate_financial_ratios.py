"""
Populate Computed Financial Ratios
Sprint 2 - Day 12
"""

import sqlite3
import pandas as pd
import numpy as np
import os

EDGE_CASE_LOG = "output/ratio_edge_cases.log"

from src.analytics.ratios import (
    calculate_net_profit_margin,
    calculate_operating_profit_margin,
    calculate_roe,
    calculate_roce,
    calculate_roa,
    calculate_debt_to_equity,
    calculate_high_leverage_flag,
    calculate_interest_coverage,
    calculate_icr_label,
    calculate_icr_warning_flag,
    calculate_net_debt,
    calculate_asset_turnover
)

from src.analytics.cagr import calculate_cagr

from src.analytics.cashflow_kpis import (
    calculate_free_cash_flow,
    calculate_cfo_quality_score,
    calculate_capex_intensity,
    calculate_fcf_conversion
)

DB_PATH = "nifty100.db"


def clean(value):
    """
    Convert NaN to None
    """

    if pd.isna(value):
        return None

    return value


def main():

    print("=" * 60)
    print("Financial Ratio Engine")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)

    # ------------------------------------------
    # Load tables
    # ------------------------------------------

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    profitandloss = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    balancesheet = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    sectors = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    print("\nTables Loaded")

    print("Companies :", len(companies))
    print("P&L       :", len(profitandloss))
    print("BS        :", len(balancesheet))
    print("Cashflow  :", len(cashflow))
    print("Sectors   :", len(sectors))

    # ------------------------------------------
    # Remove duplicate company-year rows
    # ------------------------------------------

    balancesheet = balancesheet.drop_duplicates(
        subset=["company_id", "year"]
    )

    cashflow = cashflow.drop_duplicates(
        subset=["company_id", "year"]
    )

    # ------------------------------------------
    # Merge tables
    # ------------------------------------------

    merged = (

        profitandloss

        .merge(
            balancesheet,
            on=[
                "company_id",
                "year"
            ],
            how="left",
            suffixes=(
                "_pl",
                "_bs"
            )
        )

        .merge(
            cashflow,
            on=[
                "company_id",
                "year"
            ],
            how="left"
        )

        .merge(
            companies,
            left_on="company_id",
            right_on="id",
            how="left",
            suffixes=(
                "",
                "_company"
            )
        )

        .merge(
            sectors,
            on="company_id",
            how="left"
        )

    )

    print("\nMerged Rows :", len(merged))

    # ------------------------------------------
    # Sort company history
    # ------------------------------------------

    merged = merged.sort_values(
        [
            "company_id",
            "year"
        ]
    )

    results = []

    # ------------------------------------------
    # Create edge case log
    # ------------------------------------------

    os.makedirs("output", exist_ok=True)

    with open(EDGE_CASE_LOG, "w") as log:   
            log.write("Financial Ratio Edge Case Log\n")
            log.write("=" * 60 + "\n\n")

    print("\nComputing Financial Ratios...\n")

    for company_id, company_df in merged.groupby("company_id"):

        company_df = company_df.sort_values("year").reset_index(drop=True)

        for idx, row in company_df.iterrows():

            # -----------------------------
            # Clean Values
            # -----------------------------

            sales = clean(row["sales"])
            net_profit = clean(row["net_profit"])
            operating_profit = clean(row["operating_profit"])
            other_income = clean(row["other_income"])
            interest = clean(row["interest"])

            equity = clean(row["equity_capital"])
            reserves = clean(row["reserves"])
            borrowings = clean(row["borrowings"])
            investments = clean(row["investments"])
            total_assets = clean(row["total_assets"])

            operating_activity = clean(row["operating_activity"])
            investing_activity = clean(row["investing_activity"])

            eps = clean(row["eps"])

            # Replace missing numeric values with 0 where safe
            sales = sales or 0
            net_profit = net_profit or 0
            operating_profit = operating_profit or 0
            other_income = other_income or 0
            interest = interest or 0
            equity = equity or 0
            reserves = reserves or 0
            borrowings = borrowings or 0
            investments = investments or 0
            total_assets = total_assets or 0
            operating_activity = operating_activity or 0
            investing_activity = investing_activity or 0
            eps = eps or 0

            # --------------------------------
            # Day 08
            # --------------------------------

            npm = calculate_net_profit_margin(
                net_profit,
                sales
            )

            opm = calculate_operating_profit_margin(
                operating_profit,
                sales
            )

            roe = calculate_roe(
                net_profit,
                equity,
                reserves
            )
            # ------------------------------------------
            # ROE Validation
            # ------------------------------------------

            source_roe = clean(row.get("roe_percentage"))   

            if (
                    roe is not None
                    and source_roe is not None
                ):
                    difference = abs(roe - source_roe)

                    if difference > 5:

                        with open(EDGE_CASE_LOG, "a") as log:

                            log.write(
                        f"ROE | "
                        f"{row['company_id']} | "
                        f"{row['year']} | "
                        f"Computed={roe:.2f} | "
                        f"Source={source_roe:.2f} | "
                        f"Difference={difference:.2f} | "
                        f"Category=DATA_SOURCE_ISSUE\n"
                )
                            

            roce = calculate_roce(
                operating_profit,
                other_income,
                equity,
                reserves,
                borrowings
            )

            # ------------------------------------------
            # ROCE Validation
            # ------------------------------------------

            source_roce = clean(row.get("roce_percentage"))

            is_financial_company = (
              row["broad_sector"] == "Financials"   
            )


            if (
                    not is_financial_company
                    and roce is not None
                    and source_roce is not None
            ):
                difference = abs(roce - source_roce)

                if difference > 5:

                  with open(EDGE_CASE_LOG, "a") as log:

                     log.write(
                         f"ROCE | "
                         f"{row['company_id']} | "
                        f"{row['year']} | "
                        f"Computed={roce:.2f} | "
                        f"Source={source_roce:.2f} | "
                        f"Difference={difference:.2f} | "
                        f"Category=FORMULA_DISCREPANCY\n"
            )
            

            

            roa = calculate_roa(
                net_profit,
                total_assets
            )

            # --------------------------------
            # Day 09
            # --------------------------------

            debt_to_equity = calculate_debt_to_equity(
                borrowings,
                equity,
                reserves
            )

            high_leverage = calculate_high_leverage_flag(
                debt_to_equity,
                row["broad_sector"]
            )

            interest_coverage = calculate_interest_coverage(
                operating_profit,
                other_income,
                interest
            )

            icr_label = calculate_icr_label(
                interest_coverage
            )

            icr_warning = calculate_icr_warning_flag(
                interest_coverage
            )

            net_debt = calculate_net_debt(
                borrowings,
                investments
            )

            asset_turnover = calculate_asset_turnover(
                sales,
                total_assets
            )

            # --------------------------------
            # Day 11
            # --------------------------------

            free_cash_flow = calculate_free_cash_flow(
                operating_activity,
                investing_activity
            )

            cfo_score, cfo_label = calculate_cfo_quality_score(
                operating_activity,
                net_profit
            )

            capex, capex_label = calculate_capex_intensity(
                investing_activity,
                sales
            )

            fcf_conversion = calculate_fcf_conversion(
                free_cash_flow,
                operating_profit
            )

            # --------------------------------
            # Day 10 CAGR
            # --------------------------------

            revenue_cagr = None
            revenue_flag = "INSUFFICIENT"

            pat_cagr = None
            pat_flag = "INSUFFICIENT"

            eps_cagr = None
            eps_flag = "INSUFFICIENT"

            if idx >= 5:

                revenue_cagr, revenue_flag = calculate_cagr(
                    company_df.iloc[idx-5]["sales"],
                    sales,
                    5
                )

                pat_cagr, pat_flag = calculate_cagr(
                    company_df.iloc[idx-5]["net_profit"],
                    net_profit,
                    5
                )

                eps_cagr, eps_flag = calculate_cagr(
                    company_df.iloc[idx-5]["eps"],
                    eps,
                    5
                )

            # --------------------------------
            # Composite Quality Score
            # --------------------------------

            score = 0

            if roe is not None and roe > 15:
                score += 25

            if debt_to_equity is not None and debt_to_equity < 1:
                score += 25

            if interest_coverage is not None and interest_coverage > 3:
                score += 20

            if cfo_score is not None and cfo_score > 1:
                score += 20

            if revenue_cagr is not None and revenue_cagr > 10:
                score += 10

            results.append({

                "company_id": company_id,
                "year": row["year"],

                "net_profit_margin_pct": npm,
                "operating_profit_margin_pct": opm,

                "return_on_equity_pct": roe,
                "return_on_capital_employed_pct": roce,
                "return_on_assets_pct": roa,

                "debt_to_equity": debt_to_equity,
                "high_leverage_flag": high_leverage,

                "interest_coverage": interest_coverage,
                "icr_label": icr_label,
                "icr_warning_flag": icr_warning,

                "net_debt": net_debt,
                "asset_turnover": asset_turnover,

                "free_cash_flow_cr": free_cash_flow,
                "cfo_quality_score": cfo_score,
                "cfo_quality_label": cfo_label,

                "capex_intensity_pct": capex,
                "capex_label": capex_label,

                "fcf_conversion_pct": fcf_conversion,

                "earnings_per_share": eps,
                "book_value_per_share": row["book_value"],
                "dividend_payout_ratio_pct": row["dividend_payout"],
                "total_debt_cr": borrowings,
                "cash_from_operations_cr": operating_activity,

                "revenue_cagr_5yr": revenue_cagr,
                "revenue_cagr_flag": revenue_flag,

                "pat_cagr_5yr": pat_cagr,
                "pat_cagr_flag": pat_flag,

                "eps_cagr_5yr": eps_cagr,
                "eps_cagr_flag": eps_flag,

                "composite_quality_score": score

            })


                # ==========================================================
    # Create Computed DataFrame
    # ==========================================================

    computed_df = pd.DataFrame(results)

    print("\nFinancial Ratio Engine Completed")
    print("Computed Rows :", len(computed_df))

    # ==========================================================
    # Save to SQLite
    # ==========================================================

    print("\nWriting computed ratios to SQLite...")

    computed_df.to_sql(
         "financial_ratios",
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()

    # ==========================================================
    # Verification
    # ==========================================================

    row_count = conn.execute(
        """
        SELECT COUNT(*)
        FROM computed_financial_ratios
        """
    ).fetchone()[0]

    print("\nVerification")
    print("-" * 40)

    print("Rows written :", row_count)

    if row_count >= 1100:
        print("PASS : Row count requirement satisfied")
    else:
        print("WARNING : Row count below expected")

    print("\nSample Records\n")

    print(

        pd.read_sql(
            """
            SELECT
                company_id,
                year,
                return_on_equity_pct,
                debt_to_equity,
                revenue_cagr_5yr,
                composite_quality_score
            FROM computed_financial_ratios
            LIMIT 10
            """,
            conn
        )

    )

    print("\nRatio Edge Case Log Generated")
    print(f"Location : {EDGE_CASE_LOG}")

    conn.close()

    print("\n" + "=" * 60)
    print("Day 13 Completed Successfully")
    print("=" * 60)

if __name__ == "__main__":
    main()