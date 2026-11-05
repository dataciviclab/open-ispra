-- ISPRA Pesticidi Stazioni — CLEAN

SELECT
    cast_int(year) AS anno,
    normalize_string(station_id) AS station_id,
    cast_double(lat) AS lat,
    cast_double(lon) AS lon
FROM raw_input
WHERE station_id IS NOT NULL
  AND lat IS NOT NULL
  AND lon IS NOT NULL
