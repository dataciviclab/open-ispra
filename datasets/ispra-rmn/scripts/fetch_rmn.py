#!/usr/bin/env python3
"""Fetch ISPRA RMN (Rete Mareografica Nazionale) data.

Query SPARQL per le URL dei CSV, poi scarica e merge in un unico file.
36 stazioni, 2010-2023, ~30K file CSV.

Uso: python fetch_rmn.py [output_path] [--max-files N]
"""

import csv
import io
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, WORKSPACE)

from lab_connectors.http import HttpClient
from lab_connectors.http.sparql import execute_sparql

ENDPOINT = "https://dati.isprambiente.it/sparql"
SPARQL_QUERY = """SELECT ?url ?label WHERE {
  GRAPH <https://w3id.org/italia/env/ld/rmn/> {
    ?s <https://w3id.org/italia/env/onto/top/hasDownloadURL> ?url .
    ?s rdfs:label ?label .
    FILTER(lang(?label) = 'it')
  }
} LIMIT 50000"""

MAX_WORKERS = 20


def _val(b):
    if isinstance(b, dict):
        return b.get("value", "")
    return str(b) if b else ""


def parse_filename(url):
    """Extract station_id, year, month from URL like rmn/ancona_hydrometric_201403.csv"""
    fname = url.split("/")[-1].replace(".csv", "")
    parts = fname.split("_")
    if len(parts) < 3:
        return None, None, None
    station_id = parts[0]
    ym = parts[-1]
    if len(ym) == 6:
        return station_id, ym[:4], ym[4:]
    return station_id, None, None


def download_csv(client, url, station_id, year, month):
    """Download a single CSV and return parsed rows."""
    try:
        result = client.get(url)
        if not result.is_ok or result.response is None:
            return []
        text = result.response.text
        reader = csv.reader(io.StringIO(text), delimiter=";")
        header = next(reader, None)
        rows = []
        for row in reader:
            if len(row) >= 2:
                rows.append({
                    "station_id": station_id,
                    "year": year,
                    "month": month,
                    "timestamp_utc": row[0].strip(),
                    "level": row[1].strip(),
                })
        return rows
    except Exception:
        return []


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv"
    max_files = None
    if "--max-files" in sys.argv:
        idx = sys.argv.index("--max-files")
        max_files = int(sys.argv[idx + 1])

    # 1. Fetch URLs from SPARQL
    print("Fetching URLs from SPARQL...", file=sys.stderr, flush=True)
    t0 = time.time()
    bindings = execute_sparql(ENDPOINT, SPARQL_QUERY, timeout=120)
    urls = []
    for b in bindings:
        url = _val(b.get("url"))
        label = _val(b.get("label"))
        station_id, year, month = parse_filename(url)
        if station_id and year and month:
            urls.append((url, station_id, year, month))
    print(f"  {len(urls)} file da scaricare ({time.time()-t0:.1f}s)", file=sys.stderr)

    if max_files:
        urls = urls[:max_files]
        print(f"  Limitato a {max_files} file", file=sys.stderr)

    # 2. Download in parallel
    print(f"Downloading con {MAX_WORKERS} thread...", file=sys.stderr, flush=True)
    t0 = time.time()
    client = HttpClient(timeout=30)
    all_rows = []
    done = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(download_csv, client, url, sid, y, m): (sid, y, m)
            for url, sid, y, m in urls
        }
        for future in as_completed(futures):
            rows = future.result()
            all_rows.extend(rows)
            done += 1
            if done % 500 == 0:
                print(f"  {done}/{len(urls)} ({len(all_rows):,} righe)", file=sys.stderr, flush=True)

    elapsed = time.time() - t0
    print(f"  Completato: {len(all_rows):,} righe in {elapsed:.0f}s ({len(all_rows)/elapsed:.0f} righe/s)", file=sys.stderr)

    # 3. Write CSV
    if all_rows:
        fieldnames = ["station_id", "year", "month", "timestamp_utc", "level"]
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\nScritto: {output_path} ({len(all_rows):,} righe)", file=sys.stderr)
    else:
        print("\nNessun dato!", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
