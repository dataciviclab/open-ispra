"""Ambiente Urbano — Deep dive: qualità ambientale dei comuni."""

import plotly.graph_objects as go
import streamlit as st
from sources import fmt_num, load_mart_urban

st.title("🏙️ Ambiente Urbano")

# ── Warning: colotta 2019 ───────────────────────────────────────────────
st.warning(
    "⚠️ **Dataset ridisegnato nel 2019**: il numero di indicatori è crollato "
    "da 269 (2017) a 25 (2019). I dati mostrati sono **solo fino al 2018** "
    "per coerenza temporale."
)

# ── Load data (filter <= 2018) ──────────────────────────────────────────
df = load_mart_urban("mart_sintesi")

if df.empty:
    st.warning("Nessun dato disponibile.")
    st.stop()

df = df.sort_values("anno")
df = df[df["anno"] <= 2018]

if df.empty:
    st.warning("Nessun dato disponibile (fino al 2018).")
    st.stop()

# ── KPI Row ──────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

latest = df.iloc[-1]
k1.metric("Comuni monitorati", fmt_num(int(latest["totale_comuni"])))
k2.metric("Indicatori totali", fmt_num(int(latest["totale_indicatori"])))
k3.metric("Tipi indicatore", fmt_num(int(latest["tipi_indicatori"])))
k4.metric(
    "Periodo",
    f"{int(df.iloc[0]['anno'])}–{int(latest['anno'])}",
    help=f"{len(df)} anni di dati (fino al 2018)",
)

st.divider()

# ── Trend comuni monitorati ─────────────────────────────────────────────
st.subheader("Evoluzione copertura")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["anno"], y=df["totale_comuni"],
    name="Comuni monitorati", line=dict(color="#2563eb", width=2),
    mode="lines+markers",
))
fig.update_layout(
    height=300, margin={"t": 20, "b": 40},
    yaxis_title="N° comuni", xaxis_title="Anno",
)
st.plotly_chart(fig, width="stretch")

st.divider()

# ── Trend indicatori ────────────────────────────────────────────────────
st.subheader("Evoluzione indicatori")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df["anno"], y=df["tipi_indicatori"],
    name="Tipi indicatore", line=dict(color="#059669", width=2),
    mode="lines+markers",
))
fig2.add_trace(go.Scatter(
    x=df["anno"], y=df["totale_indicatori"] / df["totale_comuni"].replace(0, 1),
    name="Media indicatori/comune", line=dict(color="#d97706", width=2),
    mode="lines+markers", yaxis="y2",
))
fig2.update_layout(
    height=300, margin={"t": 20, "b": 40},
    yaxis_title="Tipi indicatore", xaxis_title="Anno",
    yaxis2=dict(title="Media ind./comune", overlaying="y", side="right"),
)
st.plotly_chart(fig2, width="stretch")

st.divider()

# ── Tabella ──────────────────────────────────────────────────────────────
st.subheader("Riepilogo annuale")

st.dataframe(
    df[["anno", "totale_comuni", "totale_indicatori", "tipi_indicatori", "media_generale"]]
    .rename(columns={
        "anno": "Anno", "totale_comuni": "Comuni",
        "totale_indicatori": "Indicatori", "tipi_indicatori": "Tipi",
        "media_generale": "Media",
    }),
    use_container_width=True, hide_index=True,
)

st.caption("Dati: ISPRA — Qualità Ambientale Urbana (fino al 2018) · Fonte: open-ispra")
