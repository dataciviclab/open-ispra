"""Consumo Suolo — Deep dive: consumo di suolo in Italia."""

import plotly.graph_objects as go
import streamlit as st
from sources import fmt_num, load_mart_consumo_suolo

st.title("🏗️ Consumo di Suolo")

# ── Load data ────────────────────────────────────────────────────────────
df_cs = load_mart_consumo_suolo("mart_comuni")
df_trend = load_mart_consumo_suolo("mart_sintesi")

if df_cs.empty or df_trend.empty:
    st.warning("Nessun dato disponibile.")
    st.stop()

# ── Filters ──────────────────────────────────────────────────────────────
periodi = sorted(df_cs["periodo"].unique())
periodo = st.selectbox("Periodo", periodi, index=len(periodi) - 1)

df_p = df_cs[df_cs["periodo"] == periodo]

# ── KPI Row ──────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

k1.metric("Comuni monitorati", fmt_num(len(df_p)))
k2.metric(
    "Stock medio nazionale",
    f"{df_p['stock_pct'].mean():.1f}%",
)
k3.metric(
    "Incremento netto totale",
    f"{df_p['incremento_netto_ha'].sum():,.0f} ha".replace(",", "."),
)
k4.metric(
    "Ripristino totale",
    f"{df_p['ripristino_ha'].sum():,.0f} ha".replace(",", "."),
)

st.divider()

# ── Fascia consumo suolo per regione ────────────────────────────────────
st.subheader("Fascia consumo suolo per regione")

df_regione = (
    df_p.groupby("regione")
    .agg(
        stock_pct_medio=("stock_pct", "mean"),
        inc_netto_totale=("incremento_netto_ha", "sum"),
    )
    .reset_index()
    .sort_values("stock_pct_medio", ascending=False)
)

fig = go.Figure(go.Bar(
    x=df_regione["regione"], y=df_regione["stock_pct_medio"],
    marker_color="#d97706",
))
fig.update_layout(
    height=400, margin={"t": 20, "b": 40},
    yaxis_title="Stock medio (%)", xaxis_title="",
)
st.plotly_chart(fig, width="stretch")

st.divider()

# ── Trend nazionale ─────────────────────────────────────────────────────
st.subheader("Trend nazionale — stock e incremento")

df_naz = df_trend[df_trend["livello"] == "nazionale"].sort_values("anno")

col_left, col_right = st.columns(2)

with col_left:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df_naz["anno"], y=df_naz["avg_stock_pct"],
        name="Stock medio %", line=dict(color="#2563eb", width=2),
    ))
    fig2.update_layout(
        height=300, margin={"t": 20, "b": 40},
        yaxis_title="%", xaxis_title="Anno",
        title="Stock consumo suolo",
    )
    st.plotly_chart(fig2, width="stretch")

with col_right:
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=df_naz["anno"], y=df_naz["tot_inc_netto_ha"],
        name="Incremento netto (ha)", marker_color="#059669",
    ))
    fig3.add_trace(go.Bar(
        x=df_naz["anno"], y=df_naz["tot_ripristino_ha"],
        name="Ripristino (ha)", marker_color="#2563eb",
    ))
    fig3.update_layout(
        barmode="group", height=300, margin={"t": 20, "b": 40},
        yaxis_title="ettari", xaxis_title="Anno",
        title="Incremento vs Ripristino",
    )
    st.plotly_chart(fig3, width="stretch")

st.divider()

# ── Dettaglio comuni ────────────────────────────────────────────────────
st.subheader("Dettaglio comuni")

regioni = sorted(df_p["regione"].unique())
regione = st.selectbox("Regione", regioni)
df_r = df_p[df_p["regione"] == regione].sort_values("stock_pct", ascending=False)

st.dataframe(
    df_r[["comune", "provincia", "stock_pct", "incremento_netto_ha", "ripristino_ha", "fascia_consumo_suolo"]]
    .rename(columns={
        "comune": "Comune", "provincia": "Provincia",
        "stock_pct": "Stock %", "incremento_netto_ha": "Inc. netto (ha)",
        "ripristino_ha": "Ripristino (ha)", "fascia_consumo_suolo": "Fascia",
    }),
    width="stretch", hide_index=True,
)

st.caption("Dati: ISPRA — Consumo di suolo · Fonte: open-ispra")
