-- ISPRA Pesticidi Stazioni — CLEAN

SELECT
    CAST(year AS INTEGER) AS anno,
    normalize_string(station_id) AS station_id,
    TRY_CAST(lat AS DOUBLE) AS lat,
    TRY_CAST(lon AS DOUBLE) AS lon
FROM raw_input
WHERE station_id IS NOT NULL
  AND lat IS NOT NULL
  AND lon IS NOT NULL
