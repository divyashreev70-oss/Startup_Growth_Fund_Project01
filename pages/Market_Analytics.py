import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Market Analytics",
    page_icon="🌍",
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

st.title("🌍 Market Analytics Dashboard")

st.markdown("""
Analyze market share, competitive positioning,
industry dominance, and regional market trends.
""")

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Market Filters")

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

market_range = st.sidebar.slider(
    "Market Share (%)",
    float(df["Market Share (%)"].min()),
    float(df["Market Share (%)"].max()),
    (
        float(df["Market Share (%)"].min()),
        float(df["Market Share (%)"].max())
    )
)

filtered_df = df[
    (df["Industry"].isin(industry))
    &
    (df["Region"].isin(region))
    &
    (
        df["Market Share (%)"].between(
            market_range[0],
            market_range[1]
        )
    )
]

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("📊 Market KPIs")

avg_market_share = filtered_df["Market Share (%)"].mean()

max_market_share = filtered_df["Market Share (%)"].max()

total_market_share = filtered_df["Market Share (%)"].sum()

industry_count = filtered_df["Industry"].nunique()

region_count = filtered_df["Region"].nunique()

leader = filtered_df.loc[
    filtered_df["Market Share (%)"].idxmax()
]

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Avg Market Share",
    f"{avg_market_share:.2f}%"
)

c2.metric(
    "Max Market Share",
    f"{max_market_share:.2f}%"
)

c3.metric(
    "Total Share",
    f"{total_market_share:.2f}%"
)

c4.metric(
    "Industries",
    industry_count
)

c5.metric(
    "Regions",
    region_count
)

c6.metric(
    "Market Leader",
    leader["Startup Name"]
)

st.divider()

# =====================================================
# MARKET SHARE DISTRIBUTION
# =====================================================

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x="Market Share (%)",
        nbins=30,
        title="Market Share Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        filtered_df,
        x="Industry",
        y="Market Share (%)",
        title="Market Share Spread by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# INDUSTRY MARKET SHARE
# =====================================================

st.subheader("🏭 Industry Market Dominance")

industry_market = (
    filtered_df
    .groupby("Industry")
    ["Market Share (%)"]
    .sum()
    .reset_index()
    .sort_values(
        "Market Share (%)",
        ascending=False
    )
)

fig = px.bar(
    industry_market,
    x="Industry",
    y="Market Share (%)",
    text_auto=True,
    title="Market Share by Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TREEMAP
# =====================================================

st.subheader("🌐 Industry Treemap")

fig = px.treemap(
    industry_market,
    path=["Industry"],
    values="Market Share (%)",
    title="Industry Market Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# REGIONAL MARKET ANALYSIS
# =====================================================

st.subheader("🌎 Regional Market Analysis")

region_market = (
    filtered_df
    .groupby("Region")
    ["Market Share (%)"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_market,
    names="Region",
    values="Market Share (%)",
    title="Regional Market Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# MARKET SHARE VS REVENUE
# =====================================================

st.subheader("📈 Market Share vs Revenue")

fig = px.scatter(
    filtered_df,
    x="Market Share (%)",
    y="Revenue (M USD)",
    color="Industry",
    size="Valuation (M USD)",
    hover_name="Startup Name",
    title="Market Share Impact on Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# MARKET SHARE VS VALUATION
# =====================================================

st.subheader("💎 Market Share vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Market Share (%)",
    y="Valuation (M USD)",
    color="Region",
    size="Revenue (M USD)",
    hover_name="Startup Name",
    title="Market Share Impact on Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# COMPETITIVE LANDSCAPE
# =====================================================

st.subheader("⚔ Competitive Landscape")

top_companies = (
    filtered_df
    .sort_values(
        "Market Share (%)",
        ascending=False
    )
    .head(20)
)

fig = px.bar(
    top_companies,
    x="Startup Name",
    y="Market Share (%)",
    color="Industry",
    title="Top Market Leaders"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# INDUSTRY LEADERS TABLE
# =====================================================

st.subheader("🏆 Top Market Leaders")

leaders = filtered_df.sort_values(
    "Market Share (%)",
    ascending=False
).head(20)

st.dataframe(
    leaders[
        [
            "Startup Name",
            "Industry",
            "Market Share (%)",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Region"
        ]
    ],
    use_container_width=True
)

# =====================================================
# MARKET CONCENTRATION
# =====================================================

st.subheader("📊 Market Concentration Analysis")

industry_concentration = (
    filtered_df.groupby("Industry")
    ["Market Share (%)"]
    .mean()
    .reset_index()
)

fig = px.funnel(
    industry_concentration.sort_values(
        "Market Share (%)",
        ascending=False
    ),
    x="Market Share (%)",
    y="Industry",
    title="Average Industry Market Concentration"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# CORRELATION ANALYSIS
# =====================================================

st.subheader("🔥 Correlation Matrix")

numeric_cols = [
    "Market Share (%)",
    "Revenue (M USD)",
    "Valuation (M USD)",
    "Funding Amount (M USD)",
    "Employees",
    "Funding Rounds"
]

corr = filtered_df[numeric_cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    title="Market Share Correlation Analysis"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# AI INSIGHTS
# =====================================================

st.subheader("🤖 Market Intelligence")

top_industry = (
    industry_market.iloc[0]["Industry"]
)

top_region = (
    region_market.sort_values(
        "Market Share (%)",
        ascending=False
    ).iloc[0]["Region"]
)

market_leader = (
    filtered_df.sort_values(
        "Market Share (%)",
        ascending=False
    ).iloc[0]
)

st.success(
    f"Leading industry by market share: {top_industry}"
)

st.success(
    f"Top region by market share: {top_region}"
)

st.success(
    f"Market leader: "
    f"{market_leader['Startup Name']} "
    f"({market_leader['Market Share (%)']:.2f}%)"
)

st.success(
    f"Average market share across filtered startups: "
    f"{avg_market_share:.2f}%"
)

# =====================================================
# DOWNLOAD DATA
# =====================================================

st.subheader("⬇ Download Market Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Market Analytics CSV",
    data=csv,
    file_name="market_analytics.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Market Analytics Module | Startup Intelligence Platform"
)
