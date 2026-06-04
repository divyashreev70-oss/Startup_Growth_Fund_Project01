import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# =====================================================
# BAR CHART
# =====================================================

def create_bar_chart(
    df,
    x,
    y,
    title,
    color=None,
    text_auto=True
):
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        text_auto=text_auto
    )

    fig.update_layout(
        height=500,
        xaxis_title=x,
        yaxis_title=y
    )

    return fig


# =====================================================
# LINE CHART
# =====================================================

def create_line_chart(
    df,
    x,
    y,
    title,
    color=None
):
    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        markers=True
    )

    fig.update_layout(
        height=500
    )

    return fig


# =====================================================
# PIE CHART
# =====================================================

def create_pie_chart(
    df,
    names,
    values,
    title
):
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title
    )

    fig.update_layout(
        height=500
    )

    return fig


# =====================================================
# DONUT CHART
# =====================================================

def create_donut_chart(
    df,
    names,
    values,
    title
):
    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.5,
        title=title
    )

    fig.update_layout(
        height=500
    )

    return fig


# =====================================================
# SCATTER CHART
# =====================================================

def create_scatter_chart(
    df,
    x,
    y,
    title,
    color=None,
    size=None,
    hover_name=None
):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        hover_name=hover_name,
        title=title
    )

    fig.update_layout(
        height=600
    )

    return fig


# =====================================================
# BUBBLE CHART
# =====================================================

def create_bubble_chart(
    df,
    x,
    y,
    size,
    color,
    title
):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        title=title
    )

    fig.update_layout(
        height=600
    )

    return fig


# =====================================================
# HISTOGRAM
# =====================================================

def create_histogram(
    df,
    column,
    title,
    bins=30
):
    fig = px.histogram(
        df,
        x=column,
        nbins=bins,
        title=title
    )

    fig.update_layout(
        height=500
    )

    return fig


# =====================================================
# BOX PLOT
# =====================================================

def create_box_plot(
    df,
    x,
    y,
    title
):
    fig = px.box(
        df,
        x=x,
        y=y,
        title=title
    )

    fig.update_layout(
        height=500
    )

    return fig


# =====================================================
# TREEMAP
# =====================================================

def create_treemap(
    df,
    path,
    values,
    title
):
    fig = px.treemap(
        df,
        path=path,
        values=values,
        title=title
    )

    fig.update_layout(
        height=600
    )

    return fig


# =====================================================
# SUNBURST
# =====================================================

def create_sunburst(
    df,
    path,
    values,
    title
):
    fig = px.sunburst(
        df,
        path=path,
        values=values,
        title=title
    )

    fig.update_layout(
        height=600
    )

    return fig


# =====================================================
# FUNNEL CHART
# =====================================================

def create_funnel(
    df,
    x,
    y,
    title
):
    fig = px.funnel(
        df,
        x=x,
        y=y,
        title=title
    )

    fig.update_layout(
        height=500
    )

    return fig


# =====================================================
# AREA CHART
# =====================================================

def create_area_chart(
    df,
    x,
    y,
    title,
    color=None
):
    fig = px.area(
        df,
        x=x,
        y=y,
        color=color,
        title=title
    )

    fig.update_layout(
        height=500
    )

    return fig


# =====================================================
# HEATMAP
# =====================================================

def create_heatmap(
    corr_matrix,
    title="Correlation Heatmap"
):
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        title=title,
        aspect="auto"
    )

    fig.update_layout(
        height=650
    )

    return fig


# =====================================================
# KPI INDICATOR
# =====================================================

def create_indicator(
    value,
    title
):
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=value,
            title={"text": title}
        )
    )

    fig.update_layout(
        height=250
    )

    return fig


# =====================================================
# GAUGE CHART
# =====================================================

def create_gauge(
    value,
    title,
    max_value=100
):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {
                    "range": [0, max_value]
                }
            }
        )
    )

    fig.update_layout(
        height=350
    )

    return fig


# =====================================================
# TOP N TABLE
# =====================================================

def get_top_n(
    df,
    sort_column,
    n=10
):
    return (
        df.sort_values(
            sort_column,
            ascending=False
        )
        .head(n)
    )


# =====================================================
# CORRELATION MATRIX
# =====================================================

def get_correlation_matrix(
    df,
    numeric_columns
):
    return (
        df[numeric_columns]
        .corr()
    )


# =====================================================
# CHART THEME
# =====================================================

def apply_chart_theme(fig):

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    return fig
