"""
Sprint 6 - Day 39

Database service layer for company APIs.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class CompanyService:
    """Service class for company-related database operations."""

    def __init__(self, conn: sqlite3.Connection):

        self.conn = conn

        self.conn.row_factory = sqlite3.Row

    def get_company_list(
        self,
        sector: str | None = None,
        market_cap_category: str | None = None,
        search: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Return company list with optional filters.
        """

        sql = """
        SELECT
            c.id,
            c.company_name,
            s.broad_sector,
            s.sub_sector,
            c.roe_percentage AS roe_pct,
            c.roce_percentage AS roce_pct,
            s.market_cap_category
        FROM companies c
        LEFT JOIN sectors s
            ON c.id = s.company_id
        WHERE 1=1
        """

        params = []

        if sector:
            sql += """
            AND LOWER(s.broad_sector)=LOWER(?)
            """
            params.append(sector)

        if market_cap_category:
            sql += """
            AND LOWER(s.market_cap_category)=LOWER(?)
            """
            params.append(market_cap_category)

        if search:
            sql += """
            AND (
                LOWER(c.company_name) LIKE LOWER(?)
                OR LOWER(c.id) LIKE LOWER(?)
            )
            """
            value = f"%{search}%"
            params.extend([value, value])

        sql += """
        ORDER BY c.company_name
        """

        rows = self.conn.execute(sql, params).fetchall()

        return [dict(row) for row in rows]

    def get_company_profile(
        self,
        ticker: str,
    ) -> dict[str, Any] | None:
        """
        Return company profile.
        """

        sql = """
        SELECT
            c.*,
            s.broad_sector,
            s.sub_sector,
            s.index_weight_pct,
            s.market_cap_category,
            fr.*
        FROM companies c

        LEFT JOIN sectors s
            ON c.id=s.company_id

        LEFT JOIN financial_ratios fr
            ON c.id=fr.company_id

        WHERE c.id=?
        ORDER BY fr.year DESC
        LIMIT 1
        """

        row = self.conn.execute(sql, (ticker,)).fetchone()

        if row is None:
            return None

        return dict(row)

    def get_profit_loss(
        self,
        ticker: str,
        from_year: str | None,
        to_year: str | None,
    ) -> list[dict]:

        sql = """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        """

        params = [ticker]

        if from_year:
            sql += " AND year>=?"
            params.append(from_year)

        if to_year:
            sql += " AND year<=?"
            params.append(to_year)

        sql += " ORDER BY year"

        rows = self.conn.execute(sql, params).fetchall()

        return [dict(r) for r in rows]

    def get_balance_sheet(
        self,
        ticker: str,
        from_year: str | None,
        to_year: str | None,
    ) -> list[dict]:

        sql = """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        """

        params = [ticker]

        if from_year:
            sql += " AND year>=?"
            params.append(from_year)

        if to_year:
            sql += " AND year<=?"
            params.append(to_year)

        sql += " ORDER BY year"

        rows = self.conn.execute(sql, params).fetchall()

        return [dict(r) for r in rows]

    def get_cashflow(
        self,
        ticker: str,
        from_year: str | None,
        to_year: str | None,
    ) -> list[dict]:

        sql = """
        SELECT *
        FROM cashflow
        WHERE company_id=?
        """

        params = [ticker]

        if from_year:
            sql += " AND year>=?"
            params.append(from_year)

        if to_year:
            sql += " AND year<=?"
            params.append(to_year)

        sql += " ORDER BY year"

        rows = self.conn.execute(sql, params).fetchall()

        return [dict(r) for r in rows]

    def get_tearsheet_path(self, ticker: str) -> Path | None:
        """
        Return path to the company's pre-generated tearsheet PDF.
        """

        project_root = Path(__file__).resolve().parents[3]

        pdf_path = (
            project_root / "output" / "tearsheets" / f"{ticker.upper()}_tearsheet.pdf"
        )

        if pdf_path.exists():
            return pdf_path

        return None

    def get_ratios(
        self,
        ticker: str,
        year: str | None = None,
    ) -> list[dict]:

        sql = """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        """

        params = [ticker]

        if year:
            sql += " AND year=?"
            params.append(year)

        sql += " ORDER BY year"

        rows = self.conn.execute(sql, params).fetchall()

        return [dict(r) for r in rows]
