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

FIG_HEIGHT = 600


FIG_MARGIN = dict(

    l=80,

    r=50,

    t=80,

    b=60

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

    "4*": "#1B5E20",

    "A*": "#1B5E20",

    "4": "#2E7D32",

    "A": "#2E7D32",

    "3": "#558B2F",

    "B": "#F9A825",

    "2": "#EF6C00",

    "C": "#D84315",

    "Q1": "#00695C",

    "Q2": "#00897B",

    "Q3": "#FFA000",

    "Q4": "#D84315"

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


    "Business":
        "#42A5F5",


    "Economics":
        "#66BB6A",


    "Management":
        "#FFA726",


    "Accounting":
        "#EF5350",


    "Marketing":
        "#AB47BC",


    "Finance":
        "#26C6DA"

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


    "title_font":
        TITLE_FONT,


    "margin":
        FIG_MARGIN,


    "hoverlabel":
        {

            "font_size": 15

        }

}

# ==========================================================
# CHART PALETTE
# ใช้สำหรับกราฟที่ไม่มี category color เฉพาะ
# ==========================================================

CHART_PALETTE = [

    "#4F80C0",   # Blue

    "#73C088",   # Green

    "#FFC273",   # Yellow

    "#8A49A1",   # Purple

    "#6FA8DC",

    "#93C47D",

    "#F6B26B",

    "#B4A7D6"

]




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