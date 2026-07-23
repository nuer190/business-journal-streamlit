# ==========================================================
# charts.py
# Journal Dashboard Chart Library (Refactor Version)
# ==========================================================

import plotly.express as px

from theme import (
    CHART_LAYOUT,
    DATABASE_COLORS,
    MAJOR_COLORS,
    RANK_COLORS,
    SCOPUS_STATUS_COLORS,
    CHART_PALETTE,
    GRID_COLOR,
    AXIS_COLOR,
    TEXT_COLOR,
    PAPER_COLOR,
    PLOT_COLOR,
    BAR_BORDER_COLOR,
    BAR_BORDER_WIDTH,
    AREA_GRADIENT_START,
    AREA_GRADIENT_END,
    AREA_BLUE_SCALE,
    HOVER_LABEL
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
            "",
            " "
        ],
        None
    )

    return df.dropna()

# ==========================================================
# CREATE GRADIENT COLORS
# ==========================================================

def create_gradient_colors(n):


    import plotly.colors as colors

    if n <= 1:
        return [
            AREA_BLUE_SCALE[0]
        ]

    return colors.sample_colorscale(
        AREA_BLUE_SCALE,
        [
            i/(n-1)
            for i in range(n)
        ]
    )

# ==========================================================
# GRADIENT COLOR
# ==========================================================

def apply_gradient_color(fig, df):

    gradient_colors = create_gradient_colors(

        len(df)
    )
    
    for trace in fig.data:

        trace.marker.color = gradient_colors

    return fig

# ==========================================================
# COLOR SYSTEM
# ==========================================================

def get_color_map(column):

    COLOR_MAP = {

        "Source":
            DATABASE_COLORS,

        "Major Group":
            MAJOR_COLORS,

        "Rank":
            RANK_COLORS,

        "Status":
            SCOPUS_STATUS_COLORS,
        
        "Area Group": AREA_BLUE_SCALE,

        "Area": AREA_BLUE_SCALE,
    }
    return COLOR_MAP.get(column)

def get_gradient_map(values):


    import plotly.colors as colors


    n = len(values)


    if n <= 1:

        color_list = [
            AREA_BLUE_SCALE[0]
        ]

    else:

        color_list = colors.sample_colorscale(

            AREA_BLUE_SCALE,

            [
                i/(n-1)

                for i in range(n)

            ]

        )


    return dict(

        zip(

            values,

            color_list

        )

    )

# ==========================================================
# GLOBAL CHART STYLE
# ==========================================================

def style(fig,show_legend = False):

    fig.update_layout(

        **CHART_LAYOUT,
        
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=PLOT_COLOR,
        legend=dict(
            
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(
                size=14
            )

        )

    )

    fig.update_xaxes(
        title_text="",
        tickfont=dict(
            size=14
        ),

        linecolor=GRID_COLOR,
        gridcolor=GRID_COLOR,
        showgrid=True,
        gridwidth=1,
        zeroline=False,
        showline=True,
        ticks="outside",
        color=AXIS_COLOR
    )

    fig.update_yaxes(
        title_text="",
        tickfont=dict(
            size=14
        ),
        
        linecolor=GRID_COLOR,
        gridcolor=GRID_COLOR,
        showgrid=True,
        gridwidth=1,
        zeroline=False,
        showline=True,
        ticks="outside",
        color=AXIS_COLOR
    )

    fig.update_coloraxes(

        colorbar_title_text=""
    )
    
    fig.for_each_trace(
        lambda trace:
        trace.update(

            name=""

            if str(trace.name).lower()

            in [

                "undefined",

                "none",

                ""
            ]

            else trace.name

        )

    )
    return fig

# ==========================================================
# GENERIC BAR BUILDER
# ==========================================================

def build_bar(
    
    df,
    x,
    y,
    color=None,
    text=None,
    orientation="v",
    barmode="group",
    gradient=False

):
    df = clean_chart_data(df)
    params = {

        "data_frame":
            df,
        "x":
            x,
        "y":
            y,

        "orientation":
            orientation,

        "text":
            text,

        "barmode":
            barmode,

        "labels":
            {
                x:"",

                y:"",

                color:""

                if color

                else ""
            }
    }

    if color:
        params["color"] = color
        if color in [

            "Area",

            "Area Group"

        ]:

            color_map = get_gradient_map(

                df[color].tolist()

            )

        else:

            color_map = get_color_map(color)

        if color_map:

            params[
                "color_discrete_map"
                
            ] = color_map
        else:
            params[
                "color_discrete_sequence"

            ] = CHART_PALETTE
            
    if gradient:
        params["color"] = y
        params["color_continuous_scale"] = AREA_BLUE_SCALE
        params["color_continuous_midpoint"] = df[x].median()

    else:

        params[

            "color_discrete_sequence"

        ] = CHART_PALETTE

    fig = px.bar(
        
        **params
        
        
    )
    
    if gradient:

        fig = apply_gradient_color(
            fig,
            df
            )
    
    fig.update_layout(

        bargap=0.15,

        bargroupgap=0.05

    )

    if orientation == "h":
       
        fig.update_layout(

            yaxis=dict(

                categoryorder="total ascending"

            )

        )


        fig.update_traces(

            width=0.7

        )

    fig.update_traces(

        marker_line_color=

            BAR_BORDER_COLOR,

        marker_line_width=

            BAR_BORDER_WIDTH,

        opacity=0.95,

        textposition=

            "outside",

        cliponaxis=False,
        
        width=0.75

    )

    return style(fig)

# ==========================================================
# BAR
# ==========================================================

def bar(

    df,
    x,
    y,
    color=None,
    text=None,
    barmode="group"

):

    return build_bar(

        df,
        x,
        y,
        color,
        text,
        "v",
        barmode

    )
    


# ==========================================================
# HORIZONTAL BAR
# ==========================================================

def horizontal_bar(
    df,
    x,
    y,
    color=None,
    text="Total",
    gradient=False
):
    
    return build_bar(
        df,
        x,
        y,
        color,
        text,
        "h",
        gradient=gradient
    )
    
    fig.update_layout(
        showlegend=False
    )
    return fig
    
# ==========================================================
# DONUT / PIE
# ==========================================================

def donut(

    df,
    values,
    names

):

    df = clean_chart_data(df)

    params = {

        "data_frame":

            df,

        "values":

            values,

        "names":

            names,

        "hole":

            0.62,

        "color":

            names

    }

    color_map = get_color_map(names)

    if color_map:

        params[

            "color_discrete_map"

        ] = color_map

    else:

        params[

            "color_discrete_sequence"

        ] = CHART_PALETTE

    fig = px.pie(

        **params

    )

    fig.update_traces(

        textposition=

            "inside",

        textinfo=

            "percent",

        marker=dict(

            line=dict(

                color="white",

                width=2

            )

        ),

        hovertemplate=

            "<b>%{label}</b><br>"

            "%{value} Journals"

            "<extra></extra>"

    )
    return style(
        fig,
        show_legend=True)

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
    
    fig.update_layout(
        showlegend=False
    )
    
    return fig

# ==========================================================
# AREA GROUP
# ==========================================================

def area_group_chart(df):

    df = df.sort_values(
        "Total",
        ascending=False
    )

    fig = horizontal_bar(
        df,
        x="Total",
        y="Area Group",
        color="Area Group"

    )

    fig.update_layout(
        showlegend=False
    )

    return fig

# ==========================================================
# AREA
# ==========================================================

def area_chart(df):

    df = df.sort_values(
        "Total",
        ascending=False
    )

    fig = horizontal_bar(
        df,
        x="Total",
        y="Area",
        color="Area"
    )

    fig.update_layout(
        showlegend=False
    )

    return fig
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

    fig = bar(
        df,
        x="Rank",
        y="Total",
        color="Rank",
        text="Total"
    )

    fig.update_layout(
        showlegend=False
    )

    return fig

# ==========================================================
# DATABASE BY MAJOR GROUP
# ==========================================================

def database_summary_chart(df):


    fig = bar(

        df,

        x="Major Group",

        y="Total",

        color="Source",

        barmode="stack",

        text="Total"

    )


    fig.update_layout(

        showlegend=True

    )


    return fig
    

# ==========================================================
# SCOPUS STATUS
# ==========================================================

def scopus_status_chart(df):

    if "Active or Inactive" not in df.columns:


        return None

    data = df.copy()

    data["Scopus Status"] = (

        data["Active or Inactive"]

        .fillna(

            "Not in Scopus"

        )

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


    fig = donut(

        summary,

        values="Count",

        names="Status"

    )

    return fig