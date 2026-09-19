#!/usr/bin/env python3
"""Fetch IFFI summary data from IdroGEO API.

Scarica le statistiche frane per regione e le aggrega in un CSV.
API pubblica: https://idrogeo.isprambiente.it/api/

Uso: python fetch_iffi.py [output_path]
"""

import csv
import json
import ssl
import sys
import urllib.request

API_BASE = "https://idrogeo.isprambiente.it/api"


def api_get(path: str) -> dict:
    """Esegui GET all'IdroGEO API, ritorna JSON."""
    url = f"{API_BASE}{path}"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv"

    # 1. Sommario nazionale
    print("Fetching /iffi/italia...", file=sys.stderr)
    italia = api_get("/iffi/italia")
    totale_frane = sum(f.get("nr_frane", 0) for f in italia.get("frane_stats", []))

    # 2. Elenco regioni
    print("Fetching /iffi/regioni...", file=sys.stderr)
    regioni = api_get("/iffi/regioni")

    # 3. Stats per regione
    rows = []
    for reg in regioni:
        uid = reg["uid"]
        nome = reg["nome"]
        print(f"  Fetching /iffi/regioni/{uid} ({nome})...", file=sys.stderr)
        try:
            stats = api_get(f"/iffi/regioni/{uid}")
            frane_stats = stats.get("frane_stats", [])
            nr_frane = sum(f.get("nr_frane", 0) for f in frane_stats)
            rows.append({
                "regione": nome,
                "cod_regione": uid,
                "nr_frane": nr_frane,
            })
        except Exception as e:
            print(f"    ERROR: {e}", file=sys.stderr)
            rows.append({
                "regione": nome,
                "cod_regione": uid,
                "nr_frane": 0,
            })

    # 4. Scrivi CSV
    fieldnames = ["regione", "cod_regione", "nr_frane"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nScritto {len(rows)} righe in {output_path}", file=sys.stderr)
    print(f"Totale frane nazionale: {totale_frane}", file=sys.stderr)


if __name__ == "__main__":
    main()
