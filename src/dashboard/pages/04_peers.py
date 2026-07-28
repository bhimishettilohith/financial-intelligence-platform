import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.dashboard.utils.db import (
    get_company_id,
    get_company_names,
    get_latest_ratios,
    get_peer_average,
    get_peer_members,
    get_peer_percentiles,
)

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Peer Comparison")

company_names = get_company_names()

selected_company = st.selectbox(
    "Select Company",
    company_names,
)

if not selected_company:
    st.stop()

company_id = get_company_id(selected_company)

latest_df = get_latest_ratios(company_id)

if latest_df.empty:
    st.warning("No financial ratios available.")
    st.stop()

latest = latest_df.iloc[0]

peer_df = get_peer_percentiles(company_id)

if peer_df.empty:
    st.warning("No peer comparison available.")
    st.stop()

peer_group = peer_df.iloc[0]["peer_group_name"]

members = get_peer_members(peer_group)

avg_df = get_peer_average(peer_group)

st.success(f"Peer Group : {peer_group}")

st.divider()

c1, c2, c3, c4 = st.columns(4)

c1.metric("ROE", f"{latest['return_on_equity_pct']:.2f}%")

c2.metric("ROCE", f"{latest['return_on_capital_employed_pct']:.2f}%")

c3.metric("Net Margin", f"{latest['net_profit_margin_pct']:.2f}%")

c4.metric("Debt / Equity", f"{latest['debt_to_equity']:.2f}")

st.divider()

st.subheader("Peer Members")

benchmark = members[members["is_benchmark"] == 1]

if not benchmark.empty:
    st.info(f"Benchmark Company : {benchmark.iloc[0]['company_name']}")

display_members = members.copy()

display_members["Benchmark"] = display_members["is_benchmark"].map(
    {
        1: "Yes",
        0: "No",
        True: "Yes",
        False: "No",
    }
)

display_members = display_members[
    [
        "company_name",
        "Benchmark",
    ]
]

st.dataframe(
    display_members,
    hide_index=True,
    width="stretch",
)

st.divider()

st.subheader("Company Percentile Rankings")

latest_year = peer_df.iloc[0]["year"]

latest_percentiles = (
    peer_df[peer_df["year"] == latest_year]
    .copy()
    .sort_values(
        "percentile_rank",
        ascending=False,
    )
)

metric_names = {
    "return_on_equity_pct": "ROE",
    "return_on_capital_employed_pct": "ROCE",
    "net_profit_margin_pct": "Net Margin",
    "debt_to_equity": "Debt / Equity",
    "free_cash_flow_cr": "Free Cash Flow",
    "interest_coverage": "Interest Coverage",
    "asset_turnover": "Asset Turnover",
    "revenue_cagr_5yr": "Revenue CAGR",
    "pat_cagr_5yr": "PAT CAGR",
    "eps_cagr_5yr": "EPS CAGR",
}

latest_percentiles["Metric"] = latest_percentiles["metric"].map(metric_names)

latest_percentiles.rename(
    columns={
        "value": "Company Value",
        "percentile_rank": "Percentile",
    },
    inplace=True,
)

st.dataframe(
    latest_percentiles[
        [
            "Metric",
            "Company Value",
            "Percentile",
        ]
    ],
    hide_index=True,
    width="stretch",
)

st.divider()

st.subheader("Percentile Distribution")

fig = px.bar(
    latest_percentiles,
    x="Metric",
    y="Percentile",
    text="Percentile",
)

fig.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside",
)

fig.update_layout(
    yaxis_title="Percentile",
    xaxis_title="",
    height=500,
)

st.plotly_chart(
    fig,
    width="stretch",
)

st.divider()

st.subheader("Radar Comparison")

radar_metrics = [
    "ROE",
    "ROCE",
    "Net Margin",
    "Asset Turnover",
    "Revenue CAGR",
    "PAT CAGR",
    "EPS CAGR",
]

radar_df = latest_percentiles[latest_percentiles["Metric"].isin(radar_metrics)]


fig_radar = go.Figure()

fig_radar.add_trace(
    go.Scatterpolar(
        r=radar_df["Percentile"],
        theta=radar_df["Metric"],
        fill="toself",
        name=selected_company,
    )
)

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1],
        )
    ),
    showlegend=False,
    height=600,
)

st.plotly_chart(
    fig_radar,
    width="stretch",
)

st.divider()

st.subheader("Peer Group Average Metrics")

avg_df = avg_df.copy()

avg_df["Metric"] = avg_df["metric"].map(metric_names)

avg_df.rename(
    columns={
        "average_value": "Average Value",
        "average_percentile": "Average Percentile",
    },
    inplace=True,
)

avg_df = avg_df[
    [
        "Metric",
        "Average Value",
        "Average Percentile",
    ]
]

st.dataframe(
    avg_df,
    hide_index=True,
    width="stretch",
)

st.divider()

st.subheader("Company vs Peer Average")

comparison = latest_percentiles.merge(
    avg_df,
    on="Metric",
    how="left",
)

comparison = comparison[
    [
        "Metric",
        "Company Value",
        "Average Value",
    ]
]

bar = go.Figure()

bar.add_trace(
    go.Bar(
        name=selected_company,
        x=comparison["Metric"],
        y=comparison["Company Value"],
    )
)

bar.add_trace(
    go.Bar(
        name="Peer Average",
        x=comparison["Metric"],
        y=comparison["Average Value"],
    )
)

bar.update_layout(
    barmode="group",
    height=550,
    xaxis_title="",
    yaxis_title="Metric Value",
)

st.plotly_chart(
    bar,
    width="stretch",
)

st.divider()

st.subheader("Growth Comparison")

growth_metrics = [
    "Revenue CAGR",
    "PAT CAGR",
    "EPS CAGR",
]

growth_df = comparison[comparison["Metric"].isin(growth_metrics)]

growth = px.bar(
    growth_df,
    x="Metric",
    y=[
        "Company Value",
        "Average Value",
    ],
    barmode="group",
)

growth.update_layout(
    height=500,
    xaxis_title="",
    yaxis_title="Growth (%)",
)

st.plotly_chart(
    growth,
    width="stretch",
)

st.divider()

st.subheader("Financial Strength Indicators")

left, right = st.columns(2)

with left:

    st.metric(
        "Interest Coverage",
        f"{latest['interest_coverage']:.2f}",
    )

    st.metric(
        "Asset Turnover",
        f"{latest['asset_turnover']:.2f}",
    )

    st.metric(
        "Free Cash Flow",
        f"{latest['free_cash_flow_cr']:.2f} Cr",
    )

with right:

    st.metric(
        "Net Debt",
        f"{latest['net_debt']:.2f} Cr",
    )

    st.metric(
        "CFO Quality",
        latest["cfo_quality_label"],
    )

    st.metric(
        "Composite Score",
        f"{latest['composite_quality_score']:.2f}",
    )

st.divider()

st.subheader("Latest Financial Snapshot")

snapshot = pd.DataFrame(
    {
        "Metric": [
            "ROE",
            "ROCE",
            "ROA",
            "Net Margin",
            "Debt / Equity",
            "Interest Coverage",
            "Asset Turnover",
            "Revenue CAGR",
            "PAT CAGR",
            "EPS CAGR",
        ],
        "Value": [
            latest["return_on_equity_pct"],
            latest["return_on_capital_employed_pct"],
            latest["return_on_assets_pct"],
            latest["net_profit_margin_pct"],
            latest["debt_to_equity"],
            latest["interest_coverage"],
            latest["asset_turnover"],
            latest["revenue_cagr_5yr"],
            latest["pat_cagr_5yr"],
            latest["eps_cagr_5yr"],
        ],
    }
)

st.dataframe(
    snapshot,
    hide_index=True,
    width="stretch",
)

st.success("✅ Peer Comparison Loaded Successfully")
