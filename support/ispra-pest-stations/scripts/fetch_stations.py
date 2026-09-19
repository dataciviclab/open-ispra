#!/usr/bin/env python3
"""Fetch ISPRA pest stations with coordinates from SPARQL.

Output: CSV con stazioni e coordinate (lat/long).
Uso: python fetch_stations.py [output_path]
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

PLATFORM_QUERY = """
SELECT ?feature_uri ?lat ?lon WHERE {{
  GRAPH <{graph}> {{
    ?feature_uri a <https://w3id.org/italia/env/onto/place/Feature> .
    ?feature_uri <http://www.w3.org/2003/01/geo/wgs84_pos#lat> ?lat .
    ?feature_uri <http://www.w3.org/2003/01/geo/wgs84_pos#long> ?lon .
  }}
}} LIMIT 50000
"""


def _val(binding):
    if isinstance(binding, dict):
        return binding.get("value", "")
    return str(binding) if binding else ""


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv"
    all_rows = []
    seen = set()

    for year in YEARS:
        graph = f"{GRAPH_BASE}/{year}/"
        print(f"  {year}...", end="", flush=True, file=sys.stderr)
        try:
            bindings = execute_sparql(ENDPOINT, PLATFORM_QUERY.format(graph=graph), timeout=120)
            for b in bindings:
                uri = _val(b.get("feature_uri"))
                # Parse: .../pest/feature/{istat}_{station_id}_{year}
                parts = uri.split("/")
                filename = parts[-1] if parts else ""
                segs = filename.split("_")
                station_id = segs[1] if len(segs) > 1 else filename
                key = f"{station_id}_{year}"
                if key not in seen:
                    seen.add(key)
                    all_rows.append({
                        "year": year,
                        "station_id": station_id,
                        "lat": _val(b.get("lat")),
                        "lon": _val(b.get("lon")),
                    })
            print(f" {len(bindings)} stazioni", file=sys.stderr)
        except Exception as e:
            print(f" ERRORE: {e}", file=sys.stderr)

    if all_rows:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["year", "station_id", "lat", "lon"])
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\nTotale: {len(all_rows)} righe -> {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
