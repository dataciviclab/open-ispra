-- ISPRA RMN — CLEAN
-- Rete Mareografica Nazionale: livelli marini orari

SELECT
    TRIM(station_id) AS station_id,
    CAST(year AS INTEGER) AS anno,
    CAST(month AS INTEGER) AS mese,
    -- Parse timestamp: formato ISPRA "2014-03-01 00:00:00" o simile
    TRY_CAST(timestamp_utc AS TIMESTAMP) AS timestamp_utc,
    -- Level in metri (o unita' del sensore)
    TRY_CAST(REPLACE(TRIM(level), ',', '.') AS DOUBLE) AS livello
FROM raw_input
WHERE station_id IS NOT NULL
  AND year IS NOT NULL
  AND level IS NOT NULL
  AND TRY_CAST(REPLACE(TRIM(level), ',', '.') AS DOUBLE) IS NOT NULL
