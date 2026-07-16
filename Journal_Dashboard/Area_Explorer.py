# ==========================================================
# AREA EXPLORER
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from filters import apply_filters
from config import *

from utils import load_data

master, area = load_data()

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Area Explorer",

    page_icon="🗺️",

    layout="wide"

)

st.title("🗺️ Area Explorer")

st.caption(

    "Explore Journal by Major Group / Area Group / Area"

)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("Filter")

major = st.sidebar.multiselect(

    "Major Group",

    sorted(

        area["Major Group"]

        .dropna()

        .unique()

    )

)

temp = area.copy()

if major:

    temp = temp[

        temp["Major Group"]

        .isin(major)

    ]

area_group = st.sidebar.multiselect(

    "Area Group",

    sorted(

        temp["Area Group"]

        .dropna()

        .unique()

    )

)

if area_group:

    temp = temp[

        temp["Area Group"]

        .isin(area_group)

    ]

area_select = st.sidebar.multiselect(

    "Area",

    sorted(

        temp["Area"]

        .dropna()

        .unique()

    )

)

source = st.sidebar.multiselect(

    "Source",

    sorted(

        area["Source"]

        .dropna()

        .unique()

    )

)

rank = st.sidebar.multiselect(

    "Rank",

    sorted(

        area["Rank"]

        .fillna("-")

        .astype(str)

        .unique()

    )

)

# ==========================================================
# FILTER
# ==========================================================

area_filter = apply_filters(

    area,

    major_groups=major,

    area_groups=area_group,

    areas=area_select,

    sources=source,

    ranks=rank

)

journal_filter = master[

    master["Journal Title"]

    .isin(

        area_filter["Journal Title"]

    )

]
# ==========================================================
# KPI
# ==========================================================

st.divider()

c1,c2,c3,c4 = st.columns(4)

c1.metric(

    "Journal",

    len(

        journal_filter

    )

)

c2.metric(

    "Publisher",

    journal_filter["Publisher"]

    .nunique()

)

c3.metric(

    "Area",

    area_filter["Area"]

    .nunique()

)

c4.metric(

    "Database",

    area_filter["Source"]

    .nunique()

)

# ==========================================================
# AREA SUMMARY
# ==========================================================

st.divider()

summary = (

    area_filter

    .groupby(

        [

            "Major Group",

            "Area Group",

            "Area"

        ]

    )

    .size()

    .reset_index(name="Journal")

)

st.dataframe(

    summary,

    use_container_width=True,

    height=350

)