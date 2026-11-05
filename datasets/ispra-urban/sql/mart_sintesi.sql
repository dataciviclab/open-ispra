-- ISPRA Urban — MART Sintesi
-- Statistiche generali per anno.
--
-- `totale_comuni` conta SOLO il livello comune (prima includeva anche
-- regioni e province, gonfiando il numero). I conteggi per gli altri
-- livelli sono espliciti. Non c'e' una media generale dei `valore`:
-- gli indicatori hanno unita' diverse (percentuali, conteggi, per-capita),
-- quindi una media unica non e' interpretabile.
SELECT
    anno,
    COUNT(DISTINCT codice_istat) FILTER (WHERE livello = 'comune') AS totale_comuni,
    COUNT(DISTINCT codice_istat) FILTER (WHERE livello = 'provincia') AS totale_province,
    COUNT(DISTINCT codice_istat) FILTER (WHERE livello = 'regione') AS totale_regioni,
    COUNT(*) AS totale_indicatori,
    COUNT(DISTINCT indicatore) AS tipi_indicatori,
    SUM(CASE WHEN valore > 0 THEN 1 ELSE 0 END) AS valori_positivi,
    SUM(CASE WHEN valore = 0 THEN 1 ELSE 0 END) AS valori_zero
FROM clean_input
GROUP BY anno
ORDER BY anno
