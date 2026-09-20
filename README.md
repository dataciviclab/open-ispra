# open-ispra

Dati ambientali dell'Istituto Superiore per la Protezione e la Ricerca Ambientale — acque, suolo, mari, pesticidi, frane — in formato aperto e pronto per l'analisi.

## Perché questi dati

ISPRA coordina il Sistema Nazionale di Protezione dell'Ambiente, ma i dati ambientali italiani sono distribuiti su piattaforme eterogenee: SPARQL endpoint, XLSX, CSV, REST API. Questo repo li raccoglie, normalizza e rende interrogabili in un unico posto.

## Cosa contengono

| Dataset | Righe | Periodo | Copertura | Fonte |
|---|---|---|---|---|
| `rmn` — Livelli mare | 29.2M | 2010-2022 | 36 stazioni costiere | SPARQL + CSV |
| `pest` — Pesticidi acque | 10.8M | 2018-2021 | 7.541 stazioni, 492 sostanze | SPARQL |
| `urban` — Qualità urbana | 201K | 1970-2019 | 296 comuni, 225 indicatori | SPARQL |
| `bathw` — Balneazione | 173K | 1990-2024 | 5.862 siti | SPARQL |
| `consumo-suolo` — Suolo consumato | 87K | 2012-2024 | 7.896 comuni | XLSX |
| `iffi` — Frane Italia | 20 | Snapshot | 689K frane, 20 regioni | REST API |

## Esempi di domande

- Come cambiano i livelli del mare lungo le coste italiane? (**rmn**)
- Quante stazioni di monitoraggio rilevano pesticidi nelle acque sotterranee? (**pest**)
- Quali comuni hanno i tassi di consumo suolo più alti? (**consumo-suolo**)
- Com'è la qualità dell'acqua di balneazione nella mia zona? (**bathw**)
- Quante frane ci sono nella mia regione? (**iffi**)

## Come accedere

### DuckDB (consigliato)

```python
import duckdb
con = duckdb.connect()
# Esempio: trend livello mare Venezia
con.execute("""
    SELECT anno, ROUND(AVG(livello), 4) AS media
    FROM 'out/data/mart/ispra_rmn/2023/mart_sintesi.parquet'
    WHERE station_id = 'venezia'
    GROUP BY anno ORDER BY anno
""").fetchdf()
```

### MCP (toolkit)

```
toolkit_dataset(action='find', query='ispra')
toolkit_query(action='run', datasets=['ispra_bathw'], sql='SELECT * FROM clean LIMIT 10')
```

### Parquet diretto

I file clean e mart sono in `out/data/` in formato Parquet, leggibili da qualsiasi tool (pandas, Polars, DuckDB, DataExplorer).

## Approfondimenti

- [Discussioni del Lab](https://github.com/dataciviclab/dataciviclab/discussions)
- [Dataset ISPRA nel Source Observatory](https://github.com/dataciviclab/source-observatory)

## Partecipa

- **Hai trovato un dato mancante?** [Apri una Discussion](https://github.com/dataciviclab/dataciviclab/discussions)
- **Vuoi aggiungere un dataset ISPRA?** Segui la guida in `CONTRIBUTING.md`
- **Hai un'analisi su questi dati?** Pubblicala in `analysis/dataciviclab/analisi/`

## Struttura

```
datasets/<slug>/
├── dataset.yml       contratto pipeline
├── sql/
│   ├── clean.sql     RAW → CLEAN
│   └── mart_*.sql    CLEAN → MART
├── scripts/          fetch script (se type: script)
└── notes.md

support/<slug>/       anagrafiche usate dai dataset principali
scripts/              utility per probing SPARQL
```

## Licenza

Dati: CC BY 4.0 (fonti ISPRA). Codice: MIT.
