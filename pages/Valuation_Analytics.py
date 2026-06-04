import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Valuation Analytics",
    page_icon="💎",
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
# HEADER
# =====================================================

st.title("💎 Valuation Analytics Dashboard")

st.markdown("""
Analyze startup valuations, unicorn trends,
industry rankings, valuation multiples,
and growth opportunities.
""")

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Filters")

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

valuation_range = st.sidebar.slider(
    "Valuation (M USD)",
    int(df["Valuation (M USD)"].min()),
    int(df["Valuation (M USD)"].max()),
    (
        int(df["Valuation (M USD)"].min()),
        int(df["Valuation (M USD)"].max())
    )
)

filtered_df = df[
    (df["Industry"].isin(industry))
    &
    (df["Region"].isin(region))
    &
    (
        df["Valuation (M USD)"].between(
            valuation_range[0],
            valuation_range[1]
        )
    )
]

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("📊 Valuation KPIs")

total_valuation = filtered_df["Valuation (M USD)"].sum()

avg_valuation = filtered_df["Valuation (M USD)"].mean()

median_valuation = filtered_df["Valuation (M USD)"].median()

highest_valuation = filtered_df["Valuation (M USD)"].max()

unicorn_count = len(
    filtered_df[
        filtered_df["Valuation (M USD)"] >= 1000
    ]
)

avg_multiple = (
    filtered_df["Valuation (M USD)"] /
    filtered_df["Revenue (M USD)"]
).replace(np.inf, np.nan).mean()

c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric(
    "Total Valuation",
    f"${total_valuation:,.0f}M"
)

c2.metric(
    "Average",
    f"${avg_valuation:,.0f}M"
)

c3.metric(
    "Median",
    f"${median_valuation:,.0f}M"
)

c4.metric(
    "Highest",
    f"${highest_valuation:,.0f}M"
)

c5.metric(
    "Unicorns",
    unicorn_count
)

c6.metric(
    "Avg Multiple",
    f"{avg_multiple:.2f}x"
)

st.divider()

# =====================================================
# VALUATION DISTRIBUTION
# =====================================================

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x="Valuation (M USD)",
        nbins=30,
        title="Valuation Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        filtered_df,
        x="Industry",
        y="Valuation (M USD)",
        title="Valuation Spread by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# INDUSTRY VALUATION ANALYSIS
# =====================================================

st.subheader("🏭 Industry Valuation Ranking")

industry_val = (
    filtered_df
    .groupby("Industry")
    ["Valuation (M USD)"]
    .sum()
    .reset_index()
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
)

fig = px.bar(
    industry_val,
    x="Industry",
    y="Valuation (M USD)",
    text_auto=True,
    title="Industry Valuation Ranking"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# REGION ANALYSIS
# =====================================================

st.subheader("🌎 Regional Valuation Analysis")

region_val = (
    filtered_df
    .groupby("Region")
    ["Valuation (M USD)"]
    .sum()
    .reset_index()
)

fig = px.treemap(
    region_val,
    path=["Region"],
    values="Valuation (M USD)",
    title="Regional Valuation Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FUNDING VS VALUATION
# =====================================================

st.subheader("💰 Funding vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    size="Revenue (M USD)",
    color="Industry",
    hover_name="Startup Name",
    title="Funding Impact on Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# REVENUE VS VALUATION
# =====================================================

st.subheader("📈 Revenue vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Employees",
    hover_name="Startup Name",
    title="Revenue Driven Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# VALUATION MULTIPLE ANALYSIS
# =====================================================

st.subheader("📊 Valuation Multiples")

multiple_df = filtered_df.copy()

multiple_df["Valuation Multiple"] = (
    multiple_df["Valuation (M USD)"]
    /
    multiple_df["Revenue (M USD)"]
)

multiple_df = multiple_df.replace(
    [np.inf, -np.inf],
    np.nan
)

multiple_df = multiple_df.dropna()

top_multiple = (
    multiple_df
    .sort_values(
        "Valuation Multiple",
        ascending=False
    )
    .head(20)
)

fig = px.bar(
    top_multiple,
    x="Startup Name",
    y="Valuation Multiple",
    title="Top Valuation Multiples"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# UNICORN ANALYSIS
# =====================================================

st.subheader("🦄 Unicorn Startups")

unicorns = filtered_df[
    filtered_df["Valuation (M USD)"] >= 1000
]

fig = px.pie(
    unicorns.groupby("Industry")
    .size()
    .reset_index(name="Count"),
    names="Industry",
    values="Count",
    title="Unicorn Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP VALUED STARTUPS
# =====================================================

st.subheader("🏆 Top 20 Valued Startups")

top20 = (
    filtered_df
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top20[
        [
            "Startup Name",
            "Industry",
            "Valuation (M USD)",
            "Funding Amount (M USD)",
            "Revenue (M USD)",
            "Region"
        ]
    ],
    use_container_width=True
)

# =====================================================
# HEATMAP
# =====================================================

st.subheader("🔥 Correlation Heatmap")

numeric_cols = [
    "Funding Amount (M USD)",
    "Funding Rounds",
    "Valuation (M USD)",
    "Revenue (M USD)",
    "Employees",
    "Market Share (%)"
]

corr = filtered_df[numeric_cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    title="Valuation Correlation Matrix"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP GROWTH OPPORTUNITIES
# =====================================================

st.subheader("🚀 Growth Opportunity Startups")

growth_df = filtered_df.copy()

growth_df["Growth Score"] = (
    growth_df["Revenue (M USD)"] *
    growth_df["Market Share (%)"]
) / growth_df["Funding Amount (M USD)"]

growth_df = growth_df.sort_values(
    "Growth Score",
    ascending=False
)

st.dataframe(
    growth_df[
        [
            "Startup Name",
            "Industry",
            "Growth Score",
            "Revenue (M USD)",
            "Market Share (%)"
        ]
    ].head(15),
    use_container_width=True
)

# =====================================================
# AI INSIGHTS
# =====================================================

st.subheader("🤖 Automated Insights")

highest_industry = (
    filtered_df.groupby("Industry")
    ["Valuation (M USD)"]
    .sum()
    .idxmax()
)

highest_region = (
    filtered_df.groupby("Region")
    ["Valuation (M USD)"]
    .sum()
    .idxmax()
)

top_startup = (
    filtered_df.sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .iloc[0]
)

st.success(
    f"Highest valued industry: {highest_industry}"
)

st.success(
    f"Highest valuation region: {highest_region}"
)

st.success(
    f"Top startup: {top_startup['Startup Name']} "
    f"(${top_startup['Valuation (M USD)']:,.0f}M)"
)

st.success(
    f"Detected {unicorn_count} unicorn startups "
    f"in the filtered dataset."
)

# =====================================================
# DOWNLOAD DATA
# =====================================================

st.subheader("⬇ Download Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    "Download Valuation Data",
    csv,
    "valuation_analytics.csv",
    "text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Valuation Analytics Module | Startup Intelligence Platform"
)
