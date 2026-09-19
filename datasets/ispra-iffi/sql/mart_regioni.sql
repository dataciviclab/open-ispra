-- ISPRA IFFI — MART Regioni
-- Statistiche frane per regione con quota % sul totale
SELECT
    regione,
    cod_regione,
    nr_frane,
    ROUND(100.0 * nr_frane / (SELECT SUM(nr_frane) FROM clean_input), 1) AS pct_frane_nazionali
FROM clean_input
ORDER BY nr_frane DESC
