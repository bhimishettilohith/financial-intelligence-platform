# 📊 Financial Intelligence Platform

> **An end-to-end financial analytics platform for the NIFTY 100 universe, combining data engineering, financial analysis, machine learning, REST APIs, interactive dashboards, and automated reporting.**


## 🚀 Overview

The **Financial Intelligence Platform** is a comprehensive financial analytics system designed to transform raw financial statement data into actionable investment intelligence.

The platform automates the complete workflow from data ingestion and validation to financial ratio computation, company screening, peer benchmarking, cash flow intelligence, valuation analysis, report generation, REST API services, and interactive dashboards.

Built using a modular architecture, the project processes financial data for **92 NIFTY 100 companies**, generates investment insights, produces analyst-ready PDF reports, exposes RESTful APIs using FastAPI, and provides interactive visualisations through Streamlit.

The project was developed incrementally across **six development sprints**, with each sprint introducing new analytical capabilities and extending the platform into a production-style financial analysis solution.

## 📈 Project Highlights

| Feature | Details |
|---------|---------|
| 📊 Companies Analysed | 92 NIFTY 100 Companies |
| 📄 Raw Data Sources | 12 Financial Datasets |
| 🗄 Database | SQLite |
| 📉 Financial Ratio Engine | 25+ Financial Metrics |
| 🔍 Investment Screeners | 6 Preset Screeners + Custom Filters |
| 🤝 Peer Groups | 11 Industry Peer Groups |
| 📊 Radar Charts | Company vs Peer Comparison |
| 💰 Cash Flow Intelligence | CFO Quality, CapEx, Distress Detection |
| 🤖 NLP Engine | Automated Pros & Cons Generation |
| 📑 Company Reports | 92 Two-Page PDF Tearsheets |
| 🏢 Sector Reports | 11 Sector Summary PDFs |
| 📚 Portfolio Reports | Portfolio Summary PDF |
| 🌐 REST API | FastAPI with OpenAPI Documentation |
| 📊 Dashboard | Interactive Streamlit Dashboard |
| 🧪 Testing | Unit, API and Performance Tests |
| 🏗 Development Model | Agile (6 Sprints) |

---

# 🏗️ System Architecture

The Financial Intelligence Platform follows a **modular, layered architecture**, where each component has a well-defined responsibility. The workflow begins with raw financial datasets, passes through ETL and validation, stores processed data in SQLite, and builds multiple analytical layers before exposing the results through reports, REST APIs, and an interactive dashboard.

```text
                              ┌─────────────────────────────┐
                              │   Raw Financial Datasets    │
                              │ (Excel Files - 12 Sources)  │
                              └──────────────┬──────────────┘
                                             │
                                             ▼
                             ┌────────────────────────────────┐
                             │       ETL & Data Pipeline       │
                             │--------------------------------│
                             │ • Excel Loader                 │
                             │ • Data Normalisation           │
                             │ • Schema Validation            │
                             │ • Data Quality Rules           │
                             └──────────────┬─────────────────┘
                                            │
                                            ▼
                              ┌──────────────────────────────┐
                              │       SQLite Database         │
                              │------------------------------│
                              │ Companies                    │
                              │ Profit & Loss                │
                              │ Balance Sheet                │
                              │ Cash Flow                    │
                              │ Financial Ratios             │
                              │ Peer Percentiles             │
                              │ Capital Allocation           │
                              └──────────────┬───────────────┘
                                             │
            ┌────────────────────────────────┼─────────────────────────────────┐
            │                                │                                 │
            ▼                                ▼                                 ▼
 ┌──────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
 │ Financial Analytics  │      │ Investment Analytics   │      │ NLP Intelligence       │
 │----------------------│      │------------------------│      │------------------------│
 │ Ratio Engine         │      │ Screener Engine        │      │ Analysis Parser        │
 │ CAGR Engine          │      │ Composite Scoring      │      │ Pros & Cons Generator  │
 │ Valuation Engine     │      │ Peer Analytics         │      │ Confidence Scoring     │
 │ Cash Flow KPIs       │      │ Radar Charts           │      │                        │
 │ Capital Allocation   │      │ Clustering             │      │                        │
 └──────────┬───────────┘      └──────────┬─────────────┘      └──────────┬─────────────┘
            │                              │                               │
            └───────────────┬──────────────┴───────────────┬───────────────┘
                            ▼                              ▼
                 ┌──────────────────────┐       ┌──────────────────────┐
                 │ Reporting Engine     │       │ REST API             │
                 │----------------------│       │----------------------│
                 │ Company Tearsheets   │       │ FastAPI              │
                 │ Sector Reports       │       │ OpenAPI Docs         │
                 │ Portfolio Summary    │       │ JSON Endpoints       │
                 └──────────┬───────────┘       └──────────┬───────────┘
                            │                              │
                            └──────────────┬───────────────┘
                                           ▼
                              ┌────────────────────────────┐
                              │ Streamlit Dashboard        │
                              │----------------------------│
                              │ Company Profile            │
                              │ Screener                  │
                              │ Peer Analysis             │
                              │ Sector Dashboard          │
                              │ Trends & KPIs             │
                              │ Reports                  │
                              └────────────────────────────┘
```

---

# ⚙️ Project Workflow

The Financial Intelligence Platform follows an end-to-end analytics workflow consisting of six major stages.

### Stage 1 — Data Ingestion

Financial statement data is collected from multiple Excel workbooks covering company fundamentals, balance sheets, profit and loss statements, cash flow statements, market capitalisation, sector mappings, peer groups, and supporting datasets.

---

### Stage 2 — ETL & Data Quality

The ETL pipeline performs:

- Excel loading
- Data normalisation
- Schema validation
- Duplicate detection
- Missing value checks
- Data quality validation
- SQLite loading

Validated data is then stored in the central SQLite database.

---

### Stage 3 — Financial Analytics

The analytics engine computes:

- Profitability Ratios
- Liquidity Ratios
- Leverage Ratios
- Growth Metrics
- CAGR Calculations
- Valuation Metrics
- Cash Flow Intelligence
- Capital Allocation Patterns

These metrics form the analytical foundation used throughout the platform.

---

### Stage 4 — Investment Intelligence

Using the computed financial metrics, the platform performs:

- Investment Screening
- Composite Quality Scoring
- Peer Percentile Ranking
- Radar Chart Comparison
- Company Clustering
- NLP-based Investment Insights

This transforms raw financial data into actionable investment intelligence.

---

### Stage 5 — Reporting & APIs

Analytical outputs are converted into multiple formats:

- Company PDF Tearsheets
- Sector Reports
- Portfolio Summary Reports
- Excel Reports
- CSV Exports
- FastAPI REST Endpoints

---

### Stage 6 — Interactive Visualisation

The Streamlit dashboard provides an interactive interface for:

- Exploring company financials
- Running custom investment screeners
- Comparing peer companies
- Analysing financial trends
- Viewing reports
- Accessing generated insights

This enables analysts to interact with the platform without directly querying the database.

---

# ✨ Core Features

The Financial Intelligence Platform is organised into modular components, each responsible for a specific stage of the financial analysis workflow. This modular architecture improves maintainability, scalability, and code reusability while allowing independent development of analytical features.

---

## 📥 ETL & Data Processing

The ETL (Extract, Transform, Load) pipeline forms the foundation of the platform by converting raw Excel datasets into a clean, validated SQLite database.

### Key Capabilities

- Import financial data from multiple Excel workbooks
- Standardise company names and financial years
- Validate schema consistency across datasets
- Perform Data Quality (DQ) checks
- Detect duplicate and missing records
- Generate validation and load audit reports
- Populate the central SQLite database

**Modules**

```
src/etl/
├── loader.py
├── normaliser.py
└── validator.py
```

---

## 🗄️ SQLite Data Warehouse

A central SQLite database stores validated financial data and analytical outputs, providing a single source of truth for all platform modules.

### Database Contents

- Company Information
- Profit & Loss Statements
- Balance Sheets
- Cash Flow Statements
- Financial Ratios
- Peer Percentiles
- Capital Allocation Data
- Supporting Reference Data

The database enables efficient querying by the analytics engine, dashboard, and REST API.

---

## 📈 Financial Analytics Engine

The analytics engine transforms raw financial statements into meaningful investment metrics.

### Features

- Financial Ratio Computation
- CAGR Calculations
- Growth Analysis
- Profitability Analysis
- Liquidity Analysis
- Leverage Analysis
- Valuation Metrics
- Financial Health Indicators

### Analytical Modules

```
src/analytics/

ratios.py
cagr.py
valuation.py
scoring.py
populate_financial_ratios.py
```

---

## 💰 Cash Flow Intelligence

One of the platform's key analytical capabilities is the Cash Flow Intelligence module, which evaluates cash generation quality beyond traditional financial ratios.

### Generated Insights

- CFO Quality Score
- Free Cash Flow Analysis
- CapEx Intensity
- Free Cash Flow Conversion
- Distress Signal Detection
- Deleveraging Detection
- Capital Allocation Classification

### Outputs

- Cash Flow Intelligence Report
- Distress Alerts
- Capital Allocation Summary
- Pattern Change Report

---

## 🔍 Financial Screener

The screener enables investors and analysts to identify companies matching predefined or custom investment criteria.

### Features

- Configurable threshold filtering
- Six predefined investment strategies
- Analyst-editable YAML configuration
- Composite Quality Score
- Sector-aware filtering
- Custom screening support

### Preset Screeners

- Quality Compounder
- Value Pick
- Growth Accelerator
- Dividend Champion
- Debt-Free Blue Chip
- Turnaround Watch

---

## 🤝 Peer Analytics Engine

The peer engine benchmarks companies against industry peers using percentile-based ranking.

### Capabilities

- Peer Group Mapping
- Percentile Rankings
- Sector Benchmarking
- Composite Ranking
- Radar Chart Generation
- Comparative Analysis

The module supports multiple financial metrics, allowing analysts to compare company performance within the same industry.

---

## 🤖 Natural Language Processing (NLP)

The NLP module converts structured financial metrics into readable investment insights.

### Components

- Analysis Text Parser
- Automated Pros Generator
- Automated Cons Generator
- Confidence Scoring
- Rule-Based Financial Commentary

The generated insights provide explainable investment observations based on company financial performance.

---

## 📄 Automated Reporting Engine

The reporting engine generates analyst-ready documents in PDF format.

### Reports Generated

- Company Tearsheets
- Sector Reports
- Portfolio Summary Report

Each report combines financial metrics, visualisations, and NLP-generated commentary into a professional presentation.

---

## 📊 Interactive Dashboard

The Streamlit dashboard provides a user-friendly interface for exploring financial data and analytical outputs.

### Dashboard Pages

- Home
- Company Profile
- Financial Screener
- Peer Comparison
- Financial Trends
- Sector Analytics
- Capital Allocation
- Reports

The dashboard enables users to explore insights without directly interacting with the database.

---

## 🌐 REST API

The FastAPI backend exposes platform functionality through RESTful endpoints.

### API Features

- Company Information
- Financial Statements
- Ratio Data
- Sector Analytics
- Investment Screener
- Peer Comparison
- Health Check
- Portfolio Statistics

Interactive API documentation is automatically generated using the OpenAPI specification.

---

## 📊 Data Visualisation

The platform includes multiple visualisation techniques for financial analysis.

### Charts

- Revenue Trends
- Profit Trends
- ROE vs ROCE
- Radar Charts
- Correlation Heatmaps
- Elbow Curve
- Portfolio Statistics
- Balance Sheet Composition
- Cash Flow Waterfall Charts

Visualisations are used throughout reports and the Streamlit dashboard.

---

## 🧪 Testing & Quality Assurance

Testing was integrated throughout the development lifecycle to ensure correctness and reliability.

### Test Coverage

- ETL Validation
- KPI Calculations
- CAGR Engine
- Cash Flow Analytics
- REST API
- Screener Engine
- Performance Tests

The project includes dedicated unit, integration, and performance testing modules to validate analytical correctness and system stability.

---

# 📦 Feature Summary

| Module | Primary Function |
|---------|------------------|
| ETL Pipeline | Data ingestion, validation, and loading |
| SQLite Database | Central financial data repository |
| Analytics Engine | Financial ratio and KPI computation |
| Screener | Investment filtering and ranking |
| Peer Analytics | Industry benchmarking |
| Cash Flow Intelligence | Cash flow quality and capital allocation analysis |
| NLP Engine | Automated financial commentary |
| Reporting Engine | PDF report generation |
| Dashboard | Interactive visual analytics |
| REST API | Programmatic data access |
| Testing | Validation and quality assurance |

---

# 📁 Project Structure

The project follows a modular architecture that separates data engineering, analytics, reporting, APIs, dashboard development, and testing into independent components. This organisation improves maintainability, scalability, and ease of future enhancements.

```
FINANCIAL_INTELLIGENCE_PLATFORM/
│
├── config/
│   └── screener_config.yaml          # Configurable screener thresholds
│
├── data/
│   ├── raw/                          # Raw financial datasets
│   ├── supporting/                   # Supporting reference datasets
│   └── nifty100.db                   # SQLite database
│
├── db/
│   ├── loader.py                     # Database loader
│   └── schema.sql                    # Database schema
│
├── docs/
│   └── openapi.json                  # OpenAPI specification
│
├── notebooks/
│   └── exploratory_queries.sql       # SQL exploration queries
│
├── output/
│   ├── reports/
│   ├── portfolio/
│   ├── sector/
│   ├── tearsheets/
│   ├── analysis_parsed.csv
│   ├── cashflow_intelligence.xlsx
│   ├── peer_comparison.xlsx
│   ├── screener_output.xlsx
│   ├── valuation_summary.xlsx
│   └── ... additional generated outputs
│
├── reports/
│   ├── assets/
│   ├── radar_charts/
│   ├── sprint1/
│   ├── sprint2/
│   ├── sprint3/
│   ├── sprint4/
│   ├── sprint5/
│   ├── sprint6/
│   ├── cluster_profile.csv
│   ├── correlation_heatmap.png
│   ├── elbow_plot.png
│   └── pytest_report.html
│
├── src/
│   ├── analytics/
│   ├── api/
│   ├── dashboard/
│   ├── db/
│   ├── etl/
│   ├── nlp/
│   ├── reports/
│   └── screener/
│
├── tests/
│   ├── api/
│   ├── etl/
│   ├── kpi/
│   └── performance/
│
├── requirements.txt
├── Makefile
├── README.md
└── .gitignore
```

---

# 📂 Directory Overview

| Directory | Purpose |
|------------|---------|
| **config/** | Configuration files including analyst-editable screener thresholds |
| **data/** | Raw datasets, supporting datasets, and SQLite database |
| **db/** | Database schema definition and loading utilities |
| **docs/** | API documentation and project documentation |
| **notebooks/** | SQL queries and exploratory analysis scripts |
| **output/** | Generated CSV, Excel, and PDF outputs produced by the platform |
| **reports/** | Sprint documentation, visualisations, and testing reports |
| **src/** | Complete application source code |
| **tests/** | Unit, API, integration, and performance tests |

---

# 🏛 Source Code Organisation

The application source code is organised into specialised modules.

| Module | Responsibility |
|---------|----------------|
| **analytics/** | Financial ratios, CAGR, valuation, cash flow intelligence, clustering, peer analytics, radar charts |
| **api/** | FastAPI application, routers, and service layer |
| **dashboard/** | Streamlit application and dashboard pages |
| **db/** | Database helper utilities |
| **etl/** | Data extraction, validation, and normalisation |
| **nlp/** | Financial text parsing and automated pros & cons generation |
| **reports/** | PDF tearsheets, sector reports, portfolio reports |
| **screener/** | Investment screening engine and preset filters |

---

# 📊 Generated Outputs

The platform automatically generates a wide range of analytical outputs.

### Excel Reports

- Financial Screener Results
- Peer Comparison Report
- Cash Flow Intelligence Report
- Valuation Summary

### CSV Reports

- Parsed Analysis Data
- Pros & Cons
- Distress Alerts
- Portfolio Statistics
- Capital Allocation
- Cluster Labels
- Pattern Changes
- Validation Reports
- Load Audit
- Outlier Detection

### PDF Reports

- Company Tearsheets
- Sector Reports
- Portfolio Summary

### Visualisations

- Radar Charts
- Correlation Heatmap
- Elbow Plot
- Dashboard Charts

---

# 🧪 Testing Structure

Testing is organised by functional area to ensure modular validation and maintainability.

```
tests/

├── api/
│   ├── test_companies.py
│   ├── test_health.py
│   ├── test_screener.py
│   └── test_sectors.py
│
├── etl/
│   └── test_normaliser.py
│
├── kpi/
│   ├── test_cagr.py
│   ├── test_cashflow.py
│   ├── test_leverage.py
│   └── test_ratios.py
│
└── performance/
    ├── test_load.py
    └── test_profile_speed.py
```

The testing framework validates data quality, financial calculations, API endpoints, KPI accuracy, and system performance throughout the platform.

---

# 🗄️ Database Design & Data Model

The Financial Intelligence Platform uses **SQLite** as its central analytical data warehouse. After passing through the ETL pipeline, validated financial data is stored in a structured relational database that serves as the single source of truth for all analytics, reporting, APIs, and dashboard components.

The database has been designed to minimise redundancy while maintaining efficient querying for financial analysis.

---

# 🏛 Database Architecture

```
                    +-------------------+
                    |    companies      |
                    +---------+---------+
                              |
          +-------------------+-------------------+
          |                   |                   |
          ▼                   ▼                   ▼
+----------------+   +----------------+   +----------------+
| profit_loss    |   | balance_sheet  |   |  cash_flow     |
+--------+-------+   +--------+-------+   +--------+-------+
         |                    |                    |
         +--------------------+--------------------+
                              |
                              ▼
                 +---------------------------+
                 |  financial_ratios         |
                 +------------+--------------+
                              |
         +--------------------+--------------------+
         |                    |                    |
         ▼                    ▼                    ▼
+----------------+   +----------------+   +----------------+
| peer_percentiles|  | capital_alloc. |  | valuation_data  |
+----------------+   +----------------+   +----------------+
         |                    |                    |
         +--------------------+--------------------+
                              |
                              ▼
                 Reports • APIs • Dashboard
```

---

# 📋 Core Database Tables

The following tables form the analytical backbone of the platform.

| Table | Description |
|--------|-------------|
| **companies** | Master company information including ticker, sector and identifiers |
| **profit_loss** | Historical income statement data |
| **balance_sheet** | Historical balance sheet information |
| **cash_flow** | Historical cash flow statements |
| **financial_ratios** | Computed profitability, growth, liquidity and leverage metrics |
| **peer_percentiles** | Industry percentile rankings across financial metrics |
| **capital_allocation** | Capital allocation classifications and historical patterns |
| **documents** | Supporting company documentation and metadata |
| **pros_cons** | NLP-generated investment insights |

---

# 🔄 Data Flow

The database is populated through a structured ETL process.

### Step 1 – Data Extraction

Financial data is collected from multiple Excel workbooks, including:

- Company Information
- Profit & Loss Statements
- Balance Sheets
- Cash Flow Statements
- Analysis Data
- Supporting Reference Files

---

### Step 2 – Validation

Before loading into SQLite, the ETL pipeline performs:

- Schema validation
- Missing value detection
- Duplicate record checks
- Foreign key validation
- Financial year normalisation
- Company identifier standardisation

Only validated data proceeds to the database.

---

### Step 3 – Analytics

Once stored in SQLite, multiple analytical engines enrich the raw data.

Generated datasets include:

- Financial Ratios
- CAGR Metrics
- Valuation Metrics
- Cash Flow Intelligence
- Peer Rankings
- Composite Scores
- Cluster Labels
- Capital Allocation Patterns

These derived datasets are stored alongside the raw financial data, enabling fast querying and report generation.

---

# 📈 Analytical Data Model

The platform separates **raw financial data** from **derived analytical data**.

### Raw Data Layer

Contains original financial statements imported from Excel.

Examples:

- Revenue
- Expenses
- Assets
- Liabilities
- Operating Cash Flow
- Investing Cash Flow
- Financing Cash Flow

---

### Derived Data Layer

Generated automatically by analytical modules.

Examples:

- ROE
- ROCE
- ROA
- Debt-to-Equity Ratio
- Revenue CAGR
- PAT CAGR
- Free Cash Flow CAGR
- Composite Quality Score
- CFO Quality
- CapEx Intensity
- Peer Percentiles

This layered approach ensures that raw financial information remains unchanged while analytical metrics can be regenerated whenever required.

---

# 🔍 Query Optimisation

The database design supports efficient analytical queries for:

- Company-level financial analysis
- Sector comparisons
- Investment screening
- Peer benchmarking
- Portfolio analytics
- REST API responses
- Dashboard visualisations

By centralising all processed data within SQLite, the platform avoids repeated computation and improves overall performance.

---

# 📊 Database Usage Across Modules

| Module | Database Usage |
|---------|----------------|
| **ETL** | Inserts validated financial data |
| **Analytics** | Reads statements and writes computed KPIs |
| **Screener** | Queries financial ratios and composite scores |
| **Peer Engine** | Stores and retrieves percentile rankings |
| **Cash Flow Intelligence** | Generates cash flow analytics |
| **NLP** | Generates structured investment insights |
| **Reporting** | Retrieves data for PDF generation |
| **FastAPI** | Serves analytical data through REST endpoints |
| **Dashboard** | Displays financial information interactively |

---

# ✅ Database Design Highlights

- Centralised SQLite analytical warehouse
- Separation of raw and derived data
- Relational structure with reusable company identifiers
- Optimised for analytical workloads
- Supports reporting, APIs, dashboard, and machine learning modules
- Extensible architecture for future database migration (PostgreSQL/MySQL)

---

# ⚙️ ETL & Data Processing Pipeline

The Extract, Transform and Load (ETL) pipeline is the foundation of the Financial Intelligence Platform. It is responsible for ingesting raw financial datasets, validating data quality, normalising records, and loading clean data into the SQLite warehouse.

The ETL pipeline was designed with a strong emphasis on **data integrity**, **reproducibility**, and **automation**, ensuring that every analytical module operates on consistent and validated financial data.

---

# 📥 Data Sources

The platform processes multiple Excel datasets containing financial statements, company metadata, and supporting reference information.

### Core Datasets

| Dataset | Description |
|----------|-------------|
| `companies.xlsx` | Company master information |
| `profitandloss.xlsx` | Historical income statements |
| `balancesheet.xlsx` | Historical balance sheet data |
| `cashflow.xlsx` | Historical cash flow statements |
| `analysis.xlsx` | Growth and performance metrics |
| `documents.xlsx` | Company documentation metadata |
| `prosandcons.xlsx` | Reference pros and cons dataset |

### Supporting Datasets

The ETL pipeline also imports supplementary datasets required for advanced analytics, including:

- Sector mappings
- Peer group definitions
- Market capitalisation
- Shareholding patterns
- Historical price information
- Reference lookup tables

---

# 🔄 ETL Workflow

The platform follows a structured multi-stage ETL workflow.

```
Raw Excel Files
        │
        ▼
Data Extraction
        │
        ▼
Data Normalisation
        │
        ▼
Schema Validation
        │
        ▼
Data Quality Validation
        │
        ▼
SQLite Loading
        │
        ▼
Analytics Pipeline
```

Each stage performs a specific responsibility before passing validated data to the next stage.

---

# 🧹 Data Normalisation

Before loading the datasets into SQLite, the ETL pipeline standardises the data to ensure consistency across all modules.

### Normalisation Tasks

- Standardise company identifiers
- Clean company names
- Normalise financial years
- Handle missing values
- Standardise numeric formats
- Remove duplicate records
- Validate data types

This preprocessing ensures that all downstream analytical computations operate on consistent data.

---

# ✅ Data Quality Validation

To maintain high data reliability, the platform performs automated validation checks during the ETL process.

### Validation Categories

- Schema Validation
- Required Column Checks
- Duplicate Detection
- Missing Value Detection
- Foreign Key Validation
- Company Identifier Validation
- Financial Year Validation
- Numeric Data Validation

Validation failures are logged for manual review without interrupting the overall pipeline.

Generated outputs include:

```
validation_failures.csv
load_audit.csv
```

---

# 🗃 Database Loading

Once validation is complete, the cleaned datasets are loaded into the SQLite database.

The loading process ensures:

- Consistent primary keys
- Referential integrity
- Correct table relationships
- Efficient bulk insertion
- Repeatable execution

The resulting database serves as the central data repository for all analytical modules.

---

# 📊 ETL Outputs

Successful execution of the ETL pipeline produces:

### Database

- SQLite analytical database

### Validation Reports

- Validation failures
- Load audit report

### Clean Data

- Standardised company records
- Normalised financial statements
- Validated supporting datasets

These outputs become the foundation for ratio computation, screening, peer analytics, reporting, and dashboard visualisation.

---

# 🔗 Integration with Analytics

The ETL pipeline directly feeds multiple analytical modules.

| ETL Output | Consumed By |
|------------|-------------|
| Company Data | Dashboard, API, Reporting |
| Profit & Loss | Ratio Engine |
| Balance Sheet | Valuation & Leverage Analysis |
| Cash Flow | Cash Flow Intelligence |
| Analysis Data | NLP Parser |
| Supporting Data | Screener, Peer Engine |

This layered architecture eliminates duplicate processing and ensures that every analytical module operates on the same validated dataset.

---

# 🚀 ETL Design Highlights

- Automated ingestion of multiple Excel datasets
- Repeatable and modular ETL workflow
- Comprehensive data validation
- Centralised SQLite data warehouse
- Scalable architecture for future data sources
- Clean separation between raw data and analytical processing

---

# 📈 Financial Analytics Engine

The Financial Analytics Engine is the core computational component of the Financial Intelligence Platform. It transforms validated financial statements into meaningful business intelligence by calculating profitability, growth, liquidity, leverage, valuation, cash flow, and peer comparison metrics.

Rather than simply displaying financial statements, the engine derives actionable insights that support investment analysis, company benchmarking, portfolio screening, and automated reporting.

The analytics pipeline operates on the central SQLite database, ensuring that all calculations are performed on validated and standardised financial data.

---

# 🧮 Financial Ratio Engine

The ratio engine computes a comprehensive set of financial ratios covering profitability, growth, leverage, liquidity, efficiency, and valuation.

### Profitability Metrics

- Return on Equity (ROE)
- Return on Capital Employed (ROCE)
- Return on Assets (ROA)
- Operating Profit Margin (OPM)
- Net Profit Margin (NPM)

These metrics evaluate how efficiently a company generates profits from its capital and operations.

---

### Growth Metrics

Historical growth is measured using Compound Annual Growth Rate (CAGR) calculations.

Computed growth metrics include:

- Revenue CAGR
- PAT CAGR
- EPS CAGR
- Free Cash Flow CAGR

Both historical trends and long-term growth consistency are analysed.

---

### Leverage Metrics

The platform evaluates financial leverage using several indicators.

Computed metrics include:

- Debt-to-Equity Ratio
- Net Debt
- Interest Coverage Ratio
- Debt Trend Analysis

Special handling is implemented for debt-free companies to ensure meaningful analytical comparisons.

---

### Liquidity & Cash Flow Metrics

The ratio engine also evaluates cash generation capability.

Metrics include:

- Operating Cash Flow
- Free Cash Flow
- Free Cash Flow Conversion
- Cash Flow Margin

These indicators complement traditional accounting-based profitability measures.

---

# 💹 Valuation Engine

The valuation module computes market-based valuation indicators that assist in comparing companies across sectors.

Supported valuation metrics include:

- Price-to-Earnings (P/E)
- Price-to-Book (P/B)
- Enterprise Value
- EV/EBITDA
- Market Capitalisation
- Dividend Yield

These metrics provide insight into whether a company's market valuation is reasonable relative to its financial performance.

---

# 📊 Investment Scoring

To simplify financial analysis, the platform combines multiple KPIs into a Composite Quality Score.

The score ranges from **0 to 100** and evaluates companies across four dimensions.

| Category | Weight |
|----------|--------|
| Profitability | 35% |
| Cash Flow Quality | 30% |
| Growth | 20% |
| Financial Strength | 15% |

The scoring process includes:

- Winsorisation of extreme values
- Sector-relative normalisation
- Weighted aggregation
- Final ranking

This score serves as the primary ranking metric used throughout the Screener module.

---

# 🔍 Financial Screener

The Screener enables analysts to identify companies matching predefined investment criteria or custom financial thresholds.

### Supported Screening Metrics

- Return on Equity
- Return on Capital Employed
- Debt-to-Equity Ratio
- Revenue CAGR
- PAT CAGR
- EPS CAGR
- Free Cash Flow
- Operating Profit Margin
- Dividend Yield
- Interest Coverage Ratio
- Market Capitalisation
- Asset Turnover
- Sales
- Net Profit
- Price Ratios

The screening engine supports both preset investment strategies and fully configurable analyst-defined filters.

---

### Built-in Investment Presets

Six predefined investment strategies are included.

| Preset | Objective |
|---------|-----------|
| Quality Compounder | Identify fundamentally strong companies |
| Value Pick | Discover undervalued businesses |
| Growth Accelerator | Focus on rapidly expanding companies |
| Dividend Champion | Identify consistent dividend payers |
| Debt-Free Blue Chip | Find financially strong large-cap companies |
| Turnaround Watch | Detect improving businesses |

Results are ranked using the Composite Quality Score.

---

# 🤝 Peer Analytics Engine

The Peer Analytics Engine benchmarks companies against industry competitors.

Each company is compared only with businesses operating in the same peer group.

The engine computes percentile rankings across multiple financial metrics, including:

- ROE
- ROCE
- Net Profit Margin
- Debt-to-Equity Ratio
- Free Cash Flow
- Revenue CAGR
- PAT CAGR
- EPS CAGR
- Interest Coverage Ratio
- Asset Turnover

Peer rankings provide analysts with industry-relative performance instead of absolute comparisons.

---

# 📊 Radar Chart Analytics

Radar charts visually compare company performance against peer group averages.

Each radar chart displays multiple dimensions simultaneously, allowing analysts to quickly identify strengths and weaknesses.

Analysed dimensions include:

- Profitability
- Growth
- Leverage
- Cash Flow
- Operational Efficiency
- Composite Quality Score

These charts are incorporated into generated reports and visual analysis outputs.

---

# 💰 Cash Flow Intelligence

Sprint 5 introduced a dedicated Cash Flow Intelligence Engine that analyses how companies generate, invest, and allocate cash.

The module computes several advanced indicators beyond traditional accounting ratios.

### CFO Quality

Companies are classified based on the relationship between Cash Flow from Operations (CFO) and Profit After Tax (PAT).

Categories include:

- High Quality
- Moderate
- Accrual Risk

---

### CapEx Intensity

Capital expenditure is evaluated relative to revenue to classify businesses as:

- Asset Light
- Moderate
- Capital Intensive

---

### Distress Detection

The platform automatically flags companies exhibiting potential financial stress.

Indicators include:

- Negative operating cash flow
- Positive financing cash flow
- Weak cash generation
- External funding dependence

---

### Deleveraging Detection

The engine identifies companies actively reducing debt through internally generated cash flows.

---

# 🏛 Capital Allocation Analysis

Capital allocation patterns are derived from historical cash flow behaviour.

Companies are classified into predefined behavioural categories representing different capital allocation strategies.

Examples include:

- Reinvestor
- Shareholder Return
- Cash Accumulator
- Growth Funded by Debt
- Distress Signal

Historical transitions are tracked to identify changes in financial strategy over time.

---

# 🤖 NLP-Based Investment Insights

The Natural Language Processing module converts financial metrics into analyst-friendly commentary.

### Components

- Financial Analysis Parser
- Automated Pros Generation
- Automated Cons Generation
- Confidence Scoring

Each generated insight is linked to a rule-based financial signal, improving transparency and explainability.

---

# 📈 Machine Learning & Clustering

To support exploratory analysis, the platform groups companies using unsupervised learning techniques.

The clustering workflow includes:

- Missing value imputation
- Feature scaling
- K-Means clustering
- Elbow method optimisation
- Cluster profiling
- Outlier detection

This enables companies with similar financial characteristics to be analysed together.

---

# 📦 Analytics Outputs

The Financial Analytics Engine generates numerous analytical datasets consumed by downstream modules.

### Generated Reports

- Financial Ratios
- Composite Scores
- Valuation Metrics
- Peer Percentiles
- Cash Flow Intelligence
- Capital Allocation Patterns
- Pros & Cons
- Screener Results
- Cluster Labels
- Radar Charts

These outputs power the reporting engine, REST APIs, and Streamlit dashboard, ensuring consistent analytical results across the entire platform.

---

# 🚀 Analytics Engine Highlights

- Automated financial ratio computation
- Growth and CAGR analysis
- Sector-relative investment scoring
- Intelligent company screening
- Peer benchmarking
- Cash flow quality assessment
- Capital allocation analysis
- Explainable NLP-generated insights
- Machine learning–based clustering
- Unified analytical pipeline across all modules

---

# 📄 Reporting Engine

The Reporting Engine transforms analytical results into professionally formatted documents, enabling analysts and stakeholders to review financial insights without interacting directly with the database or dashboard.

Built using **ReportLab**, the reporting framework automatically generates company-level, sector-level, and portfolio-level reports with charts, KPIs, and AI-generated commentary.

---

# 📑 Company Tearsheets

One of the flagship features of the platform is the automated generation of **two-page company tearsheets**.

Each tearsheet consolidates financial information, analytical metrics, visualisations, and investment commentary into a concise report suitable for investment research.

## Page 1

Includes:

- Company Profile
- Sector & Industry
- Key Financial KPIs
- Revenue Trend
- Net Profit Trend
- ROE & ROCE Analysis

---

## Page 2

Includes:

- Balance Sheet Composition
- Cash Flow Waterfall
- NLP Generated Pros
- NLP Generated Cons
- Capital Allocation Classification
- Cash Flow Intelligence Summary

Each report is automatically generated with consistent formatting and layout, ensuring readability and preventing text overflow.

---

# 🏢 Sector Reports

The platform automatically generates sector-wise analytical reports.

Each report contains:

- Sector Overview
- Median Financial KPIs
- Company Comparison Tables
- Profitability Metrics
- Growth Metrics
- Cash Flow Indicators
- Valuation Summary

These reports provide analysts with a consolidated view of sector performance.

---

# 📚 Portfolio Summary Report

The platform generates a consolidated portfolio report covering every company in the database.

Each company receives a dedicated summary page containing:

- Company Information
- Sector Classification
- Key Financial Ratios
- Trend Indicators
- Overall Performance Summary

This report provides a high-level overview of the complete investment universe.

---

# 📊 Generated Reports

The reporting engine automatically produces:

| Report | Description |
|---------|-------------|
| Company Tearsheets | Two-page PDF report for each company |
| Sector Reports | One report for each business sector |
| Portfolio Summary | Consolidated portfolio report |
| Screener Results | Excel workbook containing screened companies |
| Peer Comparison | Excel workbook with peer rankings |
| Cash Flow Intelligence | Advanced cash flow analysis |
| Valuation Summary | Company valuation metrics |

---

# 🌐 REST API

The platform exposes analytical data through a RESTful API built using **FastAPI**.

The API enables external applications, dashboards, and analytical tools to retrieve financial data programmatically.

Interactive documentation is automatically generated using the **OpenAPI Specification**, allowing developers to explore and test endpoints directly from the browser.

---

# API Capabilities

The REST API provides endpoints for:

- Company Information
- Financial Ratios
- Profit & Loss Statements
- Balance Sheets
- Cash Flow Statements
- Investment Screener
- Sector Analytics
- Peer Comparison
- Cash Flow Intelligence
- Valuation Metrics
- Portfolio Statistics
- Health Check

The API follows a modular architecture with dedicated routers and service layers, making it easy to extend and maintain.

---

# 📖 API Documentation

FastAPI automatically generates interactive API documentation.

Available interfaces include:

- Swagger UI
- OpenAPI JSON Specification

These interfaces simplify endpoint exploration, testing, and third-party integration.

---

# 📊 Interactive Dashboard

The Financial Intelligence Platform includes a multi-page dashboard developed using **Streamlit**.

The dashboard provides an intuitive interface for exploring financial data, running investment screeners, comparing companies, and viewing analytical reports.

It is designed for financial analysts, researchers, and investors who require interactive access to the platform without writing SQL queries or using API clients.

---

# Dashboard Modules

The dashboard is organised into dedicated analytical pages.

### Home

Provides an overview of the platform, key statistics, and navigation.

---

### Company Profile

Displays comprehensive financial information for individual companies, including:

- Company Overview
- Financial Statements
- Key Ratios
- Historical Trends
- Cash Flow Intelligence

---

### Investment Screener

Allows users to:

- Apply predefined screening strategies
- Configure custom screening thresholds
- Rank companies using the Composite Quality Score
- Export screening results

---

### Peer Analytics

Provides industry benchmarking through:

- Percentile Rankings
- Radar Charts
- Company Comparisons
- Peer Group Statistics

---

### Sector Analytics

Enables comparison of companies within the same sector using:

- Sector Medians
- Ranking Tables
- Growth Analysis
- Profitability Comparison

---

### Cash Flow Intelligence

Visualises advanced cash flow indicators, including:

- CFO Quality
- CapEx Intensity
- Distress Signals
- Capital Allocation Patterns

---

### Reports

Provides access to generated:

- Company Tearsheets
- Sector Reports
- Portfolio Reports

allowing users to download analytical outputs directly from the dashboard.

---

# 📈 Data Visualisation

The dashboard incorporates multiple interactive visualisations to support financial analysis.

Examples include:

- Revenue Trends
- Net Profit Trends
- ROE & ROCE Comparison
- Radar Charts
- Cash Flow Waterfall Charts
- Balance Sheet Composition
- Correlation Heatmaps
- Cluster Analysis
- Portfolio Statistics

These visualisations enhance interpretability and enable users to identify trends and anomalies more effectively.

---

# 🚀 Reporting & Visualisation Highlights

- Automated PDF generation
- Professional report layouts
- Interactive dashboard
- RESTful API integration
- OpenAPI documentation
- Downloadable analytical reports
- Rich financial visualisations
- Modular reporting architecture

---

# 🧪 Testing & Quality Assurance

Testing was incorporated throughout the development lifecycle to ensure analytical correctness, API reliability, data integrity, and overall system stability.

The project includes dedicated test suites covering ETL validation, financial calculations, REST APIs, and performance benchmarks.

---

## Testing Strategy

The platform follows a layered testing approach.

### Unit Testing

Validates individual functions and analytical modules.

Coverage includes:

- Financial Ratio Calculations
- CAGR Engine
- Valuation Engine
- Cash Flow Intelligence
- Capital Allocation
- Peer Analytics
- Screener Logic

---

### ETL Testing

Ensures reliable data ingestion and validation.

Tests include:

- Data Normalisation
- Schema Validation
- Duplicate Detection
- Missing Value Handling
- Company Identifier Validation

---

### API Testing

REST endpoints are validated using automated API tests.

Coverage includes:

- Company Endpoints
- Financial Data Endpoints
- Screener Endpoints
- Sector Analytics
- Health Check

---

### Performance Testing

Performance tests verify that the platform scales efficiently across the complete dataset.

Areas evaluated include:

- Database Query Performance
- API Response Time
- Bulk Report Generation
- Large Dataset Processing

---

## Test Organisation

```
tests/

├── api/
├── etl/
├── kpi/
└── performance/
```

---

## Quality Assurance

Throughout development the following quality practices were followed.

- Modular Architecture
- Automated Testing
- Data Validation
- Error Handling
- Code Documentation
- Configuration-driven Design
- Separation of Concerns

These practices improve maintainability, reliability, and future extensibility of the platform.

---

# ⚡ Installation

## Prerequisites

Before running the project, ensure the following software is installed.

- Python 3.11 or later
- Git
- SQLite
- pip

---

## Clone Repository

```bash
git clone <repository-url>

cd financial_intelligence_platform
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Step 1 – Execute ETL Pipeline

```bash
python src/etl/load_database.py
```

This imports, validates, and loads financial datasets into SQLite.

---

## Step 2 – Generate Financial Analytics

```bash
python src/analytics/populate_financial_ratios.py
```

Computes all analytical metrics.

---

## Step 3 – Generate Reports

```bash
python src/reports/generate_reports.py
```

Creates:

- Company Tearsheets
- Sector Reports
- Portfolio Summary

---

## Step 4 – Launch REST API

```bash
uvicorn src.api.main:app --reload
```

Swagger UI

```
http://localhost:8000/docs
```

---

## Step 5 – Launch Dashboard

```bash
streamlit run src/dashboard/app.py
```

---

## Step 6 – Execute Tests

```bash
pytest tests -v
```

---

# 📂 Generated Outputs

Successful execution produces a comprehensive set of analytical outputs.

### Excel Reports

- Screener Results
- Peer Comparison
- Cash Flow Intelligence
- Valuation Summary

---

### CSV Reports

- Analysis Parser Output
- Pros & Cons
- Distress Alerts
- Capital Allocation
- Cluster Labels
- Pattern Changes
- Validation Reports

---

### PDF Reports

- Company Tearsheets
- Sector Reports
- Portfolio Summary

---

### Visualisations

- Radar Charts
- Correlation Heatmaps
- Elbow Plot
- Dashboard Charts

---

# 📸 Project Screenshots

The repository includes screenshots demonstrating the major components of the platform.

Suggested screenshots:

- Streamlit Dashboard
- Company Profile
- Investment Screener
- Peer Analytics
- FastAPI Swagger UI
- Company Tearsheet
- Sector Report
- Portfolio Summary

These provide a visual overview of the platform's capabilities.

---

# 🚀 Future Enhancements

The current implementation provides a strong analytical foundation and can be extended with additional enterprise-grade capabilities.

Potential enhancements include:

- PostgreSQL or MySQL backend
- Docker containerisation
- Cloud deployment
- User authentication and role management
- Live NSE/BSE market data integration
- Portfolio optimisation algorithms
- AI-powered investment recommendations
- Scheduled ETL workflows
- Email-based automated reporting
- Real-time financial alerts

---

# 👨‍💻 Author

**Bhimishetti Lohith**


---