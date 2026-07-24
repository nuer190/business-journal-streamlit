# ==========================================================
# Filter Engine
# ==========================================================

import streamlit as st
import pandas as pd

from utils import load_data

master, area = load_data()

# ==========================================================
# OPTION
# ==========================================================

def unique_sorted(df, column):

    if column not in df.columns:
        return []

    return sorted(
        df[column]
        .dropna()
        .astype(str)
        .unique()
    )
    
def clean_options(series):

    return (
        series
        .dropna()
        .astype(str)
        .str.strip()
        .replace(
            ["", "nan", "None", "undefined"],
            None
        )
        .dropna()
        .unique()
        .tolist()
    )
    
def filter_options(
    df,
    column,
    current_filters={}
):

    temp = df.copy()


    for key,value in current_filters.items():

        if value and key in temp.columns:

            temp = temp[
                temp[key].isin(value)
            ]


    return sorted(
        clean_options(
            temp[column]
        )
    )
    
def apply_rank_filter(
    df,
    ranks
):

    if not ranks:
        return df


    # หา journal ที่มี rank นี้
    journal_keep = (
        df[
            df["Rank"]
            .isin(ranks)
        ]
        ["Journal Title"]
        .unique()
    )


    return df[
        df["Journal Title"]
        .isin(journal_keep)
    ]
    
def apply_source_filter(
    df,
    sources
):

    if not sources:
        return df


    journal_keep = (
        df[
            df["Source"]
            .isin(sources)
        ]
        ["Journal Title"]
        .unique()
    )


    return df[
        df["Journal Title"]
        .isin(journal_keep)
    ]

# ==========================================================
# OPTION LIST
# ==========================================================

def get_major_options(df):

    return sorted(
        clean_options(
            df["Major Group"]
        )
    )

def get_area_group_options(df):

    return sorted(
        clean_options(
            df["Area Group"]
        )
    )

def get_area_options(df):

    return sorted(
        clean_options(
            df["Area"]
        )
    )

def get_source_options(df):

    return sorted(
        clean_options(
            df["Source"]
        )
    )

def get_rank_options(df):

    return sorted(
        clean_options(
            df["Rank"]
        )
    )


def get_dynamic_options(df, column):

    return sorted(
        df[column]
        .dropna()
        .astype(str)
        .unique()
    )
    
    
# ==========================================================
# FILTER
# ==========================================================

def apply_filters(
    df,
    major_groups=None,
    area_groups=None,
    areas=None,
    sources=None,
    ranks=None,

):
    temp = df.copy()
    if major_groups:
        temp = temp[
            temp["Major Group"]
            .isin(major_groups)
        ]

    if area_groups:
        temp = temp[
            temp["Area Group"]
            .isin(area_groups)
        ]

    if areas:
        temp = temp[
            temp["Area"]
            .isin(areas)
        ]

    if sources:
        temp = apply_source_filter(
            temp,
            sources
        )

    if ranks:
        temp = apply_rank_filter(
            temp,
            ranks
        )

    return temp

def apply_compare_filters(
    df,
    column,
    group1,
    group2

):

    df1 = df[
        df[column].isin(group1)
    ]

    df2 = df[
        df[column].isin(group2)
    ]

    return df1, df2

# ==========================================================
# SIDEBAR
# ==========================================================

def build_sidebar_filters(df):

    st.sidebar.header("Filters")


    # -------------------------
    # Major
    # -------------------------

    major = st.sidebar.multiselect(

        "Major Group",

        filter_options(
            df,
            "Major Group"
        )

    )


    # -------------------------
    # Area Group
    # -------------------------

    area_group = st.sidebar.multiselect(

        "Area Group",

        filter_options(
            df,
            "Area Group",
            {
                "Major Group":major
            }
        )

    )


    # -------------------------
    # Area
    # -------------------------

    area = st.sidebar.multiselect(

        "Area",

        filter_options(
            df,
            "Area",
            {
                "Major Group":major,
                "Area Group":area_group
            }
        )

    )


    # -------------------------
    # Database
    # -------------------------

    source = st.sidebar.multiselect(

        "Database",

        filter_options(
            df,
            "Source",
            {
                "Major Group":major,
                "Area Group":area_group,
                "Area":area
            }
        )

    )


    # -------------------------
    # Rank
    # -------------------------

    rank = st.sidebar.multiselect(

        "Rank",

        filter_options(
            df,
            "Rank",
            {
                "Source":source,
                "Major Group":major,
                "Area Group":area_group,
                "Area":area
            }
        )

    )


    return {

        "major_groups":major,

        "area_groups":area_group,

        "areas":area,

        "sources":source,

        "ranks":rank

    }

def reset_filters():

    return {

        "major_groups":[],

        "area_groups":[],

        "areas":[],

        "sources":[],

        "ranks":[],


    }
    