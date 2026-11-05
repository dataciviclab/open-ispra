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
- `istat`: codice ISTAT — **non sempre un comune**: 6 cifre = comune
  (es. `001272` = Torino), 3 cifre = provincia, 2 cifre = regione
- `indicator`: codice indicatore (es. `ur2242`, `ur77`, `ur13`)
- `year`: anno (es. 2018)

## Anni disponibili
1970-2019 (~50 anni, copertura molto disomogenea tra anni e indicatori)

## Volume
~9.000-26.000 righe/anno. Circa 150 comuni + 125 province + 20 regioni
(il codice `istat` nel URI NON è sempre un comune — vedi `livello` nel clean).

## Quirks
- Il codice ISTAT nel URI è a lunghezza variabile: 6 = comune, 3 = provincia,
  2 = regione. La colonna `livello` nel clean lo esplicita.
- Non sono ~600 comuni: i comuni distinti (6 cifre) sono ~150.
- Diverse unità di misura: n, t, %, si/no, n*10+6, n/h, kg/inh, ecc. —
  una media unica dei valori NON è interpretabile.
- Il dataset è molto ampio: serve paginazione SPARQL (pages=10, step=5000)
