#!/usr/bin/env python3
"""Probe SPARQL: testa la query su bathw e stampa statistiche.

Uso: python probe_bathw.py [year] [limit]
"""

import sys
import os

# Aggiungi il workspace root al path per lab_connectors
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORKSPACE)

from lab_connectors.http.sparql import execute_sparql

ENDPOINT = "https://dati.isprambiente.it/sparql"
GRAPH_BASE = "https://w3id.org/italia/env/ld/bathw"

QUERY_TEMPLATE = """
PREFIX top: <https://w3id.org/italia/env/onto/top/>
SELECT ?uri ?label ?value ?uom WHERE {{
  GRAPH <{graph}/ {{
    ?uri rdfs:label ?label .
    ?uri top:hasValue ?vn .
    ?vn top:value ?value .
    ?vn top:hasUnitOfMeasure ?uom .
    FILTER(lang(?label) = 'it')
  }}
}} LIMIT {limit}
"""


def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2024
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    graph = f"{GRAPH_BASE}/{year}"
    query = QUERY_TEMPLATE.format(graph=graph, limit=limit)

    print(f"Query SPARQL: {ENDPOINT}", file=sys.stderr)
    print(f"Graph: {graph}", file=sys.stderr)
    print(f"Limit: {limit}", file=sys.stderr)
    print(file=sys.stderr)

    bindings = execute_sparql(ENDPOINT, query, timeout=60)
    print(f"Risultati: {len(bindings)}", file=sys.stderr)
    print(file=sys.stderr)

    # Statistiche
    values = {}
    for b in bindings:
        v = b.get("value", "")
        values[v] = values.get(v, 0) + 1

    print("Distribuzione valori:")
    for v, cnt in sorted(values.items(), key=lambda x: -x[1]):
        print(f"  {v}: {cnt}")

    print()
    print("Campione (prime 5 righe):")
    for b in bindings[:5]:
        label = b.get("label", "?")
        value = b.get("value", "?")
        print(f"  {label} -> {value}")


if __name__ == "__main__":
    main()
