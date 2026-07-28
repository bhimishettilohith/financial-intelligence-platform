"""
Sector Service

Business logic for Sector APIs.
"""


class SectorService:

    def __init__(self, conn):
        self.conn = conn

    # -------------------------------------------------------
    # Get all sectors
    # -------------------------------------------------------

    def get_all_sectors(self) -> list[dict]:

        cursor = self.conn.cursor()

        query = """
        WITH latest_ratios AS (

            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY company_id
                       ORDER BY
                           CASE
                               WHEN year='TTM' THEN 9999
                               ELSE CAST(SUBSTR(year,-4) AS INTEGER)
                           END DESC
                   ) rn

            FROM financial_ratios
        )

        SELECT

            s.broad_sector,

            COUNT(*) AS company_count,

            AVG(lr.return_on_equity_pct) AS median_roe,

            AVG(lr.debt_to_equity) AS median_de

        FROM sectors s

        LEFT JOIN latest_ratios lr
            ON s.company_id = lr.company_id
           AND lr.rn = 1

        GROUP BY s.broad_sector

        ORDER BY s.broad_sector
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [c[0] for c in cursor.description]

        result = []

        for row in rows:

            item = dict(zip(columns, row))

            # Dataset has no PE ratio.
            item["median_pe"] = None

            result.append(item)

        return result

    # -------------------------------------------------------
    # Get companies in a sector
    # -------------------------------------------------------

    def get_sector_companies(self, sector: str):

        cursor = self.conn.cursor()

        query = """
        WITH latest_ratios AS (

            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY company_id
                       ORDER BY
                           CASE
                               WHEN year='TTM' THEN 9999
                               ELSE CAST(SUBSTR(year,-4) AS INTEGER)
                           END DESC
                   ) rn

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

        INNER JOIN sectors s
            ON c.id = s.company_id

        LEFT JOIN latest_ratios lr
            ON c.id = lr.company_id
           AND lr.rn = 1

        WHERE LOWER(s.broad_sector) = LOWER(?)

        ORDER BY
            lr.composite_quality_score DESC,
            c.company_name ASC
        """

        cursor.execute(query, (sector,))

        rows = cursor.fetchall()

        if not rows:
            return None

        columns = [c[0] for c in cursor.description]

        results = []

        for rank, row in enumerate(rows, start=1):

            company = dict(zip(columns, row))
            company["rank"] = rank

            results.append(company)

        return results
