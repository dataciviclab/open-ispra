-- ISPRA Balneazione — MART Sintesi
-- Conteggi per stato di qualità (singolo anno)
SELECT
    anno,
    COUNT(*) AS totale_siti,
    SUM(CASE WHEN valore = 1 THEN 1 ELSE 0 END) AS eccellente,
    SUM(CASE WHEN valore = 2 THEN 1 ELSE 0 END) AS buona,
    SUM(CASE WHEN valore = 3 THEN 1 ELSE 0 END) AS sufficiente,
    SUM(CASE WHEN valore = 4 THEN 1 ELSE 0 END) AS scadente,
    SUM(CASE WHEN valore = 0 THEN 1 ELSE 0 END) AS non_classificato,
    ROUND(100.0 * SUM(CASE WHEN valore IN (1, 2) THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_ottima,
    ROUND(100.0 * SUM(CASE WHEN valore IN (1, 2, 3) THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_almeno_sufficiente
FROM clean_input
WHERE indicatore = 'quality'
GROUP BY anno
