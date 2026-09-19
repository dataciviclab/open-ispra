# ispra-urban — Note

## Fonte
- Endpoint SPARQL: `https://dati.isprambiente.it/sparql`
- Graph: `https://w3id.org/italia/env/ld/urban/{year}/`
- Ontologia: `w3id.org/italia/env/onto/top/`

## Struttura RDF
Ogni indicatore è un nodo con:
- `rdfs:label` bilingue (IT+EN) — filtrato con `lang(?label) = 'it'`
- `top:hasValue` → valueNode → `top:value` (stringa numerica)
- `top:hasUnitOfMeasure` → UoM URI

## URI pattern
```
.../urban/indicator/00201_{istat}_{indicator}_{year}
```
- `00201`: prefisso catalogo
- `istat`: codice ISTAT comune (6 cifre, es. `001272` = Torino)
- `indicator`: codice indicatore (es. `ur2242`, `ur77`, `ur13`)
- `year`: anno (es. 2018)

## Anni disponibili
1970-2019 (~50 anni di serie storica)

## Volume
~22.270 indicatori per anno, ~600 comuni capoluogo

## Quirks
- I comuni sono ~600 (capoluogo + grandi città)
- L'ISTAT code nel URI è a 6 cifre (codice comune ISTAT)
- Diverse unità di misura: n, t, %, si/no, n*10+6, n/h, kg/inh, ecc.
- Il dataset è molto ampio: serve paginazione SPARQL (pages=10, step=5000)
