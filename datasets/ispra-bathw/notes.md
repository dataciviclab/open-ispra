# ispra-bathw — Note

## Fonte
- Endpoint SPARQL: `https://dati.isprambiente.it/sparql`
- Graph: `https://w3id.org/italia/env/ld/bathw/{year}/`
- Ontologia: `w3id.org/italia/env/onto/top/`

## Struttura RDF
Ogni indicatore è un nodo con:
- `rdfs:label` bilingue (IT+EN) — dedup necessario
- `top:hasValue` → valueNode → `top:value` (stringa numerica)
- `top:hasUnitOfMeasure` → UoM URI
- `top:isMemberOf` → collection
- `top:atTime` → year node

## URI pattern
```
.../bathw/indicator/{code}_{site_id}_{indicator}_{year}
```
- `code`: prefisso catalogo (es. 20201)
- `site_id`: identificativo sito balneazione (es. IT003013161002)
- `indicator`: tipo indicatore (sempre `quality` per balneazione)
- `year`: anno (es. 2024)

## Scala qualità (value)
- 0 = Non classificato
- 1 = Eccellente
- 2 = Buona
- 3 = Sufficiente
- 4 = Scadente

## Anni disponibili
1990-2024 (30+ anni di serie storica)

## Quirks
- I label sono duplicati IT/EN per ogni indicatore
- La query con FILTER su lang() fallisce su Virtuoso — usare CONTAINS su label
- Il graph bathw è relativamente piccolo (~5.538 indicatori/anno)
- Nessun geodato: i dati sono solo tabellari (qualità per sito)
