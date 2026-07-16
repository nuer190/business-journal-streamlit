# ==========================================================
# OVERVIEW PAGE
# ==========================================================

import streamlit as st
import pandas as pd

from utils import load_data

from filters import (
    build_sidebar_filters,
    apply_filters
)

from summary import (
    database_summary,
    major_summary,
    area_group_summary,
    area_summary,
    source_summary,
    rank_summary,
    major_source_summary,
    rank_source_summary,
    journal_summary,
    top_area,
    top_publisher,
    top_rank
)

from charts import *

from theme import *

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Journal Analytics Dashboard",

    page_icon="📊",

    layout="wide"

)

from theme import apply_theme

apply_theme()

st.title("📊 Journal Analytics Dashboard")

st.caption(

    "Overview of Journal Database"

)

# ==========================================================
# LOAD DATA
# ==========================================================

master, area = load_data()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Filter")

filters = build_sidebar_filters(area)

# ==========================================================
# APPLY FILTER
# ==========================================================

area_filter = apply_filters(

    area,

    major_groups=filters["major_groups"],

    area_groups=filters["area_groups"],

    areas=filters["areas"],

    sources=filters["sources"],

    ranks=filters["ranks"]

)

# ==========================================================
# FILTER MASTER
# ==========================================================

if len(area_filter):

    journal_keys = area_filter["Journal_Key"].unique()

    master_filter = master[

        master["Journal_Key"]

        .isin(journal_keys)

    ]

else:

    master_filter = master.copy()

# ==========================================================
# COMPARE
# ==========================================================

st.sidebar.divider()

compare_mode = st.sidebar.checkbox(

    "Compare Mode",

    value=False

)

compare_column = None

compare_values = []

if compare_mode:

    compare_column = st.sidebar.selectbox(

        "Compare By",

        [

            "Major Group",

            "Area Group",

            "Area",

            "Source",

            "Rank"

        ]

    )

    compare_values = st.sidebar.multiselect(

        "Select Value",

        sorted(

            area_filter[compare_column]

            .dropna()

            .unique()

        )

    )

# ==========================================================
# KPI
# ==========================================================

info = database_summary(

    master_filter

)

col1,col2,col3,col4,col5 = st.columns(5)

with col1:

    st.metric(

        "Journal",

        f"{info['Journal']:,}"

    )

with col2:

    st.metric(

        "ABDC",

        f"{info['ABDC']:,}"

    )

with col3:

    st.metric(

        "Scopus",

        f"{info['Scopus']:,}"

    )

with col4:

    st.metric(

        "Scimago",

        f"{info['Scimago']:,}"

    )

with col5:

    st.metric(

        "AJG",

        f"{info['AJG']:,}"

    )

# ==========================================================
# QUICK SUMMARY
# ==========================================================

st.divider()

left,right = st.columns([2,1])

with left:

    st.subheader("Current Filter")

    st.write(

        f"Journal : **{master_filter['Journal_Key'].nunique():,}**"

    )

    st.write(

        f"Area Record : **{len(area_filter):,}**"

    )

with right:

    st.subheader("Compare")

    if compare_mode:

        st.success(compare_column)

        st.write(compare_values)

    else:

        st.info("Disabled")

# ==========================================================
# SUMMARY DATA
# ==========================================================

major_df = major_summary(

    area_filter

)

area_group_df = area_group_summary(

    area_filter

)

area_df = area_summary(

    area_filter

)

source_df = source_summary(

    area_filter

)

rank_df = rank_summary(

    area_filter

)

major_source_df = major_source_summary(

    area_filter

)

rank_source_df = rank_source_summary(

    area_filter

)

journal_df = journal_summary(

    master_filter

)

# ==========================================================
# PREVIEW DATA
# ==========================================================

with st.expander(

    "Preview Data"

):

    tab1,tab2 = st.tabs(

        [

            "Journal Master",

            "Journal Area"

        ]

    )

    with tab1:

        st.dataframe(

            master_filter,

            use_container_width=True,

            height=350,

            hide_index=True

        )

    with tab2:

        st.dataframe(

            area_filter,

            use_container_width=True,

            height=350,

            hide_index=True

        )

# ==========================================================
# SAVE SESSION
# ==========================================================

st.session_state["master"] = master_filter

st.session_state["area"] = area_filter

st.session_state["compare"] = compare_mode

st.session_state["compare_column"] = compare_column

st.session_state["compare_values"] = compare_values


# ==========================================================
# ANALYTICS OVERVIEW
# ==========================================================

st.divider()

st.header("📊 Analytics Overview")

# ==========================================================
# ROW 1
# ==========================================================

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# Major Group
# ----------------------------------------------------------

with col1:

    st.subheader("Major Group")

    st.plotly_chart(

        major_chart(major_df),

        use_container_width=True

    )

# ----------------------------------------------------------
# Area Group
# ----------------------------------------------------------

with col2:

    st.subheader("Area Group")

    st.plotly_chart(

        area_group_chart(

            area_group_df.head(20)

        ),

        use_container_width=True

    )

# ==========================================================
# ROW 2
# ==========================================================

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# Area
# ----------------------------------------------------------

with col1:

    st.subheader("Top Area")

    st.plotly_chart(

        area_chart(

            area_df.head(20)

        ),

        use_container_width=True

    )

# ----------------------------------------------------------
# Database
# ----------------------------------------------------------

with col2:

    st.subheader("Database Distribution")

    st.plotly_chart(

        database_chart(

            source_df

        ),

        use_container_width=True

    )

# ==========================================================
# ROW 3
# ==========================================================

def show_chart(df, chart_func, title=None):

    if df.empty:
        return

    if title:
        st.subheader(title)

    st.plotly_chart(
        chart_func(df),
        use_container_width=True
    )

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# Rank
# ----------------------------------------------------------

with col1:
    show_chart(
        rank_source_df,
        rank_chart,
        "Rank Distribution"
    )
    

with col2:
    

    area_top = top_area(
        
        area_filter,
        10
    )

    show_chart(
        area_top,
        top_area_chart,
        "Top 10 Area"
    )

st.divider()

show_chart(
    major_source_df,
    database_summary_chart,
    "Database Coverage by Major Group"
)


# ==========================================================
# QUICK STATISTICS
# ==========================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "Major Group",

        major_df["Major Group"].nunique()

    )

with col2:

    st.metric(

        "Area Group",

        area_group_df["Area Group"].nunique()

    )

with col3:

    st.metric(

        "Area",

        area_df["Area"].nunique()

    )
    
# ==========================================================
# COMPARE
# ==========================================================

if compare_mode:

    st.divider()

    st.header("📈 Compare")

    compare_df = (

        area_filter

        .drop_duplicates(

            [compare_column, "Journal_Key"]

        )

        .groupby(

            compare_column,

            as_index=False

        )

        .agg(

            Total=("Journal_Key", "count")

        )

    )

    if len(compare_values):

        compare_df = compare_df[

            compare_df[compare_column]

            .isin(compare_values)

        ]

    st.plotly_chart(

        bar(

            compare_df,

            x=compare_column,

            y="Total",

            color=compare_column

        ),

        use_container_width=True

    )


# ==========================================================
# SUMMARY TABLE
# ==========================================================

st.divider()

st.header("Summary Table")

summary_table = area_summary(

    area_filter

)

st.dataframe(

    summary_table,

    use_container_width=True,

    height=450,

    hide_index=True

)

summary_csv = summary_table.to_csv(

    index=False

).encode(

    "utf-8"

)

st.download_button(

    "⬇ Download Summary",

    summary_csv,

    file_name="summary.csv",

    mime="text/csv"

)

# ==========================================================
# COMPARE TABLE
# ==========================================================

if compare_mode:

    st.divider()

    st.header("Compare Table")

    compare_table = area_filter.copy()

    if len(compare_values):

        compare_table = compare_table[

            compare_table[compare_column]

            .isin(compare_values)

        ]

    compare_table = (

        compare_table

        .sort_values(

            "Journal Title"

        )

    )

    st.dataframe(

        compare_table,

        use_container_width=True,

        height=450,

        hide_index=True

    )

    compare_csv = compare_table.to_csv(

        index=False

    ).encode(

        "utf-8"

    )

    st.download_button(

        "⬇ Download Compare",

        compare_csv,

        file_name="compare.csv",

        mime="text/csv"

    )
    
# ==========================================================
# JOURNAL INSIGHTS
# ==========================================================

st.divider()

st.header("📌 Journal Insights")

col1, col2 = st.columns(2)

# ==========================================================
# TOP PUBLISHER
# ==========================================================

with col1:

    st.subheader("Top Publisher")

    publisher_df = top_publisher(

        master_filter,

        n=15

    )

    st.plotly_chart(

        publisher_chart(

            publisher_df

        ),

        use_container_width=True

    )

# ==========================================================
# TOP RANK
# ==========================================================

with col2:

    st.subheader("Top Rank")

    rank_top = top_rank(

        area_filter,

        n=15

    )

    st.plotly_chart(

        horizontal_bar(

            rank_top,

            x="Total",

            y="Rank"

        ),

        use_container_width=True

    )
    
# ==========================================================
# COVERAGE SUMMARY
# ==========================================================

st.divider()

st.header("📈 Database Coverage")

coverage = database_summary(

    master_filter

)

coverage_df = pd.DataFrame({

    "Database":[

        "ABDC",

        "Scopus",

        "Scimago",

        "AJG"

    ],

    "Journal":[

        coverage["ABDC"],

        coverage["Scopus"],

        coverage["Scimago"],

        coverage["AJG"]

    ]

})

st.plotly_chart(

    database_bar_chart(

        coverage_df.rename(

            columns={

                "Database":"Source",

                "Journal":"Total"

            }

        )

    ),

    use_container_width=True

)

# ==========================================================
# COVERAGE PERCENT
# ==========================================================

st.divider()

st.header("Coverage")

total = coverage["Journal"]

col1,col2,col3,col4 = st.columns(4)

for col,db in zip(

    [col1,col2,col3,col4],

    ["ABDC","Scopus","Scimago","AJG"]

):

    percent = 0

    if total:

        percent = coverage[db]/total*100

    with col:

        st.metric(

            db,

            f"{percent:.1f}%"

        )
        
# ==========================================================
# DATA STATISTICS
# ==========================================================

st.divider()

st.header("Statistics")

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.metric(

        "Major Group",

        area_filter["Major Group"].nunique()

    )

with c2:

    st.metric(

        "Area Group",

        area_filter["Area Group"].nunique()

    )

with c3:

    st.metric(

        "Area",

        area_filter["Area"].nunique()

    )

with c4:

    st.metric(

        "Publisher",

        master_filter["Publisher"].nunique()

    )