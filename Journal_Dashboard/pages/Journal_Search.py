# ==========================================================
# JOURNAL SEARCH
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from config import *

from utils import (
    load_data,
    search_journal,
    get_journal_detail
)

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

st.caption(

    "Search Journal Information"

)

# ==========================================================
# SEARCH TYPE
# ==========================================================

search_type = st.radio(

    "Search by",

    [

        "Journal Title",

        "ISSN",

        "ISSNOnline",

        "Publisher"

    ],

    horizontal=True

)

# ==========================================================
# SEARCH BOX
# ==========================================================

keyword = st.text_input(

    "Keyword",

    placeholder="Type here..."

)

# ==========================================================
# SEARCH
# ==========================================================

result = master.copy()

if keyword != "":

    keyword = keyword.strip()

    if search_type == "Journal Title":

        result = result[

            result["Journal Title"]

            .fillna("")

            .str.contains(

                keyword,

                case=False,

                na=False

            )

        ]

    elif search_type == "ISSN":

        result = result[

            result["ISSN"]

            .fillna("")

            .str.contains(

                keyword,

                case=False,

                na=False

            )

        ]

    elif search_type == "ISSNOnline":

        result = result[

            result["ISSNOnline"]

            .fillna("")

            .str.contains(

                keyword,

                case=False,

                na=False

            )

        ]

    elif search_type == "Publisher":

        result = result[

            result["Publisher"]

            .fillna("")

            .str.contains(

                keyword,

                case=False,

                na=False

            )

        ]

# ==========================================================
# RESULT
# ==========================================================

st.write(

    f"Found : **{len(result):,}** Journal"

)

# ==========================================================
# SELECT JOURNAL
# ==========================================================

journal_name = st.selectbox(

    "Select Journal",

    result["Journal Title"]

    .sort_values()

    .unique()

)

# ==========================================================
# CURRENT JOURNAL
# ==========================================================

master_current = master[

    master["Journal Title"]

    == journal_name

]

area_current = area[

    area["Journal Title"]

    == journal_name

]

# ==========================================================
# QUICK INFO
# ==========================================================

if len(master_current):

    row = master_current.iloc[0]

    c1,c2,c3,c4 = st.columns(4)

    with c1:

        st.metric(

            "Publisher",

            row["Publisher"]

        )

    with c2:

        st.metric(

            "ISSN",

            row["ISSN"]

        )

    with c3:

        st.metric(

            "EISSN",

            row["ISSNOnline"]

        )

    with c4:

        st.metric(

            "ABDC",

            row["2025 rating"]

        )
    
# ==========================================================
# JOURNAL PROFILE
# ==========================================================

st.divider()

st.header("📖 Journal Profile")

def check_available(value):

    if pd.isna(value):
        return False

    value = str(value).strip()

    if value == "":
        return False

    if value.lower() in ["nan", "none", "n/a", "na"]:
        return False

    return True

if len(master_current):

    row = master_current.iloc[0]

    c1,c2 = st.columns(2)

    # ======================================================
    # BASIC INFORMATION
    # ======================================================

    with c1:

        st.subheader("Journal Information")

        st.write(f"**Journal Title** : {row['Journal Title']}")

        st.write(f"**Publisher** : {row['Publisher']}")

        st.write(f"**ISSN** : {row['ISSN']}")

        st.write(f"**EISSN** : {row['ISSNOnline']}")

        st.write(f"**Year Inception** : {row['Year Inception']}")

        st.write(f"**Area** : {row['ABDC Area']}")

    # ======================================================
    # DATABASE
    # ======================================================

    with c2:

        st.subheader("Database Coverage")


        abdc = row["2025 rating"]

        scopus = row["Scopus_Title"]

        scimago = row["Scimago_Title"]

        ajg = row["ASG_Title"]


        st.write(f"**ABDC Rank :** {abdc}")


        def status_label(name, value):

            c1, c2 = st.columns([0.1, 1])

            with c1:
                st.write(f"**{name}**")

            with c2:
                if check_available(value):
                    st.badge("Available", color="green")
                else:
                    st.badge("Not Available", color="red")



        status_label(
            "Scopus",
            scopus
        )


        status_label(
            "Scimago",
            scimago
        )


        status_label(
            "AJG",
            ajg
        )
        
# ==========================================================
# DATABASE DETAIL
# ==========================================================

st.divider()

st.header("🗂 Database Information")

col1,col2,col3 = st.columns(3)

# ==========================================================
# SCOPUS
# ==========================================================

with col1:

    st.subheader("Scopus")

    st.write(

        f"**Title** : {row['Scopus_Title']}"

    )

    st.write(

        f"**ISSN** : {row['Scopus_ISSN']}"

    )

    st.write(

        f"**EISSN** : {row['Scopus_EISSN']}"

    )

    st.write(

        f"**Status** : {row['Active or Inactive']}"

    )

    st.write(

        f"**Source Type** : {row['Source Type']}"

    )

# ==========================================================
# SCIMAGO
# ==========================================================

with col2:

    st.subheader("Scimago")

    st.write(

        f"**Title** : {row['Scimago_Title']}"

    )

    st.write(

        f"**ISSN** : {row['Scimago_ISSN']}"

    )

    st.write(

        f"**EISSN** : {row['Scimago_EISSN']}"

    )

    st.write(

        f"**Best Quartile** : {row['SJR Best Quartile']}"

    )

# ==========================================================
# AJG
# ==========================================================

with col3:

    st.subheader("AJG")

    st.write(

        f"**Title** : {row['ASG_Title']}"

    )

    st.write(

        f"**ISSN** : {row['ASG_ISSN']}"

    )

    st.write(

        f"**Rank** : {row['AJG 2024']}"

    )

# ==========================================================
# AREA SUMMARY
# ==========================================================

st.divider()

st.header("🌍 Area Summary")

summary = (

    area_current

    .groupby(

        [

            "Major Group",

            "Area Group"

        ]

    )

    .size()

    .reset_index(name="Total")

)

st.dataframe(

    summary,

    use_container_width=True,

    height=300

)

# ==========================================================
# RANK SUMMARY
# ==========================================================

st.divider()

st.header("🏆 Rank Summary")

rank = (

    area_current

    [

        [

            "Source",

            "Area",

            "Rank"

        ]

    ]

)

st.dataframe(

    rank,

    use_container_width=True,

    height=350

)

# ==========================================================
# SOURCE SUMMARY
# ==========================================================

st.divider()

st.header("Database Coverage")

coverage = (

    area_current

    .groupby(

        "Source"

    )

    .size()

    .reset_index(name="Area")

)

st.dataframe(

    coverage,

    use_container_width=True

)

# ==========================================================
# DATABASE COVERAGE
# ==========================================================

st.divider()

st.header("📚 Database Coverage")

coverage = (

    area_current

    .groupby(

        "Source"

    )

    .size()

    .reset_index(name="Total")

)

fig = px.pie(

    coverage,

    names="Source",

    values="Total",

    hole=.5

)

fig.update_layout(

    height=500

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# RANK DISTRIBUTION
# ==========================================================

st.divider()

st.header("🏆 Rank Distribution")

rank = (

    area_current

    .groupby(

        [

            "Source",

            "Rank"

        ]

    )

    .size()

    .reset_index(name="Total")

)

fig = px.bar(

    rank,

    x="Rank",

    y="Total",

    color="Source",

    barmode="group",

    text="Total"

)

fig.update_layout(

    height=600

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# MAJOR GROUP
# ==========================================================

st.divider()

st.header("Major Group")

major = (

    area_current

    .groupby(

        "Major Group"

    )

    .size()

    .reset_index(name="Total")

)

fig = px.bar(

    major,

    x="Major Group",

    y="Total",

    color="Major Group",

    text="Total"

)

fig.update_layout(

    height=450

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# AREA GROUP
# ==========================================================

group = (

    area_current

    .groupby(

        "Area Group"

    )

    .size()

    .reset_index(name="Total")

)

fig = px.bar(

    group,

    x="Total",

    y="Area Group",

    orientation="h",

    text="Total"

)

fig.update_layout(

    height=600,

    yaxis=dict(

        categoryorder="total ascending"

    )

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# AREA TABLE
# ==========================================================

st.divider()

st.header("📄 Area Detail")

st.dataframe(

    area_current,

    use_container_width=True,

    height=500

)