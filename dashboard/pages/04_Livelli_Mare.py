"""Livelli Mare — Deep dive: rete mareografica nazionale."""

import plotly.graph_objects as go
import streamlit as st
from sources import fmt_num, load_mart_rmn

st.title("🌊 Livelli del Mare")

# ── Warning: cambio protocollo 2014 ─────────────────────────────────────
st.warning(
    "⚠️ **Cambio protocollo nel 2014**: prima del 2014 i dati avevano "
    "frequenza oraria e riferimento diverso. I dati mostrati sono "
    "**solo post-2014** per coerenza. I dati pre-2014 sono disponibili "
    "nel layer clean ma non sono comparabili."
)

# ── Load data (filter post-2014) ────────────────────────────────────────
df_stazioni_raw = load_mart_rmn("mart_stazioni")
df_sintesi_raw = load_mart_rmn("mart_sintesi")

if df_stazioni_raw.empty or df_sintesi_raw.empty:
    st.warning("Nessun dato disponibile.")
    st.stop()

# Filtra post-2014 (il mart potrebbe non avere ancora la colonna era)
if "era" in df_sintesi_raw.columns:
    df_sintesi = df_sintesi_raw[df_sintesi_raw["era"] == "post_2014"]
    df_stazioni = df_stazioni_raw[df_stazioni_raw["era"] == "post_2014"]
else:
    df_sintesi = df_sintesi_raw[df_sintesi_raw["anno"] >= 2014]
    df_stazioni = df_stazioni_raw[df_stazioni_raw["primo_anno"] >= 2014]

if df_stazioni.empty or df_sintesi.empty:
    st.warning("Nessun dato post-2014 disponibile.")
    st.stop()

# ── KPI Row ──────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

k1.metric("Stazioni attive", fmt_num(len(df_stazioni)))
k2.metric(
    "Osservazioni totali",
    fmt_num(int(df_stazioni["totale_osservazioni"].sum())),
)
k3.metric(
    "Anni coperti",
    f"{int(df_stazioni['primo_anno'].min())}–{int(df_stazioni['ultimo_anno'].max())}",
)
k4.metric(
    "Media livello",
    f"{df_stazioni['media_livello'].mean():.1f}",
)

st.divider()

# ── Filtri ───────────────────────────────────────────────────────────────
stazioni = sorted(df_stazioni["station_id"].unique())
stazione = st.selectbox("Stazione", stazioni)

df_sta = df_sintesi[df_sintesi["station_id"] == stazione].sort_values("anno")

# ── Trend livello medio ─────────────────────────────────────────────────
st.subheader(f"Trend livello medio — {stazione}")

if not df_sta.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sta["anno"], y=df_sta["media_livello"],
        name="Media", line=dict(color="#2563eb", width=2), mode="lines+markers",
    ))
    fig.add_trace(go.Scatter(
        x=df_sta["anno"], y=df_sta["max_livello"],
        name="Max", line=dict(color="#dc2626", width=1, dash="dot"),
        mode="lines",
    ))
    fig.add_trace(go.Scatter(
        x=df_sta["anno"], y=df_sta["min_livello"],
        name="Min", line=dict(color="#059669", width=1, dash="dot"),
        mode="lines", fill="tonexty", fillcolor="rgba(37,99,235,0.1)",
    ))
    fig.update_layout(
        height=350, margin={"t": 20, "b": 40},
        yaxis_title="Livello", xaxis_title="Anno",
    )
    st.plotly_chart(fig, width="stretch")
else:
    st.info("Nessun dato per questa stazione.")

st.divider()

# ── Statistiche stazione ────────────────────────────────────────────────
st.subheader("Statistiche stazione")

df_sel = df_stazioni[df_stazioni["station_id"] == stazione]
if not df_sel.empty:
    s = df_sel.iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Osservazioni", fmt_num(int(s["totale_osservazioni"])))
    c2.metric("Anni attivi", fmt_num(int(s["anni_attivi"])))
    c3.metric("Media", f"{s['media_livello']:.1f}")
    c4.metric("Dev. std", f"{s['std_livello']:.1f}")

st.divider()

# ── Tutte le stazioni: confronto ────────────────────────────────────────
st.subheader("Confronto stazioni — media livello per anno")

fig2 = go.Figure()
for sta in stazioni[:10]:  # max 10 stazioni per leggibilità
    df_s = df_sintesi[df_sintesi["station_id"] == sta].sort_values("anno")
    fig2.add_trace(go.Scatter(
        x=df_s["anno"], y=df_s["media_livello"],
        name=sta, mode="lines",
    ))
fig2.update_layout(
    height=400, margin={"t": 20, "b": 40},
    yaxis_title="Livello medio", xaxis_title="Anno",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig2, width="stretch")

st.caption("Dati: ISPRA — Rete Mareografica Nazionale (post-2014) · Fonte: open-ispra")
