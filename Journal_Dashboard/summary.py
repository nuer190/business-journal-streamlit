# =========================================================
# Journal Analytics Engine v2
# =========================================================

import pandas as pd


# ==========================================================
# INTERNAL
# ==========================================================

def _journal_col(df):
    """
    Return primary key used for counting journals.
    """

    if "Journal_Key" in df.columns:
        return "Journal_Key"

    return "Journal Title"


# ==========================================================
# INTERNAL
# ==========================================================

def _clean(df):
    """
    Remove duplicated journal records.
    """

    journal = _journal_col(df)

    return (
        df
        .drop_duplicates(subset=[journal])
        .copy()
    )


# ==========================================================
# INTERNAL
# ==========================================================

def _summary(df, group_cols):
    """
    Generic summary
    Count unique journals.
    """

    journal = _journal_col(df)

    temp = (

        df

        .drop_duplicates(

            subset=group_cols + [journal]

        )

        .groupby(

            group_cols,

            as_index=False

        )

        .agg(

            Total=(journal, "count")

        )

        .sort_values(

            "Total",

            ascending=False

        )

        .reset_index(drop=True)

    )

    return temp


# ==========================================================
# KPI
# ==========================================================

def database_summary(master):

    journal = _journal_col(master)

    result = {}

    result["Journal"] = master[journal].nunique()

    result["ABDC"] = (

        master

        .loc[

            master["2025 rating"] != "",

            journal

        ]

        .nunique()

    )

    result["Scopus"] = (

        master

        .loc[

            master["Scopus_Title"] != "",

            journal

        ]

        .nunique()

    )

    result["Scimago"] = (

        master

        .loc[

            master["Scimago_Title"] != "",

            journal

        ]

        .nunique()

    )

    result["AJG"] = (

        master

        .loc[

            master["ASG_Title"] != "",

            journal

        ]

        .nunique()

    )

    return result


# ==========================================================
# JOURNAL MASTER
# ==========================================================

def journal_summary(master):

    cols = [

        "Journal_Key",

        "Journal Title",

        "Publisher",

        "ISSN",

        "ISSNOnline",

        "2025 rating",

        "SJR Best Quartile",

        "AJG 2024"

    ]

    cols = [

        c

        for c in cols

        if c in master.columns

    ]

    return (

        master

        [cols]

        .drop_duplicates(

            subset=["Journal_Key"]

        )

        .sort_values(

            "Journal Title"

        )

        .reset_index(drop=True)

    )


# ==========================================================
# PUBLISHER
# ==========================================================

def publisher_summary(master):

    return _summary(

        master,

        ["Publisher"]

    )


# ==========================================================
# TOP PUBLISHER
# ==========================================================

def top_publisher(

    master,

    n=10

):

    return (

        publisher_summary(master)

        .head(n)

    )


# ==========================================================
# DATABASE COVERAGE
# ==========================================================

def database_coverage(master):

    journal = _journal_col(master)

    temp = pd.DataFrame({

        "Database": [

            "ABDC",

            "Scopus",

            "Scimago",

            "AJG"

        ],

        "Total": [

            master.loc[
                master["2025 rating"] != "",
                journal
            ].nunique(),

            master.loc[
                master["Scopus_Title"] != "",
                journal
            ].nunique(),

            master.loc[
                master["Scimago_Title"] != "",
                journal
            ].nunique(),

            master.loc[
                master["ASG_Title"] != "",
                journal
            ].nunique()

        ]

    })

    return temp

# ==========================================================
# MAJOR GROUP
# ==========================================================

def major_summary(area):

    return _summary(

        area,

        ["Major Group"]

    )


# ==========================================================
# AREA GROUP
# ==========================================================

def area_group_summary(area):

    return _summary(

        area,

        ["Area Group"]

    )


# ==========================================================
# AREA
# ==========================================================

def area_summary(area):

    return _summary(

        area,

        ["Area"]

    )


# ==========================================================
# SOURCE
# ==========================================================

def source_summary(area):

    return _summary(

        area,

        ["Source"]

    )


# ==========================================================
# RANK
# ==========================================================

def rank_summary(area):

    temp = area.copy()

    temp = temp[
        temp["Rank"].notna() &
        (temp["Rank"].astype(str).str.strip() != "")
    ]

    return _summary(
        temp,
        ["Source", "Rank"]
    )


# ==========================================================
# TOP AREA
# ==========================================================

def top_area(

    area,

    n=10

):

    return (

        area_summary(area)

        .head(n)

    )


# ==========================================================
# TOP RANK
# ==========================================================

def top_rank(area, n=20):

    temp = area.copy()

    temp = temp[
        temp["Rank"].notna() &
        (temp["Rank"].astype(str).str.strip() != "")
    ]

    return (
        
        _summary(
            temp,
            ["Rank"]
            
        )
        
        .head(n)
        
    )


# ==========================================================
# MAJOR × DATABASE
# ==========================================================

def major_source_summary(area):

    journal = _journal_col(area)

    return (

        area

        .drop_duplicates(

            subset=[

                "Major Group",

                "Source",

                journal

            ]

        )

        .groupby(

            [

                "Major Group",

                "Source"

            ],

            as_index=False

        )

        .agg(

            Total=(journal,"count")

        )

        .sort_values(

            [

                "Major Group",

                "Source"

            ]

        )

        .reset_index(drop=True)

    )


# ==========================================================
# AREA × DATABASE
# ==========================================================

def area_source_summary(area):

    journal = _journal_col(area)

    return (

        area

        .drop_duplicates(

            subset=[

                "Area",

                "Source",

                journal

            ]

        )

        .groupby(

            [

                "Area",

                "Source"

            ],

            as_index=False

        )

        .agg(

            Total=(journal,"count")

        )

        .sort_values(

            [

                "Area",

                "Source"

            ]

        )

        .reset_index(drop=True)

    )


# ==========================================================
# RANK × DATABASE
# ==========================================================

def rank_source_summary(area):

    journal = _journal_col(area)

    return (

        area

        .drop_duplicates(

            subset=[

                "Rank",

                "Source",

                journal

            ]

        )

        .groupby(

            [

                "Rank",

                "Source"

            ],

            as_index=False

        )

        .agg(

            Total=(journal,"count")

        )

        .sort_values(

            [

                "Source",

                "Rank"

            ]

        )

        .reset_index(drop=True)

    )


# ==========================================================
# MAJOR LIST
# ==========================================================

def major_list(area):

    return (

        area

        [["Major Group"]]

        .drop_duplicates()

        .sort_values(

            "Major Group"

        )

        .reset_index(drop=True)

    )


# ==========================================================
# AREA GROUP LIST
# ==========================================================

def area_group_list(area):

    return (

        area

        [["Area Group"]]

        .drop_duplicates()

        .sort_values(

            "Area Group"

        )

        .reset_index(drop=True)

    )


# ==========================================================
# AREA LIST
# ==========================================================

def area_list(area):

    return (

        area

        [["Area"]]

        .drop_duplicates()

        .sort_values(

            "Area"

        )

        .reset_index(drop=True)

    )


# ==========================================================
# SOURCE LIST
# ==========================================================

def source_list(area):

    return (

        area

        [["Source"]]

        .drop_duplicates()

        .sort_values(

            "Source"

        )

        .reset_index(drop=True)

    )


# ==========================================================
# RANK LIST
# ==========================================================

def rank_list(area):

    return (

        area

        [["Rank"]]

        .drop_duplicates()

        .sort_values(

            "Rank"

        )

        .reset_index(drop=True)

    )
    
# ==========================================================
# JOURNAL PROFILE
# ==========================================================

def journal_profile(area, journal_key):

    journal = _journal_col(area)

    return (

        area

        .loc[
            area[journal] == journal_key
        ]

        .sort_values(
            ["Source", "Area"]
        )

        .reset_index(drop=True)

    )


# ==========================================================
# JOURNAL RANK PROFILE
# ==========================================================

def journal_rank_profile(area, journal_key):

    journal = _journal_col(area)

    cols = [

        "Source",

        "Major Group",

        "Area Group",

        "Area",

        "Rank"

    ]

    cols = [c for c in cols if c in area.columns]

    return (

        area

        .loc[
            area[journal] == journal_key
        ]

        [cols]

        .drop_duplicates()

        .sort_values(

            ["Source","Area"]

        )

        .reset_index(drop=True)

    )


# ==========================================================
# JOURNAL DETAIL
# ==========================================================

def journal_detail(master, journal_key):

    journal = _journal_col(master)

    return (

        master

        .loc[
            master[journal] == journal_key
        ]

        .reset_index(drop=True)

    )


# ==========================================================
# AREA DETAIL
# ==========================================================

def area_detail(area, area_name):

    journal = _journal_col(area)

    cols = [

        journal,

        "Journal Title",

        "Publisher",

        "Source",

        "Rank"

    ]

    cols = [c for c in cols if c in area.columns]

    return (

        area

        .loc[
            area["Area"] == area_name
        ]

        [cols]

        .drop_duplicates()

        .sort_values(

            "Journal Title"

        )

        .reset_index(drop=True)

    )


# ==========================================================
# MAJOR DETAIL
# ==========================================================

def major_detail(area, major_name):

    journal = _journal_col(area)

    cols = [

        journal,

        "Journal Title",

        "Area",

        "Source",

        "Rank"

    ]

    cols = [c for c in cols if c in area.columns]

    return (

        area

        .loc[
            area["Major Group"] == major_name
        ]

        [cols]

        .drop_duplicates()

        .sort_values(

            ["Area","Journal Title"]

        )

        .reset_index(drop=True)

    )


# ==========================================================
# PUBLISHER DETAIL
# ==========================================================

def publisher_detail(master, publisher):

    journal = _journal_col(master)

    cols = [

        journal,

        "Journal Title",

        "Publisher",

        "2025 rating",

        "SJR Best Quartile",

        "AJG 2024"

    ]

    cols = [c for c in cols if c in master.columns]

    return (

        master

        .loc[
            master["Publisher"] == publisher
        ]

        [cols]

        .drop_duplicates()

        .sort_values(

            "Journal Title"

        )

        .reset_index(drop=True)

    )


# ==========================================================
# DATABASE DETAIL
# ==========================================================

def database_detail(area, source):

    journal = _journal_col(area)

    cols = [

        journal,

        "Journal Title",

        "Major Group",

        "Area",

        "Rank"

    ]

    cols = [c for c in cols if c in area.columns]

    return (

        area

        .loc[
            area["Source"] == source
        ]

        [cols]

        .drop_duplicates()

        .sort_values(

            ["Major Group","Area"]

        )

        .reset_index(drop=True)

    )


# ==========================================================
# SEARCH JOURNAL
# ==========================================================

def search_journal(master, keyword):

    keyword = str(keyword).upper()

    return (

        master

        .loc[

            master["Search_Text"]

            .str.contains(

                keyword,

                case=False,

                na=False,

                regex=False

            )

        ]

        .reset_index(drop=True)

    )


# ==========================================================
# EXPORT CURRENT FILTER
# ==========================================================

def export_table(df):

    return (

        df

        .copy()

        .reset_index(drop=True)

    )


# ==========================================================
# DASHBOARD INFORMATION
# ==========================================================

def dashboard_information(master, area):

    return {

        "Journal":

            master["Journal_Key"].nunique(),

        "Publisher":

            master["Publisher"].nunique(),

        "Area":

            area["Area"].nunique(),

        "Major":

            area["Major Group"].nunique(),

        "Area Group":

            area["Area Group"].nunique(),

        "Source":

            area["Source"].nunique(),

        "Rank":

            area["Rank"].nunique()

    }