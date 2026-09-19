#!/usr/bin/env python3
"""Fetch ISPRA pest indicators from SPARQL endpoint.

Query paginata per ottenere le concentrazioni pesticidi.
Le coordinate stazioni sono nel support dataset ispra-pest-stations.

Uso: python fetch_indicators.py [output_path]
"""

import csv
import os
import sys

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, WORKSPACE)

from lab_connectors.http.sparql import execute_sparql

ENDPOINT = "https://dati.isprambiente.it/sparql"
GRAPH_BASE = "https://w3id.org/italia/env/ld/pest"
YEARS = [2018, 2019, 2020, 2021]

INDICATOR_QUERY = """
PREFIX top: <https://w3id.org/italia/env/onto/top/>
SELECT ?identifier ?value ?uom WHERE {{
  GRAPH <{graph}> {{
    ?indicator top:identifier ?identifier .
    ?indicator top:hasValue ?vn .
    ?vn top:value ?value .
    ?vn top:hasUnitOfMeasure ?uom .
  }}
}} LIMIT {limit} OFFSET {offset}
"""


def _val(binding):
    if isinstance(binding, dict):
        return binding.get("value", "")
    return str(binding) if binding else ""


def parse_station_id(identifier):
    parts = identifier.split("_")
    return parts[1] if len(parts) > 1 else ""


def parse_cas(identifier):
    parts = identifier.split("_")
    if len(parts) > 3:
        return parts[3].replace("_", "-")
    return ""


def fetch_indicators(graph, year, page_size=50000, max_pages=200):
    all_rows = []
    for page in range(max_pages):
        offset = page * page_size
        query = INDICATOR_QUERY.format(graph=graph, limit=page_size, offset=offset)
        try:
            bindings = execute_sparql(ENDPOINT, query, timeout=120)
            if not bindings:
                break
            for b in bindings:
                identifier = _val(b.get("identifier"))
                all_rows.append({
                    "year": year,
                    "station_id": parse_station_id(identifier),
                    "cas_number": parse_cas(identifier),
                    "identifier": identifier,
                    "value": _val(b.get("value")),
                    "uom": _val(b.get("uom")),
                })
            if len(bindings) < page_size:
                break
        except Exception as e:
            print(f"    Errore pagina {page}: {e}", file=sys.stderr)
            break
    return all_rows


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv"
    all_rows = []

    for year in YEARS:
        graph = f"{GRAPH_BASE}/{year}/"
        print(f"  {year}...", end="", flush=True, file=sys.stderr)
        try:
            indicators = fetch_indicators(graph, year)
            all_rows.extend(indicators)
            print(f" {len(indicators)} misurazioni", file=sys.stderr)
        except Exception as e:
            print(f" ERRORE: {e}", file=sys.stderr)

    if all_rows:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["year", "station_id", "cas_number", "identifier", "value", "uom"])
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\nTotale: {len(all_rows)} righe -> {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
