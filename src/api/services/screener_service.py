"""
Screener Service

Implements business logic for the Screener API.

Features
--------
- Latest KPI selection (TTM preferred, otherwise latest annual)
- Dynamic filtering
- Ranked by composite_quality_score
"""


class ScreenerService:
    def __init__(self, conn):
        self.conn = conn

    def screen_companies(
        self,
        min_roe: float | None = None,
        max_de: float | None = None,
        min_fcf: float | None = None,
        sector: str | None = None,
        min_rev_cagr_5yr: float | None = None,
        min_pat_cagr_5yr: float | None = None,
    ):
        cursor = self.conn.cursor()

        query = """
        WITH latest_ratios AS (

            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY company_id
                      ORDER BY
                    CASE
                        WHEN year = 'TTM' THEN 9999
                        ELSE CAST(SUBSTR(year, -4) AS INTEGER)
                    END DESC
                   ) AS rn

            FROM financial_ratios
        )

        SELECT

            c.id AS ticker,
            c.company_name,

            s.broad_sector,
            s.sub_sector,
            s.market_cap_category,

            lr.return_on_equity_pct,
            lr.return_on_capital_employed_pct,
            lr.debt_to_equity,
            lr.free_cash_flow_cr,
            lr.revenue_cagr_5yr,
            lr.pat_cagr_5yr,
            lr.composite_quality_score

        FROM companies c

        LEFT JOIN latest_ratios lr
            ON c.id = lr.company_id
           AND lr.rn = 1

        LEFT JOIN sectors s
            ON c.id = s.company_id

        WHERE 1=1
        """

        params = []

        # -------------------------------
        # Dynamic Filters
        # -------------------------------

        if min_roe is not None:
            query += """
                AND lr.return_on_equity_pct >= ?
            """
            params.append(min_roe)

        if max_de is not None:
            query += """
                AND lr.debt_to_equity <= ?
            """
            params.append(max_de)

        if min_fcf is not None:
            query += """
                AND lr.free_cash_flow_cr >= ?
            """
            params.append(min_fcf)

        if sector:
            query += """
                AND LOWER(s.broad_sector) = LOWER(?)
            """
            params.append(sector)

        if min_rev_cagr_5yr is not None:
            query += """
                AND lr.revenue_cagr_5yr >= ?
            """
            params.append(min_rev_cagr_5yr)

        if min_pat_cagr_5yr is not None:
            query += """
                AND lr.pat_cagr_5yr >= ?
            """
            params.append(min_pat_cagr_5yr)

        # -------------------------------
        # Ranking
        # -------------------------------

        query += """
            ORDER BY
                lr.composite_quality_score DESC,
                c.company_name ASC
        """

        cursor.execute(query, params)

        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        results = []

        for rank, row in enumerate(rows, start=1):

            company = dict(zip(columns, row))

            company["rank"] = rank

            results.append(company)

        return results
