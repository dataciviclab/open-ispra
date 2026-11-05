# Notes — ispra-consumo-suolo

## Stato

Pipeline convertita da **wide → long format** (2026-06-28).
Il clean produce una riga per comune × periodo (12 periodi, ~95.000 righe)
con serie annuale ricostruita per la copertura artificiale.

**Aggiornamento 2026-11-05**: la fonte è passata al rilascio 2026 (serie
2006-2025) sul canale SNPA. Vedi `notes` sotto per URL e foglio.

## Esecuzione

```
cd open-ispra
toolkit run full --config datasets/ispra-consumo-suolo/dataset.yml
```

## Struttura XLSX SNPA/ISPRA

- File: `consumo_suolo_2026_dati_principali-1.xlsx` (canale SNPA, ott. 2026)
- Foglio target: `Comuni_2006_2025`
- 42 colonne raw: PRO_COM, Nome_Comune, Nome_Provincia, Nome_Regione,
  incrementi netti/lordi + ripristini per 12 periodi, stock 2025 (ha e %)
- Il precedente `consumo_di_suolo_estratto_dati_2025_anni_2006_2024.xlsx`
  (isprambiente.gov.it, foglio `Comuni_2006_2024`) si ferma al 2024

## Schema clean (formato long, 11 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| pro_com | VARCHAR | Codice ISTAT comune (6 cifre) |
| comune | VARCHAR | Nome comune |
| provincia | VARCHAR | Nome provincia |
| regione | VARCHAR | Nome regione |
| periodo | VARCHAR | Periodo di riferimento (es. "2015-2016") |
| anno | INTEGER | Anno finale del periodo |
| incremento_netto_ha | DOUBLE | Incremento netto nel periodo (ha) |
| incremento_lordo_ha | DOUBLE | Incremento lordo nel periodo (ha) |
| ripristino_ha | DOUBLE | Aree ripristinate nel periodo (ha) |
| stock_ha | DOUBLE | Suolo consumato cumulato a fine periodo (ha) |
| stock_pct | DOUBLE | Suolo consumato % a fine periodo |

## Periodi disponibili

| Periodo | Anno fine | Tipo | Note |
|---|---|---|---|
| 2006-2012 | 2012 | Pluriennale | Stock ricostruito |
| 2012-2015 | 2015 | Pluriennale | Stock ricostruito |
| 2015-2016 | 2016 | Annuale | Stock ricostruito |
| 2016-2017 | 2017 | Annuale | Stock ricostruito |
| 2017-2018 | 2018 | Annuale | Stock ricostruito |
| 2018-2019 | 2019 | Annuale | Stock ricostruito |
| 2019-2020 | 2020 | Annuale | Stock ricostruito |
| 2020-2021 | 2021 | Annuale | Stock ricostruito |
| 2021-2022 | 2022 | Annuale | Stock ricostruito |
| 2022-2023 | 2023 | Annuale | Stock ricostruito |
| 2023-2024 | 2024 | Annuale | Stock ricostruito |
| 2024-2025 | 2025 | Annuale | Stock reale (fonte SNPA/ISPRA) |

## Ricostruzione stock

stock_2025 e stock_pct_2025 sono gli unici valori direttamente dal file ISPRA.
Per gli anni precedenti, stock_ha viene ricostruito come:

```
stock_ha(anno_N) = stock_ha_2025 - SUM(incrementi_netto dei periodi con anno > N)
```

La superficie comunale in ettari è calcolata come:
```
sup_ha = stock_ha_2025 / stock_pct_2025 * 100
```

## Confronto con SuoloData.it (Milano)

| Fonte | 2016 | 2024 | Δ |
|---|---|---|---|
| SuoloData.it | 58,3% | 58,9% | +0,6 pp |
| Nostra ricostruzione | 58,11% | 58,72% | +0,61 pp |

Differenza ~0,2 pp probabilmente perché SuoloData.it usa direttamente i dati
di stock annuali dal file XLSX mentre noi ricostruiamo dagli incrementi netti.

## Note tecniche

- I valori ISPRA usano la virgola come separatore decimale — gestito con
  REPLACE(',', '.') prima del TRY_CAST.
- stock_2025 e stock_pct_2025 sono gli unici valori direttamente dal file;
  gli stock precedenti sono ricostruiti.
- I periodi 2006-2012 e 2012-2015 sono pluriennali — non confrontabili
  direttamente con i periodi annuali senza normalizzazione.
- Il filtro `incremento_netto_ha IS NOT NULL` in clean.sql esclude i comuni
  senza dati per un dato periodo (raro, ma presente per alcuni comuni di
  nuova istituzione).
