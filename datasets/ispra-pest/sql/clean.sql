-- ISPRA Pesticidi — CLEAN
-- Concentrazioni pesticidi nelle acque sotterranee

SELECT
    CAST(year AS INTEGER) AS anno,
    normalize_string(station_id) AS station_id,
    normalize_string(cas_number) AS cas_number,
    CAST(value AS DOUBLE) AS valore,
    CASE
        WHEN uom LIKE '%ug/l%' THEN 'microgrammi_per_litro'
        WHEN uom LIKE '%ng/l%' THEN 'nanogrammi_per_litro'
        WHEN uom LIKE '%number%' THEN 'numero'
        WHEN uom LIKE '%percentage%' THEN 'percentuale'
        ELSE REGEXP_EXTRACT(uom, '/([^/]+)$', 1)
    END AS unita_misura
FROM raw_input
WHERE station_id IS NOT NULL
  AND cas_number IS NOT NULL
  AND year IS NOT NULL
