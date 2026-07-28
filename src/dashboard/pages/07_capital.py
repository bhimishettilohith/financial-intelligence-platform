import plotly.express as px
import streamlit as st

from src.dashboard.utils.db import get_all_latest_ratios

st.set_page_config(
    page_title="Capital Allocation Map",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Capital Allocation Map")
st.caption("Treemap of NIFTY companies grouped by capital allocation patterns.")

# ==========================================================
# Load Data
# ==========================================================


@st.cache_data
def load_ratios():
    return get_all_latest_ratios()


df = load_ratios()

# ==========================================================
# Capital Allocation Pattern Classification
# ==========================================================


def classify_pattern(row):

    # ------------------------------------------------------
    # Compounders
    # ------------------------------------------------------
    if (
        row["composite_quality_score"] >= 80
        and row["return_on_equity_pct"] >= 18
        and row["revenue_cagr_5yr"] >= 12
    ):
        return "Compounders"

    # ------------------------------------------------------
    # Growth Reinvestors
    # ------------------------------------------------------
    elif row["capex_intensity_pct"] >= 20 and row["revenue_cagr_5yr"] >= 10:
        return "Growth Reinvestors"

    # ------------------------------------------------------
    # Cash Generators
    # ------------------------------------------------------
    elif row["free_cash_flow_cr"] > 0 and row["cfo_quality_score"] >= 70:
        return "Cash Generators"

    # ------------------------------------------------------
    # Dividend Leaders
    # ------------------------------------------------------
    elif row["dividend_payout_ratio_pct"] >= 40:
        return "Dividend Leaders"

    # ------------------------------------------------------
    # Efficient Capital Allocators
    # ------------------------------------------------------
    elif row["return_on_capital_employed_pct"] >= 20 and row["debt_to_equity"] <= 0.5:
        return "Efficient Capital Allocators"

    # ------------------------------------------------------
    # Deleveraging Companies
    # ------------------------------------------------------
    elif row["debt_to_equity"] <= 0.30 or row["net_debt"] <= 0:
        return "Deleveraging Companies"

    # ------------------------------------------------------
    # Turnaround Stories
    # ------------------------------------------------------
    elif (
        row["revenue_cagr_flag"] == "TURNAROUND"
        or row["pat_cagr_flag"] == "TURNAROUND"
        or row["eps_cagr_flag"] == "TURNAROUND"
    ):
        return "Turnaround Stories"

    # ------------------------------------------------------
    # Default
    # ------------------------------------------------------
    else:
        return "Average Performers"


df["capital_pattern"] = df.apply(
    classify_pattern,
    axis=1,
)

# ==========================================================
# Dashboard KPIs
# ==========================================================

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        "Companies",
        len(df),
    )

with kpi2:
    st.metric(
        "Capital Allocation Patterns",
        df["capital_pattern"].nunique(),
    )

with kpi3:
    st.metric(
        "Average Quality Score",
        f"{df['composite_quality_score'].mean():.1f}",
    )

st.divider()

# ==========================================================
# Treemap Data
# ==========================================================

pattern_summary = df.groupby("capital_pattern", as_index=False).agg(
    company_count=("company_id", "count"),
    avg_quality=("composite_quality_score", "mean"),
)

fig = px.treemap(
    pattern_summary,
    path=["capital_pattern"],
    values="company_count",
    color="avg_quality",
    color_continuous_scale="Viridis",
    hover_data={
        "company_count": True,
        "avg_quality": ":.1f",
    },
    title="Capital Allocation Patterns",
)

fig.update_traces(
    textinfo="label+value",
)

fig.update_layout(
    margin=dict(t=40, l=10, r=10, b=10),
    height=650,
)

from streamlit_plotly_events import plotly_events

selected_points = plotly_events(
    fig,
    click_event=True,
    hover_event=False,
    select_event=False,
    override_height=650,
)

st.info(
    "💡 Tip: Click a block in the treemap to zoom into that capital allocation pattern."
)

st.divider()

# ==========================================================
# Pattern Selection
# ==========================================================

patterns = sorted(df["capital_pattern"].unique())

selected_pattern = st.selectbox(
    "Select Capital Allocation Pattern",
    patterns,
)

filtered_df = df[df["capital_pattern"] == selected_pattern].copy()

left, right = st.columns([2, 1])

with left:

    st.subheader(f"Companies in '{selected_pattern}'")

with right:

    st.metric(
        "Companies",
        len(filtered_df),
    )

st.dataframe(
    filtered_df[
        [
            "company_name",
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "dividend_payout_ratio_pct",
            "composite_quality_score",
        ]
    ].rename(
        columns={
            "company_name": "Company",
            "return_on_equity_pct": "ROE %",
            "return_on_capital_employed_pct": "ROCE %",
            "debt_to_equity": "Debt / Equity",
            "free_cash_flow_cr": "Free Cash Flow",
            "dividend_payout_ratio_pct": "Dividend Payout %",
            "composite_quality_score": "Quality Score",
        }
    ),
    hide_index=True,
    width="stretch",
)

csv = filtered_df.to_csv(index=False)

st.download_button(
    "⬇ Download Company List",
    csv,
    file_name=f"{selected_pattern.lower().replace(' ', '_')}.csv",
    mime="text/csv",
)

st.divider()

# ==========================================================
# Pattern Summary
# ==========================================================

st.subheader("📊 Pattern Performance Summary")

col1, col2, col3, col4 = st.columns(4)

avg_roe = filtered_df["return_on_equity_pct"].mean()
avg_roce = filtered_df["return_on_capital_employed_pct"].mean()
avg_quality = filtered_df["composite_quality_score"].mean()
avg_fcf = filtered_df["free_cash_flow_cr"].mean()

with col1:
    st.metric("Average ROE", f"{avg_roe:.2f}%")

with col2:
    st.metric("Average ROCE", f"{avg_roce:.2f}%")

with col3:
    st.metric("Average Quality", f"{avg_quality:.1f}")

with col4:
    st.metric("Average FCF", f"{avg_fcf:,.0f}")

st.divider()

# ==========================================================
# Distribution of Companies
# ==========================================================

st.subheader("📈 Company Distribution")

distribution = (
    df.groupby("capital_pattern")
    .size()
    .reset_index(name="Companies")
    .sort_values("Companies", ascending=False)
)

fig = px.bar(
    distribution,
    x="capital_pattern",
    y="Companies",
    text="Companies",
    color="Companies",
    title="Companies by Capital Allocation Pattern",
)

fig.update_traces(textposition="outside")

fig.update_layout(
    xaxis_title="Pattern",
    yaxis_title="Number of Companies",
    height=500,
)

st.plotly_chart(
    fig,
    width="stretch",
)

st.divider()

# ==========================================================
# Top Companies
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("🏆 Highest ROE")

    top_roe = filtered_df.sort_values(
        "return_on_equity_pct",
        ascending=False,
    ).head(10)

    fig = px.bar(
        top_roe,
        x="return_on_equity_pct",
        y="company_name",
        orientation="h",
        text="return_on_equity_pct",
        title="Top 10 ROE",
    )

    fig.update_layout(yaxis=dict(categoryorder="total ascending"))

    st.plotly_chart(
        fig,
        width="stretch",
    )

with right:

    st.subheader("💰 Highest Free Cash Flow")

    top_fcf = filtered_df.sort_values(
        "free_cash_flow_cr",
        ascending=False,
    ).head(10)

    fig = px.bar(
        top_fcf,
        x="free_cash_flow_cr",
        y="company_name",
        orientation="h",
        text="free_cash_flow_cr",
        title="Top 10 Free Cash Flow",
    )

    fig.update_layout(yaxis=dict(categoryorder="total ascending"))

    st.plotly_chart(
        fig,
        width="stretch",
    )

st.divider()

# ==========================================================
# Capital Allocation Insights
# ==========================================================

st.subheader("💡 Capital Allocation Insights")

best_roe = filtered_df.loc[filtered_df["return_on_equity_pct"].idxmax()]

best_roce = filtered_df.loc[filtered_df["return_on_capital_employed_pct"].idxmax()]

best_quality = filtered_df.loc[filtered_df["composite_quality_score"].idxmax()]

highest_fcf = filtered_df.loc[filtered_df["free_cash_flow_cr"].idxmax()]

st.success(
    f"🏆 Highest ROE: **{best_roe['company_name']}** "
    f"({best_roe['return_on_equity_pct']:.2f}%)"
)

st.info(
    f"⭐ Highest ROCE: **{best_roce['company_name']}** "
    f"({best_roce['return_on_capital_employed_pct']:.2f}%)"
)

st.info(
    f"💎 Best Quality Score: **{best_quality['company_name']}** "
    f"({best_quality['composite_quality_score']:.0f})"
)

st.info(
    f"💰 Highest Free Cash Flow: **{highest_fcf['company_name']}** "
    f"({highest_fcf['free_cash_flow_cr']:,.0f})"
)

st.divider()

# ==========================================================
# Dataset Information
# ==========================================================

with st.expander("ℹ️ About Capital Allocation Patterns"):

    st.markdown("""
The Capital Allocation Map groups companies according to their
financial characteristics using:

- Return on Equity (ROE)
- Return on Capital Employed (ROCE)
- Free Cash Flow
- Debt to Equity
- Dividend Payout Ratio
- Revenue Growth
- Composite Quality Score

Each company is assigned to one capital allocation pattern,
allowing quick comparison of businesses with similar financial
behaviour.
""")

st.divider()

st.caption("Financial Intelligence Platform • Sprint 2 • Capital Allocation Dashboard")
