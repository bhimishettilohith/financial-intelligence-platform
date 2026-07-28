# Sprint 3 – Financial Screener & Peer Analytics Engine

## Financial Intelligence Platform

### Sprint Duration
**Days 15 – 21**

### Story Points
**49 Story Points**

### Sprint Epics
- Epic 03 – Financial Screener Engine
- Epic 04 – Peer Analytics Engine

---

# Sprint Goal

The objective of Sprint 3 was to develop an intelligent financial screening and peer comparison engine capable of analysing all companies in the NIFTY 100 universe using configurable investment filters and sector-aware benchmarking.

During this sprint, a fully configurable screening engine was implemented with six investment presets, composite quality scoring, percentile-based peer ranking, radar chart visualisation and automated Excel reporting.

---

# Sprint Objectives

At the completion of Sprint 3 the platform is capable of:

- Screening companies using analyst-defined thresholds
- Running six predefined investment screeners
- Computing composite quality scores
- Ranking companies within peer groups
- Generating radar comparison charts
- Producing analyst-ready Excel reports
- Populating peer percentile rankings into SQLite
- Passing all Data Quality validation tests

---

# Features Implemented

## 1. Financial Screener Engine

Implemented:

```
src/screener/engine.py
```

### Capabilities

- Loads configurable screening thresholds from YAML
- Applies dynamic filters on financial ratios
- Supports custom analyst thresholds
- Sector-aware filtering logic
- Composite quality score calculation
- Sorted screening results

---

## Supported Screening Metrics

The screener supports filtering using fifteen financial metrics.

| Metric |
|---------|
| Return on Equity (ROE) |
| Debt to Equity |
| Free Cash Flow |
| Revenue CAGR (5 Year) |
| PAT CAGR (5 Year) |
| Operating Profit Margin |
| Price to Earnings Ratio |
| Price to Book Ratio |
| Dividend Yield |
| Interest Coverage Ratio |
| Market Capitalisation |
| Net Profit |
| EPS CAGR |
| Asset Turnover |
| Revenue |

Special business rules implemented:

- Financial companies are excluded from Debt-to-Equity filtering.
- Debt Free companies automatically satisfy Interest Coverage filters.

---

# Preset Investment Screeners

Six investment presets were implemented.

## Quality Compounder

Focuses on fundamentally strong businesses.

Criteria:

- ROE > 15%
- Debt/Equity < 1
- Positive Free Cash Flow
- Revenue CAGR > 10%

---

## Value Pick

Designed for undervalued companies.

Criteria:

- Low PE
- Low PB
- Moderate Debt
- Positive Dividend Yield

---

## Growth Accelerator

Targets rapidly growing companies.

Criteria:

- High PAT CAGR
- High Revenue CAGR
- Low Debt

---

## Dividend Champion

Identifies stable dividend-paying companies.

Criteria:

- Dividend Yield > 2%
- Sustainable Dividend Payout
- Positive Free Cash Flow

---

## Debt-Free Blue Chip

Targets financially strong companies.

Criteria:

- Zero Debt
- High ROE
- Large Revenue Base

---

## Turnaround Watch

Designed to identify recovering businesses.

Criteria:

- Improving Revenue Growth
- Positive Free Cash Flow
- Declining Debt

---

# Composite Quality Score

A weighted composite score (0–100) was implemented.

Weight allocation:

| Category | Weight |
|----------|---------|
| Profitability | 35% |
| Cash Quality | 30% |
| Growth | 20% |
| Leverage | 15% |

Features:

- Winsorisation using P10/P90
- Sector-relative normalisation
- Overall quality ranking
- Composite score sorting

---

# Peer Analytics Engine

Implemented:

```
src/analytics/peer.py
```

The peer analytics module computes percentile rankings across all peer groups.

Supported metrics:

- ROE
- ROCE
- Net Profit Margin
- Debt to Equity
- Free Cash Flow
- Revenue CAGR
- PAT CAGR
- EPS CAGR
- Interest Coverage
- Asset Turnover

Debt-to-Equity rankings are automatically inverted so that lower leverage receives a higher percentile.

---

# Peer Group Ranking

The platform computes percentile rankings for all peer groups and stores the results in SQLite.

Each record contains:

- Company ID
- Peer Group
- Financial Metric
- Metric Value
- Percentile Rank
- Financial Year

Companies without an assigned peer group are handled gracefully without generating system errors.

---

# Radar Chart Generation

Radar charts were generated for every company.

Each radar chart compares:

- Company Performance
- Peer Group Average

Eight analytical dimensions are visualised:

- ROE
- ROCE
- Net Profit Margin
- Debt to Equity
- Free Cash Flow
- Revenue CAGR
- PAT CAGR
- Composite Score

Charts are exported as PNG files for reporting purposes.

---

# Excel Reporting

## Screener Report

Generated file:

```
output/screener_output.xlsx
```

Features:

- Six worksheets
- One worksheet per investment preset
- Composite score ranking
- Twenty KPI columns
- Conditional formatting
- Analyst-friendly presentation

---

## Peer Comparison Report

Generated file:

```
output/peer_comparison.xlsx
```

Features:

- Eleven worksheets
- One worksheet per peer group
- Percentile rankings
- Benchmark highlighting
- Median summary row
- Conditional colour coding

---

# SQLite Integration

The following database object was populated:

```
peer_percentiles
```

The table stores:

- Company
- Peer Group
- Metric
- Metric Value
- Percentile Rank
- Financial Year

This enables rapid querying by both the dashboard and API.

---

# Testing & Validation

Sprint validation included:

- Data Quality Rule Testing
- Screener Output Validation
- Peer Ranking Verification
- Manual Business Logic Review
- Excel Output Verification

All Data Quality unit tests completed successfully.

Business validation confirmed:

- All six screeners returned meaningful company sets.
- Peer rankings matched expected financial ordering.
- Generated reports were successfully reviewed.

---

# Deliverables

| Deliverable | Description |
|-------------|-------------|
| `src/screener/engine.py` | Financial screening engine |
| `src/analytics/peer.py` | Peer percentile computation |
| `config/screener_config.yaml` | Analyst-editable screening thresholds |
| `output/screener_output.xlsx` | Six preset screener reports |
| `output/peer_comparison.xlsx` | Peer comparison workbook |
| `reports/radar_charts/` | Radar chart visualisations |
| `peer_percentiles` (SQLite) | Percentile ranking table |

---

# Sprint Outcome

Sprint 3 successfully delivered a configurable financial screener and peer analytics engine capable of analysing all companies within the NIFTY 100 dataset.

The implementation introduced configurable investment presets, composite quality scoring, sector-aware ranking, peer percentile analysis, radar chart visualisation and automated reporting. These capabilities established the analytical foundation for the dashboard, API services and portfolio analytics developed in subsequent sprints.

---

# Technologies Used

- Python 3.11
- Pandas
- NumPy
- SQLite
- OpenPyXL
- Matplotlib
- Plotly
- YAML
- Pytest

---

# Sprint Status

**Sprint 3 Completed Successfully**

**All planned story points achieved.**

**Exit Criteria Met**

- Financial Screener Engine
- Six Preset Screeners
- Composite Quality Score
- Peer Percentile Rankings
- Radar Charts
- Excel Reporting
- SQLite Integration
- Data Quality Validation