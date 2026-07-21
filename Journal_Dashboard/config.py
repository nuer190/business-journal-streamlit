# ==========================================================
# config.py
# Journal Analytics Dashboard
# ==========================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

MASTER_FILE = DATA_DIR / "journal_master.xlsx"
AREA_FILE = DATA_DIR / "journal_area.xlsx"

APP_TITLE = "Journal Analytics Dashboard"

# ==========================================================
# DASHBOARD
# ==========================================================

APP_ICON = "📚"

LAYOUT = "wide"

SIDEBAR = "expanded"

# ==========================================================
# DATABASE
# ==========================================================

DATABASES = [

    "ABDC",

    "Scopus",

    "Scimago",

    "AJG"

]

# ==========================================================
# SOURCE COLOR
# ==========================================================

SOURCE_COLOR = {

    "ABDC":"#003366",

    "Scopus":"#00897B",

    "Scimago":"#FF8200",

    "AJG":"#7B1FA2"

}

# ==========================================================
# RANK ORDER
# ==========================================================

RANK_ORDER = {

    "ABDC": {
        "A*": 1,
        "A": 2,
        "B": 3,
        "C": 4
    },

    "Scimago": {
        "Q1": 1,
        "Q2": 2,
        "Q3": 3,
        "Q4": 4
    },

    "AJG": {
        "4*": 1,
        "4": 2,
        "3": 3,
        "2": 4,
        "1": 5
    }

}

# ==========================================================
# RANK COLOR
# ==========================================================

RANK_COLOR = {

    "A*":"#1B5E20",

    "A":"#2E7D32",

    "B":"#F9A825",

    "C":"#D84315",

    "Q1":"#1565C0",

    "Q2":"#42A5F5",

    "Q3":"#FB8C00",

    "Q4":"#E53935",

    "4*":"#1B5E20",

    "4":"#43A047",

    "3":"#FB8C00",

    "2":"#EF6C00",

    "1":"#C62828"

}

# ==========================================================
# MAJOR GROUP
# ==========================================================

MAJOR_GROUP = [

    "Business",

    "Technology",

    "Science",

    "Health",

    "Social Sciences",

    "Other"

]

# ==========================================================
# DEFAULT FILTER
# ==========================================================

DEFAULT_SOURCE = "All"

DEFAULT_MAJOR = "All"

DEFAULT_AREA_GROUP = "All"

DEFAULT_AREA = "All"

DEFAULT_RANK = "All"

# ==========================================================
# TABLE COLUMN
# ==========================================================

TABLE_COLUMNS = [

    "Journal Title",

    "Publisher",

    "Canonical_ISSN",

    "Canonical_EISSN",

    "Source",

    "Area",

    "Rank"

]

# ==========================================================
# JOURNAL DETAIL
# ==========================================================

DETAIL_COLUMNS = [

    "Journal Title",

    "Publisher",

    "Canonical_ISSN",

    "Canonical_EISSN",

    "Year Inception",

    "FoR"

]

# ==========================================================
# EXPORT FILE
# ==========================================================

EXPORT_NAME = "Journal_Analytics.xlsx"

# ==========================================================
# CHART HEIGHT
# ==========================================================

BAR_HEIGHT = 550

PIE_HEIGHT = 500

TREEMAP_HEIGHT = 650

SUNBURST_HEIGHT = 650
