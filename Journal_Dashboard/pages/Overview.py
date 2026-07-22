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

def safe_plot(
    df,
    chart_func,
    title=None,
    category=None,
    key=None
):

    if df is None or df.empty:
        return

    if "Total" in df.columns:
        if df["Total"].fillna(0).sum() == 0:
            return

    if category:

        if category not in df.columns:
            return

        temp = (
            df[category]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        if temp.eq("").all():
            return

    if title:
        st.subheader(title)

    st.plotly_chart(
        chart_func(df),
        width="stretch",
        key=key          # <-- เพิ่มตรงนี้
    )

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

safe_plot(
    major_df,
    major_chart,
    "Major Group",
    "Major Group",
    "major_chart"
)


safe_plot(
    area_group_df.head(20),
    area_group_chart,
    "Area Group",
    "Area Group",
    "area_group_chart"
)


# ==========================================================
# ROW 2
# ==========================================================


safe_plot(
    area_df.head(20),
    area_chart,
    "Top Area",
    "Area",
    "top_area_chart"
)


safe_plot(
    source_df,
    database_chart,
    "Database Distribution",
    "Source",
    "database_chart"
)


# ==========================================================
# ROW 3
# ==========================================================

def show_chart(df, chart_func, title=None):

    if df is None:
        return

    if df.empty:
        return

    if "Total" in df.columns and df["Total"].sum() == 0:
        return

    st.subheader(title)

    st.plotly_chart(
        chart_func(df),
        width="stretch"
    )

safe_plot(
    rank_source_df,
    rank_chart,
    "Rank Distribution",
    "Rank",
    "rank_distribution"
)
    

st.divider()

safe_plot(
    major_source_df,
    database_summary_chart,
    "Database Journal Group by Major Group",
    "Major Group",
    "database_major"
)

# ==========================================================
# SCOPUS STATUS
# ==========================================================

st.subheader("Scopus Status")


fig = scopus_status_chart(

    master_filter

)


if fig:

    st.plotly_chart(

        fig,

        use_container_width=True

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

        width="stretch"

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