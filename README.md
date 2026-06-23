# Financial Intelligence Platform

## Overview

The Financial Intelligence Platform is a data engineering and analytics project built using NIFTY 100 company financial data. The platform focuses on collecting, validating, transforming, and storing financial datasets into a structured SQLite database that can later be used for analytics, reporting, dashboards, and APIs.

The project follows a sprint-based development approach with dedicated phases for data ingestion, validation, database design, quality assurance, and analytics.

---

# Sprint 1: Data Foundation

## Sprint Goal

Build a fully validated SQLite database containing financial data from multiple NIFTY 100 companies. Implement ETL pipelines, data quality checks, database schema design, and loading mechanisms to establish the foundation for analytics and reporting modules.

---

# Project Structure

```text
financial_intelligence_platform/
│
├── data/
│   ├── raw/
│   │   ├── companies.xlsx
│   │   ├── profitandloss.xlsx
│   │   ├── balancesheet.xlsx
│   │   ├── cashflow.xlsx
│   │   ├── analysis.xlsx
│   │   ├── documents.xlsx
│   │   └── prosandcons.xlsx
│   │
│   └── supporting/
│       ├── financial_ratios.xlsx
│       ├── stock_prices.xlsx
│       ├── sectors.xlsx
│       ├── peer_groups.xlsx
│       └── market_cap.xlsx
│
├── src/
│   └── etl/
│       ├── loader.py
│       ├── normaliser.py
│       └── validator.py
│
├── db/
│   ├── schema.sql
│   └── loader.py
│
├── tests/
│   └── etl/
│
├── output/
│   ├── validation_failures.csv
│   └── load_audit.csv
│
├── notebooks/
│
├── nifty100.db
├── requirements.txt
└── README.md
```

---

# Technology Stack

* Python 3.11
* Pandas
* NumPy
* SQLite
* OpenPyXL
* Pytest
* Git & GitHub

---

# Sprint 1 Progress

---

## Day 01 – Environment Setup

### Tasks Completed

* Created complete project directory structure
* Configured Python virtual environment
* Installed required dependencies
* Generated requirements.txt
* Configured environment files
* Initialized Git repository
* Connected project to GitHub repository

### Deliverables

* Project folder structure
* Virtual environment
* requirements.txt
* GitHub repository setup

---

## Day 02 – Excel Loader & Data Normalisation

### Tasks Completed

Implemented ETL components for loading Excel datasets.

### Features Developed

#### Excel Loader

* Support for Excel files using header=1
* Dynamic file loading mechanism
* Data preview and validation support

#### Data Normalisation

Implemented:

* normalize_year()
* normalize_ticker()

### Testing

Created and executed unit tests covering:

* Year normalization scenarios
* Ticker normalization scenarios
* Edge cases and invalid values

### Results

* All unit tests passed successfully
* Data loading verified for all core datasets

### Deliverables

* src/etl/loader.py
* src/etl/normaliser.py
* tests/etl/test_normaliser.py

---

## Day 03 – Data Quality Validation Framework

### Tasks Completed

Developed a comprehensive validation engine to ensure data quality before database loading.

### Implemented Validation Rules

#### Critical Rules

* DQ-01: Primary Key Uniqueness
* DQ-02: Company-Year Uniqueness
* DQ-03: Foreign Key Integrity

#### Financial Consistency Rules

* DQ-04: Balance Sheet Validation
* DQ-05: Operating Profit Margin Cross Check
* DQ-06: Positive Sales Validation
* DQ-07: Net Cash Flow Validation

#### Financial Health Rules

* DQ-08: Tax Rate Validation
* DQ-09: Dividend Payout Validation
* DQ-10: EPS Sign Consistency

#### Dataset Integrity Rules

* DQ-11: Documents Foreign Key Validation
* DQ-12: Analysis Foreign Key Validation
* DQ-13: Pros & Cons Foreign Key Validation
* DQ-14: URL Validation
* DQ-15: Duplicate Report Detection
* DQ-16: Missing Data Validation

### Outputs Generated

* validation_failures.csv
* Validation summary statistics

### Deliverables

* src/etl/validator.py
* output/validation_failures.csv

---

## Day 04 – SQLite Database Design

### Tasks Completed

Designed and implemented relational database architecture.

### Database Features

* SQLite database implementation
* Primary key constraints
* Foreign key constraints
* Referential integrity enforcement
* PRAGMA foreign_keys = ON

### Tables Created

1. companies
2. profitandloss
3. balancesheet
4. cashflow
5. analysis
6. documents
7. prosandcons
8. financial_ratios
9. stock_prices
10. sectors
11. peer_groups

### Loader Development

Implemented database loading pipeline to insert validated data into SQLite.

### Deliverables

* db/schema.sql
* db/loader.py
* nifty100.db

---

## Day 05 – Full Data Load & Audit

### Tasks Completed

Loaded all project datasets into SQLite database.

### Data Sources Loaded

#### Core Files

* companies.xlsx
* profitandloss.xlsx
* balancesheet.xlsx
* cashflow.xlsx
* analysis.xlsx
* documents.xlsx
* prosandcons.xlsx

#### Supporting Files

* financial_ratios.xlsx
* stock_prices.xlsx
* sectors.xlsx
* peer_groups.xlsx
* market_cap.xlsx

### Verification

Successfully verified:

* Database creation
* Data insertion
* Foreign key integrity
* Table population

### Audit Generation

Created load audit report containing table-level row counts.

### Deliverables

* nifty100.db
* output/load_audit.csv

---

## Day 06 – Manual Data Quality Review

### Objective

Perform manual verification of loaded data and validate database quality.

### Companies Reviewed

* ABB
* TCS
* HDFCBANK
* RELIANCE
* TATAPOWER

### Validation Performed

Verified data availability across:

* Profit & Loss
* Balance Sheet
* Cash Flow
* Financial Ratios
* Stock Prices

### Coverage Analysis

Checked:

* Historical year coverage
* Record counts per company
* Availability of financial metrics
* Data consistency across tables

### Findings

* Data available across all major tables
* Foreign key validation passed successfully
* No missing references detected
* No loader defects identified
* Database integrity maintained

### Limited History Review

Companies with limited historical coverage were identified and reviewed. The findings indicate business-specific data availability rather than ETL issues.

### Conclusion

Database quality is acceptable and suitable for Sprint 1 completion.

---

# Current Database Status

### Validation Results

* Companies Loaded: 92
* Foreign Key Check: Passed
* Data Quality Framework: Implemented
* Database Population: Completed

### Database Tables

* companies
* profitandloss
* balancesheet
* cashflow
* analysis
* documents
* prosandcons
* financial_ratios
* stock_prices
* sectors
* peer_groups

---

# Sprint Status

| Day    | Status    |
| ------ | --------- |
| Day 01 | Completed |
| Day 02 | Completed |
| Day 03 | Completed |
| Day 04 | Completed |
| Day 05 | Completed |
| Day 06 | Completed |
| Day 07 | Pending   |

---

# Next Steps

## Day 07 – Sprint Wrap-Up

Planned activities:

* Create exploratory_queries.sql
* Develop exploratory SQL queries
* Generate database insights
* Write Sprint 1 retrospective
* Review deliverables
* Complete Sprint 1 sign-off

---

# Repository

GitHub Repository:

https://github.com/bhimishettilohith/financial-intelligence-platform

---

# Author

Bhimishetti Lohith

B.Tech – Computer Science & Engineering

Sir Padampat Singhania University
