"""
Document Service
"""

from urllib.parse import urlparse


class DocumentService:

    def __init__(self, conn):
        self.conn = conn

    def _is_valid_url(self, url: str) -> bool:
        """
        Check whether the given string is a valid URL.
        """

        if not url:
            return False

        parsed = urlparse(url)

        return bool(parsed.scheme and parsed.netloc)

    def get_company_documents(
        self,
        ticker: str,
    ) -> list[dict]:

        cursor = self.conn.cursor()

        query = """
        SELECT
            company_id,
            year,
            annual_report
        FROM documents
        WHERE company_id = ?
        ORDER BY
            CASE
                WHEN year = 'TTM' THEN 9999
                ELSE CAST(SUBSTR(year, -4) AS INTEGER)
            END DESC
        """

        cursor.execute(query, (ticker,))

        rows = cursor.fetchall()

        if not rows:
            return None

        columns = [c[0] for c in cursor.description]

        results = []

        for row in rows:

            item = dict(zip(columns, row))

            item["is_url_valid"] = self._is_valid_url(item["annual_report"])

            results.append(item)

        return results
