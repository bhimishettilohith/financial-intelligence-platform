"""
Financial Intelligence Platform
Sprint 5 – Day 33

Company Tearsheet Generator
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import inch

from reportlab.pdfgen import canvas

from reportlab.platypus import (
    Paragraph,
    Table,
    TableStyle,
)

# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"

OUTPUT_DIR = PROJECT_ROOT / "output"

CHART_DIR = OUTPUT_DIR / "_charts"

TEARSHEET_DIR = OUTPUT_DIR / "tearsheets"

CHART_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

TEARSHEET_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ==========================================================
# Files
# ==========================================================

COMPANIES_FILE = RAW_DIR / "companies.xlsx"

PL_FILE = RAW_DIR / "profitandloss.xlsx"

BS_FILE = RAW_DIR / "balancesheet.xlsx"

CF_FILE = RAW_DIR / "cashflow.xlsx"

ANALYSIS_FILE = RAW_DIR / "analysis.xlsx"

PROS_FILE = OUTPUT_DIR / "pros_cons_generated.csv"

CF_INTELLIGENCE_FILE = (
    OUTPUT_DIR /
    "cashflow_intelligence.xlsx"
)

PAGE_WIDTH, PAGE_HEIGHT = A4