"""Fonti dati per la dashboard Ambiente ISPRA.

Multi-dataset: consumo_suolo, bathw, rmn, iffi, urban, pest.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st
from lab_connectors.duckdb.queries import (
    load_mart_table as _load_mart_table,
)
from lab_connectors.duckdb.queries import (
    query_clean as _query_clean,
)

try:
    from lab_connectors.duckdb.queries import detect_local_root
except ImportError:
    detect_local_root = None  # type: ignore[assignment]

from lab_connectors.formatters import fmt_num, fmt_pct  # noqa: F401  # re-export for pages

ROOT = Path(__file__).parent.parent
PREFIX = "open-ispra/"
LOCAL_ROOT = detect_local_root(repo_root=ROOT) if detect_local_root else None

# ---------------------------------------------------------------------------
# Dataset configs: (slug, years)
# ---------------------------------------------------------------------------
_DATASETS = {
    "consumo_suolo": ("ispra_consumo_suolo", [2024]),
    "bathw": ("ispra_bathw", [2024]),
    "rmn": ("ispra_rmn", [2023]),
    "iffi": ("ispra_iffi", [2024]),
    "urban": ("ispra_urban", [2018]),
    "pest": ("ispra_pest", [2021]),
}


def _slug(key: str) -> str:
    return _DATASETS[key][0]


def _years(key: str) -> list[int]:
    return _DATASETS[key][1]


def _q(key: str, sql: str, year: int | None = None):
    slug = _slug(key)
    yrs = [year] if year else _years(key)
    kwargs = {"prefix": PREFIX}
    if LOCAL_ROOT:
        kwargs["local_root"] = LOCAL_ROOT
    return _query_clean(slug, sql, yrs, **kwargs)


def _mart(key: str, table: str, year: int | None = None):
    slug = _slug(key)
    yr = year or _years(key)[-1]
    kwargs = {"prefix": PREFIX}
    if LOCAL_ROOT:
        kwargs["local_root"] = LOCAL_ROOT
    return _load_mart_table(slug, table, yr, **kwargs)


# ---------------------------------------------------------------------------
# Consumo suolo
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def query_consumo_suolo(sql: str, year: int = 2024):
    return _q("consumo_suolo", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_consumo_suolo(table: str, year: int = 2024):
    return _mart("consumo_suolo", table, year)


# ---------------------------------------------------------------------------
# Balneazione
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def query_bathw(sql: str, year: int = 2024):
    return _q("bathw", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_bathw(table: str, year: int = 2024):
    return _mart("bathw", table, year)


# ---------------------------------------------------------------------------
# Livelli mare
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def query_rmn(sql: str, year: int = 2023):
    return _q("rmn", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_rmn(table: str, year: int = 2023):
    return _mart("rmn", table, year)


# ---------------------------------------------------------------------------
# Frane
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def query_iffi(sql: str, year: int = 2024):
    return _q("iffi", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_iffi(table: str, year: int = 2024):
    return _mart("iffi", table, year)


# ---------------------------------------------------------------------------
# Ambiente urbano
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def query_urban(sql: str, year: int = 2018):
    return _q("urban", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_urban(table: str, year: int = 2018):
    return _mart("urban", table, year)


# ---------------------------------------------------------------------------
# Pesticidi
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def query_pest(sql: str, year: int = 2021):
    return _q("pest", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_pest(table: str, year: int = 2021):
    return _mart("pest", table, year)
