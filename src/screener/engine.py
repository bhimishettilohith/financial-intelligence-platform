from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml

from src.analytics.scoring import (
    calculate_composite_score,
    calculate_sector_relative_score,
)
from src.screener.export import export_all_screeners
from src.screener.presets import PRESET_SCREENERS

CONFIG_PATH = Path("config") / "screener_config.yaml"
DEFAULT_DB = Path("data") / "nifty100.db"


class ScreenerEngine:
    """
    Financial Screener Engine

    Loads financial data,
    computes composite quality scores,
    applies preset filters,
    exports ranked companies.
    """

    FILTER_MAP = {
        # ---------------- Minimum Filters ----------------
        "roe_min": (
            "return_on_equity_pct",
            ">=",
        ),
        "free_cash_flow_min": (
            "free_cash_flow_cr",
            ">=",
        ),
        "revenue_cagr_5yr_min": (
            "revenue_cagr_5yr",
            ">=",
        ),
        "pat_cagr_5yr_min": (
            "pat_cagr_5yr",
            ">=",
        ),
        "operating_profit_margin_min": (
            "operating_profit_margin_pct",
            ">=",
        ),
        "interest_coverage_min": (
            "interest_coverage",
            ">=",
        ),
        "net_profit_min": (
            "net_profit",
            ">=",
        ),
        "eps_cagr_5yr_min": (
            "eps_cagr_5yr",
            ">=",
        ),
        "asset_turnover_min": (
            "asset_turnover",
            ">=",
        ),
        "sales_min": (
            "sales",
            ">=",
        ),
        # ---------------- Maximum Filters ----------------
        "debt_to_equity_max": (
            "debt_to_equity",
            "<=",
        ),
        "pe_max": (
            "pe_ratio",
            "<=",
        ),
        "pb_max": (
            "pb_ratio",
            "<=",
        ),
        "dividend_payout_max": (
            "dividend_payout",
            "<=",
        ),
        # ---------------- Future Metrics ----------------
        "dividend_yield_min": (
            "dividend_yield",
            ">=",
        ),
        "market_cap_min": (
            "market_cap",
            ">=",
        ),
    }

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

    def run_preset(
        self,
        preset_name: str,
    ) -> pd.DataFrame:
        """
        Execute one predefined screener.
        """

        if preset_name not in PRESET_SCREENERS:
            raise ValueError(f"Unknown preset: {preset_name}")

        filters = PRESET_SCREENERS[preset_name]

        latest_df = self.get_latest_records(self.df)

        # ---------- Day 17 Composite Score ----------

        latest_df = calculate_composite_score(latest_df)

        latest_df = calculate_sector_relative_score(latest_df)

        old_df = self.df

        self.df = latest_df

        result = self.apply_filters(filters)

        self.df = old_df

        return result

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
            print(f"[INFO] Skipping filter '{column}' " "(column not available)")
            return df

        if operator == ">=":
            return df[df[column] >= threshold]

        if operator == "<=":
            return df[df[column] <= threshold]

        raise ValueError(f"Unsupported operator: {operator}")

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

        financials = df[df["broad_sector"] == "Financials"]

        others = df[df["broad_sector"] != "Financials"]

        others = others[others["debt_to_equity"] <= threshold]

        return pd.concat(
            [financials, others],
            ignore_index=True,
        ).reset_index(drop=True)

    def apply_filters(
        self,
        filters: dict | None = None,
    ) -> pd.DataFrame:
        """
        Apply all screener filters.
        """

        df = self.df.copy()

        if filters is None:
            filters = self.config["filters"]

        unsupported_filters = {
            "revenue_cagr_3yr_min",
            "debt_declining",
        }

        for filter_name, threshold in filters.items():

            if threshold is None:
                continue

            if filter_name == "debt_to_equity_max":

                df = self.apply_debt_to_equity_filter(
                    df,
                    threshold,
                )

                continue

            if filter_name in unsupported_filters:
                print(f"[INFO] '{filter_name}' " "not available yet - skipped")
                continue

            if filter_name not in self.FILTER_MAP:
                continue

            column, operator = self.FILTER_MAP[filter_name]

            # ---------- FIX ----------
            df = self._apply_single_filter(
                df,
                column,
                operator,
                threshold,
            )

        sort_column = (
            "sector_relative_score"
            if "sector_relative_score" in df.columns
            else "composite_quality_score"
        )

        df = df.sort_values(
            by=sort_column,
            ascending=False,
        ).reset_index(drop=True)

        return df

    def run(self) -> pd.DataFrame:
        """
        Execute screener.
        """

        return self.apply_filters()

    def get_latest_records(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Keep only the latest annual
        financial record for each company.
        """

        latest = df.copy()

        latest = latest[latest["year"] != "TTM"]

        latest["year_rank"] = latest["year"].str.extract(r"(\d{4})").astype(float)

        latest = (
            latest.sort_values("year_rank")
            .drop_duplicates(
                subset="company_id",
                keep="last",
            )
            .drop(columns="year_rank")
            .reset_index(drop=True)
        )

        return latest

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
        Build the master dataframe used
        for all screening operations.
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

        pnl = pnl.sort_values(["company_id", "year"]).drop_duplicates(
            subset=["company_id", "year"],
            keep="first",
        )

        df = (
            ratios.merge(
                companies,
                on="company_id",
                how="left",
            )
            .merge(
                sectors,
                on="company_id",
                how="left",
            )
            .merge(
                pnl,
                on=[
                    "company_id",
                    "year",
                ],
                how="left",
            )
        )

        # Debt-free companies should receive
        # maximum interest coverage.

        df.loc[
            df["icr_label"] == "Debt Free",
            "interest_coverage",
        ] = np.inf

        return df.reset_index(drop=True)


if __name__ == "__main__":

    engine = ScreenerEngine()

    print("\n" + "=" * 70)
    print("PRESET SCREENER SUMMARY")
    print("=" * 70)

    results = {}

    for preset in PRESET_SCREENERS:

        result = engine.run_preset(preset)

        results[preset] = result

        print(f"{preset:<25}" f"{result['company_id'].nunique():>5} companies")

        output = export_all_screeners(
            results,
            PRESET_SCREENERS,
        )
    print("\nWorkbook created:")
    print(output)

    engine.conn.close()
