# Notes — ispra-places

## Cosa è

Place graph ISPRA dal graph `https://w3id.org/italia/env/ld/place/`
(endpoint SPARQL `https://dati.isprambiente.it/sparql`).

**Non è solo un'anagrafica comuni**: contiene tutti i "places" con codice
ISTAT — Italia, regioni, province e comuni. Il campo `livello` (derivato
dalla lunghezza del codice) li distingue:

| `livello` | cifre | esempi | n (2026-11) |
|---|---|---|---|
| `italia` | 1 | `0` | 1 |
| `regione` | 2 | `01`…`20` | 20 |
| `provincia` | 3 | `001`…`133` | 133 |
| `comune` | 6 | `001001` (Torino), `001156` | 9.376 |

Per i soli comuni: `WHERE livello = 'comune'`.

## Codici ISTAT: formato

I codici sono **6 cifre zero-padded** (`001001`), non interi. **Non
normalizzare a intero**: si perdono gli zeri iniziali.

⚠️ **Incoerenza cross-dataset (da risolvere a livello org)**: lo stesso
codice comune è pubblicato in formati diversi nel Lab — qui `001001`
(padded 6), in `ispra_consumo_suolo` `1001` (unpadded), in
`rifiuti-urbani` `01001001` (8 char). Un JOIN diretto consumo-suolo ↔ places
matcha solo ~8% delle righe.

## Comuni storici

I 9.376 "comuni" includono **comuni soppressi/fusi**, non solo quelli in
vita (ISTAT corrente ~7.896). Non abbiamo una lista di riferimento ISTAT
nel dataset: il flag corrente/storico non è derivabile qui.

## Dedup

Una entry per `codice_istat`. Alcuni comuni hanno nomi bilingue
(es. `Altrei` / `Anterivo/Altrei`): si tiene il nome più corto.

## Esecuzione

```bash
cd open-ispra
toolkit run --config support/ispra-places/dataset.yml
```
