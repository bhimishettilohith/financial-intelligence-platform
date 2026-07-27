# Sprint 4 – Dashboard & Visualization

## Overview

Sprint 4 focuses on building an interactive Streamlit dashboard for the Financial Intelligence Platform. The dashboard provides users with an intuitive interface to explore company financial data, compare peers, analyse trends, evaluate sectors, and access company reports.

---

## Running the Dashboard

Activate the project environment and start the dashboard:

```bash
python -m streamlit run src/dashboard/app.py
```

> Note: In some environments, the following command may also work:

```bash
streamlit run src/dashboard/app.py
```

The dashboard will open automatically in your default web browser.

---

## Dashboard Screens

### 1. Home

**Purpose**

Provides an overview of the dashboard and quick navigation to all available modules.

**Features**

- Dashboard introduction
- Summary statistics
- Quick navigation
- Clean landing page

---

### 2. Company Profile

**Purpose**

Displays detailed information for an individual company.

**Features**

- Company overview
- Key financial ratios
- Profit & Loss summary
- Balance Sheet summary
- Cash Flow summary
- Pros & Cons
- Company documents

---

### 3. Screener

**Purpose**

Allows users to filter companies based on financial metrics.

**Features**

- ROE filter
- ROCE filter
- Debt-to-Equity filter
- Revenue Growth filter
- Market Capitalisation filter
- Dynamic filtering
- Interactive results table

---

### 4. Peer Comparison

**Purpose**

Compares a selected company with its peer group.

**Features**

- Peer group comparison
- Average peer metrics
- Percentile analysis
- Financial comparison tables

---

### 5. Financial Trends

**Purpose**

Visualises historical financial performance.

**Features**

- Revenue trends
- Profit trends
- Margin trends
- Multi-year financial charts

---

### 6. Sector Analysis

**Purpose**

Provides sector-level insights.

**Features**

- Sector summary
- Company distribution
- Sector statistics
- Company listings

---

### 7. Capital Allocation

**Purpose**

Displays capital allocation and valuation-related financial metrics.

**Features**

- Operating Cash Flow
- Investing Cash Flow
- Financing Cash Flow
- Free Cash Flow calculations
- Capital allocation visualisations

---

### 8. Reports

**Purpose**

Provides access to company reports and supporting documents.

**Features**

- Annual reports
- Financial documents
- Report download links

---

## Sprint 4 Integration Testing

The dashboard was tested across multiple sectors, including:

- Information Technology
- Financial Services
- FMCG
- Energy
- Healthcare

Testing included:

- Dashboard navigation
- Chart rendering
- Partial historical datasets
- Missing values
- Extreme screener filter values
- Responsive layouts

---

## Sprint 4 Retrospective

### UX Decisions

- Designed a simple sidebar navigation for easy access to all dashboard pages.
- Maintained a consistent layout and styling across all screens.
- Used interactive Plotly visualisations for improved data exploration.
- Ensured responsive charts using Streamlit's container width support.

### Data Edge Cases

The dashboard was tested against several edge cases:

- Companies with limited historical financial data
- Missing financial metrics
- Empty screener results
- Missing reports or documents
- Null and NaN values

Where data was unavailable, the dashboard safely displayed **"N/A"** instead of causing runtime errors.

### Performance Findings

- Company Profile page tested using five different companies.
- Average loading time remained below **3 seconds**.
- Dashboard navigation remained responsive during testing.
- All visualisations rendered successfully without overflow issues.

---

## Sprint 4 Completion Status

| Task | Status |
|------|--------|
| Dashboard Home | ✅ Completed |
| Company Profile | ✅ Completed |
| Screener | ✅ Completed |
| Peer Comparison | ✅ Completed |
| Financial Trends | ✅ Completed |
| Sector Analysis | ✅ Completed |
| Capital Allocation | ✅ Completed |
| Reports | ✅ Completed |
| Valuation Module | ✅ Completed |
| Integration Testing | ✅ Completed |
| Bug Fixes | ✅ Completed |

---

## Future Improvements

- Advanced company comparison
- Export dashboard visualisations
- Portfolio tracking
- Live market data integration
- Additional financial ratios
- Dark mode support