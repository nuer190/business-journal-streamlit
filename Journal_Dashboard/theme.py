# ==========================================================
# theme.py
# Journal Dashboard Theme
# ==========================================================


# ==========================================================
# FONT
# ==========================================================

FONT = "Segoe UI"

# ==========================================================
# FIGURE
# ==========================================================

FIG_HEIGHT = 850


FIG_MARGIN = dict(

    l=100,

    r=80,

    t=100,

    b=80

)

# ==========================================================
# CHART FONT
# ==========================================================

CHART_FONT = {

    "family": FONT,

    "size": 17

}


TITLE_FONT = {

    "family": FONT,

    "size": 26

}

# ==========================================================
# CHART STYLE
# ==========================================================

GRID_COLOR = "#E8EEF5"

AXIS_COLOR = "#5B6573"

TEXT_COLOR = "#37474F"

PAPER_COLOR = "white"

PLOT_COLOR = "white"

BAR_BORDER_COLOR = "white"

BAR_BORDER_WIDTH = 1.2

HOVER_LABEL = dict(

    bgcolor="white",

    bordercolor="#D9E2EC",

    font=dict(

        family=FONT,

        size=15,

        color=TEXT_COLOR

    )

)

# ==========================================================
# DATABASE COLORS
# ==========================================================

DATABASE_COLORS = {

    "ABDC": "#4F80C0",

    "Scopus": "#73C088",

    "Scimago": "#FFC273",

    "AJG": "#8A49A1"

}



# ==========================================================
# DATABASE LIGHT COLORS
# ใช้สำหรับ Table / Background
# ==========================================================

DATABASE_LIGHT_COLORS = {

    "ABDC":
        "rgba(79,128,192,0.12)",


    "Scopus":
        "rgba(115,192,136,0.12)",


    "Scimago":
        "rgba(255,194,115,0.15)",


    "AJG":
        "rgba(138,73,161,0.12)"

}



# ==========================================================
# RANK COLORS
# ==========================================================

RANK_COLORS = {

    "A*": "#2E5FA8",
    "A":  "#4F80C0",
    "B":  "#79A3D5",
    "C":  "#B7D0EA",
    "4*": "#5F2A77",
    "4":  "#73408D",
    "3":  "#8A49A1",
    "2":  "#A66CBD",
    "1":  "#CBB0DA",
    "Q1": "#E49B32",
    "Q2": "#F3B65B",
    "Q3": "#FFC273",
    "Q4": "#FFE0AE",

}



# ==========================================================
# KPI COLORS
# ==========================================================

KPI_COLORS = {

    "Journal": "#37474F",

    "ABDC": "#4F80C0",

    "Scopus": "#73C088",

    "Scimago": "#FFC273",

    "AJG": "#8A49A1"

}



# ==========================================================
# MAJOR GROUP COLORS
# ==========================================================

MAJOR_COLORS = {

    "Business": "#4F80C0",

    "Economics": "#6794CA",

    "Management": "#73C088",

    "Accounting": "#8FD0A3",

    "Marketing": "#FFC273",

    "Finance": "#8A49A1"

}



# ==========================================================
# SCOPUS STATUS COLORS
# ==========================================================

SCOPUS_STATUS_COLORS = {

    "Active":
        "#73C088",


    "Inactive":
        "#E57373",


    "Not in Scopus":
        "#B0BEC5"

}



# ==========================================================
# CHART DEFAULT
# ==========================================================

CHART_LAYOUT = {

    "template":
        "plotly_white",

    "height":
        FIG_HEIGHT,

    "font":
        CHART_FONT,

    "margin":
        FIG_MARGIN,

    "hoverlabel":
        HOVER_LABEL

}

# ==========================================================
# CHART PALETTE
# ==========================================================

CHART_PALETTE = [

    "#4F80C0",
    "#6794CA",
    "#8CB1DA",

    "#73C088",
    "#8FD0A3",
    "#B6E2C2",

    "#FFC273",
    "#FFD08F",
    "#FFE1B8",

    "#8A49A1",
    "#A66CBD",
    "#C6A0D7"

]

BACKGROUND_COLORS = {

    "Blue": "#F4F8FC",

    "Green": "#F5FBF7",

    "Orange": "#FFF9F2",

    "Purple": "#FAF6FC"

}

# ==========================================================
# STREAMLIT CSS
# ==========================================================

STREAMLIT_STYLE = """

<style>


/* ===============================
   MAIN CONTAINER
================================ */

.block-container{

    padding-top:1rem;

    padding-bottom:2rem;

}



/* ===============================
   HEADER
================================ */


h1{

    color:#1565C0;

    font-weight:700;

}


h2{

    color:#1565C0;

}


h3{

    color:#455A64;

}



/* ===============================
   METRIC CARD
================================ */


div[data-testid="metric-container"]{


    background:#FAFAFA;


    border-radius:12px;


    padding:15px;


    border:1px solid #E0E0E0;


}



div[data-testid="metric-container"] label{


    font-size:15px;


}



div[data-testid="metric-container"] 
[data-testid="stMetricValue"]{


    font-size:28px;


    font-weight:700;


}



/* ===============================
   DATAFRAME
================================ */


[data-testid="stDataFrame"]{


    font-size:15px;


}



/* ===============================
   TABLE HEADER
================================ */


thead tr th{


    background:#1565C0 !important;


    color:white !important;


    font-weight:700 !important;


}



/* ===============================
   SIDEBAR
================================ */


section[data-testid="stSidebar"]{


    background:#F8FAFC;


}



/* ===============================
   DIVIDER
================================ */


hr{


    margin-top:1rem;

    margin-bottom:1rem;


}



</style>

"""




# ==========================================================
# APPLY THEME
# ==========================================================

import streamlit as st



def apply_theme():


    st.markdown(

        STREAMLIT_STYLE,

        unsafe_allow_html=True

    )