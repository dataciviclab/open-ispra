-- ISPRA Places — CLEAN
-- Anagrafica comuni dal place graph SPARQL
-- Dedup: tengiamo solo una entry per codice ISTAT
-- (alcuni comuni hanno nomi bilingue es. "Altrei" / "Anterivo/Altrei")
SELECT
    istat AS codice_istat,
    normalize_string(name) AS nome
FROM (
    SELECT
        istat,
        name,
        ROW_NUMBER() OVER (
            PARTITION BY istat
            ORDER BY LENGTH(name) ASC, name
        ) AS rn
    FROM raw_input
    WHERE istat IS NOT NULL
      AND name IS NOT NULL
)
WHERE rn = 1
