"""
Peer Service

Business logic for Peer APIs.
"""


class PeerService:

    def __init__(self, conn):
        self.conn = conn

    # -------------------------------------------------------
    # Peer Group
    # -------------------------------------------------------

    def get_peer_group(
        self,
        group_name: str,
    ) -> list[dict]:

        cursor = self.conn.cursor()

        query = """
        SELECT

            pg.peer_group_name,
            pg.company_id,
            c.company_name,
            pg.is_benchmark,

            pp.metric,
            pp.value,
            pp.percentile_rank,
            pp.year

        FROM peer_groups pg

        INNER JOIN companies c
            ON pg.company_id = c.id

        LEFT JOIN peer_percentiles pp
            ON pg.company_id = pp.company_id
           AND pg.peer_group_name = pp.peer_group_name

        WHERE LOWER(pg.peer_group_name)=LOWER(?)

        ORDER BY
            c.company_name,
            pp.metric
        """

        cursor.execute(query, (group_name,))

        rows = cursor.fetchall()

        if not rows:
            return None

        companies = {}

        for row in rows:

            ticker = row["company_id"]

            if ticker not in companies:

                companies[ticker] = {
                    "ticker": ticker,
                    "company_name": row["company_name"],
                    "peer_group": row["peer_group_name"],
                    "is_benchmark": bool(row["is_benchmark"]),
                    "metrics": [],
                }

            companies[ticker]["metrics"].append(
                {
                    "metric": row["metric"],
                    "value": row["value"],
                    "percentile_rank": row["percentile_rank"],
                    "year": row["year"],
                }
            )

        return list(companies.values())

    # -------------------------------------------------------
    # Compare company with peer group
    # -------------------------------------------------------

    def compare_company_with_peers(self, ticker: str):

        cursor = self.conn.cursor()

        # Find peer group
        cursor.execute(
            """
            SELECT peer_group_name
            FROM peer_groups
            WHERE company_id = ?
            """,
            (ticker,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        peer_group = row["peer_group_name"]

        query = """
        WITH latest_peer AS (

            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY company_id, metric
                       ORDER BY
                           CASE
                               WHEN year='TTM' THEN 9999
                               ELSE CAST(SUBSTR(year,-4) AS INTEGER)
                           END DESC
                   ) rn

            FROM peer_percentiles

            WHERE peer_group_name = ?
        )

        SELECT
            company_id,
            metric,
            value,
            percentile_rank
        FROM latest_peer
        WHERE rn = 1
        """

        cursor.execute(query, (peer_group,))
        rows = cursor.fetchall()

        if not rows:
            return None

        benchmark = None

        cursor.execute(
            """
            SELECT company_id
            FROM peer_groups
            WHERE peer_group_name = ?
              AND is_benchmark = 1
            """,
            (peer_group,),
        )

        b = cursor.fetchone()

        if b:
            benchmark = b["company_id"]

        company_metrics = {}
        benchmark_metrics = {}
        peer_average = {}

        grouped = {}

        for row in rows:

            metric = row["metric"]
            company = row["company_id"]

            grouped.setdefault(metric, []).append(row["value"])

            if company == ticker:
                company_metrics[metric] = row["value"]

            if benchmark and company == benchmark:
                benchmark_metrics[metric] = row["value"]

        for metric, values in grouped.items():

            peer_average[metric] = sum(values) / len(values) if values else None

        return {
            "ticker": ticker,
            "peer_group": peer_group,
            "benchmark_company": benchmark,
            "company": company_metrics,
            "peer_average": peer_average,
            "benchmark": benchmark_metrics,
        }
