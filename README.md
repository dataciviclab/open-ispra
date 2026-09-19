# open-ispra

Repo dati ISPRA (Istituto Superiore per la Protezione e la Ricerca Ambientale) nel DataCivicLab.

## Dataset

| Dataset | Fonte | Formato | Stato |
|---|---|---|---|
| `ispra-bathw` | SPARQL linked data | RDF→CSV | 🟢 Operativo |
| `ispra-urban` | SPARQL linked data | RDF→CSV | 🟢 Operativo |
| `ispra-iffi` | IdroGEO REST API | JSON→CSV | 🟢 Operativo |
| `ispra-places` | SPARQL linked data | RDF→CSV | 🟢 Support |

### Risultati

| Dataset | Righe | Dettaglio |
|---|---|---|
| `ispra_places` | 9.530 | Anagrafica comuni italiani |
| `ispra_bathw` | 5.538 | Siti balneazione, 96.2% qualità eccellente/buona |
| `ispra_urban` | 22.270 | 245 comuni, 225 tipi indicatore |
| `ispra_iffi` | 20 | 689.201 frane, Lombardia top (20.6%) |

## Fonti dati ISPRA

| Endpoint | URL | Protocollo |
|---|---|---|
| Linked Open Data | `dati.isprambiente.it/sparql` | SPARQL |
| Catasto Rifiuti | `catasto-rifiuti.isprambiente.it` | CSV |
| Indicatori Ambientali | `indicatoriambientali.isprambiente.it` | XLS |
| Consumo Suolo | `isprambiente.gov.it` | XLSX |
| IdroGEO | `idrogeo.isprambiente.it` | REST API |

## Comandi

```bash
make check       # validazione config
make seeds       # esegui support dataset
make run         # esegui tutti i dataset
make run-all     # seeds + run
make clean       # pulisci output
```

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
