-- ISPRA Urban — MART Comuni
-- Conteggi indicatori per entita' (comune/regione/provincia) x anno.
-- La colonna `livello` distingue il livello amministrativo: per i soli
-- comuni filtra livello = 'comune'.
SELECT
    codice_istat,
    livello,
    anno,
    COUNT(*) AS totale_indicatori,
    SUM(CASE WHEN valore > 0 THEN 1 ELSE 0 END) AS indicatori_positivi,
    COUNT(DISTINCT indicatore) AS indicatori_diversi
FROM clean_input
GROUP BY codice_istat, livello, anno
