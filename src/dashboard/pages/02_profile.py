import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.utils.db import (
    get_companies,
    get_company_profile,
    get_latest_ratios,
    get_pl,
    get_pros_cons,
    get_ratios,
)

st.set_page_config(
    page_title="Company Profile",
    layout="wide",
)

st.title("🏢 Company Profile")

# ==========================================================
# Company Selector
# ==========================================================

companies = get_companies()

company_name = st.selectbox(
    "Search Company",
    companies["company_name"].tolist(),
    index=None,
    placeholder="Search company...",
)

if company_name is None:
    st.info("Select a company from the dropdown.")
    st.stop()

company_id = companies.loc[companies["company_name"] == company_name, "id"].iloc[0]

# ==========================================================
# Load Data
# ==========================================================

profile = get_company_profile(company_id)
ratios = get_ratios(company_id)
latest = get_latest_ratios(company_id)
pl = get_pl(company_id)
pros_cons = get_pros_cons(company_id)

if profile.empty:
    st.error("Company profile not found.")
    st.stop()

profile = profile.iloc[0]

# ==========================================================
# Header
# ==========================================================

st.markdown("---")

col1, col2 = st.columns([3, 1])

with col1:

    st.markdown(f"""
# {profile.get('company_name', company_name)}
**Ticker :** {company_id}
""")

    if "sector" in profile.index:
        st.write("**Sector:**", profile["sector"])

    if "broad_sector" in profile.index:
        st.write("**Broad Sector:**", profile["broad_sector"])

    if "sub_sector" in profile.index:
        st.write("**Sub Sector:**", profile["sub_sector"])

with col2:

    if "website" in profile.index:

        website = profile["website"]

        if pd.notna(website) and str(website).strip():

            st.link_button(
                "🌐 Company Website",
                website,
            )

if "about_company" in profile.index:

    about = profile["about_company"]

    if pd.notna(about):

        st.info(about)

st.divider()

# ==========================================================
# Latest KPI Cards
# ==========================================================

if latest.empty:

    st.warning("No financial ratios available.")

    st.stop()

latest = latest.iloc[0]

c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

c1.metric("ROE", f"{latest['return_on_equity_pct']:.2f}%")

c2.metric("ROCE", f"{latest['return_on_capital_employed_pct']:.2f}%")

c3.metric("Net Profit Margin", f"{latest['net_profit_margin_pct']:.2f}%")

c4.metric("Debt / Equity", f"{latest['debt_to_equity']:.2f}")

c5.metric("Revenue CAGR", f"{latest['revenue_cagr_5yr']:.2f}%")

c6.metric("Quality Score", f"{latest['composite_quality_score']:.2f}")

st.divider()

# ==========================================================
# Revenue vs Net Profit
# ==========================================================

if not pl.empty:

    revenue_chart = px.bar(
        pl.sort_values("year"),
        x="year",
        y=[
            "sales",
            "net_profit",
        ],
        barmode="group",
        title="Revenue vs Net Profit",
    )

    revenue_chart.update_layout(
        xaxis_title="Year",
        yaxis_title="₹ Crore",
    )

    st.plotly_chart(
        revenue_chart,
        width="stretch",
    )

st.divider()

# ==========================================================
# ROE vs ROCE Trend
# ==========================================================

if not ratios.empty:

    trend = px.line(
        ratios.sort_values("year"),
        x="year",
        y=[
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
        ],
        markers=True,
        title="ROE vs ROCE Trend",
    )

    trend.update_layout(
        xaxis_title="Year",
        yaxis_title="Percentage",
    )

    st.plotly_chart(
        trend,
        width="stretch",
    )

st.divider()


# ==========================================================
# Pros & Cons
# ==========================================================

st.subheader("Pros & Cons")

if pros_cons.empty:

    st.info("No Pros & Cons available.")

else:

    left, right = st.columns(2)

    with left:

        st.success("Pros")

        if "pros" in pros_cons.columns:

            for item in pros_cons["pros"].dropna():

                if str(item).strip():
                    st.markdown(f"✅ {item}")

    with right:

        st.error("Cons")

        if "cons" in pros_cons.columns:

            for item in pros_cons["cons"].dropna():

                if str(item).strip():
                    st.markdown(f"❌ {item}")

st.divider()

# ==========================================================
# Financial Health Summary
# ==========================================================

st.subheader("Financial Health Summary")

health1, health2 = st.columns(2)

with health1:

    st.metric("Interest Coverage", f"{latest['interest_coverage']:.2f}")

    st.metric("Asset Turnover", f"{latest['asset_turnover']:.2f}")

    st.metric("Return on Assets", f"{latest['return_on_assets_pct']:.2f}%")

with health2:

    st.metric("Free Cash Flow", f"{latest['free_cash_flow_cr']:.2f} Cr")

    st.metric("Cash From Operations", f"{latest['cash_from_operations_cr']:.2f} Cr")

    st.metric("Net Debt", f"{latest['net_debt']:.2f} Cr")

st.divider()

# ==========================================================
# Operating Profit Trend
# ==========================================================

if not pl.empty:

    st.subheader("Operating Profit Trend")

    fig = px.line(
        pl.sort_values("year"),
        x="year",
        y="operating_profit",
        markers=True,
        title="Operating Profit",
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="₹ Crore",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

st.divider()

# ==========================================================
# EPS Trend
# ==========================================================

if not pl.empty:

    st.subheader("EPS Trend")

    fig = px.bar(pl.sort_values("year"), x="year", y="eps", title="Earnings Per Share")

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="EPS",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

st.divider()

# ==========================================================
# Dividend Payout Trend
# ==========================================================

if not pl.empty:

    st.subheader("Dividend Payout")

    fig = px.line(
        pl.sort_values("year"),
        x="year",
        y="dividend_payout",
        markers=True,
        title="Dividend Payout Ratio",
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Dividend %",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

st.divider()

# ==========================================================
# Key Financial Highlights
# ==========================================================

st.subheader("Key Financial Highlights")

highlights = pd.DataFrame(
    {
        "Metric": [
            "ROE",
            "ROCE",
            "Net Profit Margin",
            "Debt to Equity",
            "Revenue CAGR (5Y)",
            "PAT CAGR (5Y)",
            "EPS CAGR (5Y)",
            "Quality Score",
            "Operating Margin",
            "Interest Coverage",
            "Asset Turnover",
        ],
        "Value": [
            f"{latest['return_on_equity_pct']:.2f} %",
            f"{latest['return_on_capital_employed_pct']:.2f} %",
            f"{latest['net_profit_margin_pct']:.2f} %",
            f"{latest['debt_to_equity']:.2f}",
            f"{latest['revenue_cagr_5yr']:.2f} %",
            f"{latest['pat_cagr_5yr']:.2f} %",
            f"{latest['eps_cagr_5yr']:.2f} %",
            f"{latest['composite_quality_score']:.2f}",
            f"{latest['operating_profit_margin_pct']:.2f} %",
            f"{latest['interest_coverage']:.2f}",
            f"{latest['asset_turnover']:.2f}",
        ],
    }
)

st.dataframe(
    highlights,
    hide_index=True,
    width="stretch",
)

st.divider()

st.success("Company Profile Loaded Successfully ✅")
