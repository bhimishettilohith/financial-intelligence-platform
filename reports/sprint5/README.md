# Sprint 5 – Cash Flow Intelligence, Automated Reporting & NLP Analytics

## Financial Intelligence Platform

### Sprint Duration
**Days 29 – 35**

### Story Points
**70 Story Points**

### Sprint Epics
- **Epic 07** – Cash Flow Intelligence
- **Epic 08** – Reporting Engine
- **Epic 09** – Natural Language Processing (NLP)

---

# Sprint Goal

Sprint 5 focused on transforming raw financial statement data into intelligent business insights through Natural Language Processing (NLP), advanced cash flow analytics, and automated PDF reporting.

The sprint introduced automated pros and cons generation, cash flow intelligence metrics, capital allocation analysis, and a complete reporting framework capable of generating company tearsheets, sector reports, and portfolio summaries.

By the end of Sprint 5, the platform automatically generates analyst-ready reports for all companies, classifies businesses based on cash flow behaviour, and produces explainable investment insights using rule-based NLP.

---

# Sprint Objectives

At the completion of Sprint 5, the platform is capable of:

- Parsing textual financial analysis into structured numerical data
- Automatically generating investment pros and cons
- Computing advanced cash flow intelligence metrics
- Detecting distress and deleveraging signals
- Classifying capital allocation patterns
- Generating professional company tearsheets
- Producing sector-wise analytical reports
- Creating portfolio summary reports
- Exporting analyst-ready datasets

---

# Features Implemented

---

# 1. NLP Analysis Parser

Implemented:

```
src/nlp/parser.py
```

The NLP parser converts semi-structured text available in **analysis.xlsx** into structured numerical data suitable for downstream analytics.

### Parsed Metrics

- Compounded Sales Growth
- Compounded Profit Growth
- Stock Price CAGR
- Return on Equity

### Capabilities

- Regular Expression based parsing
- Period extraction
- Percentage extraction
- Validation against computed CAGR values
- Divergence detection
- Parse failure logging

Generated Outputs

```
output/analysis_parsed.csv
output/parse_failures.csv
```

---

# 2. Automated Pros & Cons Generator

Implemented:

```
src/nlp/pros_cons_generator.py
```

A rule-based NLP engine was developed to automatically generate investment insights for every company.

### Pro Rules

The engine evaluates twelve positive business indicators including:

- High ROE
- Positive Free Cash Flow
- Debt-Free Balance Sheet
- Strong Revenue CAGR
- High Operating Margin
- Strong PAT Growth
- Excellent Interest Coverage
- Sustainable Dividend Yield
- High EPS Growth
- Improving ROE Trend
- Operating Leverage
- Self-funded Asset Growth

### Con Rules

The engine evaluates twelve financial risk indicators including:

- High Debt
- Negative Free Cash Flow
- Declining Margins
- Net Loss
- Revenue Decline
- Weak Interest Coverage
- Unsustainable Dividend Payout
- Rising Leverage
- Declining EPS
- Poor ROCE
- High Net Debt
- Weak Revenue Growth

### Confidence Scoring

Every generated insight is assigned a confidence score between **0 and 100**.

Only insights with confidence greater than **60%** are included in the final output.

Generated Output

```
output/pros_cons_generated.csv
```

Each record contains:

- Company ID
- Rule ID
- Insight Type
- Generated Text
- Confidence Score

---

# 3. Cash Flow Intelligence Engine

Implemented:

```
src/analytics/cashflow_kpis.py
```

The Cash Flow Intelligence module analyses historical cash flow behaviour and generates advanced business quality indicators.

### Features

#### CFO Quality Score

Average CFO/PAT ratio over five years.

Classification:

- High Quality
- Moderate
- Accrual Risk

---

#### CapEx Intensity

Calculated as

```
CapEx / Revenue × 100
```

Categories:

- Asset Light
- Moderate
- Capital Intensive

---

#### Distress Detection

Automatically identifies companies where:

- Operating Cash Flow is negative
- Financing Cash Flow is positive

This highlights businesses relying on external funding while operations consume cash.

---

#### Deleveraging Detection

Detects companies actively reducing borrowings using internal cash generation.

---

#### Free Cash Flow Analytics

Computed metrics include:

- Free Cash Flow
- Free Cash Flow CAGR
- Free Cash Flow Conversion

Generated Outputs

```
output/cashflow_intelligence.xlsx
output/distress_alerts.csv
```

---

# 4. Capital Allocation Analysis

The capital allocation engine classifies companies according to cash flow behaviour.

Supported classifications include:

- Shareholder Returns
- Reinvestor
- Growth Funded by Debt
- Distress Signal
- Cash Accumulator
- Liquidating Assets
- Mixed
- Pre-Revenue

Additional reporting includes:

- Distribution summary
- Pattern transition tracking
- Historical pattern analysis

Generated Output

```
output/pattern_changes.csv
```

---

# 5. Company Tearsheet Engine

Implemented:

```
src/reports/tearsheet.py
```

A professional two-page PDF tearsheet was created for every company.

---

## Page 1

Includes:

- Company Information
- KPI Summary
- Revenue Trend
- Net Profit Trend
- ROE vs ROCE Analysis

---

## Page 2

Includes:

- Balance Sheet Composition
- Cash Flow Waterfall
- Generated Pros
- Generated Cons
- Capital Allocation Badge

The layout was designed to eliminate text overflow and maximise readability.

Generated Output

```
reports/tearsheets/
```

A separate PDF is generated for each company.

---

# 6. Batch Report Generation

Automated batch processing was implemented for all companies.

Reports generated include:

- Company Tearsheets
- Sector Reports

Companies with insufficient historical data are automatically skipped and logged.

Generated Outputs

```
reports/tearsheets/
reports/sector/
output/skipped_tearsheets.csv
```

---

# 7. Sector Reports

Implemented:

```
src/reports/sector_report.py
```

Each sector report contains:

- Sector Overview
- Median KPIs
- Company Comparison
- Financial Metrics
- Sector Summary Tables

One PDF is generated for each sector.

---

# 8. Portfolio Summary Report

Implemented:

```
src/reports/portfolio_summary.py
```

A consolidated portfolio report was generated covering every company.

Each page includes:

- Company Profile
- Sector
- Top KPIs
- Trend Indicators
- Performance Summary

Generated Output

```
reports/portfolio/portfolio_summary.pdf
```

---

# Technologies Used

- Python 3.11
- Pandas
- NumPy
- SQLite
- ReportLab
- Matplotlib
- OpenPyXL
- Regular Expressions (Regex)
- Pytest

---

# Deliverables

| Deliverable | Description |
|-------------|-------------|
| `src/nlp/parser.py` | NLP Analysis Parser |
| `src/nlp/pros_cons_generator.py` | Automated Pros & Cons Generator |
| `src/analytics/cashflow_kpis.py` | Cash Flow Intelligence Engine |
| `src/reports/tearsheet.py` | Company Tearsheet Generator |
| `src/reports/sector_report.py` | Sector Report Generator |
| `src/reports/portfolio_summary.py` | Portfolio Summary Generator |
| `output/analysis_parsed.csv` | Parsed Analysis Data |
| `output/pros_cons_generated.csv` | Generated Investment Insights |
| `output/cashflow_intelligence.xlsx` | Cash Flow Intelligence Report |
| `output/distress_alerts.csv` | Distress Detection Report |
| `output/pattern_changes.csv` | Capital Allocation Changes |
| `reports/tearsheets/` | Company PDF Reports |
| `reports/sector/` | Sector Reports |
| `reports/portfolio/portfolio_summary.pdf` | Portfolio Report |

---

# Testing & Validation

Sprint validation included:

- NLP parsing verification
- Regex validation
- CAGR cross-checking
- Cash Flow KPI verification
- Distress detection validation
- Capital allocation verification
- PDF layout review
- Multi-sector tearsheet validation
- Batch report generation
- Portfolio report verification

Visual inspection confirmed:

- No text overflow
- No blank pages
- Charts rendered correctly
- Proper formatting across all generated reports

---

# Sprint Outcome

Sprint 5 successfully transformed the Financial Intelligence Platform into a complete analytical reporting system.

The platform now combines structured financial analysis, rule-based NLP, advanced cash flow intelligence, automated PDF reporting, and portfolio-level reporting into a unified workflow. Analyst insights that previously required manual interpretation are now generated automatically, enabling faster and more consistent financial analysis.

The reporting infrastructure introduced in this sprint forms the foundation for the REST API and interactive dashboard developed in the subsequent sprint.

---

# Sprint Status

**Sprint 5 Completed Successfully**

**All planned story points achieved.**

## Exit Criteria Achieved

- NLP parser successfully extracted structured analysis data.
- Every company received at least one generated pro and one generated con.
- Cash Flow Intelligence generated reports for all companies.
- Distress alerts identified qualifying companies.
- Capital allocation patterns classified successfully.
- Company tearsheets generated successfully.
- Sector reports generated for all sectors.
- Portfolio summary report completed.
- Visual verification confirmed correct layout with no text overflow.