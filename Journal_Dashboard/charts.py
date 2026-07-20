# ==========================================================
# charts.py
# Journal Dashboard Chart Library
# ==========================================================

import plotly.express as px
import plotly.graph_objects as go

from theme import (
    CHART_LAYOUT,
    DATABASE_COLORS,
    FONT,
    MAJOR_COLORS,
    RANK_COLORS,
    SCOPUS_STATUS_COLORS
)

# ==========================================================
# STYLE
# ==========================================================

def style(fig):
    """
    Apply dashboard theme to every chart
    """

    fig.update_layout(**CHART_LAYOUT)

    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")

    fig.update_annotations(font_size=12)

    return fig


# ==========================================================
# COLOR MAP
# ==========================================================

def get_color_map(color):

    if color == "Source":
        return DATABASE_COLORS

    if color == "Major Group":
        return MAJOR_COLORS

    if color == "Rank":
        return RANK_COLORS

    return None


# ==========================================================
# BAR CHART
# ==========================================================

def bar(

    df,

    x,

    y,

    color=None,

    title=None,

    barmode="group",

    text=None,

    orientation="v"

):

    kwargs = dict(

        data_frame=df,

        x=x,

        y=y,

        orientation=orientation,

        title=title,

        barmode=barmode,

        text=text

    )

    if color is not None:

        kwargs["color"] = color

        color_map = get_color_map(color)

        if color_map is not None:

            kwargs["color_discrete_map"] = color_map

    fig = px.bar(**kwargs)

    if orientation == "h":

        fig.update_layout(

            yaxis=dict(

                categoryorder="total ascending"

            )

        )

    return style(fig)


# ==========================================================
# HORIZONTAL BAR
# ==========================================================

def horizontal_bar(

    df,

    x,

    y,

    color=None,

    title=None,

    text="Total"

):

    return bar(

        df=df,

        x=x,

        y=y,

        color=color,

        title=title,

        text=text,

        orientation="h"

    )


# ==========================================================
# PIE
# ==========================================================

def pie(

    df,

    values,

    names,

    title=None,

    hole=.45

):

    fig = px.pie(

        df,

        values=values,

        names=names,

        color=names,

        color_discrete_map=get_color_map(names),

        hole=hole

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label"

    )

    return style(fig)


# ==========================================================
# DONUT
# ==========================================================

def donut(

    df,

    values,

    names,

    title=None

):

    return pie(

        df=df,

        values=values,

        names=names,

        title=title,

        hole=.60

    )


# ==========================================================
# LINE
# ==========================================================

def line(

    df,

    x,

    y,

    color=None,

    title=None,

    markers=True

):

    kwargs = dict(

        data_frame=df,

        x=x,

        y=y,

        title=title,

        markers=markers

    )

    if color is not None:

        kwargs["color"] = color

        color_map = get_color_map(color)

        if color_map is not None:

            kwargs["color_discrete_map"] = color_map

    fig = px.line(**kwargs)

    return style(fig)

# ==========================================================
# DASHBOARD CHARTS
# ==========================================================

# ==========================================================
# MAJOR GROUP
# ==========================================================

def major_chart(df):

    return horizontal_bar(

        df=df,

        x="Total",

        y="Major Group",

        color="Major Group",

        text="Total"

    )


# ==========================================================
# AREA GROUP
# ==========================================================

def area_group_chart(df):

    return horizontal_bar(

        df=df,

        x="Total",

        y="Area Group",

        text="Total"

    )


# ==========================================================
# AREA
# ==========================================================

def area_chart(df):

    return horizontal_bar(

        df=df,

        x="Total",

        y="Area",

        text="Total"

    )


# ==========================================================
# DATABASE COVERAGE
# ==========================================================

def database_chart(df):

    return donut(

        df=df,

        values="Total",

        names="Source"

    )


# ==========================================================
# DATABASE BAR
# ==========================================================

def database_bar_chart(df):

    return bar(

        df=df,

        x="Source",

        y="Total",

        color="Source",

        text="Total"

    )


# ==========================================================
# DATABASE SUMMARY
# ==========================================================

def database_summary_chart(df):

    return bar(

        df=df,

        x="Major Group",

        y="Total",

        color="Source",

        barmode="stack",

        text="Total"

    )


# ==========================================================
# AREA SUMMARY
# ==========================================================

def area_summary_chart(df):

    return bar(

        df=df,

        x="Area Group",

        y="Total",

        text="Total"

    )


# ==========================================================
# TOP AREA
# ==========================================================

def top_area_chart(df):

    return horizontal_bar(

        df=df,

        x="Total",

        y="Area",

        text="Total"

    )


# ==========================================================
# TOP PUBLISHER
# ==========================================================

def publisher_chart(df):

    return horizontal_bar(

        df=df,

        x="Total",

        y="Publisher",

        text="Total"

    )


# ==========================================================
# RANK
# ==========================================================

def rank_chart(df):

    return bar(

        df=df,

        x="Rank",

        y="Total",

        color="Source",

        text="Total"

    )


# ==========================================================
# TREND
# ==========================================================

def trend_chart(df, x, y):

    return line(

        df=df,

        x=x,

        y=y

    )


# ==========================================================
# TREND BY DATABASE
# ==========================================================

def trend_database_chart(df, x, y):

    return line(

        df=df,

        x=x,

        y=y,

        color="Source"

    )


# ==========================================================
# TREND BY MAJOR GROUP
# ==========================================================

def trend_major_chart(df, x, y):

    return line(

        df=df,

        x=x,

        y=y,

        color="Major Group"

    )
    
def scopus_status_chart(df):

    data = df.copy()

    # -----------------------------
    # Prepare Status
    # -----------------------------

    data["Scopus Status"] = (
        data["Active or Inactive"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    data.loc[
        data["Scopus Status"] == "",
        "Scopus Status"
    ] = "Not in Scopus"

    order = [
        "Active",
        "Inactive",
        "Not in Scopus"
    ]

    summary = (
        data["Scopus Status"]
        .value_counts()
        .reindex(order, fill_value=0)
        .rename_axis("Status")
        .reset_index(name="Count")
    )

    # -----------------------------
    # Chart
    # -----------------------------

    fig = px.pie(

        summary,

        names="Status",

        values="Count",

        hole=0.55,

        color="Status",

        color_discrete_map=SCOPUS_STATUS_COLORS

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label",

        hovertemplate="<b>%{label}</b><br>%{value} Journals<extra></extra>"

    )

    fig.update_layout(

        **CHART_LAYOUT,

        title="Scopus Status",

        legend=dict(

            orientation="h",

            y=-0.1,

            x=0.5,

            xanchor="center"

        )

    )

    return fig