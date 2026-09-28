#!/usr/bin/env python3
"""Ambiente ISPRA · Dashboard Streamlit

Dati ambientali ISPRA — acque, suolo, mari, pesticidi, frane — in un'unica dashboard.
"""

import streamlit as st
from lab_connectors.branding import apply_branding

st.set_page_config(
    page_title="Ambiente ISPRA · Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_branding(
    repo_name="open-ispra",
    repo_url="https://github.com/dataciviclab/open-ispra",
)

pages = {
    "Panoramica": [
        st.Page("pages/01_Panoramica.py", title="Panoramica", icon="📊", default=True),
    ],
    "Ambiente": [
        st.Page("pages/02_Consumo_Suolo.py", title="Consumo Suolo", icon="🏗️"),
        st.Page("pages/03_Balneazione.py", title="Balneazione", icon="🏖️"),
        st.Page("pages/04_Livelli_Mare.py", title="Livelli Mare", icon="🌊"),
        st.Page("pages/05_Frane.py", title="Frane", icon="⛰️"),
        st.Page("pages/06_Ambiente_Urbano.py", title="Ambiente Urbano", icon="🏙️"),
        st.Page("pages/07_Pesticidi.py", title="Pesticidi", icon="🧪"),
    ],
    "Strumenti": [
        st.Page("pages/08_SQL.py", title="Query SQL", icon="🔬"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
