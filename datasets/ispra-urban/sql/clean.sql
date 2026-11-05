-- ISPRA Urban — CLEAN
-- Parse URI, cast value, multi-anno
-- Lo script fornisce gia' la colonna 'year'
-- URI pattern: .../urban/indicator/00201_{istat}_{indicator}_{year}
--
-- ATTENZIONE: `codice_istat` NON e' sempre un comune — l'indicatore puo'
-- essere regionale (2 cifre) o provinciale (3 cifre). `livello` lo esplicita:
--   2 cifre = regione · 3 = provincia · 6 = comune

WITH base AS (
    SELECT
        -- Parse URI: estrai codice ISTAT e indicatore
        REGEXP_EXTRACT(uri, '/indicator/00201_([0-9]+)_', 1) AS codice_istat,
        REGEXP_EXTRACT(uri, '_([a-z]+[0-9]+)_', 1) AS indicatore,
        cast_int(year) AS anno,
        cast_double(value) AS valore,
        CASE
            WHEN uom LIKE '%n*10+6%' THEN 'milioni'
            WHEN uom LIKE '%n*10+3%' THEN 'migliaia'
            WHEN uom LIKE '%t*10+3%' THEN 'migliaia_tonnellate'
            WHEN uom LIKE '%percentage%' THEN 'percentuale'
            WHEN uom LIKE '%0=no1=yes%' THEN 'si_no'
            WHEN uom LIKE '%n/h%' THEN 'n_per_ettaro'
            WHEN uom LIKE '%n/m2%' THEN 'n_per_m2'
            WHEN uom LIKE '%n/inh%' THEN 'n_per_abitante'
            WHEN uom LIKE '%kg/inh%' THEN 'kg_per_abitante'
            WHEN uom LIKE '%n' THEN 'numero'
            WHEN uom LIKE '%t' THEN 'tonnellate'
            WHEN uom LIKE '%ha' THEN 'ettari'
            WHEN uom LIKE '%m2' THEN 'metri_quadri'
            ELSE REGEXP_EXTRACT(uom, '/([^/]+)$', 1)
        END AS unita_misura
    FROM raw_input
    WHERE value IS NOT NULL
      AND cast_double(value) IS NOT NULL
)
SELECT
    *,
    CASE length(codice_istat)
        WHEN 2 THEN 'regione'
        WHEN 3 THEN 'provincia'
        WHEN 6 THEN 'comune'
        ELSE 'altro'
    END AS livello
FROM base
