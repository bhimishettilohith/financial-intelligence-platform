# Sprint 4 Retrospective

## Sprint Objective

The objective of Sprint 4 was to develop a complete interactive dashboard for the Financial Intelligence Platform using Streamlit. The dashboard enables users to explore company financial data, compare peer companies, analyse historical trends, evaluate sector performance, review capital allocation, and access company reports through an intuitive interface.

---

## UX Decisions

Several design decisions were made to improve usability and consistency:

- Implemented a sidebar navigation for easy access to all dashboard modules.
- Maintained a consistent layout, spacing, and styling across all screens.
- Used interactive Plotly visualisations for better data exploration.
- Displayed financial metrics using KPI cards where appropriate.
- Designed responsive charts using Streamlit container-width support.
- Kept user interactions simple through dropdown selections and filters.

---

## Data Edge Cases Identified

During integration testing, the following edge cases were identified and handled:

- Companies with fewer than 10 years of historical financial data.
- Missing or null financial values.
- Empty screener results when extreme filter values were selected.
- Missing annual reports or supporting documents.
- Charts with limited historical observations.

Where financial data was unavailable, the dashboard displayed **"N/A"** instead of generating runtime errors.

---

## Performance Findings

Performance testing was carried out using multiple companies from different sectors.

Observations:

- Company Profile page consistently loaded in under **3 seconds**.
- Dashboard navigation remained responsive.
- Database queries executed efficiently using SQLite.
- Plotly charts rendered without layout or sizing issues.
- No crashes occurred during integration testing.

---

## Testing Summary

The dashboard was tested using companies from the following sectors:

- Information Technology
- Financial Services
- FMCG
- Energy
- Healthcare

Testing covered:

- All eight dashboard screens
- Partial historical datasets
- Missing values
- Extreme screener filters
- Chart responsiveness
- Navigation flow

---

## Challenges Faced

- Handling companies with incomplete historical data.
- Ensuring missing values did not interrupt dashboard rendering.
- Maintaining consistent layouts across all dashboard pages.
- Validating dashboard behaviour across multiple sectors.

---

## Outcome

Sprint 4 was successfully completed with all planned dashboard modules implemented, tested, and integrated. The application provides a stable, responsive, and user-friendly interface for financial data analysis and is ready for demonstration.