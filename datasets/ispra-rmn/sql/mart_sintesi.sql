-- ISPRA RMN — MART Sintesi
-- Media livello mare per stazione × anno (trend level rise)

SELECT
    station_id,
    anno,
    COUNT(*) AS osservazioni,
    ROUND(AVG(livello), 4) AS media_livello,
    ROUND(MIN(livello), 4) AS min_livello,
    ROUND(MAX(livello), 4) AS max_livello,
    ROUND(STDDEV(livello), 4) AS std_livello
FROM clean_input
GROUP BY station_id, anno
ORDER BY station_id, anno
