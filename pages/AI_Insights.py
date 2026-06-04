import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide"
)

# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

# ======================================================
# HEADER
# ======================================================

st.title("🤖 AI Executive Intelligence Center")

st.markdown("""
Generate executive-level insights, startup rankings,
growth opportunities, risk indicators, and strategic recommendations.
""")

# ======================================================
# FILTERS
# ======================================================

st.sidebar.header("AI Filters")

industry = st.sidebar.multiselect(
    "Industry",
    sorted(df["Industry"].unique()),
    default=sorted(df["Industry"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

filtered_df = df[
    (df["Industry"].isin(industry))
    &
    (df["Region"].isin(region))
]

# ======================================================
# DATA PREPARATION
# ======================================================

if filtered_df["Profitable"].dtype == object:
    filtered_df["Profitable"] = (
        filtered_df["Profitable"]
        .astype(str)
        .str.lower()
        .map({
            "true": True,
            "false": False,
            "yes": True,
            "no": False
        })
    )

analysis_df = filtered_df.copy()

analysis_df["Funding Efficiency"] = (
    analysis_df["Revenue (M USD)"]
    /
    analysis_df["Funding Amount (M USD)"]
)

analysis_df["Valuation Multiple"] = (
    analysis_df["Valuation (M USD)"]
    /
    analysis_df["Revenue (M USD)"]
)

analysis_df["Growth Score"] = (
    (
        analysis_df["Revenue (M USD)"]
        *
        analysis_df["Market Share (%)"]
    )
    /
    analysis_df["Funding Amount (M USD)"]
)

analysis_df.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)

analysis_df.dropna(inplace=True)

# ======================================================
# EXECUTIVE KPIs
# ======================================================

st.subheader("📊 Executive Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Startups",
    len(analysis_df)
)

c2.metric(
    "Total Funding",
    f"${analysis_df['Funding Amount (M USD)'].sum():,.0f}M"
)

c3.metric(
    "Total Revenue",
    f"${analysis_df['Revenue (M USD)'].sum():,.0f}M"
)

c4.metric(
    "Total Valuation",
    f"${analysis_df['Valuation (M USD)'].sum():,.0f}M"
)

st.divider()

# ======================================================
# STARTUP SCORING ENGINE
# ======================================================

st.subheader("🏆 AI Startup Ranking")

score_df = analysis_df.copy()

score_df["Startup Score"] = (
    score_df["Revenue (M USD)"] * 0.35
    +
    score_df["Market Share (%)"] * 0.25
    +
    score_df["Valuation (M USD)"] * 0.25
    +
    score_df["Funding Efficiency"] * 100 * 0.15
)

top_ranked = (
    score_df
    .sort_values(
        "Startup Score",
        ascending=False
    )
    .head(15)
)

st.dataframe(
    top_ranked[
        [
            "Startup Name",
            "Industry",
            "Startup Score",
            "Revenue (M USD)",
            "Valuation (M USD)"
        ]
    ],
    use_container_width=True
)

# ======================================================
# GROWTH OPPORTUNITIES
# ======================================================

st.subheader("🚀 Growth Opportunities")

growth = (
    analysis_df
    .sort_values(
        "Growth Score",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    growth,
    x="Startup Name",
    y="Growth Score",
    color="Industry",
    title="Top Growth Opportunities"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ======================================================
# FUNDING EFFICIENCY
# ======================================================

st.subheader("⚡ Funding Efficiency Leaders")

efficiency = (
    analysis_df
    .sort_values(
        "Funding Efficiency",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    efficiency,
    x="Startup Name",
    y="Funding Efficiency",
    title="Revenue Generated Per Funding Dollar"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ======================================================
# OUTLIER DETECTION
# ======================================================

st.subheader("🔍 Valuation Outliers")

q1 = analysis_df["Valuation (M USD)"].quantile(0.25)
q3 = analysis_df["Valuation (M USD)"].quantile(0.75)

iqr = q3 - q1

outliers = analysis_df[
    (
        analysis_df["Valuation (M USD)"]
        >
        q3 + 1.5 * iqr
    )
]

st.dataframe(
    outliers[
        [
            "Startup Name",
            "Industry",
            "Valuation (M USD)",
            "Revenue (M USD)"
        ]
    ],
    use_container_width=True
)

# ======================================================
# RISK ANALYSIS
# ======================================================

st.subheader("⚠ Risk Detection")

risk_df = analysis_df.copy()

risk_df["Risk Score"] = (
    risk_df["Funding Amount (M USD)"]
    /
    (
        risk_df["Revenue (M USD)"] + 1
    )
)

risk_df = risk_df.sort_values(
    "Risk Score",
    ascending=False
)

st.dataframe(
    risk_df[
        [
            "Startup Name",
            "Industry",
            "Risk Score",
            "Funding Amount (M USD)",
            "Revenue (M USD)"
        ]
    ].head(15),
    use_container_width=True
)

# ======================================================
# INDUSTRY INTELLIGENCE
# ======================================================

st.subheader("🏭 Industry Intelligence")

industry_summary = (
    analysis_df
    .groupby("Industry")
    .agg({
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "sum",
        "Funding Amount (M USD)": "sum",
        "Market Share (%)": "mean"
    })
    .reset_index()
)

fig = px.treemap(
    industry_summary,
    path=["Industry"],
    values="Valuation (M USD)",
    title="Industry Valuation Intelligence"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ======================================================
# CORRELATION INTELLIGENCE
# ======================================================

st.subheader("🔥 Correlation Intelligence")

cols = [
    "Funding Amount (M USD)",
    "Funding Rounds",
    "Revenue (M USD)",
    "Valuation (M USD)",
    "Employees",
    "Market Share (%)"
]

corr = analysis_df[cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    title="Strategic Correlation Matrix"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ======================================================
# AI EXECUTIVE INSIGHTS
# ======================================================

st.subheader("🧠 AI Generated Executive Insights")

highest_funding_industry = (
    analysis_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

highest_revenue_industry = (
    analysis_df.groupby("Industry")
    ["Revenue (M USD)"]
    .sum()
    .idxmax()
)

highest_valuation_industry = (
    analysis_df.groupby("Industry")
    ["Valuation (M USD)"]
    .sum()
    .idxmax()
)

profitability_rate = (
    analysis_df["Profitable"].mean() * 100
)

st.success(
    f"Highest funded industry: {highest_funding_industry}"
)

st.success(
    f"Highest revenue industry: {highest_revenue_industry}"
)

st.success(
    f"Highest valuation industry: {highest_valuation_industry}"
)

st.success(
    f"Overall profitability rate: {profitability_rate:.2f}%"
)

# ======================================================
# STRATEGIC RECOMMENDATIONS
# ======================================================

st.subheader("📋 Strategic Recommendations")

recommendations = [
    f"Increase investment focus on {highest_revenue_industry}.",
    f"Monitor valuation growth trends in {highest_valuation_industry}.",
    "Improve capital allocation for startups with low funding efficiency.",
    "Prioritize startups with high growth scores and strong market share.",
    "Review high-risk startups with elevated funding-to-revenue ratios."
]

for rec in recommendations:
    st.info(rec)

# ======================================================
# EXECUTIVE REPORT
# ======================================================

st.subheader("📄 Executive Report")

report = f"""
AI EXECUTIVE REPORT
Generated: {datetime.now()}

Total Startups: {len(analysis_df)}
Total Funding: ${analysis_df['Funding Amount (M USD)'].sum():,.0f}M
Total Revenue: ${analysis_df['Revenue (M USD)'].sum():,.0f}M
Total Valuation: ${analysis_df['Valuation (M USD)'].sum():,.0f}M

Highest Funded Industry: {highest_funding_industry}
Highest Revenue Industry: {highest_revenue_industry}
Highest Valuation Industry: {highest_valuation_industry}

Profitability Rate: {profitability_rate:.2f}%
"""

st.download_button(
    "📥 Download AI Report",
    report,
    file_name="AI_Executive_Report.txt",
    mime="text/plain"
)

# ======================================================
# FOOTER
# ======================================================

st.divider()

st.caption(
    "AI Executive Intelligence Module | Startup Intelligence Platform"
)
