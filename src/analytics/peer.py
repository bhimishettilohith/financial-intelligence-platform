from __future__ import annotations

import sqlite3

import pandas as pd

DB_PATH = "data/nifty100.db"

METRICS = {
    "return_on_equity_pct": True,
    "return_on_capital_employed_pct": True,
    "net_profit_margin_pct": True,
    "debt_to_equity": False,  # Lower is better
    "free_cash_flow_cr": True,
    "pat_cagr_5yr": True,
    "revenue_cagr_5yr": True,
    "eps_cagr_5yr": True,
    "interest_coverage": True,
    "asset_turnover": True,
}


class PeerPercentileEngine:
    """
    Computes peer-group percentile rankings
    for financial metrics.
    """

    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH)

        self.peer_groups = pd.read_sql(
            """
            SELECT
                company_id,
                peer_group_name
            FROM peer_groups
            """,
            self.conn,
        )

        self.ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn,
        )

    @staticmethod
    def percentile_rank(
        series: pd.Series,
        higher_is_better: bool = True,
    ) -> pd.Series:
        """
        Calculate percentile ranks (0–1).

        For metrics where higher values are better,
        higher values receive higher percentiles.

        For Debt-to-Equity, lower values receive
        higher percentiles.
        """

        if higher_is_better:
            return series.rank(
                pct=True,
                method="average",
                ascending=True,
            )

        return series.rank(
            pct=True,
            method="average",
            ascending=False,
        )

    def prepare_dataframe(self) -> pd.DataFrame:
        """
        Merge peer groups with
        financial ratios.
        """

        df = self.ratios.merge(
            self.peer_groups,
            on="company_id",
            how="left",
        )

        return df

    def compute_peer_percentiles(
        self,
    ) -> pd.DataFrame:

        df = self.prepare_dataframe()

        missing = df[df["peer_group_name"].isna()]["company_id"].unique()

        if len(missing):

            print("\nCompanies without peer group:")

            for company in sorted(missing):
                print(f"{company} -> " "No peer group assigned")

        results = []

        grouped = df.groupby(
            [
                "peer_group_name",
                "year",
            ],
            dropna=False,
        )

        for (
            peer_group,
            year,
        ), group in grouped:

            if pd.isna(peer_group):
                continue

            group = group.copy()

            for (
                metric,
                higher_is_better,
            ) in METRICS.items():

                if metric not in group.columns:
                    continue

                values = group[metric]

                percentiles = self.percentile_rank(
                    values,
                    higher_is_better,
                )

                for idx, row in group.iterrows():

                    value = row[metric]

                    if pd.isna(value):
                        continue

                    results.append(
                        {
                            "company_id": row["company_id"],
                            "peer_group_name": peer_group,
                            "metric": metric,
                            "value": float(value),
                            "percentile_rank": round(
                                float(percentiles.loc[idx]),
                                4,
                            ),
                            "year": row["year"],
                        }
                    )

        return pd.DataFrame(results)

    def save_to_database(
        self,
        percentile_df: pd.DataFrame,
    ) -> None:
        """
        Replace the peer_percentiles table
        with freshly computed rankings.
        """

        cursor = self.conn.cursor()

        cursor.execute("""
            DELETE FROM peer_percentiles
            """)

        self.conn.commit()

        percentile_df.to_sql(
            "peer_percentiles",
            self.conn,
            if_exists="append",
            index=False,
        )

        self.conn.commit()

        print(f"\nInserted " f"{len(percentile_df)} rows " f"into peer_percentiles.")

    def run(self) -> None:

        print("=" * 70)
        print("PEER PERCENTILE RANKING")
        print("=" * 70)

        percentile_df = self.compute_peer_percentiles()

        if percentile_df.empty:

            print("\nNo percentile rankings generated.")

            return

        self.save_to_database(percentile_df)

        print("\nCompleted successfully.")

    def close(self):

        self.conn.close()


def main():

    engine = PeerPercentileEngine()

    try:

        engine.run()

    finally:

        engine.close()


if __name__ == "__main__":
    main()
