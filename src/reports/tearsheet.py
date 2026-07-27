"""
Company Tearsheet Generator
Sprint 5 – Day 33

Generates a professional two-page PDF report for every company
using the Financial Intelligence Platform datasets.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
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

RAW_DIR = PROJECT_ROOT / "data" / "raw"

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

CHART_DIR = OUTPUT_DIR / "_charts"
CHART_DIR.mkdir(exist_ok=True)

TEARSHEET_DIR = OUTPUT_DIR / "tearsheets"
TEARSHEET_DIR.mkdir(exist_ok=True)
DEBUG_MODE = True
# ----------------------------------------------------------
# Files
# ----------------------------------------------------------

# ----------------------------------------------------------
# Core Datasets
# ----------------------------------------------------------

COMPANY_FILE = RAW_DIR / "companies.xlsx"
PL_FILE = RAW_DIR / "profitandloss.xlsx"
BS_FILE = RAW_DIR / "balancesheet.xlsx"
CF_FILE = RAW_DIR / "cashflow.xlsx"
ANALYSIS_FILE = RAW_DIR / "analysis.xlsx"
PROS_FILE = RAW_DIR / "prosandcons.xlsx"

# ----------------------------------------------------------
# Supporting Datasets
# ----------------------------------------------------------

SUPPORTING_DIR = PROJECT_ROOT / "data" / "supporting"

SECTORS_FILE = SUPPORTING_DIR / "sectors.xlsx"

FINANCIAL_RATIOS_FILE = (
    SUPPORTING_DIR / "financial_ratios.xlsx"
)

MARKET_CAP_FILE = (
    SUPPORTING_DIR / "market_cap.xlsx"
)

# ----------------------------------------------------------
# Generated Analytics
# ----------------------------------------------------------

CASHFLOW_INTELLIGENCE = (
    OUTPUT_DIR / "cashflow_intelligence.xlsx"
)

# ----------------------------------------------------------
# Theme
# ----------------------------------------------------------

NAVY = HexColor("#0B3D91")
LIGHT_BLUE = HexColor("#EAF2FF")
LIGHT_GREY = HexColor("#F5F5F5")
GREEN = HexColor("#2E8B57")
RED = HexColor("#C62828")

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "Title",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=20,
    textColor=NAVY,
    alignment=TA_CENTER,
    spaceAfter=12,
)

SECTION_STYLE = ParagraphStyle(
    "Section",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=12,
    textColor=NAVY,
    spaceAfter=6,
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

class DataRepository:
    """
    Centralised data repository.

    All raw datasets use header=1.
    Supporting datasets use the default header.
    """

    def __init__(self):

        logger.info("Loading datasets...")

        # --------------------------------------------------
        # Core datasets
        # --------------------------------------------------

        self.company = pd.read_excel(
            COMPANY_FILE,
            header=1,
        )

        self.pl = pd.read_excel(
            PL_FILE,
            header=1,
        )

        self.bs = pd.read_excel(
            BS_FILE,
            header=1,
        )

        self.cf = pd.read_excel(
            CF_FILE,
            header=1,
        )

        self.analysis = pd.read_excel(
            ANALYSIS_FILE,
            header=1,
        )

        self.pros = pd.read_excel(
            PROS_FILE,
            header=1,
        )

        # --------------------------------------------------
        # Supporting datasets
        # --------------------------------------------------

        self.sectors = pd.read_excel(
            SECTORS_FILE
        )

        self.financial_ratios = pd.read_excel(
            FINANCIAL_RATIOS_FILE
        )

        self.market_cap = pd.read_excel(
            MARKET_CAP_FILE
        )

        # --------------------------------------------------
        # Generated analytics
        # --------------------------------------------------

        if CASHFLOW_INTELLIGENCE.exists():

            self.cashflow_intelligence = pd.read_excel(
                CASHFLOW_INTELLIGENCE
            )

        else:

            self.cashflow_intelligence = pd.DataFrame()

    # --------------------------------------------------

    def company_profile(self, company_id):

        df = self.company[
            self.company["id"] == company_id
        ]

        if df.empty:

            raise ValueError(
                f"Company not found: {company_id}"
            )

        return df.iloc[0]

    # --------------------------------------------------

    @staticmethod
    def _prepare_year(df):

        df = df.copy()

        df["year_num"] = (
            df["year"]
            .astype(str)
            .str.extract(r"(\d{4})")[0]
        )

        df = df[
            df["year_num"].notna()
        ].copy()

        df["year_num"] = (
            df["year_num"]
            .astype(int)
        )

        return df

    # --------------------------------------------------

    def pnl(self, company_id):

        df = self.pl[
            self.pl.company_id == company_id
        ]

        df = self._prepare_year(df)

        return df.sort_values("year_num")

    # --------------------------------------------------

    def balance_sheet(self, company_id):

        df = self.bs[
            self.bs.company_id == company_id
        ]

        df = self._prepare_year(df)

        return df.sort_values("year_num")

    # --------------------------------------------------

    def cashflow(self, company_id):

        df = self.cf[
            self.cf.company_id == company_id
        ]

        df = self._prepare_year(df)

        return df.sort_values("year_num")

    # --------------------------------------------------

    def analysis_data(self, company_id):

        return self.analysis[
            self.analysis.company_id == company_id
        ]

    # --------------------------------------------------

    def pros_cons(self, company_id):

        return self.pros[
            self.pros.company_id == company_id
        ]

    # --------------------------------------------------

    def intelligence(self, company_id):

        if self.cashflow_intelligence.empty:
            return None

        df = self.cashflow_intelligence[
            self.cashflow_intelligence.company_id == company_id
        ]

        if df.empty:
            return None

        return df.iloc[0]
    # --------------------------------------------------

    def companies(self):
        """
        Returns all companies.
        """

        return self.company.copy()

    # --------------------------------------------------

    def sector_mapping(self):
        """
        Returns company-sector mapping.
        """

        return self.sectors.copy()

    # --------------------------------------------------

    def latest_market_data(self):
        """
        Returns the latest market-cap record
        for every company.
        """

        df = self._prepare_year(
            self.market_cap
        )

        idx = (
            df.groupby("company_id")[
                "year_num"
            ].idxmax()
        )

        return (
            df.loc[idx]
            .sort_values("company_id")
            .reset_index(drop=True)
        )

    # --------------------------------------------------

    def latest_financial_ratios(self):
        """
        Returns the latest financial-ratio record
        for every company.
        """

        df = self._prepare_year(
            self.financial_ratios
        )

        idx = (
            df.groupby("company_id")[
                "year_num"
            ].idxmax()
        )

        return (
            df.loc[idx]
            .sort_values("company_id")
            .reset_index(drop=True)
        )

    # --------------------------------------------------

    def latest_pnl(self):
        """
        Returns the latest Profit & Loss record
        for every company.
        """

        df = self._prepare_year(
            self.pl
        )

        idx = (
            df.groupby("company_id")[
                "year_num"
            ].idxmax()
        )

        return (
            df.loc[idx]
            .sort_values("company_id")
            .reset_index(drop=True)
        )
    
# ----------------------------------------------------------
# Chart Builder
# ----------------------------------------------------------

class ChartBuilder:
    """
    Creates all charts required for the PDF tearsheet.

    Each function returns the path of the generated PNG.
    """

    def __init__(self):
        CHART_DIR.mkdir(exist_ok=True)

    def _save(self, fig, filename):
        path = CHART_DIR / filename

        fig.tight_layout()
        fig.savefig(
            path,
            dpi=220,
            bbox_inches="tight",
        )

        plt.close(fig)

        return path

    # ------------------------------------------------------

    def revenue_chart(
        self,
        company_id,
        pnl,
    ):

        fig, ax = plt.subplots(figsize=(6, 3))

        ax.bar(
            pnl["year"].astype(str),
            pnl["sales"],
        )

        ax.set_title(
            "Revenue",
            fontsize=12,
            weight="bold",
        )

        ax.set_ylabel("Sales")

        ax.tick_params(
            axis="x",
            rotation=45,
        )

        return self._save(
            fig,
            f"{company_id}_revenue.png",
        )

    # ------------------------------------------------------

    def profit_chart(
        self,
        company_id,
        pnl,
    ):

        fig, ax = plt.subplots(figsize=(6, 3))

        ax.bar(
            pnl["year"].astype(str),
            pnl["net_profit"],
        )

        ax.set_title(
            "Net Profit",
            fontsize=12,
            weight="bold",
        )

        ax.set_ylabel("Profit")

        ax.tick_params(
            axis="x",
            rotation=45,
        )

        return self._save(
            fig,
            f"{company_id}_profit.png",
        )

    # ------------------------------------------------------

    def roe_chart(
        self,
        company_id,
        analysis_df,
    ):

        fig, ax = plt.subplots(figsize=(6, 3))

        if analysis_df.empty:

            ax.text(
                0.5,
                0.5,
                "No ROE History",
                ha="center",
                va="center",
                fontsize=12,
            )

            ax.set_axis_off()

        else:

            ax.plot(
                analysis_df.index,
                analysis_df["roe"],
                linewidth=2,
                marker="o",
            )

            ax.set_title(
                "ROE Trend",
                fontsize=12,
                weight="bold",
            )

            ax.set_ylabel("ROE (%)")

            ax.grid(
                alpha=0.3,
            )

        return self._save(
            fig,
            f"{company_id}_roe.png",
        )

    # ------------------------------------------------------

    def balance_chart(
        self,
        company_id,
        bs,
    ):

        fig, ax = plt.subplots(figsize=(6, 3))

        years = bs["year"].astype(str)

        equity = bs["equity_capital"]

        reserves = bs["reserves"]

        borrowings = bs["borrowings"]

        liabilities = bs["other_liabilities"]

        ax.bar(
            years,
            equity,
            label="Equity",
        )

        ax.bar(
            years,
            reserves,
            bottom=equity,
            label="Reserves",
        )

        ax.bar(
            years,
            borrowings,
            bottom=equity + reserves,
            label="Borrowings",
        )

        ax.bar(
            years,
            liabilities,
            bottom=equity + reserves + borrowings,
            label="Other Liabilities",
        )

        ax.set_title(
            "Balance Sheet Composition",
            fontsize=12,
            weight="bold",
        )

        ax.legend(
            fontsize=8,
        )

        ax.tick_params(
            axis="x",
            rotation=45,
        )

        return self._save(
            fig,
            f"{company_id}_balance.png",
        )

    # ------------------------------------------------------

    def cashflow_chart(
        self,
        company_id,
        cf,
    ):

        fig, ax = plt.subplots(figsize=(6, 3))

        years = cf["year"].astype(str)

        ax.plot(
            years,
            cf["operating_activity"],
            marker="o",
            label="Operating",
        )

        ax.plot(
            years,
            cf["investing_activity"],
            marker="o",
            label="Investing",
        )

        ax.plot(
            years,
            cf["financing_activity"],
            marker="o",
            label="Financing",
        )

        ax.set_title(
            "Cash Flow",
            fontsize=12,
            weight="bold",
        )

        ax.legend(fontsize=8)

        ax.grid(alpha=0.3)

        ax.tick_params(
            axis="x",
            rotation=45,
        )

        return self._save(
            fig,
            f"{company_id}_cashflow.png",
        )

    # ------------------------------------------------------

    def cleanup(self):

        if DEBUG_MODE:
            logger.info("Debug mode enabled - chart images are preserved.")
            return

        for image in CHART_DIR.glob("*.png"):
            try:
                image.unlink()
            except Exception as e:
                logger.warning(f"Could not delete {image}: {e}")
# ----------------------------------------------------------
# PDF Components
# ----------------------------------------------------------

class PDFComponents:
    """
    Reusable ReportLab components.
    """

    @staticmethod
    def section_title(text):

        return Paragraph(
            text,
            SECTION_STYLE,
        )

    # ------------------------------------------------------

    @staticmethod
    def company_header(company):

        title = Paragraph(
            f"""
            <b>{company['company_name']}</b><br/>
            <font size=10>{company['website']}</font>
            """,
            TITLE_STYLE,
        )

        about = str(
            company.get(
                "about_company",
                "",
            )
        )

        if len(about) > 450:
            about = about[:450] + "..."

        body = Paragraph(
            about,
            BODY_STYLE,
        )

        table = Table(
            [
                [title],
                [body],
            ],
            colWidths=[7.2 * inch],
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("TOPPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GREY),
                    ("BOX", (0, 0), (-1, -1), 1, colors.grey),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
                ]
            )
        )

        return table

    # ------------------------------------------------------

    @staticmethod
    def kpi_cards(kpis):

        """
        kpis should be a list of:

        [
            ("ROE","18.4%"),
            ("ROCE","21.6%"),
            ...
        ]
        """

        rows = []

        current = []

        for label, value in kpis:

            card = Table(
                [
                    [
                        Paragraph(
                            f"<b>{label}</b>",
                            SMALL_STYLE,
                        )
                    ],
                    [
                        Paragraph(
                            str(value),
                            SECTION_STYLE,
                        )
                    ],
                ],
                colWidths=[1.15 * inch],
            )

            card.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                        ("BOX", (0, 0), (-1, -1), 1, NAVY),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ]
                )
            )

            current.append(card)

            if len(current) == 3:
                rows.append(current)
                current = []

        while len(current) < 3:
            current.append("")

        rows.append(current)

        outer = Table(
            rows,
            colWidths=[
                2.3 * inch,
                2.3 * inch,
                2.3 * inch,
            ],
        )

        outer.setStyle(
            TableStyle(
                [
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        return outer

    # ------------------------------------------------------

    @staticmethod
    def chart(image_path):

        return Image(
            str(image_path),
            width=6.8 * inch,
            height=3.2 * inch,
        )

    # ------------------------------------------------------

    @staticmethod
    def pros_cons_box(pros, cons):

        pros = "<br/>".join(
            [
                "• " + str(x)
                for x in pros
                if pd.notna(x)
            ]
        )

        cons = "<br/>".join(
            [
                "• " + str(x)
                for x in cons
                if pd.notna(x)
            ]
        )

        left = Paragraph(
            f"<b>Pros</b><br/><br/>{pros}",
            BODY_STYLE,
        )

        right = Paragraph(
            f"<b>Cons</b><br/><br/>{cons}",
            BODY_STYLE,
        )

        table = Table(
            [[left, right]],
            colWidths=[
                3.45 * inch,
                3.45 * inch,
            ],
        )

        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                    ("BACKGROUND", (0, 0), (0, 0), HexColor("#F0FFF0")),
                    ("BACKGROUND", (1, 0), (1, 0), HexColor("#FFF5F5")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        return table

    # ------------------------------------------------------

    @staticmethod
    def capital_badge(intelligence):

        if intelligence is None:

            return Paragraph(
                "<b>Capital Allocation:</b> Not Available",
                BODY_STYLE,
            )

        html = f"""
        <b>Capital Allocation</b><br/><br/>

        Pattern :
        {intelligence.get('capital_allocation_label','N/A')}<br/><br/>

        CFO Quality :
        {intelligence.get('cfo_quality_label','N/A')}<br/><br/>

        CapEx :
        {intelligence.get('capex_label','N/A')}<br/><br/>

        Distress :
        {intelligence.get('distress_flag','N/A')}<br/><br/>

        Deleveraging :
        {intelligence.get('deleveraging_flag','N/A')}
        """

        badge = Table(
            [
                [
                    Paragraph(
                        html,
                        BODY_STYLE,
                    )
                ]
            ],
            colWidths=[7.1 * inch],
        )

        badge.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                    ("BOX", (0, 0), (-1, -1), 1.5, NAVY),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )

        return badge
# ----------------------------------------------------------
# Tearsheet Generator
# ----------------------------------------------------------

class TearsheetGenerator:

    def __init__(self):

        self.repo = DataRepository()

        self.charts = ChartBuilder()

    # ------------------------------------------------------

    def build_page_one(
        self,
        story,
        company_id,
    ):

        company = self.repo.company_profile(
            company_id
        )

        pnl = self.repo.pnl(
            company_id
        )

        analysis = self.repo.analysis_data(
            company_id
        )

        # -----------------------------
        # Charts
        # -----------------------------

        revenue_chart = self.charts.revenue_chart(
            company_id,
            pnl,
        )

        profit_chart = self.charts.profit_chart(
            company_id,
            pnl,
        )

        roe_chart = self.charts.roe_chart(
            company_id,
            analysis,
        )

        # -----------------------------
        # Latest Financials
        # -----------------------------

        latest = pnl.iloc[-1]

        kpis = [

            (
                "Revenue",
                f"{latest['sales']:,.0f}",
            ),

            (
                "Net Profit",
                f"{latest['net_profit']:,.0f}",
            ),

            (
                "EPS",
                f"{latest['eps']:.2f}",
            ),

            (
                "Dividend %",
                f"{latest['dividend_payout']:.1f}",
            ),

            (
                "ROE",
                f"{company['roe_percentage']}%",
            ),

            (
                "ROCE",
                f"{company['roce_percentage']}%",
            ),

        ]

        # -----------------------------
        # Layout
        # -----------------------------

        story.append(
            PDFComponents.company_header(
                company
            )
        )

        story.append(
            Spacer(
                1,
                0.20 * inch,
            )
        )

        story.append(
            PDFComponents.kpi_cards(
                kpis
            )
        )

        story.append(
            Spacer(
                1,
                0.20 * inch,
            )
        )

        story.append(
            PDFComponents.section_title(
                "Revenue"
            )
        )

        story.append(
            PDFComponents.chart(
                revenue_chart
            )
        )

        story.append(
            Spacer(
                1,
                0.15 * inch,
            )
        )

        story.append(
            PDFComponents.section_title(
                "Net Profit"
            )
        )

        story.append(
            PDFComponents.chart(
                profit_chart
            )
        )

        story.append(
            Spacer(
                1,
                0.15 * inch,
            )
        )

        story.append(
            PDFComponents.section_title(
                "ROE Trend"
            )
        )

        story.append(
            PDFComponents.chart(
                roe_chart
            )
        )

    # ------------------------------------------------------

    def build_page_two(
        self,
        story,
        company_id,
    ):

        bs = self.repo.balance_sheet(
            company_id
        )

        cf = self.repo.cashflow(
            company_id
        )

        pros_df = self.repo.pros_cons(
            company_id
        )

        intelligence = self.repo.intelligence(
            company_id
        )

        balance_chart = (
            self.charts.balance_chart(
                company_id,
                bs,
            )
        )

        cash_chart = (
            self.charts.cashflow_chart(
                company_id,
                cf,
            )
        )

        story.append(
            PageBreak()
        )

        story.append(
            PDFComponents.section_title(
                "Balance Sheet Composition"
            )
        )

        story.append(
            PDFComponents.chart(
                balance_chart
            )
        )

        story.append(
            Spacer(
                1,
                0.20 * inch,
            )
        )

        story.append(
            PDFComponents.section_title(
                "Cash Flow"
            )
        )

        story.append(
            PDFComponents.chart(
                cash_chart
            )
        )

        story.append(
            Spacer(
                1,
                0.20 * inch,
            )
        )

        # -----------------------------
        # Pros / Cons
        # -----------------------------

        pros = []

        cons = []

        if not pros_df.empty:

            if "pros" in pros_df.columns:

                pros = (
                    pros_df["pros"]
                    .dropna()
                    .tolist()
                )

            if "cons" in pros_df.columns:

                cons = (
                    pros_df["cons"]
                    .dropna()
                    .tolist()
                )

        story.append(
            PDFComponents.pros_cons_box(
                pros,
                cons,
            )
        )

        story.append(
            Spacer(
                1,
                0.20 * inch,
            )
        )

        story.append(
            PDFComponents.capital_badge(
                intelligence
            )
        )

    # ------------------------------------------------------

    def generate_company(
        self,
        company_id,
    ):

        logger.info(
            "Generating %s",
            company_id,
        )

        pdf_file = (
            TEARSHEET_DIR
            /
            f"{company_id}_tearsheet.pdf"
        )

        doc = SimpleDocTemplate(
            str(pdf_file),
        )

        story = []

        self.build_page_one(
            story,
            company_id,
        )

        self.build_page_two(
            story,
            company_id,
        )

        doc.build(
            story
        )

        logger.info(
            "Saved -> %s",
            pdf_file,
        )
    # ------------------------------------------------------

    def generate_all(self):

        logger.info("--------------------------------")
        logger.info("Generating Company Tearsheets")
        logger.info("--------------------------------")

        companies = (
            self.repo.company["id"]
            .dropna()
            .unique()
        )

        success = 0
        failed = 0

        for company_id in companies:

            try:

                self.generate_company(
                    company_id
                )

                success += 1

            except Exception as e:

                logger.exception(
                    "Failed for %s",
                    company_id,
                )

                failed += 1

        self.charts.cleanup()

        logger.info("--------------------------------")
        logger.info("Completed")
        logger.info("Generated : %s", success)
        logger.info("Failed    : %s", failed)
        logger.info("--------------------------------")


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main():

    generator = TearsheetGenerator()

    generator.generate_all()


if __name__ == "__main__":
    main()
