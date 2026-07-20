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

FIG_HEIGHT = 500

FIG_MARGIN = dict(

    l=20,

    r=20,

    t=50,

    b=20

)

# ==========================================================
# DATABASE COLORS
# ==========================================================

DATABASE_COLORS = {

    "ABDC": "#4F80C0",       # Blue

    "Scopus": "#73C088",     # Green

    "Scimago": "#FFC273",    # Orange

    "AJG": "#8A49A1"         # Red

}

# ==========================================================
# RANK COLORS
# ==========================================================

RANK_COLORS = {

    "A*": "#1B5E20",

    "A": "#2E7D32",

    "B": "#F9A825",

    "C": "#EF6C00",

    "Q1": "#00695C",

    "Q2": "#00897B",

    "Q3": "#FFA000",

    "Q4": "#D84315"

}

# ==========================================================
# KPI COLORS
# ==========================================================

KPI_COLORS = {

    "Journal":"#37474F",

    "ABDC":"#4F80C0",

    "Scopus":"#73C088",

    "Scimago":"#FFC273",

    "AJG":"#8A49A1"

}

# ==========================================================
# MAJOR GROUP COLORS
# ==========================================================

MAJOR_COLORS = {

    "Business":"#42A5F5",

    "Economics":"#66BB6A",

    "Management":"#FFA726",

    "Accounting":"#EF5350",

    "Marketing":"#AB47BC",

    "Finance":"#26C6DA"

}

# ==========================================================
# SCOPUS STATUS COLORS
# ==========================================================

SCOPUS_STATUS_COLORS = {

    "Active": "#73C088",          # Green (ใช้สีเดียวกับ Scopus)

    "Inactive": "#E57373",        # Soft Red

    "Not in Scopus": "#B0BEC5"    # Grey

}

# ==========================================================
# CHART DEFAULT
# ==========================================================

CHART_LAYOUT = dict(

    template="plotly_white",

    height=FIG_HEIGHT,

    font_family=FONT,

    margin=FIG_MARGIN,

    legend_title=None

)

# ==========================================================
# STREAMLIT CSS
# ==========================================================

STREAMLIT_STYLE = """

<style>

.block-container{

    padding-top:1rem;

    padding-bottom:1rem;

}

h1{

    color:#1565C0;

}

h2{

    color:#1565C0;

}

h3{

    color:#455A64;

}

div[data-testid="metric-container"]{

    background:#FAFAFA;

    border-radius:12px;

    padding:10px;

    border:1px solid #E0E0E0;

}

thead tr th{

    background:#1565C0 !important;

    color:white !important;

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
