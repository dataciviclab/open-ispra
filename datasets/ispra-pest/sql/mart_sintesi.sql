-- ISPRA Pesticidi — MART Sintesi
-- Statistiche generali per anno

SELECT
    anno,
    COUNT(DISTINCT station_id) AS stazioni,
    COUNT(DISTINCT cas_number) AS sostanze,
    COUNT(*) AS totale_misurazioni,
    SUM(CASE WHEN valore > 0 THEN 1 ELSE 0 END) AS rilevazioni_positive,
    ROUND(100.0 * SUM(CASE WHEN valore > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_positive,
    ROUND(AVG(CASE WHEN valore > 0 THEN valore END), 4) AS media_positivi
FROM clean_input
GROUP BY anno
ORDER BY anno
