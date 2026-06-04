import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Profitability Insights",
    page_icon="📈",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

# =====================================================
# DATA PREPARATION
# =====================================================

if df["Profitable"].dtype == object:
    df["Profitable"] = (
        df["Profitable"]
        .astype(str)
        .str.lower()
        .map({
            "true": True,
            "false": False,
            "yes": True,
            "no": False
        })
    )

# =====================================================
# HEADER
# =====================================================

st.title("📈 Profitability Insights Dashboard")

st.markdown("""
Analyze profitability performance, operational efficiency,
industry benchmarks, and drivers of sustainable growth.
""")

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Profitability Filters")

industry = st.sidebar.multiselect(
    "Industry",
    sorted(df["Industry"].dropna().unique()),
    default=sorted(df["Industry"].dropna().unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

profit_filter = st.sidebar.multiselect(
    "Profitability Status",
    ["Profitable", "Not Profitable"],
    default=["Profitable", "Not Profitable"]
)

filtered_df = df[
    (df["Industry"].isin(industry))
    &
    (df["Region"].isin(region))
]

if profit_filter == ["Profitable"]:
    filtered_df = filtered_df[
        filtered_df["Profitable"] == True
    ]

elif profit_filter == ["Not Profitable"]:
    filtered_df = filtered_df[
        filtered_df["Profitable"] == False
    ]

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("📊 Profitability KPIs")

total_startups = len(filtered_df)

profitable_count = (
    filtered_df["Profitable"].sum()
)

non_profitable_count = (
    total_startups - profitable_count
)

profitability_rate = (
    profitable_count / total_startups * 100
    if total_startups > 0
    else 0
)

avg_revenue = (
    filtered_df["Revenue (M USD)"].mean()
)

avg_funding = (
    filtered_df["Funding Amount (M USD)"].mean()
)

avg_valuation = (
    filtered_df["Valuation (M USD)"].mean()
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Startups",
    total_startups
)

c2.metric(
    "Profitable",
    int(profitable_count)
)

c3.metric(
    "Not Profitable",
    int(non_profitable_count)
)

c4.metric(
    "Profitability Rate",
    f"{profitability_rate:.1f}%"
)

c5.metric(
    "Avg Revenue",
    f"${avg_revenue:,.1f}M"
)

c6.metric(
    "Avg Valuation",
    f"${avg_valuation:,.1f}M"
)

st.divider()

# =====================================================
# PROFITABILITY SPLIT
# =====================================================

st.subheader("💹 Profitability Distribution")

profit_dist = (
    filtered_df.groupby("Profitable")
    .size()
    .reset_index(name="Count")
)

profit_dist["Profitable"] = (
    profit_dist["Profitable"]
    .replace({
        True: "Profitable",
        False: "Not Profitable"
    })
)

fig = px.pie(
    profit_dist,
    names="Profitable",
    values="Count",
    title="Profitable vs Non-Profitable"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# INDUSTRY PROFITABILITY
# =====================================================

st.subheader("🏭 Industry Profitability Ranking")

industry_profit = (
    filtered_df.groupby("Industry")
    ["Profitable"]
    .mean()
    .reset_index()
)

industry_profit["Profitability Rate"] = (
    industry_profit["Profitable"] * 100
)

industry_profit = industry_profit.sort_values(
    "Profitability Rate",
    ascending=False
)

fig = px.bar(
    industry_profit,
    x="Industry",
    y="Profitability Rate",
    text_auto=".1f",
    title="Industry Profitability Rate (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# REGION PROFITABILITY
# =====================================================

st.subheader("🌍 Regional Profitability")

region_profit = (
    filtered_df.groupby("Region")
    ["Profitable"]
    .mean()
    .reset_index()
)

region_profit["Profitability Rate"] = (
    region_profit["Profitable"] * 100
)

fig = px.bar(
    region_profit,
    x="Region",
    y="Profitability Rate",
    text_auto=".1f",
    title="Regional Profitability Rate (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# REVENUE COMPARISON
# =====================================================

st.subheader("💰 Revenue Comparison")

fig = px.box(
    filtered_df,
    x="Profitable",
    y="Revenue (M USD)",
    color="Profitable",
    title="Revenue Distribution by Profitability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FUNDING COMPARISON
# =====================================================

st.subheader("💸 Funding Comparison")

fig = px.box(
    filtered_df,
    x="Profitable",
    y="Funding Amount (M USD)",
    color="Profitable",
    title="Funding Distribution by Profitability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# EFFICIENCY ANALYSIS
# =====================================================

st.subheader("⚡ Revenue Efficiency")

eff_df = filtered_df.copy()

eff_df["Revenue_to_Funding"] = (
    eff_df["Revenue (M USD)"]
    /
    eff_df["Funding Amount (M USD)"]
)

eff_df = eff_df.replace(
    [np.inf, -np.inf],
    np.nan
).dropna()

top_efficiency = (
    eff_df.sort_values(
        "Revenue_to_Funding",
        ascending=False
    )
    .head(20)
)

fig = px.bar(
    top_efficiency,
    x="Startup Name",
    y="Revenue_to_Funding",
    title="Top Revenue-to-Funding Efficient Startups"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# PROFITABILITY DRIVERS
# =====================================================

st.subheader("🚀 Profitability Drivers")

fig = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    color="Profitable",
    size="Employees",
    hover_name="Startup Name",
    title="Revenue vs Valuation by Profitability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP PROFITABLE STARTUPS
# =====================================================

st.subheader("🏆 Top Performing Startups")

top_startups = (
    filtered_df[
        filtered_df["Profitable"] == True
    ]
    .sort_values(
        "Revenue (M USD)",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_startups[
        [
            "Startup Name",
            "Industry",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Funding Amount (M USD)",
            "Region"
        ]
    ],
    use_container_width=True
)

# =====================================================
# CORRELATION MATRIX
# =====================================================

st.subheader("🔥 Correlation Analysis")

numeric_cols = [
    "Funding Amount (M USD)",
    "Funding Rounds",
    "Revenue (M USD)",
    "Valuation (M USD)",
    "Employees",
    "Market Share (%)"
]

corr = filtered_df[numeric_cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    title="Business Metrics Correlation Matrix"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# AI INSIGHTS
# =====================================================

st.subheader("🤖 Automated Insights")

if len(industry_profit) > 0:

    best_industry = (
        industry_profit.iloc[0]["Industry"]
    )

    st.success(
        f"Most profitable industry: {best_industry}"
    )

if len(region_profit) > 0:

    best_region = (
        region_profit.sort_values(
            "Profitability Rate",
            ascending=False
        ).iloc[0]["Region"]
    )

    st.success(
        f"Most profitable region: {best_region}"
    )

st.success(
    f"Overall profitability rate is "
    f"{profitability_rate:.1f}%."
)

if len(top_startups) > 0:

    st.success(
        f"Top profitable startup: "
        f"{top_startups.iloc[0]['Startup Name']}"
    )

# =====================================================
# DOWNLOAD DATA
# =====================================================

st.subheader("⬇ Download Profitability Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Profitability Analytics CSV",
    data=csv,
    file_name="profitability_analytics.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Profitability Insights Module | Startup Intelligence Platform"
)
