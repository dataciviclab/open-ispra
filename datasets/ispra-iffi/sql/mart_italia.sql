-- ISPRA IFFI — MART Italia
-- Totali nazionali
SELECT
    SUM(nr_frane) AS totale_frane,
    COUNT(*) AS totale_regioni,
    ROUND(AVG(nr_frane), 0) AS media_frane_per_regione,
    MAX(nr_frane) AS max_frane_regione,
    MIN(nr_frane) AS min_frane_regione
FROM clean_input
