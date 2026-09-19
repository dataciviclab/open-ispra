-- ISPRA IFFI — CLEAN
-- Statistiche frane per regione da IdroGEO API

SELECT
    normalize_string(regione) AS regione,
    CAST(cod_regione AS INTEGER) AS cod_regione,
    CAST(nr_frane AS BIGINT) AS nr_frane
FROM raw_input
WHERE regione IS NOT NULL
  AND nr_frane > 0
