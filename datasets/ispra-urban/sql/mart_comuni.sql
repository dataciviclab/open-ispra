-- ISPRA Urban — MART Comuni
-- Conteggi indicatori per comune
SELECT
    codice_istat,
    anno,
    COUNT(*) AS totale_indicatori,
    SUM(CASE WHEN valore > 0 THEN 1 ELSE 0 END) AS indicatori_positivi,
    ROUND(AVG(valore), 2) AS media_valori,
    COUNT(DISTINCT indicatore) AS indicatori_diversi
FROM clean_input
GROUP BY codice_istat, anno
