import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_ratios_by_year,
    get_sectors,
)

st.title("🏠 Home Dashboard")

# ---------------- Sidebar ----------------

year = st.sidebar.selectbox(
    "Reporting Year",
    ["2024", "2023", "2022", "2021", "2020", "2019"],
)

ratios = get_ratios_by_year(year)
sectors = get_sectors()

# ---------------- KPI ----------------

st.subheader("Key Performance Indicators")

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Average ROE",
    f"{ratios['return_on_equity_pct'].mean():.2f}%"
)

c2.metric(
    "Median EPS",
    f"{ratios['earnings_per_share'].median():.2f}"
)

c3.metric(
    "Median D/E",
    f"{ratios['debt_to_equity'].median():.2f}"
)

c4.metric(
    "Companies",
    len(ratios)
)

c5.metric(
    "Revenue CAGR",
    f"{ratios['revenue_cagr_5yr'].median():.2f}%"
)

c6.metric(
    "Debt Free",
    int((ratios["debt_to_equity"] == 0).sum())
)

st.divider()

# ---------------- Charts ----------------

left, right = st.columns([2, 1])

with left:

    sector_summary = (
        sectors.groupby("broad_sector")
        .size()
        .reset_index(name="Companies")
    )

    fig = px.pie(
        sector_summary,
        names="broad_sector",
        values="Companies",
        hole=0.55,
        title="Sector Breakdown"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

with right:

    st.subheader("Top 5 Quality Companies")

    top5 = (
        ratios[
            [
                "company_name",
                "composite_quality_score",
            ]
        ]
        .sort_values(
            "composite_quality_score",
            ascending=False,
        )
        .head(5)
    )

    st.dataframe(
        top5,
        hide_index=True,
        use_container_width=True,
    )