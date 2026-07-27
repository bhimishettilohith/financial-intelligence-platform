"""
Sector Report Generator
Sprint 5 – Day 34

Generates one PDF per sector.

Each report contains

Page 1
-------
Sector Summary

Page 2+
-------
Company comparison table.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from src.reports.tearsheet import (
    DataRepository,
)

# ----------------------------------------------------------
# Logging
# ----------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ----------------------------------------------------------
# Paths
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "output"

SECTOR_REPORT_DIR = OUTPUT_DIR / "sector"

SECTOR_REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ----------------------------------------------------------
# Theme
# ----------------------------------------------------------

NAVY = HexColor("#0B3D91")
LIGHT_BLUE = HexColor("#EAF2FF")
LIGHT_GREY = HexColor("#F5F5F5")
GREEN = HexColor("#2E8B57")

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "Title",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=20,
    alignment=TA_CENTER,
    textColor=NAVY,
    spaceAfter=16,
)

SECTION_STYLE = ParagraphStyle(
    "Section",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=12,
    textColor=NAVY,
    spaceAfter=8,
)

BODY_STYLE = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9,
    leading=14,
)

SMALL_STYLE = ParagraphStyle(
    "Small",
    parent=BODY_STYLE,
    fontSize=8,
)

# ----------------------------------------------------------
# Repository
# ----------------------------------------------------------


class SectorRepository:

    def __init__(self):

        self.repo = DataRepository()

        self.company = self.repo.companies()

        self.sectors = self.repo.sector_mapping()

        self.market = self.repo.latest_market_data()

        self.ratios = self.repo.latest_financial_ratios()

        self.pnl = self.repo.latest_pnl()

    # ------------------------------------------------------

    def merged_dataset(self):

        df = self.company.copy()

        # ---------------- Sector ----------------
        sector = self.sectors.drop(columns=["id"], errors="ignore")

        df = df.merge(
            sector,
            left_on="id",
            right_on="company_id",
            how="left",
        )

        df = df.drop(columns=["company_id"], errors="ignore")

        # ---------------- P&L ----------------
        pnl = self.pnl[
            [
                "company_id",
                "sales",
                "net_profit",
                "eps",
                "dividend_payout",
            ]
        ]

        df = df.merge(
            pnl,
            left_on="id",
            right_on="company_id",
            how="left",
        )

        df = df.drop(columns=["company_id"], errors="ignore")

        # ---------------- Market ----------------
        market = self.market[
            [
                "company_id",
                "market_cap_crore",
                "pe_ratio",
            ]
        ]

        df = df.merge(
            market,
            left_on="id",
            right_on="company_id",
            how="left",
        )

        df = df.drop(columns=["company_id"], errors="ignore")

        # ---------------- Ratios ----------------
        ratios = self.ratios[
            [
                "company_id",
                "return_on_equity_pct",
            ]
        ]

        df = df.merge(
            ratios,
            left_on="id",
            right_on="company_id",
            how="left",
        )

        df = df.drop(columns=["company_id"], errors="ignore")

        return df

    # ------------------------------------------------------

    def companies_in_sector(
        self,
        sector_name,
    ):

        df = self.merged_dataset()

        return (

            df[
                df["broad_sector"] == sector_name
            ]

            .sort_values(
                "company_name"
            )

            .reset_index(drop=True)

        )

    def sectors_list(self):
        """
        Return all unique broad sectors sorted alphabetically.
        """
        return sorted(
            self.sectors["broad_sector"]
            .dropna()
            .unique()
            .tolist()
        )
# ----------------------------------------------------------
# Sector Report Generator
# ----------------------------------------------------------


class SectorReportGenerator:

    def __init__(self):

        self.repo = SectorRepository()

    # ------------------------------------------------------

    @staticmethod
    def _median(series):

        series = pd.to_numeric(
            series,
            errors="coerce",
        )

        if series.dropna().empty:
            return 0

        return series.median()

    # ------------------------------------------------------

    @staticmethod
    def _fmt(value, decimals=0):

        if pd.isna(value):
            return "-"

        if decimals == 0:
            return f"{value:,.0f}"

        return f"{value:,.{decimals}f}"

    # ------------------------------------------------------

    def sector_summary(self, df):

        return {

            "Companies":
                len(df),

            "Median Revenue":
                self._median(df["sales"]),

            "Median Net Profit":
                self._median(df["net_profit"]),

            "Median ROE":
                self._median(
                    df["return_on_equity_pct"]
                ),

            "Median ROCE":
                self._median(
                    df["roce_percentage"]
                ),

            "Median PE":
                self._median(
                    df["pe_ratio"]
                ),

            "Median Market Cap":
                self._median(
                    df["market_cap_crore"]
                ),

            "Median Dividend":
                self._median(
                    df["dividend_payout"]
                ),

            "Median EPS":
                self._median(
                    df["eps"]
                ),
        }

    # ------------------------------------------------------

    def build_summary_page(
        self,
        story,
        sector_name,
        df,
    ):

        story.append(

            Paragraph(

                sector_name,

                TITLE_STYLE,

            )

        )

        story.append(
            Spacer(
                1,
                0.25 * inch,
            )
        )

        summary = self.sector_summary(
            df
        )

        rows = [

            [

                Paragraph(
                    "<b>Metric</b>",
                    BODY_STYLE,
                ),

                Paragraph(
                    "<b>Value</b>",
                    BODY_STYLE,
                ),

            ]

        ]

        for metric, value in summary.items():

            if isinstance(
                value,
                (int, float),
            ):

                value = self._fmt(
                    value,
                    2,
                )

            rows.append(

                [

                    Paragraph(
                        str(metric),
                        BODY_STYLE,
                    ),

                    Paragraph(
                        str(value),
                        BODY_STYLE,
                    ),

                ]

            )

        table = Table(

            rows,

            colWidths=[
                3.5 * inch,
                2.0 * inch,
            ],

        )

        table.setStyle(

            TableStyle(

                [

                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        NAVY,
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),

                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        LIGHT_GREY,
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, 0),
                        8,
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),

                    (
                        "FONTNAME",
                        (0, 1),
                        (-1, -1),
                        "Helvetica",
                    ),

                ]

            )

        )

        story.append(
            table
        )

        story.append(
            PageBreak()
        )
    # ------------------------------------------------------

    def build_company_table(
        self,
        story,
        df,
    ):

        story.append(
            Paragraph(
                "Companies",
                SECTION_STYLE,
            )
        )

        rows = [[
            "Company",
            "Revenue",
            "Profit",
            "ROE",
            "ROCE",
            "PE",
            "Market Cap",
            "Dividend",
            "EPS",
        ]]

        for _, row in df.iterrows():

            rows.append([

                row["company_name"],

                self._fmt(
                    row["sales"]
                ),

                self._fmt(
                    row["net_profit"]
                ),

                self._fmt(
                    row["return_on_equity_pct"],
                    2,
                ),

                self._fmt(
                    row["roce_percentage"],
                    2,
                ),

                self._fmt(
                    row["pe_ratio"],
                    2,
                ),

                self._fmt(
                    row["market_cap_crore"],
                ),

                self._fmt(
                    row["dividend_payout"],
                    2,
                ),

                self._fmt(
                    row["eps"],
                    2,
                ),

            ])

        table = Table(
            rows,
            repeatRows=1,
        )

        table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    NAVY,
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.25,
                    colors.grey,
                ),

                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    LIGHT_GREY,
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    6,
                ),

            ])

        )

        story.append(table)

    # ------------------------------------------------------

    def generate_sector_report(
        self,
        sector_name,
    ):

        logger.info(
            "Generating %s",
            sector_name,
        )

        df = self.repo.companies_in_sector(
            sector_name
        )

        if df.empty:

            logger.warning(
                "No companies found for %s",
                sector_name,
            )

            return

        filename = (
            sector_name.replace(
                " ",
                "_",
            )
            + "_report.pdf"
        )

        pdf = (
            SECTOR_REPORT_DIR
            / filename
        )

        doc = SimpleDocTemplate(
            str(pdf),
        )

        story = []

        self.build_summary_page(
            story,
            sector_name,
            df,
        )

        self.build_company_table(
            story,
            df,
        )

        doc.build(
            story
        )

        logger.info(
            "Saved -> %s",
            pdf,
        )

    # ------------------------------------------------------

    def generate_all(self):

        sectors = self.repo.sectors_list()

        logger.info(
            "Generating %s sector reports",
            len(sectors),
        )

        for sector in sectors:

            self.generate_sector_report(
                sector
            )

        logger.info(
            "-" * 60
        )

        logger.info(
            "Completed"
        )

        logger.info(
            "Reports : %s",
            len(sectors),
        )


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------


def main():

    generator = SectorReportGenerator()

    generator.generate_all()


if __name__ == "__main__":

    main()