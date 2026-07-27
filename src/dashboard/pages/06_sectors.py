import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard.utils.db import (
    get_sector_summary,
    get_sectors,
    get_companies_by_sector,
    get_all_latest_ratios,
    get_pl,
)

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 Sector Analysis Dashboard")
st.caption(
    "Analyze sectors using profitability, revenue and market-cap insights."
)

# ==========================================================
# Cached Data Loaders
# ==========================================================

@st.cache_data
def load_sector_summary():
    return get_sector_summary()


@st.cache_data
def load_sector_details():
    return get_sectors()


@st.cache_data
def load_latest_ratios():
    return get_all_latest_ratios()


sector_summary = load_sector_summary()
sector_details = load_sector_details()
latest_ratios = load_latest_ratios()

# ==========================================================
# Sidebar
# ==========================================================

available_sectors = sorted(
    sector_summary["broad_sector"].dropna().unique().tolist()
)

selected_sector = st.sidebar.selectbox(
    "Select Sector",
    available_sectors,
)

market_caps = ["All"] + sorted(
    sector_details["market_cap_category"]
    .dropna()
    .unique()
    .tolist()
)

selected_market_cap = st.sidebar.selectbox(
    "Market Cap",
    market_caps,
)

# ==========================================================
# Merge Sector + Latest Ratios
# ==========================================================

merged = sector_details.merge(
    latest_ratios,
    on="company_id",
    how="left",
)

# ==========================================================
# Load Latest Revenue
# ==========================================================

sales_list = []

for company_id in merged["company_id"].unique():

    try:

        pl = get_pl(company_id)

        if pl.empty:
            continue

        latest = (
            pl.sort_values("year")
            .iloc[-1]
        )

        sales_list.append(
            {
                "company_id": company_id,
                "revenue": latest["sales"],
            }
        )

    except Exception:
        continue

sales_df = pd.DataFrame(sales_list)

merged = merged.merge(
    sales_df,
    on="company_id",
    how="left",
)

# ==========================================================
# Convert Market Cap Category to Bubble Size
# ==========================================================

market_cap_size = {
    "Large Cap": 100,
    "Mid Cap": 60,
    "Small Cap": 30,
}

merged["bubble_size"] = (
    merged["market_cap_category"]
    .map(market_cap_size)
    .fillna(25)
)

# ==========================================================
# Filter Sector
# ==========================================================

filtered_df = merged[
    merged["broad_sector"] == selected_sector
].copy()

if selected_market_cap != "All":

    filtered_df = filtered_df[
        filtered_df["market_cap_category"]
        == selected_market_cap
    ]

# ==========================================================
# KPI Cards
# ==========================================================

summary = sector_summary[
    sector_summary["broad_sector"] == selected_sector
].iloc[0]

col1, col2 = st.columns(2)

with col1:

    st.metric(
    "Companies",
    int(summary["company_count"]),
)

st.metric(
    "Average Index Weight",
    f"{summary['avg_index_weight']:.2f}%",
)

st.divider()

# ==========================================================
# Company Table
# ==========================================================

st.subheader(f"📋 Companies in {selected_sector}")

display_df = filtered_df[
    [
        "company_name",
        "sub_sector",
        "market_cap_category",
        "index_weight_pct",
        "revenue",
        "return_on_equity_pct",
    ]
].copy()

display_df.columns = [
    "Company",
    "Sub Sector",
    "Market Cap",
    "Index Weight (%)",
    "Revenue",
    "ROE (%)",
]

display_df["Revenue"] = (
    pd.to_numeric(display_df["Revenue"], errors="coerce")
    .round(2)
)

display_df["ROE (%)"] = (
    pd.to_numeric(display_df["ROE (%)"], errors="coerce")
    .round(2)
)

st.dataframe(
    display_df,
    hide_index=True,
    width="stretch",
)

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Sector Data",
    csv,
    file_name=f"{selected_sector}.csv",
    mime="text/csv",
)

st.divider()

# ==========================================================
# Bubble Chart (Sprint Requirement)
# ==========================================================

st.subheader("🫧 Revenue vs ROE")

bubble_df = filtered_df.copy()

bubble_df["revenue"] = pd.to_numeric(
    bubble_df["revenue"],
    errors="coerce",
)

bubble_df["return_on_equity_pct"] = pd.to_numeric(
    bubble_df["return_on_equity_pct"],
    errors="coerce",
)

bubble_df = bubble_df.dropna(
    subset=[
        "revenue",
        "return_on_equity_pct",
    ]
)

if bubble_df.empty:

    st.warning(
        "No Revenue / ROE data available for this sector."
    )

else:

    fig = px.scatter(
        bubble_df,
        x="revenue",
        y="return_on_equity_pct",
        size="bubble_size",
        color="sub_sector",
        hover_name="company_name",
        hover_data={
            "market_cap_category": True,
            "index_weight_pct": ":.2f",
            "revenue": ":,.0f",
            "return_on_equity_pct": ":.2f",
        },
        title="Revenue vs Return on Equity",
        labels={
            "revenue": "Revenue",
            "return_on_equity_pct": "ROE (%)",
        },
        size_max=55,
    )

    fig.update_layout(
        height=650,
        legend_title="Sub Sector",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

st.divider()

# ==========================================================
# Sector Performance Summary
# ==========================================================

st.subheader("📊 Sector Performance Summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)

avg_revenue = pd.to_numeric(
    filtered_df["revenue"],
    errors="coerce",
).mean()

avg_roe = pd.to_numeric(
    filtered_df["return_on_equity_pct"],
    errors="coerce",
).mean()

avg_quality = pd.to_numeric(
    filtered_df["composite_quality_score"],
    errors="coerce",
).mean()

with summary_col1:

    st.metric(
        "Average Revenue",
        f"{avg_revenue:,.2f}"
        if pd.notna(avg_revenue)
        else "N/A",
    )

with summary_col2:

    st.metric(
        "Average ROE",
        f"{avg_roe:.2f}%"
        if pd.notna(avg_roe)
        else "N/A",
    )

with summary_col3:

    st.metric(
        "Average Quality Score",
        f"{avg_quality:.2f}"
        if pd.notna(avg_quality)
        else "N/A",
    )

st.divider()

# ==========================================================
# Top Companies
# ==========================================================

left, right = st.columns(2)

# ----------------------------------------------------------
# Top Revenue Companies
# ----------------------------------------------------------

with left:

    st.subheader("💰 Top Revenue Companies")

    revenue_df = filtered_df.copy()

    revenue_df["revenue"] = pd.to_numeric(
        revenue_df["revenue"],
        errors="coerce",
    )

    revenue_df = (
        revenue_df
        .dropna(subset=["revenue"])
        .sort_values(
            "revenue",
            ascending=False,
        )
        .head(10)
    )

    if revenue_df.empty:

        st.info("No revenue data available.")

    else:

        fig = px.bar(
            revenue_df,
            x="revenue",
            y="company_name",
            orientation="h",
            text="revenue",
            title="Top 10 by Revenue",
        )

        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            xaxis_title="Revenue",
            yaxis_title="Company",
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

# ----------------------------------------------------------
# Top ROE Companies
# ----------------------------------------------------------

with right:

    st.subheader("📈 Top ROE Companies")

    roe_df = filtered_df.copy()

    roe_df["return_on_equity_pct"] = pd.to_numeric(
        roe_df["return_on_equity_pct"],
        errors="coerce",
    )

    roe_df = (
        roe_df
        .dropna(subset=["return_on_equity_pct"])
        .sort_values(
            "return_on_equity_pct",
            ascending=False,
        )
        .head(10)
    )

    if roe_df.empty:

        st.info("No ROE data available.")

    else:

        fig = px.bar(
            roe_df,
            x="return_on_equity_pct",
            y="company_name",
            orientation="h",
            text="return_on_equity_pct",
            title="Top 10 by ROE",
        )

        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            xaxis_title="ROE (%)",
            yaxis_title="Company",
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )
# ==========================================================
# Sector Median KPI Chart (Sprint Requirement)
# ==========================================================

st.subheader("📊 Sector Median KPI Comparison")

kpi_columns = {
    "ROE": "return_on_equity_pct",
    "ROCE": "return_on_capital_employed_pct",
    "Net Profit Margin": "net_profit_margin_pct",
    "Operating Margin": "operating_profit_margin_pct",
    "Debt / Equity": "debt_to_equity",
    "Interest Coverage": "interest_coverage",
    "Revenue CAGR": "revenue_cagr_5yr",
    "PAT CAGR": "pat_cagr_5yr",
    "EPS CAGR": "eps_cagr_5yr",
    "Quality Score": "composite_quality_score",
}

median_values = []

for label, column in kpi_columns.items():

    if column in filtered_df.columns:

        values = pd.to_numeric(
            filtered_df[column],
            errors="coerce",
        )

        median_values.append(
            {
                "KPI": label,
                "Median": values.median(),
            }
        )

median_df = pd.DataFrame(median_values)

median_df = median_df.dropna()

if median_df.empty:

    st.warning("No KPI data available for the selected sector.")

else:

    median_df = median_df.sort_values(
        "Median",
        ascending=False,
    )

    fig = px.bar(
        median_df,
        x="KPI",
        y="Median",
        text="Median",
        title=f"Median Financial KPIs — {selected_sector}",
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
    )

    fig.update_layout(
        xaxis_title="Financial KPI",
        yaxis_title="Median Value",
        height=500,
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )        

st.divider()

# ==========================================================
# Sector Statistics
# ==========================================================

st.subheader("📑 Sector Statistics")

stats = filtered_df.copy()

stats["revenue"] = pd.to_numeric(
    stats["revenue"],
    errors="coerce",
)

stats["return_on_equity_pct"] = pd.to_numeric(
    stats["return_on_equity_pct"],
    errors="coerce",
)

stats["composite_quality_score"] = pd.to_numeric(
    stats["composite_quality_score"],
    errors="coerce",
)

statistics = pd.DataFrame(
    {
        "Metric": [
            "Companies",
            "Sub-sectors",
            "Average Revenue",
            "Highest Revenue",
            "Average ROE (%)",
            "Highest ROE (%)",
            "Average Quality Score",
        ],
        "Value": [
            len(stats),
            stats["sub_sector"].nunique(),
            round(stats["revenue"].mean(), 2),
            round(stats["revenue"].max(), 2),
            round(stats["return_on_equity_pct"].mean(), 2),
            round(stats["return_on_equity_pct"].max(), 2),
            round(stats["composite_quality_score"].mean(), 2),
        ],
    }
)

st.dataframe(
    statistics,
    hide_index=True,
    width="stretch",
)

st.divider()

# ==========================================================
# Key Insights
# ==========================================================

st.subheader("💡 Key Insights")

if not filtered_df.empty:

    # Highest Revenue
    revenue_df = filtered_df.dropna(subset=["revenue"])

    if not revenue_df.empty:

        highest_revenue = revenue_df.loc[
            revenue_df["revenue"].idxmax()
        ]

        st.success(
            f"💰 Highest Revenue: **{highest_revenue['company_name']}** "
            f"({highest_revenue['revenue']:,.2f})"
        )

    # Highest ROE
    roe_df = filtered_df.dropna(
        subset=["return_on_equity_pct"]
    )

    if not roe_df.empty:

        highest_roe = roe_df.loc[
            roe_df["return_on_equity_pct"].idxmax()
        ]

        st.info(
            f"📈 Highest ROE: **{highest_roe['company_name']}** "
            f"({highest_roe['return_on_equity_pct']:.2f}%)"
        )

    # Highest Quality Score
    quality_df = filtered_df.dropna(
        subset=["composite_quality_score"]
    )

    if not quality_df.empty:

        best_quality = quality_df.loc[
            quality_df["composite_quality_score"].idxmax()
        ]

        st.info(
            f"⭐ Best Quality Score: **{best_quality['company_name']}** "
            f"({best_quality['composite_quality_score']:.2f})"
        )

else:

    st.warning(
        "No data available for the selected sector."
    )

st.divider()

# ==========================================================
# Dataset Information
# ==========================================================

with st.expander("ℹ️ Dataset Information"):

    st.markdown(
        """
This dashboard combines information from multiple datasets:

- Company Sector Classification
- Latest Financial Ratios
- Profit & Loss Statements

### Bubble Chart

- **X-axis:** Latest Revenue
- **Y-axis:** Return on Equity (ROE)
- **Bubble Size:** Market Cap Category
- **Bubble Color:** Sub-sector

This visualization helps identify high-performing companies with
strong profitability while comparing them across different sub-sectors.
"""
    )

st.divider()

# ==========================================================
# Footer
# ==========================================================

st.caption(
    "Financial Intelligence Platform • Sprint 2 • Sector Analysis Dashboard"
)

