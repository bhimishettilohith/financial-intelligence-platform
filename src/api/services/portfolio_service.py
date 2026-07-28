"""
Portfolio Service

Computes percentile statistics for key financial KPIs.
"""

from __future__ import annotations

import numpy as np


class PortfolioService:

    KPI_COLUMNS = [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "interest_coverage",
        "asset_turnover",
        "net_profit_margin_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
    ]

    def __init__(self, conn):
        self.conn = conn

    def get_percentile_stats(self) -> list[dict]:

        cursor = self.conn.cursor()

        query = """
        WITH latest_ratios AS (

            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY company_id
                       ORDER BY
                           CASE
                               WHEN year='TTM' THEN 9999
                               ELSE CAST(SUBSTR(year,-4) AS INTEGER)
                           END DESC
                   ) rn

            FROM financial_ratios

        )

        SELECT *
        FROM latest_ratios
        WHERE rn = 1
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        results = []

        for metric in self.KPI_COLUMNS:

            values = []

            for row in rows:

                value = row[metric]

                if value is not None:
                    values.append(float(value))

            if not values:
                continue

            results.append(
                {
                    "metric": metric,
                    "P10": round(float(np.percentile(values, 10)), 2),
                    "P20": round(float(np.percentile(values, 20)), 2),
                    "P30": round(float(np.percentile(values, 30)), 2),
                    "P40": round(float(np.percentile(values, 40)), 2),
                    "P50": round(float(np.percentile(values, 50)), 2),
                    "P60": round(float(np.percentile(values, 60)), 2),
                    "P70": round(float(np.percentile(values, 70)), 2),
                    "P80": round(float(np.percentile(values, 80)), 2),
                    "P90": round(float(np.percentile(values, 90)), 2),
                }
            )

        return results
