# ==========================================================
# AREA EXPLORER
# ==========================================================

import streamlit as st
import pandas as pd

from utils import load_data
from filters import (
    build_sidebar_filters,
    apply_filters
)

# ==========================================================
# LOAD DATA
# ==========================================================
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
    "Explore Journals by Major Group, Area Group, Area, Source and Rank"
)

# ==========================================================
# SESSION STATE
# ==========================================================

if "selected_journal" not in st.session_state:
    st.session_state.selected_journal = None

# ==========================================================
# SIDEBAR FILTER
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
    
if area_filter.empty:
    st.warning(
        "⚠️ No journal found with selected filters"
    )
    st.stop()

# ==========================================================
# JOURNAL FILTER
# ==========================================================

journal_filter = (
    master[
        master["Journal Title"].isin(
            area_filter["Journal Title"]
        )
    ][
        [
            "Journal Title",
            "Publisher",
            "ISSN",
            "ISSNOnline"
        ]
    ]
    .drop_duplicates()

)

# ==========================================================
# GET ALL JOURNAL QUALITY RANK
# ==========================================================

selected_journals = (
    area_filter["Journal Title"]
    .unique()
)


rank_table = (
    area[
        area["Journal Title"]
        .isin(selected_journals)
    ]
    .dropna(subset=["Rank"])
    .copy()
)

# ตัดค่า Rank ที่ว่าง
rank_table["Rank"] = (
    rank_table["Rank"]
    .astype(str)
    .str.strip()
)

rank_table = rank_table[
    ~rank_table["Rank"].isin(
        ["", "-", "nan", "None", "N/A"]
    )
]

rank_table = (

    rank_table
    .groupby("Journal Title")["Rank"]
    .apply(
        lambda x:
        ", ".join(
            sorted(
                set(x)
            )
        )
    )
    .reset_index()
)

journal_filter = (
    journal_filter
    .merge(
        rank_table,
        on="Journal Title",
        how="left"

    )
)

journal_filter = journal_filter.rename(
    columns={
        "Rank": "Rank Quality"
    }
)

journal_filter = (
    journal_filter[
        [
            "Journal Title",
            "Publisher",
            "Rank Quality",
            "ISSN",
            "ISSNOnline"
        ]
    ]
)

# ==========================================================
# JOURNAL RESULT
# ==========================================================
st.divider()

st.subheader(
    "📚 Journal List"
)

if journal_filter.empty:

    st.warning(
        "No journal found"
    )

else:

    st.write(
        f"Found **{len(journal_filter):,}** journals"
    )

    event = st.dataframe(
    journal_filter,
    use_container_width=True,
    height=400,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row"
)
    
    selected_rows = event.selection.rows

if selected_rows:

    selected_journal = (
        journal_filter
        .iloc[selected_rows[0]]
        ["Journal Title"]
    )

    st.session_state.selected_journal = selected_journal

# ==========================================================
# OPEN JOURNAL PROFILE
# ==========================================================

st.divider()

selected = st.session_state.get("selected_journal")

if selected:

    st.info(f"Selected Journal: **{selected}**")

    if st.button(
        "🔍 Open Journal Profile",
        type="primary"
    ):
        st.switch_page("pages/Journal_Search.py")
        
# ==========================================================
# KPI
# ==========================================================

st.divider()

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.metric(
        "Journal",
        f"{len(journal_filter):,}"
    )

with c2:

    st.metric(
        "Publisher",
        journal_filter["Publisher"]
        .nunique()

    )

with c3:

    st.metric(
        "Area",
        area_filter["Area"]
        .nunique()

    )

with c4:

    st.metric(
        "Database",
        area_filter["Source"]
        .nunique()

    )