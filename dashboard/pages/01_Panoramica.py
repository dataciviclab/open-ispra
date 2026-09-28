"""Panoramica — Vista unificata dei dataset ISPRA."""

import plotly.graph_objects as go
import streamlit as st
from sources import (
    fmt_num,
    load_mart_bathw,
    load_mart_consumo_suolo,
    load_mart_iffi,
    load_mart_rmn,
)

st.title("📊 Ambiente ISPRA — Panoramica")

# ── KPI Row ──────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

df_italia = load_mart_iffi("mart_italia")
if not df_italia.empty:
    k1.metric("Frane totali", fmt_num(int(df_italia["totale_frane"].iloc[0])))
else:
    k1.metric("Frane totali", "—")

df_bathw = load_mart_bathw("mart_sintesi_anno")
if not df_bathw.empty:
    # Post-2013 per KPI (scala 4 livelli)
    df_bathw_post = df_bathw[df_bathw["anno"] >= 2013]
    if not df_bathw_post.empty:
        latest = df_bathw_post.sort_values("anno").iloc[-1]
        k2.metric(
            "Siti balneazione",
            fmt_num(int(latest["totale_siti"])),
            help=f"Anno {int(latest['anno'])} (post-2013)",
        )
    else:
        k2.metric("Siti balneazione", "—")
else:
    k2.metric("Siti balneazione", "—")

df_rmn = load_mart_rmn("mart_stazioni")
if not df_rmn.empty:
    # Post-2014 per coerenza
    if "era" in df_rmn.columns:
        df_rmn_post = df_rmn[df_rmn["era"] == "post_2014"]
    else:
        df_rmn_post = df_rmn[df_rmn["primo_anno"] >= 2014]
    k3.metric("Stazioni mare", fmt_num(len(df_rmn_post)) if not df_rmn_post.empty else "—")
else:
    k3.metric("Stazioni mare", "—")

df_cs = load_mart_consumo_suolo("mart_sintesi")
df_cs_naz = df_cs[df_cs["livello"] == "nazionale"] if not df_cs.empty else df_cs
if not df_cs_naz.empty:
    latest_cs = df_cs_naz.sort_values("anno").iloc[-1]
    k4.metric(
        "Stock consumo suolo",
        f"{latest_cs['avg_stock_pct']:.1f}%",
        help=f"Media nazionale {int(latest_cs['anno'])}",
    )
else:
    k4.metric("Stock consumo suolo", "—")

st.divider()

# ── Balneazione: trend qualità post-2013 ────────────────────────────────
st.subheader("🏖️ Qualità acque di balneazione (2013–2024)")

if not df_bathw.empty:
    df_bathw_post = df_bathw[df_bathw["anno"] >= 2013].sort_values("anno")

    if not df_bathw_post.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_bathw_post["anno"], y=df_bathw_post["eccellente"],
            name="Eccellente", stackgroup="one", line=dict(color="#059669"),
        ))
        fig.add_trace(go.Scatter(
            x=df_bathw_post["anno"], y=df_bathw_post["buona"],
            name="Buona", stackgroup="one", line=dict(color="#2563eb"),
        ))
        fig.add_trace(go.Scatter(
            x=df_bathw_post["anno"], y=df_bathw_post["sufficiente"],
            name="Sufficiente", stackgroup="one", line=dict(color="#d97706"),
        ))
        fig.add_trace(go.Scatter(
            x=df_bathw_post["anno"], y=df_bathw_post["scadente"],
            name="Scadente", stackgroup="one", line=dict(color="#dc2626"),
        ))
        fig.update_layout(
            height=350, margin={"t": 20, "b": 40},
            yaxis_title="N° siti", xaxis_title="Anno",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Nessun dato balneazione post-2013.")
else:
    st.info("Nessun dato balneazione disponibile.")

st.caption("Nota: dati pre-2013 su scala binaria (non mostrati). Vedere pagina Balneazione per dettagli.")

st.divider()

# ── Consumo suolo: trend nazionale ──────────────────────────────────────
st.subheader("🏗️ Consumo di suolo — trend nazionale")

if not df_cs_naz.empty:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df_cs_naz["anno"], y=df_cs_naz["tot_stock_ha"],
        name="Stock totale (ha)", line=dict(color="#2563eb", width=2),
    ))
    fig2.update_layout(
        height=300, margin={"t": 20, "b": 40},
        yaxis_title="ettari", xaxis_title="Anno",
    )
    st.plotly_chart(fig2, width="stretch")
else:
    st.info("Nessun dato consumo suolo disponibile.")

st.divider()

# ── Frane per regione ───────────────────────────────────────────────────
st.subheader("⛰️ Frane per regione")

df_regioni = load_mart_iffi("mart_regioni")
if not df_regioni.empty:
    df_sorted = df_regioni.sort_values("nr_frane", ascending=True)
    fig3 = go.Figure(go.Bar(
        x=df_sorted["nr_frane"], y=df_sorted["regione"],
        orientation="h", marker_color="#d97706",
    ))
    fig3.update_layout(
        height=500, margin={"t": 20, "b": 40, "l": 150},
        xaxis_title="N° frane",
    )
    st.plotly_chart(fig3, width="stretch")
else:
    st.info("Nessun dato frane disponibile.")

st.caption("Dati: ISPRA · Fonte: open-ispra")
