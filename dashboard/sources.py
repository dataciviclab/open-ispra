"""Fonti dati per la dashboard Ambiente ISPRA.

Multi-dataset: consumo_suolo, bathw, rmn, iffi, urban, pest.
Tutto derivato dal registry — zero hardcoded.
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
from lab_connectors.duckdb.queries import (
    years_from_registry,
)
from lab_connectors.formatters import fmt_num, fmt_pct  # noqa: F401  # re-export for pages
from lab_connectors.registry import load_registry

ROOT = Path(__file__).parent.parent
PREFIX = "open-ispra/"

# ---------------------------------------------------------------------------
# Registry: slug e anni derivati dal registry
# ---------------------------------------------------------------------------
_registry = load_registry(ROOT / "registry" / "registry.json")

# Map key -> (slug, years) — tutto dal registry
_DS = {}
_KEY_MAP = {
    "consumo_suolo": "ispra_consumo_suolo",
    "bathw": "ispra_bathw",
    "rmn": "ispra_rmn",
    "iffi": "ispra_iffi",
    "urban": "ispra_urban",
    "pest": "ispra_pest",
}
for _key, _slug in _KEY_MAP.items():
    _DS[_key] = (_slug, years_from_registry(_registry, slug=_slug))


def _q(key: str, sql: str, year: int | None = None):
    slug, years = _DS[key]
    yrs = [year] if year else years
    return _query_clean(slug, sql, yrs, prefix=PREFIX)


def _mart(key: str, table: str, year: int | None = None):
    slug, years = _DS[key]
    yr = year or years[-1]
    return _load_mart_table(slug, table, yr, prefix=PREFIX)


# ---------------------------------------------------------------------------
# Query functions
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def query_consumo_suolo(sql: str, year: int | None = None):
    return _q("consumo_suolo", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_consumo_suolo(table: str, year: int | None = None):
    return _mart("consumo_suolo", table, year)


@st.cache_data(ttl=3600, show_spinner=False)
def query_bathw(sql: str, year: int | None = None):
    return _q("bathw", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_bathw(table: str, year: int | None = None):
    return _mart("bathw", table, year)


@st.cache_data(ttl=3600, show_spinner=False)
def query_rmn(sql: str, year: int | None = None):
    return _q("rmn", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_rmn(table: str, year: int | None = None):
    return _mart("rmn", table, year)


@st.cache_data(ttl=3600, show_spinner=False)
def query_iffi(sql: str, year: int | None = None):
    return _q("iffi", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_iffi(table: str, year: int | None = None):
    return _mart("iffi", table, year)


@st.cache_data(ttl=3600, show_spinner=False)
def query_urban(sql: str, year: int | None = None):
    return _q("urban", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_urban(table: str, year: int | None = None):
    return _mart("urban", table, year)


@st.cache_data(ttl=3600, show_spinner=False)
def query_pest(sql: str, year: int | None = None):
    return _q("pest", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_pest(table: str, year: int | None = None):
    return _mart("pest", table, year)
