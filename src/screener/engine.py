from __future__ import annotations

from pathlib import Path
from typing import Any

import sqlite3

import numpy as np
import pandas as pd
import yaml

CONFIG_PATH = Path("config") / "screener_config.yaml"

DEFAULT_DB = Path("data") / "nifty100.db"

class ScreenerEngine:
    """
    Financial Screener Engine

    Loads financial data,
    applies analyst-defined filters,
    returns ranked companies.
    """

    def __init__(
        self,
        config_path: Path = CONFIG_PATH,
    ):

        self.config = self.load_config(config_path)

        db_path = self.config.get(
            "database",
            {},
        ).get(
            "path",
            str(DEFAULT_DB),
        )

        self.conn = sqlite3.connect(db_path)

        self.df = self.load_master_dataframe()

    FILTER_MAP = {
        # Minimum Threshold Filters
        "roe_min": ("return_on_equity_pct", ">="),
        "free_cash_flow_min": ("free_cash_flow_cr", ">="),
        "revenue_cagr_5yr_min": ("revenue_cagr_5yr", ">="),
        "pat_cagr_5yr_min": ("pat_cagr_5yr", ">="),
        "operating_profit_margin_min": (
            "operating_profit_margin_pct",
            ">=",
        ),
        "interest_coverage_min": (
            "interest_coverage",
            ">=",
        ),
        "net_profit_min": ("net_profit", ">="),
        "eps_cagr_5yr_min": ("eps_cagr_5yr", ">="),
        "asset_turnover_min": ("asset_turnover", ">="),
        "sales_min": ("sales", ">="),

        # Maximum Threshold Filters
        "debt_to_equity_max": ("debt_to_equity", "<="),
        "pe_max": ("pe_ratio", "<="),
        "pb_max": ("pb_ratio", "<="),

        # Future Metrics
        "dividend_yield_min": (
            "dividend_yield",
            ">=",
        ),
        "market_cap_min": (
            "market_cap",
            ">=",
        ),
    }

    def _apply_single_filter(
        self,
        df: pd.DataFrame,
        column: str,
        operator: str,
        threshold,
    ) -> pd.DataFrame:
        """
        Apply one threshold filter.
        """

        if threshold is None:
            return df

        if column not in df.columns:
            print(f"[INFO] Skipping filter '{column}' (column not available)")
            return df

        if operator == ">=":
            return df[df[column] >= threshold]

        if operator == "<=":
            return df[df[column] <= threshold]

        raise ValueError(
            f"Unsupported operator: {operator}"
        )
    
    def apply_debt_to_equity_filter(
        self,
        df: pd.DataFrame,
        threshold,
    ) -> pd.DataFrame:
        """
        Financial companies bypass
        Debt-to-Equity screening.
        """

        if threshold is None:
            return df

        financials = df[
            df["broad_sector"] == "Financials"
        ]

        others = df[
            df["broad_sector"] != "Financials"
        ]

        others = others[
            others["debt_to_equity"] <= threshold
        ]

        return pd.concat(
            [financials, others],
            ignore_index=True,
        )
    
    def apply_filters(
        self,
        filters: dict | None = None,
    ) -> pd.DataFrame:
        """
        Apply all configured screener filters.
        """

        df = self.df.copy()

        if filters is None:
            filters = self.config["filters"]

        for filter_name, threshold in filters.items():

            if threshold is None:
                continue

            if filter_name == "debt_to_equity_max":

                df = self.apply_debt_to_equity_filter(
                    df,
                    threshold,
                )

                continue

            if filter_name not in self.FILTER_MAP:
                continue

            column, operator = self.FILTER_MAP[
                filter_name
            ]

            df = self._apply_single_filter(
                df,
                column,
                operator,
                threshold,
            )

        df = df.sort_values(
            by="composite_quality_score",
            ascending=False,
        )

        df.reset_index(
            drop=True,
            inplace=True,
        )

        return df

    def run(self) -> pd.DataFrame:
        """
        Execute screener.
        """

        return self.apply_filters()

    @staticmethod
    def load_config(
        config_path: Path,
    ) -> dict[str, Any]:

        with open(
            config_path,
            "r",
            encoding="utf-8",
        ) as file:

            return yaml.safe_load(file)
        
    def load_master_dataframe(
        self,
    ) -> pd.DataFrame:
        """
        Build one dataframe for
        all screening operations.
        """

        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn,
        )

        companies = pd.read_sql(
            """
            SELECT
                id AS company_id,
                company_name,
                book_value,
                roce_percentage,
                roe_percentage
            FROM companies
            """,
            self.conn,
        )


        sectors = pd.read_sql(
            """
            SELECT
                company_id,
                broad_sector,
                sub_sector,
                market_cap_category
            FROM sectors
            """,
            self.conn,
        )


        pnl = pd.read_sql(
         """
        SELECT
            company_id,
            year,
            sales,
            net_profit,
            dividend_payout
        FROM profitandloss
        """,
        self.conn,
        )

        # Remove duplicate company-year records
        pnl = (
            pnl.sort_values(["company_id", "year"])
            .drop_duplicates(
                subset=["company_id", "year"],
                 keep="first",
                )
        )

        df = ratios.merge(
            companies,
            on="company_id",
            how="left",
        )

        df = df.merge(
            sectors,
            on="company_id",
            how="left",
        )

        df = df.merge(
            pnl,
            on=[
                "company_id",
                "year",
            ],
            how="left",
        )

        df.loc[
            df["icr_label"] == "Debt Free",
            "interest_coverage",
        ] = np.inf


        df.sort_values(
            by="composite_quality_score",
            ascending=False,
            inplace=True,
        )

        df.reset_index(
            drop=True,
            inplace=True,
        )

        return df
    

if __name__ == "__main__":

    engine = ScreenerEngine()

    result = engine.run()

    print()

    print("=" * 70)
    print("FINANCIAL SCREENER")
    print("=" * 70)


    print(f"Rows Selected      : {len(result)}")
    print(f"Unique Companies   : {result['company_id'].nunique()}")

    print()

    print(
        result[
            [
                "company_id",
                "company_name",
                "return_on_equity_pct",
                "debt_to_equity",
                "composite_quality_score",
            ]
        ].head(20)
    )



