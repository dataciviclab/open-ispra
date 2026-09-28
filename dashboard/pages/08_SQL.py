"""Query SQL — Explorer libero su tutti i dataset ISPRA."""

from pathlib import Path

from lab_connectors.duckdb.sql_page import render_sql_query
from lab_connectors.registry import load_registry

REPO_ROOT = Path(__file__).parent.parent.parent
registry = load_registry(REPO_ROOT / "registry" / "registry.json")

render_sql_query(
    registry=registry,
    prefix="open-ispra/",
    default_slug="ispra_consumo_suolo",
)
