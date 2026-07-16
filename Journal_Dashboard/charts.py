# ==========================================================
# charts.py
# Journal Dashboard Chart Library
# ==========================================================

from turtle import st

import plotly.express as px
import plotly.graph_objects as go
from theme import DATABASE_COLORS

from theme import (
    DATABASE_COLORS,
    FIG_HEIGHT,
    FONT
)

# ==========================================================
# INTERNAL
# ==========================================================

def style(fig):

    fig.update_layout(
        
        template="plotly_white",
        
        height=FIG_HEIGHT,
        
        font_family=FONT,
        margin=dict(l=20, r=20, t=50, b=20),
        legend_title_text="",
        title_text=""
    )

    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")

    fig.update_annotations(text="")

    return fig


# ==========================================================
# HORIZONTAL BAR
# ==========================================================

def horizontal_bar(

    df,

    x,

    y,

    title=None,

    color=None,

    text="Total"

):

    fig = px.bar(

        df,

        x=x,

        y=y,

        orientation="h",

        text=text,

        color=color,
        color_discrete_map=DATABASE_COLORS

    )

    fig.update_layout(

        title=title,

        yaxis=dict(

            categoryorder="total ascending"

        )

    )

    return style(fig)


# ==========================================================
# BAR
# ==========================================================

def bar(

    df,

    x,

    y,

    title=None,

    color=None,

    barmode="group"

):

    kwargs = dict(
        data_frame=df,
        x=x,
        y=y,
        title=title,
        barmode=barmode
    )

    if color is not None:
        kwargs["color"] = color

        if color == "Source":

            kwargs["color_discrete_map"] = DATABASE_COLORS

    fig = px.bar(**kwargs)

    return style(fig)


# ==========================================================
# PIE
# ==========================================================

def pie(

    df,

    values,

    names,

    title=None

):

    fig = px.pie(

        df,

        values=values,

        names=names,

        color=names,

        color_discrete_map=DATABASE_COLORS

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label"

    )

    fig.update_layout(

        title=title

    )

    return style(fig)

# ==========================================================
# DASHBOARD CHART
# ==========================================================


# ==========================================================
# MAJOR GROUP
# ==========================================================

def major_chart(df):

    return horizontal_bar(

        df,

        x="Total",

        y="Major Group"

    )


# ==========================================================
# AREA GROUP
# ==========================================================

def area_group_chart(df):

    return horizontal_bar(

        df,

        x="Total",

        y="Area Group"

    )


# ==========================================================
# AREA
# ==========================================================

def area_chart(df):

    return horizontal_bar(

        df,

        x="Total",

        y="Area"

    )


# ==========================================================
# DATABASE
# ==========================================================

def database_chart(df):

    return pie(

        df,

        values="Total",

        names="Source"

    )


# ==========================================================
# DATABASE BAR
# ==========================================================

def database_bar_chart(df):

    return bar(

        df,

        x="Source",

        y="Total",

        color="Source"

    )


# ==========================================================
# DATABASE SUMMARY
# ==========================================================

def database_summary_chart(df):

    return bar(

        df,

        x="Major Group",

        y="Total",

        color="Source",

        barmode="stack"

    )


# ==========================================================
# AREA SUMMARY
# ==========================================================

def area_summary_chart(df):

    return bar(

        df,

        x="Area Group",

        y="Total"

    )


# ==========================================================
# TOP AREA
# ==========================================================

def top_area_chart(df):

    return horizontal_bar(

        df,

        x="Total",

        y="Area"

    )


# ==========================================================
# TOP PUBLISHER
# ==========================================================

def publisher_chart(df):

    return horizontal_bar(

        df,

        x="Total",

        y="Publisher"

    )
    
# ==========================================================
# RANK CHART
# ==========================================================

def rank_chart(df):

    return bar(

        df,

        x="Rank",

        y="Total",

        color="Source",

        barmode="group"

    )
    
def show_chart(df, chart_func, title=None):

    if df.empty:
        return

    if title:
        st.subheader(title)

    st.plotly_chart(
        chart_func(df),
        use_container_width=True
    )