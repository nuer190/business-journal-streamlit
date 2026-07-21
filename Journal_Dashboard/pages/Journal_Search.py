# ==========================================================
# JOURNAL SEARCH
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import html

from config import *
from utils import load_data

from theme import (
    DATABASE_LIGHT_COLORS,
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

default_index = 0


if (
    "selected_journal"
    in st.session_state
    and
    st.session_state.selected_journal
    in journal_list
):

    default_index = list(
        journal_list
    ).index(
        st.session_state.selected_journal
    )



journal_name = st.selectbox(

    "Select Journal",

    journal_list,

    index=default_index

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

# ==========================================================
# BEST QUALITY
# ==========================================================

QUALITY_RANK = {

    "4*": 1,

    "A*": 2,
    "4": 2,
    "Q1": 2,

    "A": 3,
    "3": 3,
    "Q2": 3,

    "B": 4,
    "2": 4,
    "Q3": 4,

    "C": 5,
    "1": 5,
    "Q4": 5

}

# ==========================================================
# GET BEST AREA
# ==========================================================


def get_best_area(
        journal_title,
        database,
        area_df
):


    temp = area_df[

        (area_df["Journal Title"] == journal_title)

        &

        (area_df["Source"] == database)

    ].copy()



    if len(temp)==0:

        return "N/A"



    # --------------------------
    # ABDC / Scimago
    # มี Rank
    # --------------------------

    if database in [
        "ABDC",
        "Scimago"
    ]:


        temp = temp[
            temp["Rank"].notna()
        ]


        if len(temp)>0:


            temp["score"] = temp["Rank"].apply(

                lambda x:

                RANK_ORDER[database].get(
                    str(x).strip(),
                    999
                )

            )


            best = (

                temp

                .sort_values(
                    "score"
                )

                .iloc[0]

            )


            return best["Area"]




    # --------------------------
    # AJG
    # --------------------------

    if database=="AJG":


        temp = temp[
            temp["Rank"].notna()
        ]


        if len(temp)>0:

            return temp.iloc[0]["Area"]



    # --------------------------
    # Scopus
    # ไม่มี Rank
    # --------------------------


    return temp.iloc[0]["Area"]


# ==========================================================
# GET BEST RANK
# ==========================================================


def get_best_rank(
        journal_title,
        database,
        area_df
):


    temp = area_df[

        (area_df["Journal Title"] == journal_title)

        &

        (area_df["Source"] == database)

    ].copy()



    if len(temp)==0:

        return "N/A"



    temp = temp[
        temp["Rank"].notna()
    ]



    if len(temp)==0:

        return "N/A"



    if database not in RANK_ORDER:

        return temp.iloc[0]["Rank"]



    temp["score"] = temp["Rank"].apply(

        lambda x:

        RANK_ORDER[database].get(

            str(x).strip(),

            999

        )

    )


    best = (

        temp

        .sort_values(
            "score"
        )

        .iloc[0]

    )


    return best["Rank"]

# ==========================================================
# DATABASE STATUS
# ==========================================================


def database_status(
        journal_title,
        database,
        area_df
):


    check = area_df[

        (area_df["Journal Title"] == journal_title)

        &

        (area_df["Source"] == database)

    ]


    return len(check)>0




def get_best_quality(row):
    """
    หา Ranking ที่ดีที่สุดจาก
    - ABDC
    - AJG
    - Scimago

    หากอันดับเท่ากันให้แสดงทั้งหมด
    """

    rankings = []

    # -------------------------
    # ABDC
    # -------------------------
    abdc = display_value(row["2025 rating"])

    if abdc != "N/A":
        rank = QUALITY_RANK.get(abdc)

        if rank:
            rankings.append((rank, f"{abdc} (ABDC)"))

    # -------------------------
    # AJG
    # -------------------------
    ajg = display_value(row["AJG 2024"])

    if ajg != "N/A":
        rank = QUALITY_RANK.get(ajg)

        if rank:
            rankings.append((rank, f"{ajg} (AJG)"))

    # -------------------------
    # Scimago
    # -------------------------
    sjr = display_value(row["SJR Best Quartile"])

    if sjr != "N/A":
        rank = QUALITY_RANK.get(sjr)

        if rank:
            rankings.append((rank, f"{sjr} (Scimago)"))

    if len(rankings) == 0:
        return "N/A"

    best_rank = min(x[0] for x in rankings)

    best = [
        x[1]
        for x in rankings
        if x[0] == best_rank
    ]

    return " | ".join(best)


def status_badge(name, data):

    c1, c2 = st.columns([1, 5.5])

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

title = display_value(row["Journal Title"])
publisher = display_value(row["Publisher"])

best_quality = get_best_quality(row)


# ==========================================================
# Header Cards
# ==========================================================

left, right = st.columns([3,2])


with left:

    with st.container(border=True):

        st.markdown("📚 **Journal Title**")

        st.subheader(title)



with right:

    with st.container(border=True):

        st.markdown("🏢 **Publisher**")

        st.subheader(publisher)



# ==========================================================
# Information Cards
# ==========================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    with st.container(border=True):

        st.markdown(
            "🆔 **ISSN**"
        )

        st.info(
            display_value(row["ISSN"])
        )



with c2:

    with st.container(border=True):

        st.markdown(
            "🌐 **EISSN**"
        )

        st.success(
            display_value(row["ISSNOnline"])
        )



with c3:

    with st.container(border=True):

        st.markdown(
            "📅 **Year Inception**"
        )

        st.warning(
            display_value(row["Year Inception"])
        )



with c4:

    with st.container(border=True):

        st.markdown(
            "🏆 **Best Quality**"
        )

        st.success(
            best_quality
        )
    
    
# ======================================================
# MAINNOTE
# ======================================================

note = display_value(row["หมายเหตุหลัก"])

if note not in ["", "-", "N/A", None]:

    st.markdown("### 📝 หมายเหตุ")

    with st.container(border=True):
        st.write(note)


# ==========================================================
# DATABASE PROFILE CARDS
# ==========================================================

card_cols = st.columns(4)


for col, db in zip(
    card_cols,
    [
        "ABDC",
        "Scopus",
        "Scimago",
        "AJG"
    ]
):

    with col:


        # ===============================
        # Database Status
        # ===============================

        available = database_status(
            row["Journal Title"],
            db,
            area
        )


        if available:

            status_text = "🟢 Available"

        else:

            status_text = "🔴 Not Available"



        area_name = get_best_area(
            row["Journal Title"],
            db,
            area
        )


        rank = get_best_rank(
            row["Journal Title"],
            db,
            area
        )



        # ===============================
        # Card
        # ===============================

        with st.container(border=True):


            # Database Name

            st.markdown(
                f"## {db}"
            )


            # Availability

            st.caption(
                status_text
            )


            st.divider()



            # Common Fields

            st.caption(
                "Area"
            )

            st.write(
                area_name
            )



            st.caption(
                "Rank"
            )

            st.write(
                rank
            )



            # ===============================
            # ABDC
            # ===============================

            if db == "ABDC":

                st.caption(
                    "Year Inception"
                )

                st.write(
                    row.get(
                        "Year Inception",
                        "N/A"
                    )
                )



            # ===============================
            # Scopus
            # ===============================

            elif db == "Scopus":

                st.caption(
                    "Status"
                )

                st.write(
                    row.get(
                        "Active or Inactive",
                        "N/A"
                    )
                )


                st.caption(
                    "Source Type"
                )

                st.write(
                    row.get(
                        "Source Type",
                        "N/A"
                    )
                )


                st.caption(
                    "Coverage"
                )

                st.write(
                    row.get(
                        "Coverage",
                        "N/A"
                    )
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
    [
        [
            "Major Group",
            "Area Group"
        ]
    ]
    .drop_duplicates()
    .reset_index(drop=True)
)

rank_summary = (
    area_current[
        [
            "Source",
            "Major Group",
            "Area Group",
            "Area",
            "Rank"
        ]
    ]
    .copy()
    .sort_values(
        [
            "Source",
            "Rank",
            "Area"
        ]
    )
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


def highlight_source(row):

    color = DATABASE_LIGHT_COLORS.get(
        row["Source"],
        "white"
    )

    return [
        f"""
        background-color:{color};
        color:#222222;
        font-weight:400;
        """
    ] * len(row)


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

styled_rank = (
    rank_summary
    .style
    .apply(
        highlight_source,
        axis=1
    )
)

st.dataframe(
    styled_rank,
    use_container_width=True,
    height=350
)



# ==========================================================
# AREA DETAIL
# ==========================================================

st.subheader("📋 Area Detail")

area_detail = (
    area_current
    .drop(
        columns=["Journal Key"],
        errors="ignore"
    )
    .sort_values(
        ["Source", "Area"]
    )
)


styled_area = (
    area_detail
    .style
    .apply(
        highlight_source,
        axis=1
    )
)


st.dataframe(
    styled_area,
    use_container_width=True,
    height=500
)