-- ISPRA Urban — MART Sintesi
-- Statistiche generali per anno
SELECT
    anno,
    COUNT(DISTINCT codice_istat) AS totale_comuni,
    COUNT(*) AS totale_indicatori,
    COUNT(DISTINCT indicatore) AS tipi_indicatori,
    ROUND(AVG(valore), 2) AS media_generale,
    SUM(CASE WHEN valore > 0 THEN 1 ELSE 0 END) AS valori_positivi,
    SUM(CASE WHEN valore = 0 THEN 1 ELSE 0 END) AS valori_zero
FROM clean_input
GROUP BY anno
ORDER BY anno
