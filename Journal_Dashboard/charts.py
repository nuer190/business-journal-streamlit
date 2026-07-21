# ==========================================================
# charts.py
# Journal Dashboard Chart Library
# ==========================================================

import plotly.express as px

from theme import (
    CHART_LAYOUT,
    DATABASE_COLORS,
    MAJOR_COLORS,
    RANK_COLORS,
    SCOPUS_STATUS_COLORS,
    CHART_PALETTE
)


# ==========================================================
# CLEAN DATA
# ==========================================================

def clean_chart_data(df):

    df = df.copy()


    df = df.replace(

        [
            "Undefined",
            "undefined",
            "None",
            "none",
            "nan",
            ""

        ],

        None

    )


    return df.dropna()



# ==========================================================
# STYLE
# ==========================================================

def style(fig):

    fig.update_layout(

        **CHART_LAYOUT,

        legend=dict(

            font=dict(
                size=14
            )

        )

    )


    # ลบ undefined จาก legend

    fig.for_each_trace(

        lambda trace:

        trace.update(
            name=""
            if trace.name in [
                "undefined",
                "Undefined",
                "None"
            ]
            else trace.name
        )

    )


    fig.update_xaxes(

        title_text="",

        tickfont=dict(
            size=14
        )

    )


    fig.update_yaxes(

        title_text="",

        tickfont=dict(
            size=14
        )

    )


    return fig



# ==========================================================
# COLOR MAP
# ==========================================================

def get_color_map(column):


    if column == "Source":

        return DATABASE_COLORS


    if column == "Major Group":

        return MAJOR_COLORS


    if column == "Rank":

        return RANK_COLORS


    return None



# ==========================================================
# BAR
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


    df = clean_chart_data(df)


    params = {


        "data_frame": df,


        "x": x,


        "y": y,


        "orientation": orientation,


        "title": title,


        "text": text


    }



    if color:


        params["color"] = color


        color_map = get_color_map(color)



        if color_map:


            params["color_discrete_map"] = color_map



        else:

            params["color_discrete_sequence"] = CHART_PALETTE



    else:


        params["color_discrete_sequence"] = CHART_PALETTE




    fig = px.bar(

        **params

    )



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

    text="Total"

):


    return bar(

        df,

        x=x,

        y=y,

        color=color,

        text=text,

        orientation="h"

    )



# ==========================================================
# DONUT
# ==========================================================

def donut(

    df,

    values,

    names

):


    df = clean_chart_data(df)



    fig = px.pie(

        df,

        values=values,

        names=names,

        hole=0.55,

        color=names,


        color_discrete_map=get_color_map(names)


    )



    fig.update_traces(

        textposition="inside",

        textinfo="percent+label"

    )



    return style(fig)



# ==========================================================
# MAJOR GROUP
# ==========================================================

def major_chart(df):


    fig = horizontal_bar(

        df,

        x="Total",

        y="Major Group",

        color="Major Group"

    )



    # remove legend

    fig.update_layout(

        showlegend=False

    )


    return fig



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
# DATABASE DISTRIBUTION
# ==========================================================

def database_chart(df):


    return donut(

        df,

        values="Total",

        names="Source"

    )



# ==========================================================
# RANK DISTRIBUTION
# ==========================================================

def rank_chart(df):


    return bar(

        df,

        x="Rank",

        y="Total",

        color="Source",

        text="Total"

    )



# ==========================================================
# DATABASE BY MAJOR GROUP
# ==========================================================

def database_summary_chart(df):


    return bar(

        df,

        x="Major Group",

        y="Total",

        color="Source",

        barmode="stack",

        text="Total"

    )



# ==========================================================
# SCOPUS STATUS
# ==========================================================

def scopus_status_chart(df):


    if "Active or Inactive" not in df.columns:

        return None



    data = df.copy()



    data["Scopus Status"] = (

        data["Active or Inactive"]

        .fillna("Not in Scopus")

        .replace(

            "",

            "Not in Scopus"

        )

    )



    summary = (

        data["Scopus Status"]

        .value_counts()

        .reset_index()

    )



    summary.columns = [

        "Status",

        "Count"

    ]



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

        textinfo="percent+label"

    )


    return style(fig)