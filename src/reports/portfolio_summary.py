"""
Portfolio Summary Generator
Sprint 5 – Day 35

Creates

output/portfolio/portfolio_summary.pdf

One page per company.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.reports.tearsheet import DataRepository

# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "output"

PORTFOLIO_DIR = OUTPUT_DIR / "portfolio"

PORTFOLIO_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

PORTFOLIO_FILE = PORTFOLIO_DIR / "portfolio_summary.pdf"


# ---------------------------------------------------------
# Theme
# ---------------------------------------------------------

NAVY = HexColor("#0B3D91")
LIGHT = HexColor("#F5F5F5")
GREEN = HexColor("#2E8B57")
RED = HexColor("#D32F2F")
GREY = HexColor("#757575")

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "Title",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    fontSize=20,
    textColor=NAVY,
    spaceAfter=16,
)

HEADER_STYLE = ParagraphStyle(
    "Header",
    parent=styles["Heading2"],
    textColor=NAVY,
    spaceAfter=8,
)

BODY_STYLE = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontSize=9,
    leading=14,
)

SMALL_STYLE = ParagraphStyle(
    "Small",
    parent=BODY_STYLE,
    fontSize=8,
)


# ---------------------------------------------------------
# Repository
# ---------------------------------------------------------


class PortfolioRepository:

    def __init__(self):

        self.repo = DataRepository()

        self.company = self.repo.companies()

        self.sector = self.repo.sector_mapping()

        self.market = self.repo.latest_market_data()

        self.ratios = self.repo.latest_financial_ratios()

        self.pnl_latest = self.repo.latest_pnl()

        self.pnl_all = self.repo.pl.copy()

    # -----------------------------------------------------

    def merged(self):

        df = self.company.copy()

        sector = self.sector.drop(
            columns=["id"],
            errors="ignore",
        )

        df = df.merge(
            sector,
            left_on="id",
            right_on="company_id",
            how="left",
        ).drop(
            columns=["company_id"],
            errors="ignore",
        )

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
        ).drop(
            columns=["company_id"],
            errors="ignore",
        )

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
        ).drop(
            columns=["company_id"],
            errors="ignore",
        )

        pnl = self.pnl_latest[
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
        ).drop(
            columns=["company_id"],
            errors="ignore",
        )

        return df.sort_values("company_name").reset_index(drop=True)

    # -----------------------------------------------------
    def previous_pnl(self, company_id):

        df = self.pnl_all.copy()

        df = df[df["company_id"] == company_id]

        if len(df) < 2:
            return None

        years = df["year"].astype(str).str.extract(r"(\d{4})")[0]

        df = df.assign(
            year_num=pd.to_numeric(
                years,
                errors="coerce",
            )
        )

        df = (
            df.dropna(subset=["year_num"])
            .sort_values("year_num")
            .drop_duplicates(
                subset="year_num",
                keep="last",
            )
        )

        if len(df) < 2:
            return None

        return df.iloc[-2]


# ---------------------------------------------------------
# Portfolio Summary Generator
# ---------------------------------------------------------


class PortfolioSummaryGenerator:

    def __init__(self):

        self.repo = PortfolioRepository()

    # -----------------------------------------------------

    @staticmethod
    def fmt(value, decimals=2):

        if pd.isna(value):
            return "-"

        if isinstance(value, (int, float)):
            return f"{value:,.{decimals}f}"

        return str(value)

    # -----------------------------------------------------

    @staticmethod
    def trend_arrow(current, previous):

        if previous is None:
            return "→"

        if pd.isna(current) or pd.isna(previous):
            return "→"

        if previous == 0:
            return "→"

        change = ((current - previous) / abs(previous)) * 100

        if change > 2:
            return "↑"

        elif change < -2:
            return "↓"

        return "→"

    # -----------------------------------------------------

    def company_kpis(self, company):

        previous = self.repo.previous_pnl(company["id"])

        revenue_arrow = self.trend_arrow(
            company["sales"],
            None if previous is None else previous["sales"],
        )

        profit_arrow = self.trend_arrow(
            company["net_profit"],
            None if previous is None else previous["net_profit"],
        )

        eps_arrow = self.trend_arrow(
            company["eps"],
            None if previous is None else previous["eps"],
        )

        dividend_arrow = self.trend_arrow(
            company["dividend_payout"],
            None if previous is None else previous["dividend_payout"],
        )

        return [
            ["Revenue", self.fmt(company["sales"]), revenue_arrow],
            ["Net Profit", self.fmt(company["net_profit"]), profit_arrow],
            ["ROE", self.fmt(company["return_on_equity_pct"]), "→"],
            ["ROCE", self.fmt(company["roce_percentage"]), "→"],
            ["P/E Ratio", self.fmt(company["pe_ratio"]), "→"],
            ["Market Cap", self.fmt(company["market_cap_crore"]), "→"],
            ["EPS", self.fmt(company["eps"]), eps_arrow],
            ["Dividend", self.fmt(company["dividend_payout"]), dividend_arrow],
        ]

    # -----------------------------------------------------

    def build_company_page(
        self,
        story,
        company,
    ):

        story.append(
            Paragraph(
                company["company_name"],
                TITLE_STYLE,
            )
        )

        story.append(
            Paragraph(
                f"<b>Sector:</b> {company['broad_sector']}",
                HEADER_STYLE,
            )
        )

        story.append(
            Spacer(
                1,
                0.2 * inch,
            )
        )

        rows = [
            [
                "KPI",
                "Value",
                "Trend",
            ]
        ]

        rows.extend(self.company_kpis(company))

        table = Table(
            rows,
            colWidths=[
                2.5 * inch,
                2.0 * inch,
                1.0 * inch,
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
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
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
                        LIGHT,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, 0),
                        6,
                    ),
                    (
                        "ALIGN",
                        (2, 1),
                        (2, -1),
                        "CENTER",
                    ),
                ]
            )
        )

        story.append(table)

        story.append(PageBreak())

    # -----------------------------------------------------

    def generate_pdf(self):

        logger.info("Generating portfolio summary PDF...")

        companies = self.repo.merged()

        doc = SimpleDocTemplate(str(PORTFOLIO_FILE))

        story = []

        for _, company in companies.iterrows():

            self.build_company_page(
                story,
                company,
            )

        doc.build(story)

        logger.info(
            "Saved -> %s",
            PORTFOLIO_FILE,
        )

        logger.info(
            "Companies : %s",
            len(companies),
        )

    # -----------------------------------------------------

    def sprint_review(self):

        review_dir = OUTPUT_DIR / "reports"

        review_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        review_file = review_dir / "sprint5_review.txt"

        companies = len(self.repo.company)

        sectors = len(self.repo.sector["broad_sector"].dropna().unique())

        with open(
            review_file,
            "w",
            encoding="utf-8",
        ) as f:

            f.write("=" * 60 + "\n")
            f.write("SPRINT 5 RETROSPECTIVE\n")
            f.write("=" * 60 + "\n\n")

            f.write("Completed Modules\n")
            f.write("-----------------\n")
            f.write("✓ Company Tear Sheets\n")
            f.write("✓ Batch Tear Sheets\n")
            f.write("✓ Sector Reports\n")
            f.write("✓ Portfolio Summary PDF\n\n")

            f.write("Generated Outputs\n")
            f.write("-----------------\n")
            f.write(f"Company PDFs : {companies}\n")
            f.write(f"Sector PDFs  : {sectors}\n")
            f.write("Portfolio PDF: 1\n\n")

            f.write("Status\n")
            f.write("------\n")
            f.write("Sprint 5 completed successfully.\n")

        logger.info(
            "Saved -> %s",
            review_file,
        )

    # -----------------------------------------------------

    def generate(self):

        self.generate_pdf()

        self.sprint_review()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------


def main():

    generator = PortfolioSummaryGenerator()

    generator.generate()


if __name__ == "__main__":

    main()
