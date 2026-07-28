from __future__ import annotations

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DB_PATH = "data/nifty100.db"

OUTPUT_DIR = Path("reports/radar_charts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

METRICS = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score",
]

LABELS = [
    "ROE",
    "ROCE",
    "NPM",
    "D/E",
    "FCF",
    "PAT CAGR",
    "Revenue CAGR",
    "Composite",
]


class RadarChartGenerator:

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

        self.df = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn,
        )

        self.df = self.df.merge(
            self.peer_groups,
            on="company_id",
            how="left",
        )

        self.df = self.get_latest_records(self.df)

        self.normalize_metrics()

    @staticmethod
    def get_latest_records(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        latest = df.copy()

        latest = latest[latest["year"] != "TTM"]

        latest["year_num"] = latest["year"].str.extract(r"(\d{4})").astype(float)

        latest = (
            latest.sort_values("year_num")
            .drop_duplicates(
                subset="company_id",
                keep="last",
            )
            .drop(columns="year_num")
            .reset_index(drop=True)
        )

        return latest

    def normalize_metrics(self):

        for metric in METRICS:

            if metric not in self.df.columns:
                continue

            minimum = self.df[metric].min()
            maximum = self.df[metric].max()

            if pd.isna(minimum) or pd.isna(maximum):
                continue

            if maximum == minimum:
                self.df[metric] = 50
                continue

            self.df[metric] = ((self.df[metric] - minimum) / (maximum - minimum)) * 100

        # Lower Debt/Equity is better

        if "debt_to_equity" in self.df.columns:

            self.df["debt_to_equity"] = 100 - self.df["debt_to_equity"]

    def get_peer_average(
        self,
        peer_group: str | None,
    ) -> pd.Series:
        """
        Return the average normalized metrics for a peer group.

        If the company has no peer group,
        return the Nifty 100 average.
        """

        if pd.isna(peer_group):

            return self.df[METRICS].mean()

        peers = self.df[self.df["peer_group_name"] == peer_group]

        if peers.empty:

            return self.df[METRICS].mean()

        return peers[METRICS].mean()

    @staticmethod
    def radar_angles():

        angles = np.linspace(
            0,
            2 * np.pi,
            len(METRICS),
            endpoint=False,
        ).tolist()

        angles += angles[:1]

        return angles

    def plot_company(
        self,
        company_row: pd.Series,
    ):

        company = company_row["company_id"]

        peer_group = company_row["peer_group_name"]

        company_values = company_row[METRICS].fillna(0).tolist()

        company_values += company_values[:1]

        peer_values = self.get_peer_average(peer_group).fillna(0).tolist()

        peer_values += peer_values[:1]

        angles = self.radar_angles()

        fig = plt.figure(figsize=(8, 8))

        ax = plt.subplot(
            111,
            polar=True,
        )

        ax.set_theta_offset(np.pi / 2)

        ax.set_theta_direction(-1)

        ax.set_xticks(angles[:-1])

        ax.set_xticklabels(
            LABELS,
            fontsize=10,
        )

        ax.set_ylim(
            0,
            100,
        )

        ax.plot(
            angles,
            company_values,
            linewidth=2,
            label=company,
        )

        ax.fill(
            angles,
            company_values,
            alpha=0.25,
        )

        label = peer_group if pd.notna(peer_group) else "Nifty 100 Avg"

        ax.plot(
            angles,
            peer_values,
            linestyle="--",
            linewidth=2,
            label=label,
        )

        ax.legend(
            loc="upper right",
            bbox_to_anchor=(1.25, 1.1),
        )

        plt.title(
            f"{company} Radar Chart",
            fontsize=14,
            pad=20,
        )

    def save_chart(
        self,
        company_row: pd.Series,
    ) -> None:
        """
        Generate and save a radar chart for one company.
        """

        self.plot_company(company_row)

        company = company_row["company_id"]

        output_file = OUTPUT_DIR / f"{company}_radar.png"

        plt.savefig(
            output_file,
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

    def run(self):

        print("=" * 70)
        print("RADAR CHART GENERATION")
        print("=" * 70)

        generated = 0

        for _, row in self.df.iterrows():

            try:

                self.save_chart(row)

                generated += 1

            except Exception as e:

                print(f"Failed for " f"{row['company_id']}: {e}")

        print(f"\nGenerated " f"{generated} radar charts.")

        print(f"Saved to: {OUTPUT_DIR}")

    def close(self):

        self.conn.close()


def main():

    generator = RadarChartGenerator()

    try:

        generator.run()

    finally:

        generator.close()


if __name__ == "__main__":
    main()
