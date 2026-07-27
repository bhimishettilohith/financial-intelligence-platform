import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.dashboard.utils.db import (
    get_company_names,
    get_company_id,
    get_pl,
    get_bs,
    get_cf,
)

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Trend Analysis",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Trend Analysis")
st.caption(
    "Analyze financial trends over the last 10 years with YoY growth."
)

# -------------------------------------------------------
# Company Selection
# -------------------------------------------------------

companies = get_company_names()

selected_company = st.selectbox(
    "Select Company",
    companies,
)

company_id = get_company_id(selected_company)

# -------------------------------------------------------
# Load Financial Statements
# -------------------------------------------------------

pl = get_pl(company_id)
bs = get_bs(company_id)
cf = get_cf(company_id)

# -------------------------------------------------------
# Metric Dictionary
# -------------------------------------------------------

METRICS = {

    # Profit & Loss
    "Sales": ("sales", "PL"),
    "Expenses": ("expenses", "PL"),
    "Operating Profit": ("operating_profit", "PL"),
    "OPM %": ("opm_percentage", "PL"),
    "Other Income": ("other_income", "PL"),
    "Interest": ("interest", "PL"),
    "Depreciation": ("depreciation", "PL"),
    "Profit Before Tax": ("profit_before_tax", "PL"),
    "Tax %": ("tax_percentage", "PL"),
    "Net Profit": ("net_profit", "PL"),
    "EPS": ("eps", "PL"),
    "Dividend Payout": ("dividend_payout", "PL"),

    # Balance Sheet
    "Equity Capital": ("equity_capital", "BS"),
    "Reserves": ("reserves", "BS"),
    "Borrowings": ("borrowings", "BS"),
    "Other Liabilities": ("other_liabilities", "BS"),
    "Total Liabilities": ("total_liabilities", "BS"),
    "Fixed Assets": ("fixed_assets", "BS"),
    "CWIP": ("cwip", "BS"),
    "Investments": ("investments", "BS"),
    "Other Asset": ("other_asset", "BS"),
    "Total Assets": ("total_assets", "BS"),

    # Cash Flow
    "Operating Activity": ("operating_activity", "CF"),
    "Investing Activity": ("investing_activity", "CF"),
    "Financing Activity": ("financing_activity", "CF"),
    "Net Cash Flow": ("net_cash_flow", "CF"),
}

# -------------------------------------------------------
# Metric Selection
# -------------------------------------------------------

selected_metrics = st.multiselect(
    "Select up to 3 Metrics",
    options=list(METRICS.keys()),
    default=["Sales"],
    max_selections=3,
)

if len(selected_metrics) == 0:
    st.warning("Please select at least one metric.")
    st.stop()

# -------------------------------------------------------
# Prepare Financial Data
# -------------------------------------------------------

# Merge all statements on year
financial_df = (
    pl.merge(
        bs,
        on=["company_id", "year"],
        how="outer",
        suffixes=("", "_bs"),
    )
    .merge(
        cf,
        on=["company_id", "year"],
        how="outer",
        suffixes=("", "_cf"),
    )
)

st.write("PL Shape:", pl.shape)
st.write("BS Shape:", bs.shape)
st.write("CF Shape:", cf.shape)

st.write("Merged Shape:", financial_df.shape)

st.dataframe(financial_df.head())

# Remove duplicate ID columns created during merge
financial_df = financial_df.loc[
    :,
    ~financial_df.columns.str.startswith("id_")
]

financial_df = financial_df.sort_values("year")

# Keep only latest 10 years
financial_df = financial_df.tail(10).reset_index(drop=True)

# Convert year to string for plotting
financial_df["year"] = financial_df["year"].astype(str)

# -------------------------------------------------------
# Build Trend Data
# -------------------------------------------------------

trend_df = pd.DataFrame()

trend_df["Year"] = financial_df["year"]

for metric in selected_metrics:

    column_name, source = METRICS[metric]

    if column_name in financial_df.columns:

        trend_df[metric] = pd.to_numeric(
            financial_df[column_name],
            errors="coerce",
        )

# -------------------------------------------------------
# Calculate YoY Growth
# -------------------------------------------------------

yoy_data = {}

for metric in selected_metrics:

    yoy = trend_df[metric].pct_change() * 100

    yoy_data[metric] = yoy.round(2)

# -------------------------------------------------------
# Preview
# -------------------------------------------------------

st.subheader("Financial Trend")

st.caption(
    f"Displaying the latest {len(trend_df)} years for "
    f"{selected_company}."
)

# -------------------------------------------------------
# Plot Trend Chart
# -------------------------------------------------------

st.subheader("📈 10-Year Financial Trend")

fig = go.Figure()

colors = [
    "#1f77b4",  # Blue
    "#2ca02c",  # Green
    "#d62728",  # Red
]

for i, metric in enumerate(selected_metrics):

    fig.add_trace(
        go.Scatter(
            x=trend_df["Year"],
            y=trend_df[metric],
            mode="lines+markers",
            name=metric,
            line=dict(
                width=3,
                color=colors[i % len(colors)],
            ),
            marker=dict(
                size=8,
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                + metric
                + ": %{y:,.2f}"
                + "<extra></extra>"
            ),
        )
    )

    # ---------------------------------------------------
    # YoY Annotation
    # ---------------------------------------------------

    for x, y, yoy in zip(
        trend_df["Year"],
        trend_df[metric],
        yoy_data[metric],
    ):

        if pd.notna(y) and pd.notna(yoy):

            fig.add_annotation(
                x=x,
                y=y,
                text=f"{yoy:+.1f}%",
                showarrow=False,
                yshift=18,
                font=dict(
                    size=10,
                ),
            )

# -------------------------------------------------------
# Layout
# -------------------------------------------------------

fig.update_layout(
    height=650,
    hovermode="x unified",
    template="plotly_white",
    legend_title="Metrics",
    xaxis_title="Financial Year",
    yaxis_title="Value",
    margin=dict(
        l=30,
        r=30,
        t=60,
        b=30,
    ),
)

fig.update_xaxes(
    showgrid=True,
)

fig.update_yaxes(
    showgrid=True,
)

st.plotly_chart(
    fig,
    width="stretch",
)

# -------------------------------------------------------
# Latest Values
# -------------------------------------------------------

st.divider()

st.subheader("📊 Latest Available Values")

cols = st.columns(len(selected_metrics))

if trend_df.empty:
    st.warning("No trend data available for the selected company.")
    st.stop()

latest = trend_df.iloc[-1]

for i, metric in enumerate(selected_metrics):

    value = latest[metric]

    yoy = yoy_data[metric].iloc[-1]

    if pd.isna(yoy):
        delta = "N/A"
    else:
        delta = f"{yoy:+.2f}%"

    cols[i].metric(
        label=metric,
        value=f"{value:,.2f}",
        delta=delta,
    )

# -------------------------------------------------------
# Trend Data Table
# -------------------------------------------------------

st.divider()

st.subheader("📋 Trend Data")

table_df = trend_df.copy()

for metric in selected_metrics:
    table_df[f"{metric} YoY %"] = yoy_data[metric]

st.dataframe(
    table_df,
    hide_index=True,
    width="stretch",
)

# -------------------------------------------------------
# Download CSV
# -------------------------------------------------------

csv = table_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Trend Data",
    data=csv,
    file_name=f"{selected_company}_trend_analysis.csv",
    mime="text/csv",
    width="stretch",
)

# -------------------------------------------------------
# Summary Statistics
# -------------------------------------------------------

st.divider()

st.subheader("📊 Summary Statistics")

summary_rows = []

for metric in selected_metrics:

    values = trend_df[metric].dropna()

    if values.empty:
        continue

    summary_rows.append(
        {
            "Metric": metric,
            "Latest": round(values.iloc[-1], 2),
            "Minimum": round(values.min(), 2),
            "Maximum": round(values.max(), 2),
            "Average": round(values.mean(), 2),
            "YoY Latest (%)": (
                round(yoy_data[metric].iloc[-1], 2)
                if pd.notna(yoy_data[metric].iloc[-1])
                else None
            ),
        }
    )

summary_df = pd.DataFrame(summary_rows)

st.dataframe(
    summary_df,
    hide_index=True,
    width="stretch",
)

# -------------------------------------------------------
# Insights
# -------------------------------------------------------

st.divider()

st.subheader("💡 Quick Insights")

for metric in selected_metrics:

    values = trend_df[metric].dropna()

    if len(values) < 2:
        continue

    latest = values.iloc[-1]
    previous = values.iloc[-2]

    if latest > previous:
        icon = "📈"
        direction = "increased"

    elif latest < previous:
        icon = "📉"
        direction = "decreased"

    else:
        icon = "➖"
        direction = "remained unchanged"

    yoy = yoy_data[metric].iloc[-1]

    if pd.notna(yoy):
        st.write(
            f"{icon} **{metric}** {direction} by "
            f"**{yoy:.2f}%** in the latest year."
        )
    else:
        st.write(
            f"{icon} **{metric}** has insufficient data for YoY comparison."
        )

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.divider()

st.caption(
    "Financial Intelligence Platform • Trend Analysis Dashboard"
)