-- ISPRA IFFI — CLEAN
-- Statistiche frane per regione da IdroGEO API

SELECT
    normalize_string(regione) AS regione,
    cast_int(cod_regione) AS cod_regione,
    cast_bigint(nr_frane) AS nr_frane
FROM raw_input
WHERE regione IS NOT NULL
  AND nr_frane > 0
