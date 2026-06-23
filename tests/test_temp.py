import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.etl.normaliser import normalize_year
from src.etl.normaliser import normalize_ticker


print(normalize_year("FY24"))
print(normalize_year("2024"))

print(normalize_ticker("tcs"))
print(normalize_ticker(" tcs.ns "))