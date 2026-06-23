from pathlib import Path
import pandas as pd

RAW_DATA_PATH = Path("data/raw")

CORE_FILES = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx"
]


def load_excel(file_name: str):
    """
    Load Excel file using header=1.
    """

    file_path = RAW_DATA_PATH / file_name

    df = pd.read_excel(
        file_path,
        header=1
    )

    print("\n" + "=" * 50)
    print(f"Loaded: {file_name}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    return df


if __name__ == "__main__":

    for file_name in CORE_FILES:

        try:
            load_excel(file_name)

        except Exception as e:
            print(f"\nError loading {file_name}")
            print(e)