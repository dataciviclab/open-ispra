-- ISPRA Places — CLEAN
-- Place graph ISPRA: NON solo comuni — contiene Italia, regioni, province e comuni.
-- Dedup: una entry per codice ISTAT (alcuni comuni hanno nomi bilingue,
-- es. "Altrei" / "Anterivo/Altrei": teniamo il nome piu' corto).
--
-- `livello` distingue il livello amministrativo dalla lunghezza del codice:
--   1 cifra = italia · 2 = regione · 3 = provincia · 6 = comune
-- Per i soli comuni: WHERE livello = 'comune'.
SELECT
    normalize_string(istat) AS codice_istat,
    normalize_string(name) AS nome,
    CASE length(TRIM(CAST(istat AS VARCHAR)))
        WHEN 1 THEN 'italia'
        WHEN 2 THEN 'regione'
        WHEN 3 THEN 'provincia'
        WHEN 6 THEN 'comune'
        ELSE 'altro'
    END AS livello
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
