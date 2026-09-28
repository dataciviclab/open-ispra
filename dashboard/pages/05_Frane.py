"""Frane — Deep dive: inventario fenomeni franosi."""

import plotly.graph_objects as go
import streamlit as st
from sources import fmt_num, load_mart_iffi

st.title("⛰️ Frane in Italia")

# ── Load data ────────────────────────────────────────────────────────────
df_italia = load_mart_iffi("mart_italia")
df_regioni = load_mart_iffi("mart_regioni")

if df_italia.empty or df_regioni.empty:
    st.warning("Nessun dato disponibile.")
    st.stop()

# ── KPI Row ──────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

italia = df_italia.iloc[0]
k1.metric("Frane totali", fmt_num(int(italia["totale_frane"])))
k2.metric("Regioni", fmt_num(int(italia["totale_regioni"])))
k3.metric("Media per regione", f"{italia['media_frane_per_regione']:.0f}")

max_row = df_regioni.loc[df_regioni["nr_frane"].idxmax()]
k4.metric("Regione con più frane", max_row["regione"], f"{int(max_row['nr_frane']):,}".replace(",", "."))

st.divider()

# ── Bar chart regioni ───────────────────────────────────────────────────
st.subheader("Frane per regione")

df_sorted = df_regioni.sort_values("nr_frane", ascending=True)

fig = go.Figure(go.Bar(
    x=df_sorted["nr_frane"], y=df_sorted["regione"],
    orientation="h", marker_color="#d97706",
    text=df_sorted["pct_frane_nazionali"].apply(lambda x: f"{x:.1f}%"),
    textposition="outside",
))
fig.update_layout(
    height=550, margin={"t": 20, "b": 40, "l": 150},
    xaxis_title="N° frane",
)
st.plotly_chart(fig, width="stretch")

st.divider()

# ── Tabella ──────────────────────────────────────────────────────────────
st.subheader("Dettaglio regioni")

st.dataframe(
    df_regioni.sort_values("nr_frane", ascending=False)
    .rename(columns={
        "regione": "Regione", "nr_frane": "N° frane",
        "pct_frane_nazionali": "% nazionale",
    }),
    width="stretch", hide_index=True,
)

st.caption("Dati: ISPRA — Inventario Fenomeni Franosi in Italia (IFFI) · Fonte: open-ispra")
