-- ISPRA RMN — MART Stazioni
-- Statistiche per stazione: copertura, media, min/max

SELECT
    station_id,
    COUNT(*) AS totale_osservazioni,
    COUNT(DISTINCT anno) AS anni_attivi,
    MIN(anno) AS primo_anno,
    MAX(anno) AS ultimo_anno,
    ROUND(AVG(livello), 4) AS media_livello,
    ROUND(MIN(livello), 4) AS min_livello,
    ROUND(MAX(livello), 4) AS max_livello,
    ROUND(STDDEV(livello), 4) AS std_livello
FROM clean_input
GROUP BY station_id
ORDER BY station_id
