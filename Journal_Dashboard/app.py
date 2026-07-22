# ==========================================================
# Journal Analytics Dashboard
# app.py
# ==========================================================

import streamlit as st
from utils import load_data
import pandas as pd
from config import APP_TITLE

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# LOAD DATA
# ==========================================================

master, _ = load_data()

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

/* Hide Streamlit menu */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Card */

.card{

    background-color:white;

    border:1px solid #E5E7EB;

    border-radius:15px;

    padding:22px;

    min-height:180px;

    box-shadow:0 2px 10px rgba(0,0,0,.08);

}

.card-title{

    font-size:24px;

    font-weight:700;

    color:#1F2937;

    margin-bottom:10px;

}

.card-text{

    color:#6B7280;

    font-size:15px;

    line-height:1.7;

    margin-bottom:20px;

}

.metric-box{

    border-radius:12px;

    padding:10px;

    background:#F8FAFC;

    border:1px solid #E5E7EB;

}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("📚 Journal Dashboard")

st.sidebar.success("Journal Analytics System")

st.sidebar.markdown("---")

st.sidebar.markdown("### Database")

st.sidebar.write("✅ ABDC")
st.sidebar.write("✅ Scopus")
st.sidebar.write("✅ Scimago")
st.sidebar.write("✅ AJG")

st.sidebar.markdown("---")

st.sidebar.info(
"""
Version 1.0

Journal Analytics Dashboard
"""
)

# ==========================================================
# TITLE
# ==========================================================

st.title("📚 Journal Analytics Dashboard")

st.caption(
"""
Journal Analytics & Ranking System

ABDC | Scopus | Scimago | AJG
"""
)

st.divider()

# ==========================================================
# NAVIGATION
# ==========================================================

st.subheader("Navigation")

c1, c2, c3 = st.columns(3)

# ----------------------------------------------------------
# OVERVIEW
# ----------------------------------------------------------

with c1:

    st.markdown("""
    <div class="card">

    <div class="card-title">
    📈 Dashboard & Ranking
    </div>

    <div class="card-text">

    • Dashboard Overview<br>

    • Journal Statistics<br>

    • Ranking Analysis<br>

    • Database Coverage

    </div>

    </div>

    """, unsafe_allow_html=True)

    st.page_link(
        "pages/Overview.py",
        label="Open Dashboard",
        icon="📈"
    )

# ----------------------------------------------------------
# JOURNAL SEARCH
# ----------------------------------------------------------

with c2:

    st.markdown("""
    <div class="card">

    <div class="card-title">
    🔍 Journal Search
    </div>

    <div class="card-text">

    • Search Journal Title<br>

    • Search ISSN / EISSN<br>

    • Publisher Information<br>

    • Database Coverage

    </div>

    </div>

    """, unsafe_allow_html=True)

    st.page_link(
        "pages/Journal_Search.py",
        label="Open Journal Search",
        icon="🔍"
    )

# ----------------------------------------------------------
# JOURNAL TABLE
# ----------------------------------------------------------

with c3:

    st.markdown("""
    <div class="card">

    <div class="card-title">
    📄 Journal Table
    </div>

    <div class="card-text">

    • Browse All Journals<br>

    • Filter Data<br>

    • Sort Columns<br>

    • Export Excel

    </div>

    </div>

    """, unsafe_allow_html=True)

    st.page_link(
    "pages/Journal_Search.py",
    label="Open Journal Table",
    icon="📄"
)

st.divider()

# ==========================================================
# DATASET INFORMATION
# ==========================================================

st.subheader("📊 Dataset Information")

info1, info2, info3, info4 = st.columns(4)

with info1:

    st.metric(
        "Total Journals",
        f"{len(master):,}"
    )

with info2:

    st.metric(
        "Publishers",
        f"{master['Publisher'].nunique():,}"
    )

with info3:

    st.metric(
        "ABDC Areas",
        f"{master['ABDC Area'].nunique():,}"
    )

with info4:

    years = pd.to_numeric(
        master["Year Inception"],
        errors="coerce"
    ).dropna()

    if not years.empty:

        st.metric(
            "Oldest Journal",
            int(years.min())
        )

    else:

        st.metric(
            "Oldest Journal",
            "N/A"
        )

st.divider()

# ==========================================================
# JOURNAL MASTER PREVIEW
# ==========================================================

st.subheader("📄 Journal Master Preview")

st.caption("Preview of the first 20 journals in the database.")

preview_columns = [

    "Journal Title",

    "Publisher",

    "ISSN",

    "ISSNOnline",

    "ABDC Area",

    "2025 rating"

]

preview_columns = [

    col

    for col in preview_columns

    if col in master.columns

]

st.dataframe(

    master[preview_columns].head(20),

    use_container_width=True,

    hide_index=True

)

st.info(
"""
💡 **Tip**

To search for a specific journal, view database coverage,
or export filtered results, open **Journal Search**
from the Navigation section above.
"""
)

st.divider()

# ==========================================================
# EXPORT DATASET
# ==========================================================

st.subheader("📥 Export Dataset")

download_col1, download_col2 = st.columns([1,3])

with download_col1:

    csv = master.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(

        label="⬇ Download CSV",

        data=csv,

        file_name="Journal_Master.csv",

        mime="text/csv",

        use_container_width=True

    )

with download_col2:

    st.success(
        """
Export the complete Journal Master dataset.

The exported file contains all journal information including

• Journal Information

• ABDC

• Scopus

• Scimago

• AJG

• ISSN / EISSN

• Publisher
"""
    )

st.divider()

# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

st.subheader("ℹ️ System Information")

left, right = st.columns(2)

with left:

    st.markdown(
        """
**Journal Analytics Dashboard**

Version : **1.0**

Framework : **Streamlit**

Database :

- ABDC
- Scopus
- Scimago
- AJG
"""
    )

with right:

    st.markdown(
        """
**Available Features**

✅ Dashboard Overview

✅ Journal Search

✅ Database Coverage

✅ Journal Ranking

✅ Export Dataset
"""
    )

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
"""
<div style="text-align:center;color:gray;font-size:14px;">

Journal Analytics Dashboard © 2026

Developed with Streamlit

</div>
""",
unsafe_allow_html=True
)