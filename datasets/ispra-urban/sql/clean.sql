-- ISPRA Urban — CLEAN
-- Parse URI, cast value, multi-anno
-- Lo script fornisce gia' la colonna 'year'
-- URI pattern: .../urban/indicator/00201_{istat}_{indicator}_{year}

SELECT
    -- Parse URI: estrai codice ISTAT comune e indicatore
    REGEXP_EXTRACT(uri, '/indicator/00201_([0-9]+)_', 1) AS codice_istat,
    REGEXP_EXTRACT(uri, '_([a-z]+[0-9]+)_', 1) AS indicatore,
    CAST(year AS INTEGER) AS anno,
    CAST(value AS DOUBLE) AS valore,
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
  AND TRY_CAST(value AS DOUBLE) IS NOT NULL
