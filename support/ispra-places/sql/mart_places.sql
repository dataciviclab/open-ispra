-- ISPRA Places — MART
-- Place graph (passthrough da clean): Italia, regioni, province e comuni.
-- Per i soli comuni filtra livello = 'comune'.
SELECT
    codice_istat,
    nome,
    livello
FROM clean_input
