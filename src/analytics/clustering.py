"""
Sprint 6 - Day 36

KMeans clustering for financial company archetypes.
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import zscore
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from src.reports.tearsheet import DataRepository

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "output"
REPORTS_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

FEATURE_COLUMNS = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct",
]

CLUSTER_NAMES = {
    0: "Cluster 0",
    1: "Cluster 1",
    2: "Cluster 2",
    3: "Cluster 3",
    4: "Cluster 4",
}


# -----------------------------------------------------------------------------
# Repository
# -----------------------------------------------------------------------------


class ClusteringRepository:

    def __init__(self):

        logger.info("Loading repository...")

        repo = DataRepository()

        self.feature_table = repo.latest_financial_ratios()
        self.sectors = repo.sector_mapping()
        self.pl = repo.pl.copy()
        self.ratios = repo.financial_ratios.copy()


class KMeansClustering:
    """Financial company clustering using KMeans."""

    def __init__(self):

        self.repo = ClusteringRepository()

        self.feature_table = None
        self.scaled_features = None
        self.scaler = StandardScaler()
        self.model = None

    def profile_clusters(self):
        """
        Generate cluster profile statistics.
        """

        logger.info("Profiling clusters...")

        profile = self.feature_table.groupby("cluster_id").agg(
            {
                "return_on_equity_pct": ["mean", "median"],
                "debt_to_equity": ["mean", "median"],
                "operating_profit_margin_pct": ["mean", "median"],
                "revenue_cagr_5yr": ["mean", "median"],
                "fcf_cagr_5yr": ["mean", "median"],
                "company_id": "count",
            }
        )

        profile.columns = ["_".join(col).strip("_") for col in profile.columns]

        profile = profile.rename(columns={"company_id_count": "company_count"})

        profile.to_csv("reports/cluster_profile.csv")

        self.cluster_profile = profile

        logger.info("Saved reports/cluster_profile.csv")

    def assign_cluster_names(self):
        """
        Assign descriptive names to clusters.
        """

        logger.info("Assigning cluster names...")

        profile = self.cluster_profile.copy()

        names = {}

        for cluster_id, row in profile.iterrows():

            roe = row["return_on_equity_pct_mean"]
            growth = row["revenue_cagr_5yr_mean"]
            debt = row["debt_to_equity_mean"]

            if roe > 20 and growth > 12:
                name = "High-Quality Compounders"

            elif debt < 0.5 and roe > 10:
                name = "Defensive Dividend Payers"

            elif growth > 10:
                name = "Emerging Growth"

            elif roe < 8:
                name = "Distressed / Turnaround"

            else:
                name = "Value Cyclicals"

            names[cluster_id] = name

        self.feature_table["cluster_name"] = self.feature_table["cluster_id"].map(names)

        self.feature_table[
            [
                "company_id",
                "cluster_id",
                "cluster_name",
                "distance_from_centroid",
            ]
        ].to_csv(
            "output/cluster_labels.csv",
            index=False,
        )

        logger.info("Updated cluster_labels.csv")

    # -----------------------------------------------------------------

    @staticmethod
    def _latest_rows(df: pd.DataFrame) -> pd.DataFrame:
        """
        Keep the latest record per company.
        """

        temp = df.copy()

        temp["parsed_year"] = pd.to_datetime(temp["year"], errors="coerce")

        temp = temp.sort_values("parsed_year").drop_duplicates(
            "company_id", keep="last"
        )

        return temp.drop(columns="parsed_year")

    # -----------------------------------------------------------------

    # -----------------------------------------------------------------

    @staticmethod
    def _calculate_cagr(series: pd.Series) -> float:
        """
        Calculate 5-year CAGR from a chronological series.
        Returns NaN if CAGR cannot be computed.
        """

        values = series.dropna().astype(float)

        if len(values) < 6:
            return np.nan

        start = values.iloc[-6]
        end = values.iloc[-1]

        if start <= 0 or end <= 0:
            return np.nan

        return ((end / start) ** (1 / 5) - 1) * 100

    # -----------------------------------------------------------------

    def revenue_cagr(self) -> pd.DataFrame:
        """
        Compute 5-year Revenue CAGR using Profit & Loss data.
        """

        df = self.repo.pl.copy()

        # Extract numeric year (e.g. "Mar 2024" -> 2024)
        df["year_num"] = pd.to_numeric(
            df["year"].astype(str).str.extract(r"(\d{4})", expand=False),
            errors="coerce",
        )

        # Drop rows where no valid year could be extracted
        df = df.dropna(subset=["year_num"])

        df["year_num"] = df["year_num"].astype(int)

        # Keep one record per company per year
        df = df.sort_values(["company_id", "year_num"]).drop_duplicates(
            subset=["company_id", "year_num"], keep="last"
        )

        records = []

        for company_id, group in df.groupby("company_id"):

            group = group.sort_values("year_num")

            records.append(
                {
                    "company_id": company_id,
                    "revenue_cagr_5yr": self._calculate_cagr(group["sales"]),
                }
            )

        return pd.DataFrame(records)

    # -----------------------------------------------------------------

    def fcf_cagr(self) -> pd.DataFrame:
        """
        Compute 5-year Free Cash Flow CAGR using historical ratios.
        """

        df = self.repo.ratios.copy()

        # year_num already exists in latest ratios, but create it if missing
        if "year_num" not in df.columns:

            df["year_num"] = (
                df["year"].astype(str).str.extract(r"(\d{4})", expand=False).astype(int)
            )

        df = df.sort_values(["company_id", "year_num"]).drop_duplicates(
            subset=["company_id", "year_num"], keep="last"
        )

        records = []

        for company_id, group in df.groupby("company_id"):

            group = group.sort_values("year_num")

            records.append(
                {
                    "company_id": company_id,
                    "fcf_cagr_5yr": self._calculate_cagr(group["free_cash_flow_cr"]),
                }
            )

        return pd.DataFrame(records)

    # -----------------------------------------------------------------

    def build_feature_table(self):
        """
        Build feature matrix for clustering.
        """

        logger.info("Building feature table...")

        latest = self.repo.ratios.copy()

        latest["year_num"] = (
            latest["year"].astype(str).str.extract(r"(\d{4})", expand=False)
        )

        latest["year_num"] = pd.to_numeric(latest["year_num"], errors="coerce")

        latest = latest.dropna(subset=["year_num"])

        latest["year_num"] = latest["year_num"].astype(int)

        latest = (
            latest.sort_values(["company_id", "year_num"])
            .groupby("company_id", as_index=False)
            .tail(1)
        )

        sectors = self.repo.sectors[
            [
                "company_id",
                "broad_sector",
                "sub_sector",
                "market_cap_category",
            ]
        ]

        revenue = self.revenue_cagr()

        fcf = self.fcf_cagr()

        df = (
            latest.merge(sectors, on="company_id", how="left")
            .merge(revenue, on="company_id", how="left")
            .merge(fcf, on="company_id", how="left")
        )

        self.feature_table = df

        logger.info("Companies : %d", len(df))

    # -----------------------------------------------------------------

    def impute_missing_values(self):
        """
        Impute missing feature values using sector median.
        """

        logger.info("Imputing missing values using sector medians...")

        df = self.feature_table.copy()

        for feature in FEATURE_COLUMNS:

            df[feature] = df.groupby("broad_sector")[feature].transform(
                lambda x: x.fillna(x.median())
            )

            overall = df[feature].median()

            df[feature] = df[feature].fillna(overall)

        self.feature_table = df

    # -----------------------------------------------------------------

    def scale_features(self):
        """
        Standardise clustering features.
        """

        logger.info("Scaling features...")

        self.scaled_features = self.scaler.fit_transform(
            self.feature_table[FEATURE_COLUMNS]
        )

    # -----------------------------------------------------------------

    def generate_elbow_plot(self):
        """
        Generate inertia vs K plot.
        """

        logger.info("Generating elbow plot...")

        inertia = []

        ks = range(2, 11)

        for k in ks:

            model = KMeans(n_clusters=k, random_state=42, n_init=10)

            model.fit(self.scaled_features)

            inertia.append(model.inertia_)

        plt.figure(figsize=(7, 5))

        plt.plot(ks, inertia, marker="o")

        plt.xlabel("Number of Clusters (k)")
        plt.ylabel("Inertia")
        plt.title("KMeans Elbow Curve")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(REPORTS_DIR / "elbow_plot.png", dpi=300)

        plt.close()

    # -----------------------------------------------------------------

    def fit_clusters(self):
        """
        Fit KMeans clustering model.
        """

        logger.info("Running KMeans...")

        self.model = KMeans(n_clusters=5, random_state=42, n_init=10)

        labels = self.model.fit_predict(self.scaled_features)

        self.feature_table["cluster_id"] = labels

        distances = self.model.transform(self.scaled_features)

        self.feature_table["distance_from_centroid"] = distances.min(axis=1)

        self.feature_table["cluster_name"] = self.feature_table["cluster_id"].map(
            CLUSTER_NAMES
        )

    def generate_correlation_heatmap(self):
        """
        Generate Pearson correlation heatmap
        for the latest financial KPIs.
        """

        logger.info("Generating correlation heatmap...")

        kpis = [
            "return_on_equity_pct",
            "debt_to_equity",
            "operating_profit_margin_pct",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow_cr",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr",
            "composite_quality_score",
        ]

        available = [col for col in kpis if col in self.feature_table.columns]

        corr = self.feature_table[available].corr(method="pearson")

        plt.figure(figsize=(10, 8))

        sns.heatmap(
            corr,
            annot=True,
            cmap="RdYlGn",
            fmt=".2f",
            square=True,
        )

        plt.title("Financial KPI Correlation")

        plt.tight_layout()

        plt.savefig(
            "reports/correlation_heatmap.png",
            dpi=300,
        )

        plt.close()

        logger.info("Saved reports/correlation_heatmap.png")

    def detect_outliers(self):
        """
        Detect sector-wise outliers
        using Z-score.
        """

        logger.info("Detecting outliers...")

        kpis = [
            "return_on_equity_pct",
            "debt_to_equity",
            "operating_profit_margin_pct",
            "revenue_cagr_5yr",
            "fcf_cagr_5yr",
        ]

        df = self.feature_table.copy()

        outliers = []

        for sector, group in df.groupby("broad_sector"):

            temp = group.copy()

            for metric in kpis:

                if metric not in temp.columns:
                    continue

                if temp[metric].nunique(dropna=True) <= 1:
                    temp["z"] = np.nan
                else:
                    temp["z"] = pd.Series(
                        zscore(temp[metric], nan_policy="omit"),
                        index=temp.index,
                    )

                flagged = temp[temp["z"].abs() > 3]

                for _, row in flagged.iterrows():

                    outliers.append(
                        {
                            "company_id": row["company_id"],
                            "broad_sector": sector,
                            "metric": metric,
                            "value": row[metric],
                            "z_score": row["z"],
                        }
                    )

        pd.DataFrame(outliers).to_csv(
            "output/outlier_report.csv",
            index=False,
        )

        logger.info("Saved output/outlier_report.csv")

    def generate_portfolio_statistics(self):
        """
        Generate descriptive statistics
        across all companies.
        """

        logger.info("Generating portfolio statistics...")

        kpis = [
            "return_on_equity_pct",
            "debt_to_equity",
            "operating_profit_margin_pct",
            "revenue_cagr_5yr",
            "fcf_cagr_5yr",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow_cr",
            "pat_cagr_5yr",
            "eps_cagr_5yr",
        ]

        rows = []

        for metric in kpis:

            if metric not in self.feature_table.columns:
                continue

            s = self.feature_table[metric].dropna()

            rows.append(
                {
                    "KPI": metric,
                    "P10": s.quantile(0.10),
                    "P25": s.quantile(0.25),
                    "P50": s.quantile(0.50),
                    "P75": s.quantile(0.75),
                    "P90": s.quantile(0.90),
                    "Mean": s.mean(),
                    "Std": s.std(),
                }
            )

        pd.DataFrame(rows).to_csv(
            "output/portfolio_stats.csv",
            index=False,
        )

        logger.info("Saved output/portfolio_stats.csv")

    # -----------------------------------------------------------------

    def export_cluster_labels(self):
        """
        Export cluster assignments.
        """

        output = self.feature_table[
            ["company_id", "cluster_id", "cluster_name", "distance_from_centroid"]
        ]

        output.to_csv(OUTPUT_DIR / "cluster_labels.csv", index=False)

        logger.info("Saved %s", OUTPUT_DIR / "cluster_labels.csv")


def main():

    clustering = KMeansClustering()

    clustering.build_feature_table()

    clustering.impute_missing_values()

    clustering.scale_features()

    clustering.generate_elbow_plot()

    clustering.fit_clusters()

    # -------- Day 37 --------

    clustering.profile_clusters()

    clustering.assign_cluster_names()

    clustering.export_cluster_labels()

    clustering.generate_correlation_heatmap()

    clustering.detect_outliers()

    clustering.generate_portfolio_statistics()

    logger.info("Day 37 completed successfully.")


if __name__ == "__main__":
    main()
