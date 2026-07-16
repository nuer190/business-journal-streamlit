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


# ==========================================================
# OPTION LIST
# ==========================================================

def get_major_options(df):
    return unique_sorted(df, "Major Group")


def get_area_group_options(df):
    return unique_sorted(df, "Area Group")


def get_area_options(df):
    return unique_sorted(df, "Area")


def get_source_options(df):
    return unique_sorted(df, "Source")


def get_rank_options(df):
    return unique_sorted(df, "Rank")




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

        temp = temp[
            temp["Source"]
            .isin(sources)
        ]

    if ranks:

        temp = temp[
            temp["Rank"]
            .isin(ranks)
        ]


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

    major = st.sidebar.multiselect(

        "Major Group",

        get_major_options(df)

    )

    temp = apply_filters(

        df,

        major_groups=major

    )

    area_group = st.sidebar.multiselect(

        "Area Group",

        get_area_group_options(temp)

    )

    temp = apply_filters(

        temp,

        area_groups=area_group

    )

    area = st.sidebar.multiselect(

        "Area",

        get_area_options(temp)

    )

    temp = apply_filters(

        temp,

        areas=area

    )

    source = st.sidebar.multiselect(

        "Database",

        get_source_options(temp)

    )

    temp = apply_filters(

        temp,

        sources=source

    )

    rank = st.sidebar.multiselect(

        "Rank",

        get_rank_options(temp)

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
    