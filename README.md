# 📊 Financial Intelligence Platform

An End-to-End Financial Data Engineering & Analytics Platform built using Python, SQLite, and the financial statements of NIFTY 100 companies.

---

# 📖 Project Overview

The **Financial Intelligence Platform** is a comprehensive data engineering project designed to transform raw financial data into a structured, analytics-ready database capable of supporting financial analysis, screening, ranking, dashboards, and APIs.

The project uses financial statements of NIFTY 100 companies collected from multiple Excel datasets. These datasets are processed through a robust ETL (Extract, Transform, Load) pipeline where the data is cleaned, validated, normalized, and stored in a relational SQLite database.

Once the data foundation is established, the platform computes a wide range of financial Key Performance Indicators (KPIs), including profitability, leverage, efficiency, growth, and cash flow metrics. These KPIs form the foundation for company screening, financial health analysis, investment research, and business intelligence dashboards.

The project follows an **Agile Scrum** methodology, where development is divided into six sprints. Each sprint focuses on a specific module, gradually building a complete Financial Intelligence Platform similar to those used by financial institutions and investment research firms.

---

# 🎯 Project Objectives

The primary objectives of this project are:

- Build a robust ETL pipeline for loading financial datasets.
- Validate data quality using configurable business rules.
- Design a normalized SQLite database with referential integrity.
- Compute more than 50 financial KPIs across multiple years.
- Develop company screening and ranking capabilities.
- Build REST APIs for financial data access.
- Develop an interactive dashboard for financial analytics.
- Follow software engineering best practices including testing, modularity, documentation, and version control.

---

# 🚀 Key Features

### Data Engineering

- Automated Excel data ingestion
- Data normalization and standardization
- Validation using 16 Data Quality Rules
- Automated ETL pipeline
- SQLite database generation
- Audit report generation

### Financial Analytics

- Profitability Ratios
- Leverage Ratios
- Efficiency Ratios
- CAGR Engine
- Cash Flow KPIs
- Composite Quality Score
- Capital Allocation Classification

### Software Engineering

- Modular Python architecture
- Unit testing using PyTest
- Git version control
- Sprint-based development
- Comprehensive documentation
- Automated reporting

---

# 🏗️ Project Architecture

```
                   Raw Excel Files
                          │
                          ▼
                 ETL Loader & Parser
                          │
                          ▼
               Data Normalisation Layer
                          │
                          ▼
             Data Quality Validation Engine
                          │
                          ▼
                SQLite Database (11 Tables)
                          │
                          ▼
                Financial Ratio Engine
                          │
                          ▼
         Screening • Ranking • APIs • Dashboard
```

---

# 📅 Project Roadmap

| Sprint | Days | Module | Status |
|---------|------|--------|--------|
| Sprint 1 | Day 01 – Day 07 | Data Foundation & ETL | ✅ Completed |
| Sprint 2 | Day 08 – Day 14 | Financial Ratio Engine | 🟡 In Progress |
| Sprint 3 | Day 15 – Day 21 | Company Screener Engine | ⏳ Pending |
| Sprint 4 | Day 22 – Day 28 | Scoring & Ranking Engine | ⏳ Pending |
| Sprint 5 | Day 29 – Day 35 | REST API Development | ⏳ Pending |
| Sprint 6 | Day 36 – Day 42 | Dashboard & Deployment | ⏳ Pending |

---

# 📂 Current Project Structure

```text
financial_intelligence_platform/
│
├── data/
│   ├── raw/
│   └── supporting/
│
├── db/
│   ├── schema.sql
│   ├── loader.py
│   └── nifty100.db
│
├── src/
│   ├── etl/
│   ├── analytics/
│   ├── api/
│   └── dashboard/
│
├── tests/
│   ├── etl/
│   └── kpi/
│
├── reports/
│   ├── sprint1/
│   ├── sprint2/
│   ├── sprint3/
│   ├── sprint4/
│   ├── sprint5/
│   ├── sprint6/
│   └── README.md
│
├── output/
├── notebooks/
├── requirements.txt
└── README.md
```

---

# 💻 Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python 3.11 |
| Database | SQLite |
| Data Processing | Pandas, NumPy |
| Excel Processing | OpenPyXL |
| Testing | PyTest |
| Version Control | Git & GitHub |
| Future Dashboard | Streamlit |
| Future APIs | FastAPI |

---

# 📈 Current Project Statistics

| Metric | Value |
|---------|------:|
| Development Duration | 42 Days |
| Sprints | 6 |
| Sprints Completed | 1 |
| Current Sprint | Sprint 2 |
| Days Completed | 12 / 42 |
| Companies Loaded | 92 |
| Database Tables | 11 |
| Financial Records | 5,000+ |
| Financial KPIs Implemented | 20+ |
| Data Quality Rules | 16 |
| Unit Tests Passed | 48 |
| Database | SQLite |
| Status | 🟢 Active Development |

---

# 🚀 Sprint 1 — Data Foundation (Day 01 – Day 07)

## Sprint Goal

The objective of Sprint 1 was to establish a reliable data foundation for the Financial Intelligence Platform. This sprint focused on building the complete ETL pipeline, validating multiple financial datasets, designing the SQLite database schema, loading all datasets successfully, and ensuring the database was ready for analytics in subsequent sprints.

By the end of Sprint 1, the platform successfully loaded financial data for **92 NIFTY 100 companies** into a normalized SQLite database while enforcing data quality and referential integrity.

---

## Sprint Deliverables

- Complete project structure
- Python virtual environment
- ETL Loader
- Data Normalisation Engine
- Data Quality Validator
- SQLite Database Schema
- SQLite Database Loader
- Validation Reports
- Load Audit Report
- Manual Data Quality Review
- Exploratory SQL Queries
- Sprint Retrospective

---

# 📅 Day 01 — Environment Setup

## Objective

Create the development environment and initialize the project repository following a modular and scalable directory structure.

### Work Completed

The project repository was initialized using Git and organized into dedicated folders for ETL, analytics, testing, database scripts, reports, notebooks, and output files. A Python virtual environment was created to isolate dependencies and ensure reproducibility across development environments.

Required libraries were installed and documented using `requirements.txt`. Environment configuration files and Git ignore rules were added to support future development.

### Deliverables

- Project directory structure
- Virtual Environment
- requirements.txt
- .gitignore
- Git Repository Initialization

### Verification

- Python virtual environment activated successfully
- All dependencies installed without errors
- Git repository initialized successfully

**Status:** ✅ Completed

---

# 📅 Day 02 — Excel Loader & Data Normalisation

## Objective

Develop reusable ETL utilities capable of loading Excel datasets while normalizing inconsistent financial data formats.

### Work Completed

Implemented an Excel loader supporting multiple worksheets and custom header positions. Developed normalization functions to standardize company tickers and financial year formats across all datasets.

The implementation ensured that downstream database loading could rely on consistent primary keys and year representations.

### Components Developed

#### Excel Loader

- Dynamic Excel loading
- Support for `header=1`
- Automatic dataframe generation
- Error handling for missing files

#### Data Normalisation

Implemented reusable functions:

- `normalize_year()`
- `normalize_ticker()`

These functions standardize year formats and company identifiers before validation and database loading.

### Testing

A comprehensive unit test suite was written to validate normalisation logic.

**Results**

- 40 Unit Tests Passed
- No failures
- Edge cases verified

### Deliverables

- `src/etl/loader.py`
- `src/etl/normaliser.py`
- `tests/etl/test_normaliser.py`

**Status:** ✅ Completed

---

# 📅 Day 03 — Data Quality Validation Framework

## Objective

Design and implement a validation engine capable of identifying inconsistencies before data enters the database.

### Work Completed

A modular validation framework was implemented consisting of sixteen Data Quality (DQ) rules. These rules verify uniqueness, foreign key integrity, financial consistency, missing values, duplicate reports, and URL validity.

Validation results are automatically exported to a CSV report for manual review.

### Data Quality Rules

#### Critical Rules

- DQ-01 — Primary Key Uniqueness
- DQ-02 — Company-Year Uniqueness
- DQ-03 — Foreign Key Integrity

#### Financial Validation

- DQ-04 — Balance Sheet Validation
- DQ-05 — Operating Margin Cross Check
- DQ-06 — Positive Sales Validation
- DQ-07 — Net Cash Flow Validation

#### Financial Health Rules

- DQ-08 — Tax Percentage Validation
- DQ-09 — Dividend Payout Validation
- DQ-10 — EPS Consistency

#### Dataset Integrity

- DQ-11 — Documents Validation
- DQ-12 — Analysis Validation
- DQ-13 — Pros & Cons Validation
- DQ-14 — URL Validation
- DQ-15 — Duplicate Report Detection
- DQ-16 — Missing Data Validation

### Outputs Generated

- `validation_failures.csv`
- Validation summary report

### Deliverables

- `src/etl/validator.py`
- `output/validation_failures.csv`

**Status:** ✅ Completed

---

# 📅 Day 04 — SQLite Database Design

## Objective

Design a normalized relational database capable of storing financial statements and supporting future analytical modules.

### Work Completed

A complete SQLite schema was designed using primary keys, foreign keys, and relational constraints. Referential integrity was enforced using SQLite foreign key support.

The schema supports company financial statements, ratios, stock prices, sectors, and supporting metadata.

### Database Features

- Normalized relational schema
- Primary Keys
- Foreign Keys
- Referential Integrity
- PRAGMA foreign_keys = ON

### Tables Created

1. Companies
2. Profit & Loss
3. Balance Sheet
4. Cash Flow
5. Analysis
6. Documents
7. Pros & Cons
8. Financial Ratios
9. Stock Prices
10. Sectors
11. Peer Groups

### Deliverables

- `db/schema.sql`
- `db/loader.py`
- `nifty100.db`

**Status:** ✅ Completed

---

# 📅 Day 05 — Full Data Load & Audit

## Objective

Populate the SQLite database with all available financial datasets and verify successful loading.

### Work Completed

All core and supplementary datasets were successfully loaded into the SQLite database following dependency order to preserve referential integrity.

An automated load audit report was generated to verify row counts across all database tables.

### Datasets Loaded

#### Core Files

- Companies
- Profit & Loss
- Balance Sheet
- Cash Flow
- Analysis
- Documents
- Pros & Cons

#### Supporting Files

- Financial Ratios
- Stock Prices
- Sectors
- Peer Groups
- Market Capitalization

### Database Summary

| Table | Records |
|--------|--------:|
| Companies | 92 |
| Profit & Loss | 1177 |
| Balance Sheet | 1227 |
| Cash Flow | 1091 |
| Financial Ratios | 1160 |
| Stock Prices | 5520 |
| Peer Groups | 56 |

### Outputs Generated

- `nifty100.db`
- `output/load_audit.csv`

### Verification

- Database created successfully
- Foreign keys validated
- Row counts verified
- Load audit generated

**Status:** ✅ Completed

---

# 📅 Day 06 — Manual Data Quality Review

## Objective

Perform manual verification of randomly selected companies to ensure correctness of loaded financial data.

### Companies Reviewed

- ABB
- TCS
- RELIANCE
- HDFCBANK
- TATAPOWER

### Validation Performed

The following checks were completed:

- Historical year coverage
- Profit & Loss records
- Balance Sheet records
- Cash Flow records
- Financial Ratio availability
- Stock Price availability
- Foreign key consistency

### Findings

The review confirmed that data had been loaded consistently across related tables. Historical coverage was appropriate for the selected companies, and no ETL defects or referential integrity issues were identified.

Companies with shorter financial histories were reviewed separately and determined to reflect genuine business history rather than data loading problems.

### Result

Database quality was considered suitable for analytical processing in subsequent sprints.

**Status:** ✅ Completed

---

# 📅 Day 07 — Sprint Wrap-Up & Review

## Objective

Complete Sprint 1 by validating the database, writing exploratory SQL queries, reviewing deliverables, and documenting sprint outcomes.

### Work Completed

- Created exploratory SQL queries
- Verified database row counts
- Confirmed foreign key integrity
- Executed ETL unit tests
- Reviewed Sprint 1 deliverables
- Documented sprint retrospective

### Validation Summary

- Companies Loaded: **92**
- SQLite Database: **Created Successfully**
- ETL Unit Tests: **40 Passed**
- Foreign Key Check: **Passed**
- Data Quality Framework: **16 Rules Implemented**

### Deliverables

- `notebooks/exploratory_queries.sql`
- Sprint 1 Retrospective
- Updated Project Documentation

**Status:** ✅ Completed

---

# ✅ Sprint 1 Summary

Sprint 1 established the complete data engineering foundation of the Financial Intelligence Platform. By the end of the sprint, all datasets had been successfully validated, transformed, and loaded into SQLite. A comprehensive validation framework, automated ETL pipeline, relational database schema, audit reporting mechanism, and unit testing suite were completed successfully.

This sprint provides the stable foundation required for the Financial Ratio Engine and subsequent analytical modules implemented in later sprints.

# 🚀 Sprint 2 — Financial Ratio Engine (Day 08 – Day 14)

## Sprint Goal

The objective of Sprint 2 is to build a comprehensive Financial Ratio Engine capable of computing more than **50 financial Key Performance Indicators (KPIs)** for every company across all available financial years.

The sprint extends the ETL pipeline developed in Sprint 1 by transforming raw financial statement data into meaningful analytical metrics. These KPIs serve as the foundation for company screening, scoring, ranking, investment analysis, and dashboard visualizations in later sprints.

The implementation focuses on profitability analysis, leverage measurement, efficiency metrics, growth calculations using CAGR, cash flow analytics, and automated ratio population into the SQLite database.

---

## Sprint Deliverables

- Profitability Ratio Engine
- Leverage & Efficiency Ratio Engine
- CAGR Engine
- Cash Flow KPI Engine
- Capital Allocation Classification
- Financial Ratio Population Engine
- SQLite Ratio Table
- KPI Unit Tests
- Manual Validation Reports
- Ratio Edge Case Logging (Upcoming)

---

# 📅 Day 08 — Profitability Ratio Engine

## Objective

Develop reusable analytical functions capable of calculating profitability ratios for every company-year combination while handling financial edge cases such as zero sales and negative equity.

---

### Work Completed

A dedicated analytics module (`ratios.py`) was developed containing reusable financial ratio functions. These functions are independent of the ETL process and can be reused by APIs, dashboards, screeners, and reporting modules.

Special attention was given to handling missing values and division-by-zero scenarios to ensure that invalid calculations do not interrupt execution.

---

### Financial Ratios Implemented

#### Net Profit Margin (NPM)

Measures the percentage of profit generated from revenue.

Formula:

```
Net Profit / Sales × 100
```

Edge Cases

- Sales = 0 → Returns None

---

#### Operating Profit Margin (OPM)

Measures operating profitability before taxes and financing costs.

Formula

```
Operating Profit / Sales × 100
```

Additional Validation

Computed OPM is cross-checked against the source dataset. Differences greater than 1% are treated as validation mismatches.

---

#### Return on Equity (ROE)

Measures profitability generated using shareholders' equity.

Formula

```
Net Profit / (Equity Capital + Reserves) × 100
```

Edge Cases

- Negative Equity
- Zero Equity

Returns None whenever denominator is invalid.

---

#### Return on Capital Employed (ROCE)

Formula

```
EBIT / Capital Employed × 100
```

where

```
Capital Employed =
Equity + Reserves + Borrowings
```

The implementation also prepares the platform for Financial Sector specific benchmarks which will be expanded during Day 13.

---

#### Return on Assets (ROA)

Formula

```
Net Profit / Total Assets × 100
```

Edge Cases

- Total Assets = 0

Returns None.

---

### Unit Testing

Comprehensive test cases were written covering

- Standard calculations
- Zero denominator
- Negative equity
- Missing values
- OPM cross validation

All implemented ratio functions behaved as expected.

---

### Deliverables

```
src/analytics/ratios.py
tests/kpi/test_ratios.py
```

**Status:** ✅ Completed

---

# 📅 Day 09 — Leverage & Efficiency Ratio Engine

## Objective

Implement leverage and operational efficiency metrics to evaluate company solvency and capital utilization.

---

### Work Completed

Additional reusable functions were integrated into the Ratio Engine for debt analysis and operational efficiency measurement.

These functions also include business-specific logic for Financial Sector companies where leverage behaves differently compared to manufacturing and service industries.

---

### Financial Ratios Implemented

#### Debt-to-Equity Ratio

Formula

```
Borrowings /
(Equity Capital + Reserves)
```

Special Handling

- Borrowings = 0

Returns

```
0
```

instead of None.

---

#### High Leverage Flag

Companies with

```
Debt-to-Equity > 5
```

are automatically flagged.

Financial Sector companies are excluded from this warning because higher leverage is structurally normal.

---

#### Interest Coverage Ratio (ICR)

Formula

```
(Operating Profit + Other Income)
/ Interest
```

Edge Cases

Interest = 0

Returns

```
None
```

and assigns

```
Debt Free
```

as the display label.

---

#### Net Debt

Formula

```
Borrowings − Investments
```

Investments are treated as liquid assets.

---

#### Asset Turnover Ratio

Formula

```
Sales / Total Assets
```

Edge Cases

- Total Assets = 0

Returns None.

---

### Unit Testing

Validation included

- Debt-free companies
- High leverage scenarios
- Zero interest
- Asset turnover calculations

---

### Deliverables

```
src/analytics/ratios.py
tests/kpi/test_leverage.py
```

**Status:** ✅ Completed

---

# 📅 Day 10 — CAGR Growth Engine

## Objective

Develop a reusable Compound Annual Growth Rate (CAGR) engine capable of calculating long-term financial growth while handling multiple financial edge cases.

---

### Work Completed

A dedicated CAGR engine (`cagr.py`) was implemented to calculate Revenue, PAT, and EPS growth over multiple historical periods.

Unlike simple percentage growth, CAGR provides a normalized annualized growth rate that is more meaningful for long-term financial analysis.

---

### Growth Metrics

Implemented for

- Revenue
- Net Profit (PAT)
- Earnings Per Share (EPS)

Supported Windows

- 3 Year
- 5 Year
- 10 Year

---

### CAGR Formula

```
((Ending Value / Starting Value)
^(1 / Years) − 1)
× 100
```

---

### Edge Cases Handled

- Positive → Positive
- Positive → Negative
- Negative → Positive
- Negative → Negative
- Zero Base
- Insufficient Historical Data

Each edge case generates an associated flag to support downstream analytics.

---

### Deliverables

```
src/analytics/cagr.py
tests/kpi/test_cagr.py
```


# 📅 Day 11 — Cash Flow KPIs & Capital Allocation

## Objective

Develop advanced cash flow analytics capable of evaluating the quality of business operations, capital expenditure behaviour, free cash flow generation, and overall capital allocation strategy.

Unlike profitability ratios, cash flow metrics provide insight into how effectively a company generates and utilizes cash. These indicators are essential for identifying financially strong businesses that consistently convert accounting profits into actual cash flows.

---

### Work Completed

A dedicated analytics module (`cashflow_kpis.py`) was developed containing reusable functions for calculating operational cash flow metrics and identifying capital allocation patterns.

The implementation includes financial classifications that simplify interpretation of complex cash flow statements and prepares the platform for future screening and ranking modules.

---

### KPIs Implemented

#### Free Cash Flow (FCF)

Free Cash Flow represents the cash generated after accounting for investments made in business assets.

Formula

```
Free Cash Flow = Operating Cash Flow + Investing Cash Flow
```

Negative Free Cash Flow is considered a valid outcome because expanding businesses often invest heavily in long-term assets.

---

#### CFO Quality Score

Measures the quality of reported earnings by comparing cash generated from operations with accounting profit.

Formula

```
Operating Cash Flow
-------------------
Net Profit (PAT)
```

Classification

| Ratio | Classification |
|--------|----------------|
| > 1.0 | High Quality |
| 0.5 – 1.0 | Moderate |
| < 0.5 | Accrual Risk |

Companies with higher ratios generally demonstrate stronger earnings quality.

---

#### CapEx Intensity

Measures how aggressively a company invests in long-term assets relative to its sales.

Formula

```
|Investing Cash Flow|
----------------------
Sales
× 100
```

Classification

| CapEx % | Category |
|----------|----------|
| <3% | Asset Light |
| 3–8% | Moderate |
| >8% | Capital Intensive |

---

#### Free Cash Flow Conversion

Evaluates the proportion of operating profit converted into free cash flow.

Formula

```
Free Cash Flow
------------------
Operating Profit
×100
```

Edge Case

Operating Profit = 0

Returns None.

---

### Capital Allocation Engine

An automated classification engine was developed to categorize companies based on the signs of their operating, investing, and financing cash flows.

The implemented classifications include:

| Cash Flow Pattern | Classification |
|-------------------|----------------|
| (+,-,-) | Reinvestor |
| (+,-,-) + High CFO/PAT | Shareholder Returns |
| (+,+,-) | Liquidating Assets |
| (-,+,+) | Distress Signal |
| (-,-,+) | Growth Funded by Debt |
| (+,+,+) | Cash Accumulator |
| (-,-,-) | Pre-Revenue |
| (+,-,+) | Mixed |
| Other | Other |

---

### Outputs Generated

The engine automatically generates

```
output/capital_allocation.csv
```

containing

- Company ID
- Financial Year
- CFO Sign
- CFI Sign
- CFF Sign
- Pattern Classification

A total of **1103 company-year records** were successfully classified.

---

### Deliverables

```
src/analytics/cashflow_kpis.py
src/analytics/generate_capital_allocation.py
output/capital_allocation.csv
```

**Status:** ✅ Completed

---

# 📅 Day 12 — Financial Ratio Population Engine

## Objective

Integrate all analytical modules developed during Sprint 2 into a unified Financial Ratio Engine capable of computing KPIs for every available company-year record and storing the results in SQLite.

This marks the transition from individual analytical functions to a complete financial analytics pipeline.

---

### Work Completed

A comprehensive ratio population engine (`populate_financial_ratios.py`) was developed to combine data from multiple financial statement tables and compute analytical metrics automatically.

The pipeline performs the following operations:

1. Connects to SQLite database.
2. Loads all required financial tables.
3. Removes duplicate company-year records.
4. Merges Profit & Loss, Balance Sheet, Cash Flow, Company, and Sector data.
5. Computes all implemented KPIs.
6. Calculates five-year CAGR metrics.
7. Generates a Composite Quality Score.
8. Stores computed results back into SQLite.

---

### KPIs Generated

The Financial Ratio Engine currently computes:

#### Profitability

- Net Profit Margin
- Operating Profit Margin
- Return on Equity
- Return on Capital Employed
- Return on Assets

#### Leverage

- Debt to Equity
- Interest Coverage Ratio
- Net Debt
- High Leverage Flag

#### Efficiency

- Asset Turnover

#### Cash Flow

- Free Cash Flow
- CFO Quality Score
- CapEx Intensity
- Free Cash Flow Conversion

#### Growth

- Revenue CAGR (5-Year)
- PAT CAGR (5-Year)
- EPS CAGR (5-Year)

#### Quality

- Composite Quality Score

---

### Database Processing Summary

During execution the engine successfully

- Loaded all financial tables
- Removed duplicate records
- Merged financial datasets
- Computed analytical KPIs
- Generated quality scores
- Populated SQLite output table

---

### Execution Results

| Metric | Value |
|---------|------:|
| Companies | 92 |
| Profit & Loss Records | 1177 |
| Balance Sheet Records | 1227 |
| Cash Flow Records | 1091 |
| Computed Ratio Records | **1177** |
| SQLite Population | Successful |

---

### Sample Output

Example computed metrics include

| Company | ROE | Debt/Equity | Revenue CAGR | Composite Score |
|---------|----:|------------:|-------------:|----------------:|
| ABB | 22.41 | 0.00 | 14.81% | 100 |
| ABB | 23.69 | 0.00 | 14.81% | 80 |
| ABB | 28.33 | 0.05 | 11.10% | 100 |

---

### Verification

The Financial Ratio Engine successfully produced

- **1177 computed company-year records**
- SQLite population completed successfully
- Revenue CAGR calculations verified
- Composite scores generated
- Manual spot checks completed for sample companies

The implementation satisfies the Sprint 2 requirement of generating more than **1100 analytical records**.

---

### Deliverables

```
src/analytics/populate_financial_ratios.py
computed_financial_ratios (SQLite)
```

**Status:** ✅ Completed

---

# 📊 Current Project Status

## Completed Sprints

| Sprint | Status |
|---------|--------|
| Sprint 1 – Data Foundation | ✅ Completed |
| Sprint 2 – Financial Ratio Engine | 🟡 5 of 7 Days Completed (Day 08–12) |

---

## Overall Progress

| Item | Progress |
|------|----------|
| Project Duration | 12 / 42 Days |
| Sprints Completed | 1 |
| Current Sprint | Sprint 2 |
| Companies Loaded | 92 |
| Database Tables | 11 |
| Company-Year Financial Records | 1177 |
| KPIs Implemented | 20+ |
| Data Quality Rules | 16 |
| Unit Tests | 48+ Passed |
| SQLite Database | Operational |
| Financial Ratio Engine | Operational |

---

# 🚀 Upcoming Work

The remaining work for Sprint 2 includes:

## Day 13

- Bank ROCE carve-out
- ROCE anomaly detection
- ROE anomaly detection
- Ratio edge case logging
- Edge case categorisation

## Day 14

- KPI formula validation
- Full test execution
- Manual verification
- Sprint retrospective
- Documentation updates
- Sprint review and sign-off

---

# 👨‍💻 Author

**Bhimishetti Lohith**

B.Tech – Computer Science & Engineering

Sir Padampat Singhania University

---

# ⭐ Repository

**GitHub Repository**

https://github.com/bhimishettilohith/financial-intelligence-platform


---

# 📊 Outputs Generated

Throughout the first two sprints, the project generates several reports, database artifacts, and analytical outputs. These outputs serve as verification evidence for successful ETL execution, data validation, and financial ratio computation.

## Sprint 1 Outputs

| Output | Description |
|---------|-------------|
| `nifty100.db` | SQLite database containing normalized financial data |
| `load_audit.csv` | Table-wise record count generated after database loading |
| `validation_failures.csv` | Data quality violations identified during ETL validation |
| `exploratory_queries.sql` | SQL queries used for manual database verification |
| ETL Unit Tests | Validation of normalization and loader functions |

---

## Sprint 2 Outputs

| Output | Description |
|---------|-------------|
| `capital_allocation.csv` | Company-wise capital allocation classification |
| `computed_financial_ratios` | SQLite table containing calculated financial KPIs |
| Financial Ratio Engine | Automated KPI computation for every company-year |
| CAGR Engine | Revenue, PAT and EPS growth calculations |
| Composite Quality Score | Overall financial quality score for each company |

---

# 🗂 Database Overview

The SQLite database currently contains the following major tables.

| Table | Purpose |
|---------|----------|
| companies | Company master information |
| profitandloss | Income Statement |
| balancesheet | Balance Sheet |
| cashflow | Cash Flow Statement |
| analysis | Additional financial analysis |
| documents | Company reports and documents |
| prosandcons | Business strengths and weaknesses |
| financial_ratios | Source financial ratios |
| stock_prices | Historical stock prices |
| sectors | Sector classification |
| peer_groups | Comparable companies |

All tables are linked using relational constraints to maintain referential integrity.

---

# 🧪 Testing & Validation

Testing has been an integral part of every sprint to ensure correctness and reliability.

## ETL Validation

- Header normalization
- Year normalization
- Company ticker normalization
- Duplicate detection
- Foreign key validation
- Missing value validation

---

## KPI Validation

Financial ratio functions were tested for:

- Division by zero
- Missing values
- Negative equity
- Zero borrowings
- Debt-free companies
- CAGR edge cases
- Cash flow classifications

---

## Current Test Summary

| Test Category | Status |
|---------------|--------|
| ETL Unit Tests | ✅ Passed |
| KPI Formula Tests | ✅ Passed |
| Database Validation | ✅ Passed |
| Foreign Key Validation | ✅ Passed |
| Manual Spot Check | ✅ Completed |

---

# 📈 Current Project Statistics

| Metric | Value |
|---------|-------|
| Project Days Completed | 12 / 42 |
| Sprint Completed | 1 |
| Current Sprint | Sprint 2 |
| Companies | 92 |
| Financial Statement Records | 1177 |
| Database Tables | 11 |
| KPIs Implemented | 20+ |
| Data Quality Rules | 16 |
| Unit Tests Passing | 48+ |
| SQLite Database Size | Growing |
| Programming Language | Python 3.11 |

---

# 📌 Folder Description

The repository follows a modular architecture.

| Folder | Purpose |
|---------|----------|
| `src/etl` | ETL Pipeline |
| `src/analytics` | Financial Ratio Engine |
| `src/api` | Future REST APIs |
| `src/dashboard` | Future Dashboard |
| `tests` | Unit Testing |
| `db` | SQLite Schema & Loader |
| `reports` | Sprint Reports |
| `output` | Generated Reports |
| `data` | Raw & Supporting Datasets |

---

# 🚀 Future Roadmap

## Sprint 3

Company Screener Engine

- Multi-filter screening
- Dynamic SQL builder
- Industry comparison
- Market capitalization filters

---

## Sprint 4

Scoring Engine

- Composite Quality Score
- Ranking algorithm
- Investment score
- Financial health classification

---

## Sprint 5

REST APIs

- Company API
- Ratio API
- Screener API
- Ranking API
- Swagger Documentation

---

## Sprint 6

Dashboard & Deployment

- Streamlit Dashboard
- Interactive Charts
- Company Comparison
- Financial Trends
- Deployment
- Final Documentation

---

# 🎯 Learning Outcomes

This project demonstrates practical implementation of:

- Data Engineering
- ETL Pipeline Design
- Data Validation Frameworks
- Relational Database Design
- Financial Statement Analysis
- Financial Ratio Computation
- Software Engineering Practices
- Unit Testing
- Git Version Control
- Agile Scrum Methodology

---