# ==========================================================
# JOURNAL SEARCH
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from config import *
from utils import load_data

from theme import (
    apply_theme,
    DATABASE_COLORS,
    RANK_COLORS,
    MAJOR_COLORS,
    CHART_LAYOUT
)

# ==========================================================
# LOAD DATA
# ==========================================================

master, area = load_data()

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Journal Search",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Journal Search")
st.caption("Search Journal Information")

# ==========================================================
# SEARCH OPTION
# ==========================================================

SEARCH_COLUMN = {
    "Journal Title": "Journal Title",
    "ISSN": "ISSN",
    "ISSNOnline": "ISSNOnline",
    "Publisher": "Publisher"
}

search_type = st.radio(
    "Search by",
    list(SEARCH_COLUMN.keys()),
    horizontal=True
)

keyword = st.text_input(
    "Keyword",
    placeholder="Type here..."
)

# ==========================================================
# FILTER DATA
# ==========================================================

result = master.copy()

if keyword.strip():

    column = SEARCH_COLUMN[search_type]

    result = result[
        result[column]
        .fillna("")
        .astype(str)
        .str.contains(
            keyword.strip(),
            case=False,
            na=False
        )
    ]

# ==========================================================
# RESULT
# ==========================================================

st.write(f"Found : **{len(result):,}** Journal")

# ==========================================================
# NO RESULT
# ==========================================================

if result.empty:

    if keyword.strip():
        st.info("No journal found.")

    st.stop()

# ==========================================================
# SELECT JOURNAL
# ==========================================================

journal_list = (
    result["Journal Title"]
    .dropna()
    .sort_values()
    .unique()
)

journal_name = st.selectbox(
    "Select Journal",
    journal_list,
    index=0
)

# ==========================================================
# CURRENT JOURNAL
# ==========================================================

master_current = master[
    master["Journal Title"] == journal_name
]

area_current = area[
    area["Journal Title"] == journal_name
]

# กันพลาดอีกชั้น
if master_current.empty:
    st.stop()

# ใช้ row ตัวเดียวทั้งไฟล์
row = master_current.iloc[0]

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def display_value(data):
    """
    แสดง N/A หากข้อมูลว่าง
    """
    if pd.isna(data):
        return "N/A"

    data = str(data).strip()

    if data == "":
        return "N/A"

    if data.lower() in ["nan", "none", "na", "n/a"]:
        return "N/A"

    return data


def check_available(data):
    """
    ตรวจสอบว่ามีข้อมูลหรือไม่
    """
    return display_value(data) != "N/A"


def status_badge(name, data):

    c1, c2 = st.columns([1, 3.7])

    with c1:
        st.write(f"**{name}**")

    with c2:
        if check_available(data):
            st.badge("Available", color="green")
        else:
            st.badge("Not Available", color="red")
            
# ==========================================================
# QUICK INFO
# ==========================================================

st.divider()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Publisher",
        display_value(row["Publisher"])
    )

with c2:
    st.metric(
        "ISSN",
        display_value(row["ISSN"])
    )

with c3:
    st.metric(
        "EISSN",
        display_value(row["ISSNOnline"])
    )

with c4:
    st.metric(
        "ABDC",
        display_value(row["2025 rating"])
    )

# ==========================================================
# JOURNAL PROFILE
# ==========================================================

st.divider()

st.header("📖 Journal Profile")

left, right = st.columns(2)

# ==========================================================
# BASIC INFORMATION
# ==========================================================

with left:

    st.subheader("Journal Information")

    journal_info = {
        "Journal Title": "Journal Title",
        "Publisher": "Publisher",
        "ISSN": "ISSN",
        "EISSN": "ISSNOnline",
        "Year Inception": "Year Inception",
        "ABDC Area": "ABDC Area"
    }

    for label, column in journal_info.items():

        st.write(
            f"**{label} :** {display_value(row[column])}"
        )

# ==========================================================
# DATABASE Journal Group
# ==========================================================

with right:

    st.subheader("Database Journal Group")

    st.write(
        f"**ABDC Rank :** {display_value(row['2025 rating'])}"
    )

    status_badge(
        "Scopus",
        row["Scopus_Title"]
    )

    status_badge(
        "Scimago",
        row["Scimago_Title"]
    )

    status_badge(
        "AJG",
        row["ASG_Title"]
    )

# ==========================================================
# DATABASE INFORMATION
# ==========================================================

st.divider()

st.header("🗂 Database Information")

tab1, tab2, tab3 = st.columns(3)

# ==========================================================
# SCOPUS
# ==========================================================

with tab1:

    st.subheader("Scopus")

    scopus_info = {
        "Title": "Scopus_Title",
        "ISSN": "Scopus_ISSN",
        "EISSN": "Scopus_EISSN",
        "Status": "Active or Inactive",
        "Source Type": "Source Type"
    }

    for label, column in scopus_info.items():

        st.write(
            f"**{label} :** {display_value(row[column])}"
        )

# ==========================================================
# SCIMAGO
# ==========================================================

with tab2:

    st.subheader("Scimago")

    scimago_info = {
        "Title": "Scimago_Title",
        "ISSN": "Scimago_ISSN",
        "EISSN": "Scimago_EISSN",
        "Best Quartile": "SJR Best Quartile"
    }

    for label, column in scimago_info.items():

        st.write(
            f"**{label} :** {display_value(row[column])}"
        )

# ==========================================================
# AJG
# ==========================================================

with tab3:

    st.subheader("AJG")

    ajg_info = {
        "Title": "ASG_Title",
        "ISSN": "ASG_ISSN",
        "Rank": "AJG 2024"
    }

    for label, column in ajg_info.items():

        st.write(
            f"**{label} :** {display_value(row[column])}"
        )
        
# ==========================================================
# AREA DATA CHECK
# ==========================================================

st.divider()

st.header("🌍 Journal Area Analysis")

if area_current.empty:

    st.warning("No area information available.")

    st.stop()

# ==========================================================
# SUMMARY DATA
# ==========================================================

summary = (
    area_current
    .groupby(
        ["Major Group", "Area Group"],
        dropna=False
    )
    .size()
    .reset_index(name="Total")
)

rank_summary = (
    area_current[
        ["Source", "Area", "Rank"]
    ]
    .copy()
)

coverage = (
    area_current
    .groupby(
        "Source",
        dropna=False
    )
    .size()
    .reset_index(name="Total")
)

rank_distribution = (
    area_current
    .groupby(
        ["Source", "Rank"],
        dropna=False
    )
    .size()
    .reset_index(name="Total")
)

major_group = (
    area_current
    .groupby(
        "Major Group",
        dropna=False
    )
    .size()
    .reset_index(name="Total")
)

area_group = (
    area_current
    .groupby(
        "Area Group",
        dropna=False
    )
    .size()
    .reset_index(name="Total")
)

# ==========================================================
# TABLE : AREA SUMMARY
# ==========================================================

st.subheader("📄 Area Summary")

st.dataframe(
    summary,
    use_container_width=True,
    height=300
)

# ==========================================================
# TABLE : RANK SUMMARY
# ==========================================================

st.subheader("🏆 Rank Summary")

st.dataframe(
    rank_summary,
    use_container_width=True,
    height=350
)

# ==========================================================
# TABLE : DATABASE COVERAGE
# ==========================================================

st.subheader("📚 Database Journal Group")

st.dataframe(
    coverage,
    use_container_width=True
)

# ==========================================================
# PIE CHART
# ==========================================================

st.subheader("📊 Database Journal Group Chart")

fig = px.pie(
    coverage,
    names="Source",
    values="Total",
    hole=0.55,
    color="Source",
    color_discrete_map=DATABASE_COLORS
)

fig.update_layout(**CHART_LAYOUT)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# RANK DISTRIBUTION
# ==========================================================

st.subheader("🏆 Rank Distribution")

fig = px.bar(
    rank_distribution,
    x="Rank",
    y="Total",
    color="Source",
    barmode="group",
    text="Total",
    color_discrete_map=DATABASE_COLORS
)

fig.update_layout(**CHART_LAYOUT)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# MAJOR GROUP
# ==========================================================

st.subheader("📊 Major Group")

fig = px.bar(
    major_group,
    x="Major Group",
    y="Total",
    color="Major Group",
    text="Total",
    color_discrete_map=MAJOR_COLORS
)

fig.update_layout(**CHART_LAYOUT)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# AREA GROUP
# ==========================================================

st.subheader("📊 Area Group")

fig = px.bar(
    area_group,
    x="Total",
    y="Area Group",
    orientation="h",
    text="Total"
)

fig.update_layout(
    height=max(450, len(area_group) * 28),
    yaxis=dict(
        categoryorder="total ascending"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# AREA DETAIL
# ==========================================================

st.subheader("📋 Area Detail")

st.dataframe(
    area_current.sort_values(
        ["Source", "Area"]
    ),
    use_container_width=True,
    height=500
)