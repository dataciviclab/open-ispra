#!/usr/bin/env python3
"""Fetch ISPRA bathw data from SPARQL endpoint for all available years.

Genera un CSV con tutti gli anni (1990-2024).
Uso: python fetch_bathw.py [output_path]
"""

import csv
import os
import sys

# Aggiungi workspace root al path per lab_connectors
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, WORKSPACE)

from lab_connectors.http.sparql import execute_sparql

ENDPOINT = "https://dati.isprambiente.it/sparql"
GRAPH_BASE = "https://w3id.org/italia/env/ld/bathw"
YEARS = list(range(1990, 2025))  # 1990-2024


def _val(binding):
    """Extract value from SPARQL binding dict."""
    if isinstance(binding, dict):
        return binding.get("value", "")
    return str(binding) if binding else ""


def build_query(graph: str) -> str:
    return (
        "PREFIX top: <https://w3id.org/italia/env/onto/top/>\n"
        "SELECT ?uri ?label ?value ?uom WHERE {\n"
        f"  GRAPH <{graph}> {{\n"
        "    ?uri rdfs:label ?label .\n"
        "    ?uri top:hasValue ?vn .\n"
        "    ?vn top:value ?value .\n"
        "    ?vn top:hasUnitOfMeasure ?uom .\n"
        "    FILTER(lang(?label) = 'it')\n"
        "  }\n"
        "} LIMIT 50000"
    )


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv"
    all_rows = []

    for year in YEARS:
        graph = f"{GRAPH_BASE}/{year}/"
        query = build_query(graph)
        print(f"  {year}...", end="", flush=True, file=sys.stderr)
        try:
            bindings = execute_sparql(ENDPOINT, query, timeout=120)
            for b in bindings:
                all_rows.append({
                    "uri": _val(b.get("uri")),
                    "label": _val(b.get("label")),
                    "value": _val(b.get("value")),
                    "uom": _val(b.get("uom")),
                    "year": year,
                })
            print(f" {len(bindings)} righe", file=sys.stderr)
        except Exception as e:
            print(f" ERRORE: {e}", file=sys.stderr)

    if all_rows:
        fieldnames = ["uri", "label", "value", "uom", "year"]
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\nTotale: {len(all_rows)} righe in {output_path}", file=sys.stderr)
    else:
        print("\nNessun dato recuperato!", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
