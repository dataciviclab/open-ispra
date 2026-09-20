# Contribuire a open-ispra

Repo multi-dataset per i dati ISPRA nel DataCivicLab.

## Creare un nuovo dataset

1. Crea `datasets/<slug>/dataset.yml` seguendo il pattern di `ispra-bathw`
2. Scrivi `sql/clean.sql` — usa le macro toolkit (`cast_int`, `cast_double`, `normalize_string`)
3. Scrivi `sql/mart_*.sql` — 1 file = 1 tabella mart
4. Aggiungi `notes.md` con quirk e decisioni
5. Apri una PR — la CI valida config e struttura

## Tipi di fonte ISPRA

| Tipo | Plugin | Esempio |
|---|---|---|
| SPARQL linked data | `sparql` o `script` + `execute_sparql` | bathw, urban, pest |
| Download diretto (CSV/XLSX) | `http_file` | consumo-suolo |
| REST API JSON | `script` + `requests` | iffi |
| CSV multipli | `script` + `HttpClient` | rmn |

## Dataset SPARQL

Per dataset che usano il plugin `sparql`:
- L'endpoint è sempre `https://dati.isprambiente.it/sparql`
- Le query SPARQL usano l'ontologia `w3id.org/italia/env/onto/top/`
- I label sono bilingue IT/EN — usa `FILTER(lang(?label) = 'it')` per dedup
- Le unità di misura sono URI (`common/unitofmeasure/*`)
- La paginazione è gestita da `pages` e `step` in dataset.yml
- Virtuoso NON accetta `CONTAINS` in FILTER — usa `lang()` o `REGEX`

## Note ISPRA

- Il SPARQL endpoint ha un hard limit di 100K righe per query
- Per dataset voluminosi (>100K righe), usa `script` + paginazione con `execute_sparql`
- I CSV da `rep.isprambiente.it` sono delimitati da `;`
- I label bilingue appaiono 2 volte — tieni solo quelli IT

## Comandi

```bash
make check       # validazione config (preflight)
make run         # esegui tutti i dataset
make seeds       # esegui support datasets (prima dei principali)
make clean       # pulisci output
```

## Standard

- Pipeline: `toolkit` (dataciviclab-toolkit)
- Test: pytest con marcatori (`contract`, `policy`, `regression`, `adapter`, `pure_unit`, `smoke`)
- Lint: ruff
- Type check: mypy

## Struttura

```
datasets/<slug>/
├── dataset.yml       contratto pipeline
├── sql/
│   ├── clean.sql     RAW → CLEAN (usa macro standard)
│   └── mart_*.sql    CLEAN → MART (1 file = 1 tabella)
├── scripts/          fetch script (se type: script)
└── notes.md          quirk, decisioni, deroga

support/<slug>/       anagrafiche usate dai dataset principali
scripts/              utility per probing SPARQL
```

## Link

- [Discussioni](https://github.com/dataciviclab/dataciviclab/discussions)
- [Toolkit docs](https://github.com/dataciviclab/toolkit/tree/main/docs)
- [ADR-001](https://github.com/dataciviclab/.github/blob/main/docs/adr/001-workflow-architecture.md)
