#!/usr/bin/env python3
"""Fetch ISPRA pest indicators from SPARQL endpoint — ottimizzato.

Usa CSV diretto (100K righe/query) invece di JSON.
4 query da 100K per anno = ~30 pagine/anno = ~120 totali.

Uso: python fetch_indicators.py [output_path]
"""

import csv
import io
import os
import sys
import time
import urllib.parse

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, WORKSPACE)

from lab_connectors.http import HttpClient

ENDPOINT = "https://dati.isprambiente.it/sparql"
GRAPH_BASE = "https://w3id.org/italia/env/ld/pest"
YEARS = [2018, 2019, 2020, 2021]
PAGE_SIZE = 100000  # Hard limit SPARQL endpoint


def build_query(graph, limit, offset):
    return (
        "PREFIX top: <https://w3id.org/italia/env/onto/top/>\n"
        "SELECT ?identifier ?value ?uom WHERE {\n"
        f"  GRAPH <{graph}> {{\n"
        "    ?indicator top:identifier ?identifier .\n"
        "    ?indicator top:hasValue ?vn .\n"
        "    ?vn top:value ?value .\n"
        "    ?vn top:hasUnitOfMeasure ?uom .\n"
        "  }\n"
        f"}} LIMIT {limit} OFFSET {offset}"
    )


def fetch_page_csv(client, graph, offset):
    """Fetch one page as CSV, return parsed rows."""
    query = build_query(graph, PAGE_SIZE, offset)
    url = f"{ENDPOINT}?query={urllib.parse.quote(query)}"
    result = client.get(url, headers={"Accept": "text/csv"})
    if not result.is_ok or result.response is None:
        return []
    text = result.response.text
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv"
    all_rows = []
    client = HttpClient(timeout=120)

    for year in YEARS:
        graph = f"{GRAPH_BASE}/{year}/"
        print(f"  {year}...", end="", flush=True, file=sys.stderr)
        year_start = time.time()
        page = 0
        while True:
            offset = page * PAGE_SIZE
            rows = fetch_page_csv(client, graph, offset)
            if not rows:
                break
            for r in rows:
                identifier = r.get("identifier", "")
                parts = identifier.split("_")
                station_id = parts[1] if len(parts) > 1 else ""
                cas_raw = parts[3] if len(parts) > 3 else ""
                cas_number = cas_raw.replace("_", "-") if cas_raw else ""
                all_rows.append({
                    "year": year,
                    "station_id": station_id,
                    "cas_number": cas_number,
                    "identifier": identifier,
                    "value": r.get("value", ""),
                    "uom": r.get("uom", ""),
                })
            if len(rows) < PAGE_SIZE:
                break
            page += 1
        elapsed = time.time() - year_start
        print(f" {len([r for r in all_rows if r['year'] == year])} misurazioni ({elapsed:.0f}s)", file=sys.stderr)

    if all_rows:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["year", "station_id", "cas_number", "identifier", "value", "uom"])
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\nTotale: {len(all_rows)} righe -> {output_path}", file=sys.stderr)
    else:
        print("\nNessun dato recuperato!", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
