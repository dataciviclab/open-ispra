-- ISPRA RMN — CLEAN
-- Rete Mareografica Nazionale: livelli marini orari

SELECT
    normalize_string(station_id) AS station_id,
    cast_int(year) AS anno,
    cast_int(month) AS mese,
    -- Parse timestamp: formato ISPRA "2014-03-01 00:00:00" o simile
    TRY_CAST(timestamp_utc AS TIMESTAMP) AS timestamp_utc,
    -- Level in metri (o unita' del sensore), formato italiano (virgola)
    normalize_italian_number(level) AS livello
FROM raw_input
WHERE station_id IS NOT NULL
  AND year IS NOT NULL
  AND level IS NOT NULL
  AND normalize_italian_number(level) IS NOT NULL
