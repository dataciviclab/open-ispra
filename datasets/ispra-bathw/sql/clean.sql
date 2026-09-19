-- ISPRA Balneazione — CLEAN
-- Parse URI, cast value
-- La query SPARQL filtra già i label italiani (lang = 'it')
-- URI pattern: .../bathw/indicator/{code}_{site_id}_{indicator}_{year}

SELECT
    -- Parse URI: estrai codice sito e indicatore
    -- Pattern: .../bathw/indicator/{code}_{site_id}_{indicator}_{year}
    REGEXP_EXTRACT(uri, '/indicator/([^_]+_[^_]+)_([a-z]+)_', 1) AS codice_sito,
    REGEXP_EXTRACT(uri, '/indicator/[^_]+_[^_]+_([a-z]+)_', 1) AS indicatore,
    CAST(REGEXP_EXTRACT(uri, '_([0-9]{4})$', 1) AS INTEGER) AS anno,
    CAST(value AS DOUBLE) AS valore,
    CASE
        WHEN uom LIKE '%quality%' THEN 'qualita_0_4'
        WHEN uom LIKE '%number%' THEN 'numero'
        ELSE REGEXP_EXTRACT(uom, '/([^/]+)$', 1)
    END AS unita_misura
FROM raw_input
WHERE value IS NOT NULL
  AND TRY_CAST(value AS DOUBLE) IS NOT NULL
