import streamlit as st
import pandas as pd
import re
from io import BytesIO

from config import MASTER_FILE, AREA_FILE


# ==========================================================
# CLEAN COLUMN NAME
# ==========================================================

def clean_columns(df):

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    return df


# ==========================================================
# NORMALIZE TEXT
# ==========================================================

def normalize_text(text):

    if pd.isna(text):
        return ""

    text = str(text).upper()

    text = text.replace("&", "AND")

    text = re.sub(r"[^\w\s-]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================================
# CREATE SEARCH COLUMN
# ==========================================================

def create_search_column(df):

    df = df.copy()

    search_columns = [

        "Journal Title",
        "ISSN",
        "ISSNOnline",

        "Scopus_Title",
        "Scopus_ISSN",
        "Scopus_EISSN",

        "Scimago_Title",
        "Scimago_ISSN",
        "Scimago_EISSN",

        "ASG_Title",
        "ASG_ISSN"

    ]

    search = ""

    for col in search_columns:

        if col in df.columns:

            search += (
                df[col]
                .fillna("")
                .astype(str)
                + " "
            )

    df["Search_Text"] = search.apply(normalize_text)

    return df


# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data(show_spinner=False)
def load_data():

    # ------------------------------------------------------
    # Load Excel
    # ------------------------------------------------------

    master = pd.read_excel(MASTER_FILE)

    area = pd.read_excel(AREA_FILE)

    # ------------------------------------------------------
    # Clean Column Name
    # ------------------------------------------------------

    master = clean_columns(master)

    area = clean_columns(area)

    # ------------------------------------------------------
    # Convert Text Columns (Master)
    # ------------------------------------------------------

    master_text_columns = [

        "Journal Title",
        "Publisher",
        "ISSN",
        "ISSNOnline",

        "Scopus_Title",
        "Scopus_ISSN",
        "Scopus_EISSN",

        "Scimago_Title",
        "Scimago_ISSN",
        "Scimago_EISSN",

        "ASG_Title",
        "ASG_ISSN",

        "2025 rating",
        "SJR Best Quartile",
        "AJG 2024",

        "ABDC Area",
        "FoR"

    ]

    for col in master_text_columns:

        if col in master.columns:

            master[col] = (

                master[col]

                .fillna("")

                .astype(str)

                .str.strip()

            )

    # ------------------------------------------------------
    # Convert Text Columns (Area)
    # ------------------------------------------------------

    area_text_columns = [

        "Journal Title",
        "ISSN",
        "ISSNOnline",
        "Source",
        "Area",
        "Area Group",
        "Major Group",
        "Rank"

    ]

    for col in area_text_columns:

        if col in area.columns:

            area[col] = (

                area[col]

                .fillna("")

                .astype(str)

                .str.strip()

            )

    # ------------------------------------------------------
    # Journal Key
    # ใช้ Journal Title ของ ABDC เป็น Master
    # ------------------------------------------------------

    master["Journal_Key"] = (

        master["Journal Title"]

        .replace("", pd.NA)

        .fillna(master["ISSN"])

    )

    if "Journal_Key" not in area.columns:

        area["Journal_Key"] = (

            area["Journal Title"]

            .replace("", pd.NA)

            .fillna(area["ISSN"])

        )

    # Search Column

    master = create_search_column(master)

    # Remove Duplicate Journal Key

    master = master.drop_duplicates(

        subset="Journal_Key",

        keep="first"

    )

    # Reset Index
    
    master = master.reset_index(drop=True)
    area = area.reset_index(drop=True)
    
    master.rename(
    columns={

        "AJG2024 4*-1": "AJG 2024",

        "AJG 2024\n4*-1": "AJG 2024",

        "AJG 2024\r\n4*-1": "AJG 2024",

    },
    inplace=True
    )
    
    return master, area


# ==========================================================
# SEARCH
# ==========================================================

def search_journal(df, keyword):

    if keyword == "":

        return df

    keyword = normalize_text(keyword)

    return df[

        df["Search_Text"]

        .str.contains(

            keyword,

            regex=False,

            na=False

        )

    ]


# ==========================================================
# FILTER
# ==========================================================

def filter_data(

    df,

    major_groups=None,

    area_groups=None,

    areas=None,

    sources=None,

    ranks=None,

    publishers=None

):

    temp = df.copy()

    if major_groups:
        temp = temp[temp["Major Group"].isin(major_groups)]

    if area_groups:
        temp = temp[temp["Area Group"].isin(area_groups)]

    if areas:
        temp = temp[temp["Area"].isin(areas)]

    if sources:
        temp = temp[temp["Source"].isin(sources)]

    if ranks:
        temp = temp[temp["Rank"].isin(ranks)]

    if publishers:
        temp = temp[temp["Publisher"].isin(publishers)]

    return temp


# ==========================================================
# FILTER OPTION
# ==========================================================

def get_filter_options(df, column):

    if column not in df.columns:

        return []

    return sorted(

        df[column]

        .dropna()

        .astype(str)

        .unique()

    )


# ==========================================================
# SUMMARY
# ==========================================================

def summary_major(df):

    return (

        df.groupby("Major Group")

        .size()

        .reset_index(name="Total")

        .sort_values("Total", ascending=False)

    )


def summary_area(df):

    return (

        df.groupby("Area")

        .size()

        .reset_index(name="Total")

        .sort_values("Total", ascending=False)

    )


def summary_source(df):

    return (

        df.groupby("Source")

        .size()

        .reset_index(name="Total")

    )


def summary_rank(df):

    return (

        df.groupby("Rank")

        .size()

        .reset_index(name="Total")

    )


# ==========================================================
# COMPARE
# ==========================================================

def compare(df, column):

    return (

        df.groupby(column)

        .size()

        .reset_index(name="Total")

        .sort_values("Total", ascending=False)

    )


# ==========================================================
# PIVOT
# ==========================================================

def pivot_major_source(df):

    return pd.pivot_table(

        df,

        index="Major Group",

        columns="Source",

        aggfunc="size",

        fill_value=0

    )


def pivot_area_source(df):

    return pd.pivot_table(

        df,

        index="Area",

        columns="Source",

        aggfunc="size",

        fill_value=0

    )


def pivot_rank_source(df):

    return pd.pivot_table(

        df,

        index="Rank",

        columns="Source",

        aggfunc="size",

        fill_value=0

    )


# ==========================================================
# JOURNAL DETAIL
# ==========================================================

def get_journal_detail(master, area, key):

    info = master[

        master["Journal_Key"] == key

    ]

    detail = area[

        area["Journal_Key"] == key

    ]

    return info, detail


# ==========================================================
# EXPORT
# ==========================================================

def dataframe_to_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(

        output,

        engine="openpyxl"

    ) as writer:

        df.to_excel(

            writer,

            index=False

        )

    return output.getvalue()