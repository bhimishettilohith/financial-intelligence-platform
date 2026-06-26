# =====================================
# Financial Intelligence Platform
# Makefile
# =====================================

test:
	pytest

validate:
	python src/etl/validator.py

load:
	python db/loader.py

audit:
	python -c "import pandas as pd; print(pd.read_csv('output/load_audit.csv'))"

db-check:
	python -c "import sqlite3; conn=sqlite3.connect('nifty100.db'); print(conn.execute('PRAGMA foreign_key_check').fetchall())"

clean:
	del /Q __pycache__ 2>nul