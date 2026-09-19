# open-ispra

Repo dati ISPRA (Istituto Superiore per la Protezione e la Ricerca Ambientale) nel DataCivicLab.

## Dataset

| Dataset | Fonte | Formato | Stato |
|---|---|---|---|
| `ispra-bathw` | SPARQL linked data | RDF→CSV | 🟢 Pilot |
| `ispra-places` | SPARQL linked data | RDF→CSV | 🟢 Support |
| `ispra-ru-base` | catasto-rifiuti CSV | CSV | 🟡 Da migrare |
| `ispra-ru-costi-kg` | catasto-rifiuti CSV | CSV | 🟡 Da migrare |
| `ispra-ru-costi-procapite` | catasto-rifiuti CSV | CSV | 🟡 Da migrare |
| `ispra-consumo-suolo` | XLSX download | XLSX | 🟡 Da migrare |
| `ispra-emissioni-ghg` | XLS download | XLS | 🟡 Da migrare |

## Fonti dati ISPRA

| Endpoint | URL | Protocollo |
|---|---|---|
| Linked Open Data | `dati.isprambiente.it/sparql` | SPARQL |
| Catasto Rifiuti | `catasto-rifiuti.isprambiente.it` | CSV |
| Indicatori Ambientali | `indicatoriambientali.isprambiente.it` | XLS |
| Consumo Suolo | `isprambiente.gov.it` | XLSX |
| IdroGEO | `idrogeo.isprambiente.it` | CSV/SHP/GeoJSON |

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
└── notes.md

support/<slug>/       anagrafiche usate dai dataset principali
scripts/              utility per probing SPARQL
```
