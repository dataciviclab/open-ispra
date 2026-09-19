# Contribuire a open-ispra

Repo multi-dataset per i dati ISPRA nel DataCivicLab.

## Creare un nuovo dataset

1. Crea `datasets/<slug>/dataset.yml` seguendo il pattern di `ispra-bathw`
2. Scrivi `sql/clean.sql` — usa le macro toolkit (`cast_int`, `cast_double`, `normalize_string`)
3. Scrivi `sql/mart_*.sql` — 1 file = 1 tabella mart
4. Aggiungi `notes.md` con quirk e decisioni
5. Apri una PR — la CI valida config e struttura

## Dataset SPARQL

Per dataset che usano il plugin `sparql`:
- L'endpoint è sempre `https://dati.isprambiente.it/sparql`
- Le query SPARQL usano l'ontologia `w3id.org/italia/env/onto/top/`
- I label sono bilingue IT/EN — dedup in clean.sql
- Le unità di misura sono URI (`common/unitofmeasure/*`)
- La paginazione è gestita da `pages` e `step` in dataset.yml

## Standard

- Pipeline: `toolkit` (dataciviclab-toolkit)
- Test: pytest con marcatori (`contract`, `policy`, `regression`)
- Lint: ruff
- Type check: mypy
