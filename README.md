# Financial Intelligence Platform

A data analytics platform built using NIFTY 100 company financial data. The project focuses on data ingestion, validation, storage, analysis, and reporting through a modular ETL pipeline.

## Sprint 1: Data Foundation

### Objective

Build a validated SQLite database from multiple financial datasets while ensuring data quality through automated validation rules.

## Project Structure

```text
financial_intelligence_platform/
│
├── data/
│   ├── raw/
│   └── supporting/
│
├── src/
│   └── etl/
│       ├── loader.py
│       ├── normaliser.py
│       └── validator.py
│
├── tests/
│   └── etl/
│
├── db/
├── output/
├── notebooks/
├── requirements.txt
└── README.md
```

## Completed Work

### Day 01 – Environment Setup

* Project structure created
* Python virtual environment configured
* Dependencies installed
* Repository initialized

### Day 02 – Excel Loader & Normaliser

* Excel loader implemented
* `normalize_year()` function implemented
* `normalize_ticker()` function implemented
* Unit tests created and passing

### Day 03 – Data Quality Validation

Implemented DQ-01 to DQ-16 validation rules:

* DQ-01 PK Uniqueness
* DQ-02 Company-Year Uniqueness
* DQ-03 Foreign Key Integrity
* DQ-04 Balance Sheet Validation
* DQ-05 OPM Cross Check
* DQ-06 Positive Sales Validation
* DQ-07 Net Cash Flow Validation
* DQ-08 Tax Rate Validation
* DQ-09 Dividend Payout Validation
* DQ-10 EPS Sign Consistency
* DQ-11 Documents FK Validation
* DQ-12 Analysis FK Validation
* DQ-13 Pros & Cons FK Validation
* DQ-14 URL Validation
* DQ-15 Duplicate Report Detection
* DQ-16 Missing Data Validation

Generated:

* `validation_failures.csv`
* Validation summary report

## Technology Stack

* Python 3.11
* Pandas
* NumPy
* Pytest
* OpenPyXL
* SQLite

## Current Sprint Status

| Day    | Status      |
| ------ | ----------- |
| Day 01 | Completed   |
| Day 02 | Completed   |
| Day 03 | Completed   |
| Day 04 | In Progress |
| Day 05 | Pending     |
| Day 06 | Pending     |
| Day 07 | Pending     |

## Next Steps

* Create SQLite schema
* Build database loader
* Load all source files
* Perform foreign key validation
* Generate load audit reports
