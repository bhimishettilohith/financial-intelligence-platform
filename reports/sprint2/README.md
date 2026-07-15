# 🚀 Sprint 2 Report

# Financial Ratio Engine

---

## Sprint Information

| Item | Details |
|------|---------|
| Sprint | Sprint 2 |
| Duration | Day 08 – Day 14 |
| Current Progress | Day 08 – Day 14 Completed |
| Status | ✅ Completed |
| Goal | Build a reusable Financial Ratio Engine capable of generating analytical KPIs for every company-year record |

---

# Sprint Objective

Sprint 2 focuses on transforming raw financial statement data into meaningful business intelligence by implementing a comprehensive Financial Ratio Engine.

The objective is to calculate profitability, leverage, efficiency, growth, and cash flow metrics for every available company-year combination while ensuring correctness through automated validation and robust edge-case handling.

Unlike Sprint 1, which concentrated on data engineering, Sprint 2 shifts the project toward financial analytics by building reusable analytical functions that will later power the company screener, ranking engine, REST APIs, and dashboard.

---

# Sprint Deliverables

## Financial Analytics

- Profitability Ratio Engine
- Leverage Ratio Engine
- Efficiency Ratio Engine
- CAGR Engine
- Cash Flow KPI Engine
- Capital Allocation Engine
- Composite Quality Score

---

## Database

- Financial Ratio Population Engine
- SQLite Ratio Table
- Ratio Validation

---

## Testing

- KPI Unit Tests
- CAGR Edge Case Tests
- Manual Ratio Verification

---

# Sprint Architecture

```

SQLite Database

↓

Financial Statement Merge

↓

Ratio Engine

↓

Growth Engine

↓

Cash Flow Engine

↓

Composite Score

↓

SQLite Update

↓

Financial Analytics Ready

```

---

# Development Timeline

| Day | Module | Status |
|-----|--------|--------|
| Day 08 | Profitability Ratios | ✅ |
| Day 09 | Leverage & Efficiency Ratios | ✅ |
| Day 10 | CAGR Engine | ✅ |
| Day 11 | Cash Flow KPIs | ✅ |
| Day 12 | Financial Ratio Population | ✅ |
| Day 13 | KPI Validation | ⏳ |
| Day 14 | Sprint Review | ⏳ |

---

# 📅 Day 08 — Profitability Ratio Engine

## Objective

Develop reusable analytical functions to calculate profitability metrics for every company-year record while handling invalid financial values and division-by-zero scenarios.

The implementation focused on writing modular functions that can be reused throughout the project, including the Financial Ratio Engine, Company Screener, REST APIs, and Dashboard.

---

## Tasks Completed

A dedicated analytics module (`ratios.py`) was created to calculate core profitability ratios.

Each function was implemented independently to maximize code reusability and simplify testing.

The implementation also included appropriate handling for missing values and invalid denominators to ensure that the ratio engine remains robust when processing real-world financial statements.

---

## Profitability Ratios Implemented

### Net Profit Margin

Measures the percentage of revenue retained as profit after all expenses.

Formula

```
Net Profit
-----------
Sales
×100
```

Edge Case Handling

- Sales = 0 → Returns None

---

### Operating Profit Margin

Measures operating efficiency before taxes and financing costs.

Formula

```
Operating Profit
----------------
Sales
×100
```

Additional validation was implemented to compare calculated OPM with the original dataset values.

---

### Return on Equity (ROE)

Measures profitability generated using shareholders' equity.

Formula

```
Net Profit
------------------------------
Equity Capital + Reserves
×100
```

Edge Cases

- Negative Equity
- Zero Equity

Returns None whenever equity is invalid.

---

### Return on Capital Employed (ROCE)

Formula

```
EBIT
------------------------------
Capital Employed
×100
```

where

```
Capital Employed

=

Equity
+ Reserves
+ Borrowings
```

---

### Return on Assets (ROA)

Formula

```
Net Profit
-----------
Total Assets
×100
```

Returns None whenever Total Assets equals zero.

---

## Testing

The implemented functions were validated using multiple scenarios including:

- Standard calculations
- Zero denominator
- Missing values
- Negative equity
- Financial edge cases

---

## Deliverables

```
src/analytics/ratios.py

tests/kpi/test_ratios.py
```

---

## Outcome

A reusable profitability analytics module was successfully completed and became the foundation for all subsequent KPI calculations.

---

# 📅 Day 09 — Leverage & Efficiency Ratio Engine

## Objective

Extend the Financial Ratio Engine by implementing leverage and efficiency metrics capable of evaluating financial risk, debt management, and asset utilization.

---

## Tasks Completed

Several additional analytical functions were integrated into the existing ratio engine.

These functions evaluate a company's capital structure, debt servicing ability, and operational efficiency.

Industry-specific business rules were also introduced, particularly for Financial Sector companies where leverage characteristics differ from other industries.

---

## Ratios Implemented

### Debt-to-Equity Ratio

Formula

```
Borrowings
-----------------------------
Equity + Reserves
```

Special Handling

Borrowings = 0

Returns

```
0
```

instead of None.

---

### High Leverage Flag

Companies with

```
Debt-to-Equity > 5
```

are automatically flagged.

Financial Sector companies are excluded because high leverage is expected in banking and financial services.

---

### Interest Coverage Ratio

Formula

```
Operating Profit + Other Income
--------------------------------
Interest
```

Special Handling

Interest = 0

Returns

```
None
```

and assigns the company the label

```
Debt Free
```

---

### Net Debt

Formula

```
Borrowings

−

Investments
```

This represents debt remaining after liquid investments are considered.

---

### Asset Turnover Ratio

Formula

```
Sales
---------
Total Assets
```

Measures how efficiently assets generate revenue.

Edge Case

- Total Assets = 0

Returns None.

---

## Testing

Validation covered

- Debt-free companies
- Highly leveraged companies
- Zero interest expense
- Asset turnover calculations
- Missing values

All implemented functions produced expected outputs.

---

## Deliverables

```
src/analytics/ratios.py

tests/kpi/test_leverage.py
```

---

## Outcome

The Financial Ratio Engine was successfully expanded to include leverage and efficiency analysis, enabling more comprehensive financial health evaluation.


# 📅 Day 10 — CAGR Growth Engine

## Objective

Develop a reusable Compound Annual Growth Rate (CAGR) engine capable of measuring long-term business growth while correctly handling multiple financial edge cases.

Unlike simple percentage growth, CAGR provides an annualized growth rate, making it significantly more useful for evaluating long-term company performance.

---

## Tasks Completed

A dedicated module (`cagr.py`) was developed to calculate historical growth across multiple financial metrics.

The implementation supports multiple time windows and returns descriptive flags whenever CAGR cannot be computed due to invalid financial conditions.

---

## Growth Metrics Implemented

The CAGR engine currently supports:

- Revenue CAGR
- PAT (Net Profit) CAGR
- Earnings Per Share (EPS) CAGR

Supported historical windows include:

- 3-Year CAGR
- 5-Year CAGR
- 10-Year CAGR

---

## CAGR Formula

```
((Ending Value / Starting Value)
^(1 / Number of Years) − 1)
×100
```

---

## Edge Cases Handled

The implementation detects and classifies the following situations:

| Condition | Flag Returned |
|-----------|---------------|
| Positive → Positive | OK |
| Positive → Negative | DECLINE_TO_LOSS |
| Negative → Positive | TURNAROUND |
| Negative → Negative | BOTH_NEGATIVE |
| Starting Value = 0 | ZERO_BASE |
| Insufficient Historical Data | INSUFFICIENT |

Instead of producing misleading numerical values, these conditions generate descriptive flags that can be used for screening and financial analysis.

---

## Testing

The CAGR engine was validated using multiple scenarios covering:

- Normal growth
- Revenue decline
- Business turnaround
- Loss-making companies
- Zero starting value
- Insufficient historical records

All edge cases returned the expected results.

---

## Deliverables

```
src/analytics/cagr.py

tests/kpi/test_cagr.py
```

---

## Outcome

The project now includes a reusable CAGR engine capable of calculating consistent long-term growth metrics across multiple financial indicators while handling real-world financial edge cases.

---

# 📅 Day 11 — Cash Flow KPIs & Capital Allocation

## Objective

Implement advanced cash flow analytics to evaluate operational cash generation, capital expenditure behaviour, free cash flow generation, and overall capital allocation strategy.

Cash flow analysis complements profitability analysis by measuring the quality of earnings and the effectiveness of management's capital allocation decisions.

---

## Tasks Completed

A dedicated analytics module (`cashflow_kpis.py`) was developed containing reusable functions for calculating operational cash flow metrics and classifying company cash flow behaviour.

The implementation provides meaningful financial insights that will later be incorporated into the screening and ranking engines.

---

## KPIs Implemented

### Free Cash Flow (FCF)

Formula

```
Operating Cash Flow

+

Investing Cash Flow
```

Negative Free Cash Flow is considered valid because growing businesses often invest heavily in long-term assets.

---

### CFO Quality Score

Formula

```
Operating Cash Flow
-------------------
Net Profit
```

Classification

| Ratio | Classification |
|--------|----------------|
| >1.0 | High Quality |
| 0.5 – 1.0 | Moderate |
| <0.5 | Accrual Risk |

This metric evaluates the quality of reported earnings.

---

### CapEx Intensity

Formula

```
|Investing Cash Flow|
---------------------
Sales
×100
```

Classification

| Percentage | Category |
|------------|----------|
| <3% | Asset Light |
| 3–8% | Moderate |
| >8% | Capital Intensive |

---

### Free Cash Flow Conversion

Formula

```
Free Cash Flow
-------------------
Operating Profit
×100
```

Edge Case

Operating Profit = 0

Returns None.

---

## Capital Allocation Engine

An automated classification engine was implemented based on the sign of operating, investing, and financing cash flows.

Implemented classifications include:

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
| Others | Other |

---

## Output Generated

```
output/capital_allocation.csv
```

The report includes:

- Company ID
- Financial Year
- CFO Sign
- CFI Sign
- CFF Sign
- Capital Allocation Pattern

A total of **1103 company-year records** were successfully classified.

---

## Deliverables

```
src/analytics/cashflow_kpis.py

src/analytics/generate_capital_allocation.py

output/capital_allocation.csv
```

---

## Outcome

The platform now includes advanced cash flow analytics capable of evaluating operational quality and management's capital allocation behaviour, adding another important dimension to financial analysis.

# 📅 Day 12 — Financial Ratio Population Engine

## Objective

Integrate all analytical modules developed during Sprint 2 into a single Financial Ratio Engine capable of computing KPIs for every available company-year record and storing the computed values inside the SQLite database.

This milestone transformed the project from a collection of standalone analytical functions into a complete financial analytics pipeline capable of producing database-ready business intelligence.

---

## Tasks Completed

A comprehensive population engine (`populate_financial_ratios.py`) was developed to automate ratio generation.

The engine performs the following workflow:

1. Connects to the SQLite database.
2. Loads all required financial statement tables.
3. Detects and removes duplicate company-year records.
4. Merges Profit & Loss, Balance Sheet, Cash Flow, Company, and Sector datasets.
5. Computes all implemented KPIs.
6. Calculates Revenue, PAT, and EPS CAGR values.
7. Generates Composite Quality Scores.
8. Writes computed results back into the SQLite database.
9. Performs validation checks after insertion.

---

## Data Processing Pipeline

```
SQLite Database

↓

Load Financial Tables

↓

Clean Duplicate Records

↓

Merge Financial Statements

↓

Calculate KPIs

↓

Generate CAGR Metrics

↓

Generate Composite Score

↓

Populate financial_ratios Table

↓

Verification
```

---

## Financial KPIs Generated

### Profitability

- Net Profit Margin
- Operating Profit Margin
- Return on Equity
- Return on Capital Employed
- Return on Assets

---

### Leverage

- Debt to Equity Ratio
- High Leverage Flag
- Interest Coverage Ratio
- Interest Coverage Label
- Interest Coverage Warning
- Net Debt

---

### Efficiency

- Asset Turnover

---

### Cash Flow

- Free Cash Flow
- CFO Quality Score
- CapEx Intensity
- Free Cash Flow Conversion

---

### Growth

- Revenue CAGR (5-Year)
- PAT CAGR (5-Year)
- EPS CAGR (5-Year)

---

### Quality

- Composite Quality Score

---

## Database Processing Summary

The Financial Ratio Engine successfully completed the following tasks:

- Loaded all financial datasets.
- Removed duplicate Balance Sheet records.
- Removed duplicate Cash Flow records.
- Merged all financial statements.
- Calculated analytical KPIs.
- Generated CAGR metrics.
- Computed Composite Quality Scores.
- Updated SQLite database.

---

## Execution Statistics

| Metric | Value |
|---------|------:|
| Companies | 92 |
| Profit & Loss Records | 1177 |
| Balance Sheet Records | 1227 |
| Cash Flow Records | 1091 |
| Computed Ratio Records | **1177** |
| SQLite Update | Successful |

---

## Sample Output

Example output generated by the Financial Ratio Engine.

| Company | Year | ROE | D/E | Revenue CAGR | Composite Score |
|---------|------|----:|----:|-------------:|----------------:|
| ABB | Dec 2012 | 22.41 | 0.00 | N/A | 50 |
| ABB | Mar 2018 | 23.69 | 0.00 | 14.81% | 80 |
| ABB | Mar 2019 | 22.41 | 0.00 | 10.08% | 100 |
| ABB | Mar 2020 | 24.39 | 0.07 | 12.33% | 100 |
| ABB | Mar 2022 | 28.33 | 0.05 | 11.10% | 100 |

---

## Validation

The following validations were completed successfully.

- Database connection established.
- Duplicate company-year records removed.
- Financial statements merged correctly.
- KPI calculations completed.
- SQLite table updated successfully.
- Computed row count exceeded project requirement.

Verification Result

```
Computed Rows : 1177

PASS

SQLite Updated Successfully
```

---

## Deliverables

```
src/analytics/populate_financial_ratios.py

SQLite financial_ratios table

Computed Financial KPIs

Validation Output
```

---

## Outcome

The Financial Ratio Engine is now fully operational and capable of computing analytical metrics for every available company-year record.

The project now contains a centralized analytical database that will support screening, ranking, APIs, dashboards, and future financial intelligence modules.

---

# Sprint 2 Progress Summary

## Major Accomplishments

During Days 08–14, the following modules were successfully completed:

- Profitability Ratio Engine
- Leverage Ratio Engine
- Efficiency Ratio Engine
- CAGR Engine
- Cash Flow KPI Engine
- Capital Allocation Engine
- Financial Ratio Population Engine
- Composite Quality Score
- SQLite Integration
- ROCE Validation
- ROE Validation
- Ratio Edge Case Logging
- KPI Test Suite
- Sprint Review

---

## Current Project Statistics

| Metric | Current Value |
|---------|--------------:|
| Development Days Completed | 14 / 42 |
| Sprints Completed | 1 |
| Current Sprint | Sprint 2 |
| Companies Processed | 92 |
| Financial Records | 1177 |
| Database Tables | 11 |
| Financial KPIs Implemented | 20+ |
| Data Quality Rules | 16 |
| Unit Tests Passing | 44 / 44 |
| Capital Allocation Records | 1103 |
| Financial Ratio Records | 1177 |

---

# Challenges Faced

Several implementation challenges were encountered during Sprint 2.

Major challenges included:

- Handling division-by-zero cases.
- Supporting companies with missing historical records.
- CAGR calculation for negative financial values.
- Duplicate company-year records during merges.
- Cash Flow classification edge cases.
- SQLite merge consistency.
- Handling missing Balance Sheet and Cash Flow data.

Each issue was resolved through modular function design, validation checks, and extensive testing.

---

# Lessons Learned

Sprint 2 reinforced several important engineering concepts.

- Keep analytical functions completely reusable.
- Handle edge cases before implementing formulas.
- Separate financial calculations into independent modules.
- Validate intermediate results before database insertion.
- Merge datasets carefully to avoid duplicate records.
- Always verify analytical outputs against manual calculations.
- Build scalable analytical pipelines rather than one-off scripts.

---

# 📅 Day 13 — Bank ROCE Validation & Edge Case Logging

## Objective

Improve the reliability of the Financial Ratio Engine by validating computed ROCE and ROE values against source data while handling industry-specific exceptions for Financial Sector companies.

---

## Tasks Completed

The Financial Ratio Population Engine was enhanced with an automated validation layer.

Implemented improvements include:

- Financial sector carve-out for ROCE validation.
- ROCE comparison against source values.
- ROE comparison against source values.
- Automatic anomaly logging.
- Ratio edge-case documentation.

---

## Financial Sector Handling

Companies classified under the **Financials** broad sector (banks, NBFCs and insurance companies) were excluded from ROCE anomaly validation because traditional capital employed calculations are not directly comparable for financial institutions.

The computed ROCE values remain available for analytics, while anomaly detection is suppressed for these companies.

---

## Edge Case Logging

A dedicated log file was introduced:

```
output/ratio_edge_cases.log
```

Each anomaly records:

- Company
- Financial Year
- Computed Value
- Source Value
- Difference
- Category

---

## Categories Used

- Data Source Issue
- Formula Discrepancy
- Version Difference

---

## Outcome

The Financial Ratio Engine now provides an auditable validation layer that records significant deviations between calculated ratios and source values, improving traceability and future debugging.

# 📅 Day 14 — Testing & Sprint Review

## Objective

Validate the complete Financial Ratio Engine through automated testing, edge-case review, screener verification, and sprint retrospective.

---

## KPI Testing

All KPI unit tests were executed using PyTest.

### Result

```
44 Tests Passed

0 Failed

Execution Time: 0.15 seconds
```

The analytical engine exceeded the original sprint requirement of 20 unit tests.

---

## Edge Case Review

The generated `ratio_edge_cases.log` was reviewed to verify that all detected anomalies were properly documented and categorized.

The review confirmed that the logging mechanism successfully captures discrepancies requiring manual investigation.

---

## Screener Validation

A preliminary screener query was executed using:

```
ROE > 15%

Debt-to-Equity < 1
```

Key observations:

- TTM records were excluded because they contain incomplete financial statement data.
- Multiple financially strong companies were returned during historical analysis.
- Extremely high ROE values were observed for companies with very small shareholder equity, resulting in mathematically valid but unusually large percentages.
- These observations have been documented for future refinement of screening logic.

---

## Sprint Retrospective

The sprint concluded with a review of:

- Formula implementation decisions
- CAGR edge-case handling
- Financial sector validation rules
- SQLite integration
- KPI testing strategy
- Documentation improvements

---

## Deliverables

```
output/ratio_edge_cases.log

reports/sprint2/sprint2_retro.md
```

---

## Outcome

Sprint 2 concluded with a fully operational Financial Ratio Engine capable of generating analytical KPIs for all available company-year records and storing them within the SQLite database.

The project is now ready to begin Sprint 3 development.


# Sprint Status

| Day | Module | Status |
|-----|--------|--------|
| Day 08 | Profitability Ratios | ✅ |
| Day 09 | Leverage & Efficiency Ratios | ✅ |
| Day 10 | CAGR Engine | ✅ |
| Day 11 | Cash Flow KPIs | ✅ |
| Day 12 | Financial Ratio Population | ✅ |
| Day 13 | Bank ROCE Validation & Edge Case Logging | ✅ |
| Day 14 | Testing & Sprint Review | ✅ |

---

# Sprint Completion

Sprint 2 has been successfully completed.

The Financial Ratio Engine now provides:

- Profitability Analytics
- Leverage Analytics
- Growth Analytics
- Cash Flow Analytics
- Composite Quality Scores
- Automated SQLite Population
- KPI Validation
- Edge Case Logging
- Comprehensive Unit Test Coverage
