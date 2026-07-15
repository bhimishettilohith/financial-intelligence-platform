# 🚀 Sprint 1 Report

# Data Foundation

---

## Sprint Information

| Item | Details |
|------|---------|
| Sprint | Sprint 1 |
| Duration | Day 01 – Day 07 |
| Status | ✅ Completed |
| Goal | Build the complete ETL pipeline and SQLite database foundation |

---

# Sprint Objective

Sprint 1 focused on building the data engineering foundation of the Financial Intelligence Platform. The objective was to design and implement a robust ETL pipeline capable of loading multiple financial datasets, validating their quality, normalizing inconsistent formats, and storing them in a relational SQLite database.

The sprint also established coding standards, project structure, automated testing, and documentation practices that will be followed throughout the remaining development.

By the end of Sprint 1, the project had a fully functional database containing financial information for 92 NIFTY companies, ready for analytical processing in Sprint 2.

---

# Sprint Deliverables

## ETL Pipeline

- Excel Loader
- Data Normaliser
- Validation Engine
- SQLite Loader

---

## Database

- SQLite Schema
- Relational Database
- Foreign Keys
- Primary Keys

---

## Reports

- Load Audit Report
- Validation Failure Report
- Exploratory SQL Queries

---

## Testing

- Unit Tests
- Manual Validation
- Database Verification

---

# Sprint Architecture

```

Raw Excel Files

↓

Excel Loader

↓

Normalisation Engine

↓

Validation Engine

↓

SQLite Loader

↓

SQLite Database

↓

Verification

```

---

# Development Timeline

| Day | Module | Status |
|-----|--------|--------|
| Day 01 | Environment Setup | ✅ |
| Day 02 | Excel Loader | ✅ |
| Day 03 | Validation Framework | ✅ |
| Day 04 | SQLite Schema | ✅ |
| Day 05 | Data Loading | ✅ |
| Day 06 | Manual Review | ✅ |
| Day 07 | Sprint Review | ✅ |

---


# 📅 Day 01 — Environment Setup

## Objective

Establish the development environment and create a scalable project structure for the Financial Intelligence Platform.

---

## Tasks Completed

During the first day of development, the entire project repository was initialized following a modular architecture. The focus was on preparing the workspace so that future development could be organized efficiently.

The following activities were completed:

- Created the project directory structure.
- Configured a Python virtual environment.
- Installed all required Python dependencies.
- Generated the `requirements.txt` file.
- Initialized a Git repository.
- Connected the local repository with GitHub.
- Configured `.gitignore`.
- Created placeholder folders for ETL, analytics, API, dashboard, testing, reports, notebooks, and output.

---

## Deliverables

```
requirements.txt
.gitignore
Project Folder Structure
Python Virtual Environment
Git Repository
```

---

## Verification

| Check | Status |
|--------|--------|
| Virtual Environment | ✅ |
| Python Installed | ✅ |
| Dependencies Installed | ✅ |
| Git Initialized | ✅ |
| Repository Created | ✅ |

---

## Outcome

A clean and scalable project foundation was successfully established. The environment was fully prepared for ETL development in the following sprint days.

---

# 📅 Day 02 — Excel Loader & Data Normalisation

## Objective

Develop reusable ETL utilities capable of reading financial Excel files and standardizing company identifiers and financial year formats.

---

## Tasks Completed

A reusable Excel loading utility was implemented using **Pandas**, allowing datasets to be loaded consistently despite variations in formatting.

The loader supports Excel sheets where the actual header begins from the second row (`header=1`), matching the structure of the provided financial datasets.

To ensure consistent database keys, normalization functions were also implemented.

---

## Components Developed

### Excel Loader

Implemented features include:

- Reading Excel workbooks.
- Support for `header=1`.
- Automatic DataFrame creation.
- File existence validation.
- Exception handling.

---

### Data Normalisation

Implemented reusable helper functions:

- `normalize_year()`
- `normalize_ticker()`

These utilities standardize:

- Financial year formats.
- Company ticker symbols.
- Missing and inconsistent values.

---

## Testing

A dedicated unit test suite was developed to validate every normalization scenario.

The tests covered:

- Valid year formats.
- Invalid year values.
- Empty values.
- Different ticker formats.
- Edge cases.

---

## Test Result

```
PyTest Result

40 Tests Passed

0 Failed
```

---

## Deliverables

```
src/etl/loader.py

src/etl/normaliser.py

tests/etl/test_normaliser.py
```

---

## Outcome

A reusable and reliable ETL loading layer was completed. The platform could now consistently load financial datasets while ensuring standardized identifiers for downstream validation and database loading.

# 📅 Day 03 — Data Quality Validation Framework

## Objective

Develop a comprehensive validation framework to ensure that all financial datasets satisfy predefined business rules before being loaded into the SQLite database.

The primary goal was to detect inconsistent, duplicate, incomplete, or invalid records early in the ETL pipeline, thereby preventing poor-quality data from entering downstream analytics.

---

## Tasks Completed

A reusable validation engine was implemented to automatically inspect every dataset and generate detailed validation reports.

The validator performs multiple levels of checking, including structural validation, business rule verification, financial consistency checks, foreign key validation, and dataset completeness analysis.

Whenever a validation rule fails, the issue is recorded in a CSV report instead of stopping execution. This approach enables comprehensive quality reporting while allowing developers to review all issues in a single run.

---

## Validation Rules Implemented

### Primary Key & Integrity Rules

- DQ-01 – Primary Key Uniqueness
- DQ-02 – Company-Year Uniqueness
- DQ-03 – Foreign Key Validation

---

### Financial Consistency Rules

- DQ-04 – Balance Sheet Validation
- DQ-05 – Operating Profit Margin Validation
- DQ-06 – Positive Sales Validation
- DQ-07 – Net Cash Flow Validation

---

### Financial Health Rules

- DQ-08 – Tax Percentage Validation
- DQ-09 – Dividend Payout Validation
- DQ-10 – EPS Sign Consistency

---

### Dataset Quality Rules

- DQ-11 – Documents Validation
- DQ-12 – Analysis Validation
- DQ-13 – Pros & Cons Validation
- DQ-14 – URL Validation
- DQ-15 – Duplicate Report Detection
- DQ-16 – Missing Data Validation

---

## Outputs Generated

The validation engine automatically generated:

```

output/validation_failures.csv

Validation Summary Report

```

Each validation failure records:

- Dataset
- Company
- Financial Year
- Validation Rule
- Description of Failure

---

## Deliverables

```

src/etl/validator.py

output/validation_failures.csv

```

---

## Verification

Validation was executed successfully against all available datasets.

The generated report provided a complete overview of data quality issues, enabling manual review and future corrections.

---

## Outcome

A reusable Data Quality Framework was successfully integrated into the ETL pipeline. This ensures that only validated financial data proceeds to database loading, significantly improving the reliability of later analytical modules.

---

# 📅 Day 04 — SQLite Database Design

## Objective

Design and implement a normalized relational database capable of storing financial statements and supporting future analytical operations.

The database schema needed to support multiple financial datasets while maintaining referential integrity and minimizing redundancy.

---

## Tasks Completed

A complete SQLite schema was designed using relational database principles.

The implementation included:

- Primary Keys
- Foreign Keys
- Relational Constraints
- Referential Integrity
- Normalized Table Design

SQLite foreign key enforcement was enabled using:

```

PRAGMA foreign_keys = ON;

```

to ensure all relationships remain valid during data loading.

---

## Database Tables Created

The following tables were created:

| Table | Purpose |
|--------|----------|
| companies | Company master data |
| profitandloss | Income Statement |
| balancesheet | Balance Sheet |
| cashflow | Cash Flow Statement |
| analysis | Financial analysis data |
| documents | Company documents |
| prosandcons | Business strengths & weaknesses |
| financial_ratios | Ratio storage |
| stock_prices | Historical market prices |
| sectors | Sector classification |
| peer_groups | Peer company mapping |

---

## Database Relationships

The schema links financial statements using Company ID as the primary reference, allowing efficient joins across multiple years and datasets.

The relational model enables future analytical modules to retrieve data from multiple financial statements without redundancy.

---

## Deliverables

```

db/schema.sql

db/loader.py

nifty100.db

```

---

## Verification

The schema was successfully created inside SQLite.

Verification included:

- Table creation
- Foreign key validation
- Constraint validation
- Schema inspection

No structural issues were identified.

---

## Outcome

Sprint 1 now had a production-ready relational database capable of storing validated financial information and supporting future analytics, KPI calculations, and reporting modules.

# 📅 Day 05 — Full Data Load & Audit Reporting

## Objective

Populate the SQLite database with all available financial datasets and verify that every table was loaded correctly without violating database constraints.

This stage marked the completion of the ETL pipeline by transforming validated Excel datasets into a centralized relational database that would serve as the foundation for all future analytics.

---

## Tasks Completed

All core and supplementary datasets were loaded into the SQLite database using the custom database loader developed during previous days.

The loading sequence was carefully designed to preserve referential integrity by inserting master tables before dependent tables.

After loading, an audit report was automatically generated to verify successful insertion into every table.

---

## Datasets Loaded

### Core Financial Datasets

- Companies
- Profit & Loss
- Balance Sheet
- Cash Flow
- Analysis
- Documents
- Pros & Cons

---

### Supporting Datasets

- Financial Ratios
- Stock Prices
- Sectors
- Peer Groups
- Market Capitalization

---

## Validation Performed

The following checks were completed after loading:

- Successful database creation
- Table creation verification
- Row count verification
- Foreign key validation
- Duplicate record review
- Data availability across tables

---

## Outputs Generated

```
nifty100.db

output/load_audit.csv
```

The audit report contains the number of rows successfully inserted into each table, making it easy to verify database completeness.

---

## Deliverables

```
db/loader.py

nifty100.db

output/load_audit.csv
```

---

## Outcome

The SQLite database was successfully populated with financial data for all available companies. The ETL pipeline could now perform end-to-end execution from raw Excel files to a fully populated relational database.

---

# 📅 Day 06 — Manual Data Quality Review

## Objective

Perform manual verification of randomly selected companies to ensure that the loaded data accurately reflects the source datasets and that relationships between tables remain consistent.

Although automated validation was already implemented, manual inspection provides an additional layer of confidence before analytical development begins.

---

## Companies Reviewed

The following companies were selected for manual inspection:

- ABB
- TCS
- RELIANCE
- HDFCBANK
- TATAPOWER

---

## Manual Verification

For each selected company, the following tables were reviewed:

- Profit & Loss
- Balance Sheet
- Cash Flow
- Financial Ratios
- Stock Prices

---

## Checks Performed

The review focused on:

- Historical year coverage
- Record availability
- Duplicate entries
- Missing values
- Company-year consistency
- Cross-table relationships
- Financial statement continuity

---

## Findings

The manual review confirmed that:

- Financial records were successfully loaded.
- Historical coverage matched the available source data.
- Foreign key relationships remained valid.
- No ETL defects were identified.
- Data consistency was maintained across all related tables.

Companies with shorter historical records were found to reflect genuine business history rather than loading errors.

---

## Deliverables

- Manual database review
- Data quality confirmation
- ETL verification report

---

## Outcome

The manual review validated the correctness of the ETL process and confirmed that the SQLite database was ready for financial analytics development in Sprint 2.

---

# 📅 Day 07 — Sprint Review & Retrospective

## Objective

Complete Sprint 1 by validating all deliverables, reviewing implementation quality, documenting lessons learned, and preparing the project for analytical development.

---

## Tasks Completed

During the final day of Sprint 1, the following activities were completed:

- Executed exploratory SQL queries
- Verified database row counts
- Reviewed ETL pipeline
- Confirmed database integrity
- Reviewed validation reports
- Updated project documentation
- Conducted sprint retrospective

---

## Sprint Deliverables Review

| Deliverable | Status |
|-------------|--------|
| Project Structure | ✅ |
| ETL Loader | ✅ |
| Data Normalisation | ✅ |
| Validation Engine | ✅ |
| SQLite Schema | ✅ |
| Database Loader | ✅ |
| Load Audit | ✅ |
| Manual Review | ✅ |
| SQL Queries | ✅ |
| Documentation | ✅ |

---

## Sprint Statistics

| Metric | Value |
|---------|------:|
| Companies Loaded | 92 |
| Database Tables | 11 |
| Core Datasets | 7 |
| Supporting Datasets | 5 |
| Data Quality Rules | 16 |
| ETL Unit Tests | 40 Passed |
| Database | SQLite |
| Sprint Duration | 7 Days |

---

# Sprint Summary

Sprint 1 successfully established the complete data engineering foundation of the Financial Intelligence Platform.

Major accomplishments include:

- Modular ETL pipeline
- Automated validation framework
- Normalized SQLite database
- Data quality reporting
- Database audit reporting
- Unit testing framework
- Manual quality verification
- Documentation

The project is now capable of loading, validating, and storing financial data in a structured relational database, providing a reliable foundation for analytical development.

---

# Challenges Faced

During Sprint 1, several implementation challenges were encountered and resolved.

Major challenges included:

- Handling inconsistent financial year formats.
- Standardizing company identifiers.
- Designing normalized database relationships.
- Managing duplicate company-year records.
- Maintaining referential integrity.
- Creating reusable validation rules.
- Handling missing financial values gracefully.

Each challenge was addressed through modular implementation and iterative testing.

---

# Lessons Learned

Sprint 1 reinforced several important software engineering principles:

- Validate data before loading.
- Design reusable ETL components.
- Keep business logic modular.
- Build automated testing early.
- Maintain clear documentation.
- Verify database integrity before analytics.
- Separate validation from transformation.

These practices significantly improved code quality and prepared the project for future expansion.

---

# Sprint Completion Status

| Sprint | Status |
|---------|--------|
| Sprint 1 | ✅ Completed |

**Completion Date:** Sprint 1 successfully completed with all planned deliverables achieved.

---

