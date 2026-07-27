import streamlit as st
import pandas as pd

from src.dashboard.utils.db import (
        get_all_latest_ratios,
    get_sectors,
)

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="Stock Screener",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Stock Screener")
st.caption("Filter companies using financial metrics.")

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

@st.cache_data
def load_data():

    ratios = get_all_latest_ratios()
    sectors = get_sectors()

    df = ratios.merge(
        sectors[
            [
                "company_id",
                "broad_sector",
                "sub_sector",
                "market_cap_category",
            ]
        ],
        on="company_id",
        how="left",
    )

    return df


df = load_data()

# -------------------------------------------------------
# Presets
# -------------------------------------------------------

PRESETS = {
    "Custom": {
        "roe": 15.0,
        "de": 1.00,
        "fcf": 0.0,
        "rev": 10.0,
        "pat": 10.0,
        "opm": 15.0,
        "icr": 3.0,
        "quality": 50,
    },

    "Quality": {
        "roe": 20.0,
        "de": 0.50,
        "fcf": 0.0,
        "rev": 10.0,
        "pat": 10.0,
        "opm": 20.0,
        "icr": 5.0,
        "quality": 75,
    },

    "Value": {
        "roe": 12.0,
        "de": 1.00,
        "fcf": 0.0,
        "rev": 5.0,
        "pat": 5.0,
        "opm": 10.0,
        "icr": 2.0,
        "quality": 40,
    },

    "Growth": {
        "roe": 15.0,
        "de": 1.50,
        "fcf": 0.0,
        "rev": 20.0,
        "pat": 20.0,
        "opm": 15.0,
        "icr": 3.0,
        "quality": 60,
    },

    "Dividend": {
        "roe": 10.0,
        "de": 1.00,
        "fcf": 0.0,
        "rev": 5.0,
        "pat": 5.0,
        "opm": 10.0,
        "icr": 2.0,
        "quality": 40,
    },

    "Debt-Free": {
        "roe": 10.0,
        "de": 0.20,
        "fcf": 0.0,
        "rev": 5.0,
        "pat": 5.0,
        "opm": 10.0,
        "icr": 3.0,
        "quality": 50,
    },

    "Turnaround": {
        "roe": 5.0,
        "de": 2.00,
        "fcf": -1000.0,
        "rev": 5.0,
        "pat": 5.0,
        "opm": 5.0,
        "icr": 1.0,
        "quality": 30,
    },
}

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.header("Screening Filters")

preset = st.sidebar.radio(
    "Quick Preset",
    list(PRESETS.keys()),
)

preset_values = PRESETS[preset]

# -------------------------------------------------------
# Financial Filters
# -------------------------------------------------------

roe_min = st.sidebar.slider(
    "Minimum ROE (%)",
    min_value=0.0,
    max_value=50.0,
    value=float(preset_values["roe"]),
    step=1.0,
)

de_max = st.sidebar.slider(
    "Maximum Debt / Equity",
    min_value=0.0,
    max_value=5.0,
    value=float(preset_values["de"]),
    step=0.1,
)

fcf_min = st.sidebar.slider(
    "Minimum Free Cash Flow (Cr)",
    min_value=-5000.0,
    max_value=100000.0,
    value=float(preset_values["fcf"]),
    step=100.0,
)

rev_cagr = st.sidebar.slider(
    "Minimum Revenue CAGR (%)",
    min_value=-20.0,
    max_value=50.0,
    value=float(preset_values["rev"]),
    step=1.0,
)

pat_cagr = st.sidebar.slider(
    "Minimum PAT CAGR (%)",
    min_value=-20.0,
    max_value=50.0,
    value=float(preset_values["pat"]),
    step=1.0,
)

opm_min = st.sidebar.slider(
    "Minimum Operating Profit Margin (%)",
    min_value=-20.0,
    max_value=60.0,
    value=float(preset_values["opm"]),
    step=1.0,
)

icr_min = st.sidebar.slider(
    "Minimum Interest Coverage",
    min_value=0.0,
    max_value=30.0,
    value=float(preset_values["icr"]),
    step=0.5,
)

quality_min = st.sidebar.slider(
    "Minimum Composite Quality Score",
    min_value=0,
    max_value=100,
    value=int(preset_values["quality"]),
    step=1,
)

# -------------------------------------------------------
# Sector Filter
# -------------------------------------------------------

sector_options = ["All"] + sorted(
    df["broad_sector"]
    .dropna()
    .unique()
    .tolist()
)

selected_sector = st.sidebar.selectbox(
    "Sector",
    sector_options,
)

# -------------------------------------------------------
# Market Cap Filter
# -------------------------------------------------------

market_cap_options = ["All"] + sorted(
    df["market_cap_category"]
    .dropna()
    .unique()
    .tolist()
)

selected_market_cap = st.sidebar.selectbox(
    "Market Cap",
    market_cap_options,
)

# -------------------------------------------------------
# Information
# -------------------------------------------------------

if preset == "Dividend":
    st.sidebar.info(
        "Dividend Yield data is unavailable in the current database. "
        "This preset uses conservative profitability filters instead."
    )

st.sidebar.divider()

st.sidebar.caption(
    "Adjust the filters to narrow down companies matching your investment criteria."
)

# -------------------------------------------------------
# Apply Filters
# -------------------------------------------------------

filtered = df.copy()

# Financial Filters
filtered = filtered[
    filtered["return_on_equity_pct"].fillna(-999) >= roe_min
]

filtered = filtered[
    filtered["debt_to_equity"].fillna(999) <= de_max
]

filtered = filtered[
    filtered["free_cash_flow_cr"].fillna(-999999) >= fcf_min
]

filtered = filtered[
    filtered["revenue_cagr_5yr"].fillna(-999) >= rev_cagr
]

filtered = filtered[
    filtered["pat_cagr_5yr"].fillna(-999) >= pat_cagr
]

filtered = filtered[
    filtered["operating_profit_margin_pct"].fillna(-999) >= opm_min
]

filtered = filtered[
    filtered["interest_coverage"].fillna(-999) >= icr_min
]

filtered = filtered[
    filtered["composite_quality_score"].fillna(-999) >= quality_min
]

# Sector Filter
if selected_sector != "All":
    filtered = filtered[
        filtered["broad_sector"] == selected_sector
    ]

# Market Cap Filter
if selected_market_cap != "All":
    filtered = filtered[
        filtered["market_cap_category"] == selected_market_cap
    ]

# -------------------------------------------------------
# Sort Results
# -------------------------------------------------------

filtered = filtered.sort_values(
    by=[
        "composite_quality_score",
        "return_on_equity_pct",
        "revenue_cagr_5yr",
    ],
    ascending=False,
)

# -------------------------------------------------------
# Results Header
# -------------------------------------------------------

st.subheader("📋 Screening Results")

st.info(
    f"Found **{len(filtered)}** companies matching the selected filters."
)

# -------------------------------------------------------
# Display Table
# -------------------------------------------------------

display_columns = [
    "company_name",
    "broad_sector",
    "sub_sector",
    "market_cap_category",
    "return_on_equity_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "composite_quality_score",
]

display_df = filtered[display_columns].copy()

display_df.columns = [
    "Company",
    "Sector",
    "Sub Sector",
    "Market Cap",
    "ROE %",
    "OPM %",
    "Debt/Equity",
    "Interest Coverage",
    "Free Cash Flow (Cr)",
    "Revenue CAGR %",
    "PAT CAGR %",
    "EPS CAGR %",
    "Quality Score",
]

st.dataframe(
    display_df,
    hide_index=True,
    width="stretch",
)

# -------------------------------------------------------
# Download CSV
# -------------------------------------------------------

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Results",
    data=csv,
    file_name="stock_screener_results.csv",
    mime="text/csv",
    width="stretch",
)

# -------------------------------------------------------
# Empty Result Handling
# -------------------------------------------------------

if display_df.empty:

    st.warning(
        "No companies matched the selected screening criteria. "
        "Try relaxing one or more filters."
    )

    st.stop()

# -------------------------------------------------------
# KPI Dashboard
# -------------------------------------------------------

st.divider()

st.subheader("📊 Screening Summary")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    "Companies",
    len(display_df),
)

kpi2.metric(
    "Average ROE",
    f"{display_df['ROE %'].mean():.2f}%"
)

kpi3.metric(
    "Average Quality",
    f"{display_df['Quality Score'].mean():.2f}"
)

kpi4.metric(
    "Average Revenue CAGR",
    f"{display_df['Revenue CAGR %'].mean():.2f}%"
)

# -------------------------------------------------------
# Top Companies
# -------------------------------------------------------

st.divider()

st.subheader("🏆 Top 10 Companies")

top10 = display_df.sort_values(
    by="Quality Score",
    ascending=False,
).head(10)

st.dataframe(
    top10,
    hide_index=True,
    width="stretch",
)

# -------------------------------------------------------
# Sector Distribution
# -------------------------------------------------------

st.divider()

st.subheader("🏭 Sector Distribution")

sector_summary = (
    filtered.groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
    .sort_values(
        "Companies",
        ascending=False,
    )
)

if not sector_summary.empty:

    st.bar_chart(
        sector_summary.set_index("broad_sector"),
        width="stretch",
    )

# -------------------------------------------------------
# Quality Score Distribution
# -------------------------------------------------------

st.divider()

st.subheader("⭐ Quality Score Distribution")

quality_dist = (
    filtered["composite_quality_score"]
    .dropna()
    .round()
    .value_counts()
    .sort_index()
)

if not quality_dist.empty:

    st.line_chart(
        quality_dist,
        width="stretch",
    )

# -------------------------------------------------------
# Sector-wise Average ROE
# -------------------------------------------------------

st.divider()

st.subheader("📈 Average ROE by Sector")

sector_roe = (
    filtered.groupby("broad_sector")[
        "return_on_equity_pct"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
)

if not sector_roe.empty:

    st.bar_chart(
        sector_roe,
        width="stretch",
    )

# -------------------------------------------------------
# Database Information
# -------------------------------------------------------

st.divider()

with st.expander("ℹ️ About this Screener"):

    st.markdown(
        """
### Metrics Used

- Return on Equity (ROE)
- Debt to Equity
- Free Cash Flow
- Revenue CAGR (5 Years)
- PAT CAGR (5 Years)
- Operating Profit Margin
- Interest Coverage Ratio
- Composite Quality Score

### Notes

- P/E Ratio is not available in the current database.
- P/B Ratio is not available in the current database.
- Dividend Yield is not available in the current database.
- Screening is performed using the latest available financial ratios.
        """
    )

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.divider()

st.caption(
    "Financial Intelligence Platform • Sprint 2 • Stock Screener Dashboard"
)

