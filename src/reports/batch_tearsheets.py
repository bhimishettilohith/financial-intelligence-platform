import logging
from pathlib import Path

import pandas as pd

from src.reports.tearsheet import TearsheetGenerator

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class BatchTearsheetGenerator:

    def __init__(self):

        self.generator = TearsheetGenerator()

        self.repo = self.generator.repo

        self.skipped = []

    # ----------------------------------------------------------

    def has_minimum_history(self, company_id):

        pnl = self.repo.pnl(company_id)

        if pnl.empty:
            return False

        return pnl["year_num"].nunique() >= 3

    # ----------------------------------------------------------

    def run(self):

        companies = self.repo.companies()

        generated = 0
        skipped = 0
        failed = 0

        for company_id in companies["id"]:

            if not self.has_minimum_history(company_id):

                logger.warning(
                    "%s skipped (<3 years of history)",
                    company_id,
                )

                skipped += 1

                self.skipped.append(
                    {
                        "company_id": company_id,
                        "reason": "Less than 3 years of data",
                    }
                )

                continue

            try:

                self.generator.generate_company(company_id)

                generated += 1

            except Exception:

                logger.exception(
                    "Failed generating %s",
                    company_id,
                )

                failed += 1

        if self.skipped:

            pd.DataFrame(self.skipped).to_csv(
                OUTPUT_DIR / "skipped_tearsheets.csv",
                index=False,
            )

        logger.info("=" * 60)
        logger.info("Companies : %s", len(companies))
        logger.info("Generated : %s", generated)
        logger.info("Skipped   : %s", skipped)
        logger.info("Failed    : %s", failed)
        logger.info("=" * 60)


def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    BatchTearsheetGenerator().run()


if __name__ == "__main__":
    main()
