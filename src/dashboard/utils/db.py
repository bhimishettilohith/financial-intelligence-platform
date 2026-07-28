"""
Database utility functions for the Financial Intelligence Dashboard.

Sprint 4 - Day 22

This module acts as the single data access layer (DAL) for the dashboard.
All Streamlit pages should access SQLite only through this file.

Author: Bhimishetti Lohith
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "data" / "nifty100.db"

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

_MONTH_PRIORITY = {
    "MAR": 1,
    "JUN": 2,
    "SEP": 3,
    "DEC": 4,
}


def get_connection() -> sqlite3.Connection:
    """
    Create a SQLite connection.

    Returns
    -------
    sqlite3.Connection
    """

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


@st.cache_data(ttl=600, show_spinner=False)
def run_query(
    sql: str,
    params: tuple | None = None,
) -> pd.DataFrame:
    """
    Execute a SQL query and return a DataFrame.

    Parameters
    ----------
    sql : str
        SQL query.

    params : tuple | None
        Query parameters.

    Returns
    -------
    pd.DataFrame
    """

    conn = get_connection()

    try:
        return pd.read_sql_query(
            sql,
            conn,
            params=params,
        )

    finally:
        conn.close()


# ---------------------------------------------------------------------
# Reporting Period Helpers
# ---------------------------------------------------------------------


def _parse_period(period: str):
    """
    Convert reporting period into sortable tuple.

    Examples
    --------
    Mar 2024 -> (2024,1)

    Sep 2024 -> (2024,3)

    Dec 2023 -> (2023,4)

    TTM -> None
    """

    if period is None:
        return None

    period = period.strip()

    if period.upper() == "TTM":
        return None

    match = re.search(
        r"(Mar|Jun|Sep|Dec)\s+(\d{4})",
        period,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    month = match.group(1).upper()
    year = int(match.group(2))

    return (
        year,
        _MONTH_PRIORITY.get(month, 0),
    )


@st.cache_data(ttl=600, show_spinner=False)
def get_latest_year() -> str:
    """
    Return latest reporting period.

    Example
    -------
    Sep 2024
    """

    df = run_query("""
        SELECT DISTINCT year
        FROM financial_ratios
        """)

    periods = []

    for period in df["year"]:

        parsed = _parse_period(period)

        if parsed is not None:
            periods.append(
                (
                    parsed,
                    period,
                )
            )

    periods.sort(reverse=True)

    return periods[0][1]


# ---------------------------------------------------------------------
# Company Functions
# ---------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def get_companies() -> pd.DataFrame:
    """
    Return all companies sorted alphabetically.
    """

    df = run_query("""
        SELECT
            id,
            TRIM(company_name) AS company_name
        FROM companies
        ORDER BY company_name
        """)

    df["company_name"] = (
        df["company_name"].astype(str).str.replace("\n", "", regex=False).str.strip()
    )

    return df


@st.cache_data(ttl=600, show_spinner=False)
def search_company(
    search_text: str,
) -> pd.DataFrame:
    """
    Search companies by name.
    """

    df = run_query(
        """
        SELECT
            id,
            TRIM(company_name) AS company_name
        FROM companies
        WHERE company_name LIKE ?
        ORDER BY company_name
        """,
        (f"%{search_text}%",),
    )

    df["company_name"] = (
        df["company_name"].astype(str).str.replace("\n", "", regex=False).str.strip()
    )

    return df


@st.cache_data(ttl=600, show_spinner=False)
def get_company_profile(company_id: str) -> pd.DataFrame:
    """
    Return company profile information.
    """

    return run_query(
        """
        SELECT *
        FROM companies
        WHERE id = ?
        """,
        (company_id,),
    )


# ---------------------------------------------------------------------
# Financial Ratio Functions
# ---------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def get_ratios(company_id: str) -> pd.DataFrame:
    """
    Return all financial ratios for a company ordered by latest period.
    """

    df = run_query(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        """,
        (company_id,),
    )

    if df.empty:
        return df

    df["_sort_key"] = df["year"].apply(_parse_period)

    df = (
        df[df["_sort_key"].notna()]
        .sort_values("_sort_key", ascending=False)
        .drop(columns="_sort_key")
        .reset_index(drop=True)
    )

    return df


@st.cache_data(ttl=600, show_spinner=False)
def get_latest_ratios(company_id: str) -> pd.DataFrame:
    """
    Return latest available financial ratios for one company.
    """

    latest_period = get_latest_year()

    df = run_query(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
          AND year = ?
        """,
        (
            company_id,
            latest_period,
        ),
    )

    if not df.empty:
        return df

    # Fallback in case the latest global period
    # doesn't exist for this company.
    ratios = get_ratios(company_id)

    return ratios.head(1)


# ---------------------------------------------------------------------
# Optimized Latest Ratios
# ---------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def get_all_latest_ratios() -> pd.DataFrame:
    """
    Return the latest available financial ratios for every company.

    The latest row is determined in Python using the reporting-period parser,
    so mixed values such as 'Mar 2023 15', 'Sep 2024', and 'TTM' are handled
    correctly.
    """

    df = run_query("""
        SELECT
            fr.*,
            c.company_name
        FROM financial_ratios fr
        INNER JOIN companies c
            ON fr.company_id = c.id
        """)

    if df.empty:
        return df

    df["_sort_key"] = df["year"].apply(_parse_period)

    df = df[df["_sort_key"].notna()].copy()

    df = (
        df.sort_values(
            by=["company_id", "_sort_key"],
            ascending=[True, False],
        )
        .drop_duplicates(
            subset="company_id",
            keep="first",
        )
        .drop(columns="_sort_key")
        .reset_index(drop=True)
    )

    return df


@st.cache_data(ttl=600, show_spinner=False)
def get_ratios_by_year(year: str) -> pd.DataFrame:
    """
    Return ratios for a reporting year.
    Example:
        2024
        2023
    """

    return run_query(
        """
        SELECT
            fr.*,
            c.company_name
        FROM financial_ratios fr
        INNER JOIN companies c
            ON fr.company_id = c.id
        WHERE fr.year LIKE ?
        """,
        (f"%{year}",),
    )


@st.cache_data(ttl=600, show_spinner=False)
def get_ratios_by_year(year: str) -> pd.DataFrame:
    """
    Return financial ratios for a reporting period.
    Example:
        Mar 2024
        Mar 2023
    """

    df = run_query(
        """
        SELECT
            fr.*,
            c.company_name
        FROM financial_ratios fr
        INNER JOIN companies c
            ON fr.company_id = c.id
        WHERE fr.year LIKE ?
        """,
        (f"%{year}",),
    )

    return df


# ---------------------------------------------------------------------
# Peer Group Functions
# ---------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def get_peer_groups() -> pd.DataFrame:
    """
    Return all peer groups.
    """

    return run_query("""
        SELECT DISTINCT
            peer_group_name
        FROM peer_groups
        ORDER BY peer_group_name
        """)


@st.cache_data(ttl=600, show_spinner=False)
def get_peer_members(peer_group: str) -> pd.DataFrame:
    """
    Return all companies in a peer group.
    """

    return run_query(
        """
        SELECT

            pg.peer_group_name,

            pg.company_id,

            c.company_name,

            pg.is_benchmark

        FROM peer_groups pg

        INNER JOIN companies c

        ON pg.company_id = c.id

        WHERE pg.peer_group_name = ?

        ORDER BY

            pg.is_benchmark DESC,

            c.company_name
        """,
        (peer_group,),
    )


@st.cache_data(ttl=600, show_spinner=False)
def get_peer_percentiles(company_id: str) -> pd.DataFrame:
    """
    Return percentile metrics for one company.
    """

    df = run_query(
        """
        SELECT *

        FROM peer_percentiles

        WHERE company_id = ?
        """,
        (company_id,),
    )

    if df.empty:
        return df

    df["_sort_key"] = df["year"].apply(_parse_period)

    return (
        df[df["_sort_key"].notna()]
        .sort_values(
            "_sort_key",
            ascending=False,
        )
        .drop(columns="_sort_key")
        .reset_index(drop=True)
    )


@st.cache_data(ttl=600, show_spinner=False)
def get_peer_average(peer_group: str) -> pd.DataFrame:
    """
    Return average percentile values for a peer group.
    """

    return run_query(
        """
        SELECT

            metric,

            AVG(value) AS average_value,

            AVG(percentile_rank) AS average_percentile

        FROM peer_percentiles

        WHERE peer_group_name = ?

        GROUP BY metric

        ORDER BY metric
        """,
        (peer_group,),
    )


# ---------------------------------------------------------------------
# Pros & Cons
# ---------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def get_pros_cons(company_id: str) -> pd.DataFrame:
    """
    Return company strengths and weaknesses.
    """

    return run_query(
        """
        SELECT

            pros,

            cons

        FROM prosandcons

        WHERE company_id = ?
        """,
        (company_id,),
    )


# ---------------------------------------------------------------------
# Valuation (Day 26 Placeholder)
# ---------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def get_valuation(company_id: str) -> pd.DataFrame:
    """
    Placeholder for Sprint 4 Day 26.
    """

    return pd.DataFrame()


# ---------------------------------------------------------------------
# Dashboard Helpers
# ---------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def get_dashboard_summary() -> dict:
    """
    Return high-level dashboard statistics.
    """

    latest = get_all_latest_ratios()
    sectors = get_sectors()
    companies = get_companies()

    summary = {
        "total_companies": len(companies),
        "total_sectors": sectors["broad_sector"].nunique(),
        "latest_period": get_latest_year(),
        "average_roe": (
            float(round(latest["return_on_equity_pct"].mean(), 2))
            if not latest.empty
            else 0
        ),
        "average_roce": (
            float(round(latest["return_on_capital_employed_pct"].mean(), 2))
            if not latest.empty
            else 0
        ),
        "average_quality_score": (
            float(round(latest["composite_quality_score"].mean(), 2))
            if not latest.empty
            else 0
        ),
    }

    return summary


@st.cache_data(ttl=600, show_spinner=False)
def get_company_names() -> list[str]:
    """
    Return company names for select boxes.
    """

    df = get_companies()

    return df["company_name"].tolist()


@st.cache_data(ttl=600, show_spinner=False)
def get_company_id(company_name: str) -> str | None:
    """
    Return company ID from company name.
    """

    df = run_query(
        """
        SELECT
            id
        FROM companies
        WHERE company_name = ?
        """,
        (company_name,),
    )

    if df.empty:
        return None

    return df.iloc[0]["id"]


# ---------------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def get_pl(company_id: str) -> pd.DataFrame:
    """
    Return Profit & Loss statement.
    """

    df = run_query(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        """,
        (company_id,),
    )

    if df.empty:
        return df

    df["_sort_key"] = df["year"].apply(_parse_period)

    return (
        df[df["_sort_key"].notna()]
        .sort_values("_sort_key", ascending=False)
        .drop(columns="_sort_key")
        .reset_index(drop=True)
    )


# ---------------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def get_bs(company_id: str) -> pd.DataFrame:
    """
    Return Balance Sheet.
    """

    df = run_query(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
        """,
        (company_id,),
    )

    if df.empty:
        return df

    df["_sort_key"] = df["year"].apply(_parse_period)

    return (
        df[df["_sort_key"].notna()]
        .sort_values("_sort_key", ascending=False)
        .drop(columns="_sort_key")
        .reset_index(drop=True)
    )


# ---------------------------------------------------------------------
# Cash Flow
# ---------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def get_cf(company_id: str) -> pd.DataFrame:
    """
    Return Cash Flow statement.
    """

    df = run_query(
        """
        SELECT *
        FROM cashflow
        WHERE company_id = ?
        """,
        (company_id,),
    )

    if df.empty:
        return df

    df["_sort_key"] = df["year"].apply(_parse_period)

    return (
        df[df["_sort_key"].notna()]
        .sort_values("_sort_key", ascending=False)
        .drop(columns="_sort_key")
        .reset_index(drop=True)
    )


# ---------------------------------------------------------------------
# Sector Functions
# ---------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def get_sectors() -> pd.DataFrame:
    """
    Return all sector information.
    """

    return run_query("""
        SELECT *
        FROM sectors
        ORDER BY broad_sector, company_id
        """)


@st.cache_data(ttl=600, show_spinner=False)
def get_sector_summary() -> pd.DataFrame:
    """
    Return company count by broad sector.
    """

    return run_query("""
        SELECT

            broad_sector,

            COUNT(*) AS company_count,

            AVG(index_weight_pct) AS avg_index_weight

        FROM sectors

        GROUP BY broad_sector

        ORDER BY company_count DESC
        """)


@st.cache_data(ttl=600, show_spinner=False)
def get_companies_by_sector(
    sector: str,
) -> pd.DataFrame:
    """
    Return all companies belonging to one sector.
    """

    return run_query(
        """
        SELECT

            c.id,

            c.company_name,

            s.broad_sector,

            s.sub_sector,

            s.market_cap_category,

            s.index_weight_pct

        FROM companies c

        INNER JOIN sectors s

        ON c.id = s.company_id

        WHERE s.broad_sector = ?

        ORDER BY c.company_name
        """,
        (sector,),
    )


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Annual Reports
# ---------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def get_documents(company_id: str) -> pd.DataFrame:
    """
    Return annual reports for one company.
    """

    return run_query(
        """
        SELECT
            year,
            annual_report
        FROM documents
        WHERE company_id = ?
        ORDER BY year DESC
        """,
        (company_id,),
    )
