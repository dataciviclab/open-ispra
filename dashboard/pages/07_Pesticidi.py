"""Pesticidi — Deep dive: concentrazioni pesticidi nelle acque sotterranee."""

import plotly.graph_objects as go
import streamlit as st
from sources import fmt_num, load_mart_pest

st.title("🧪 Pesticidi nelle Acque Sotterranee")

# ── Load data ────────────────────────────────────────────────────────────
df = load_mart_pest("mart_sintesi")

if df.empty:
    st.warning("Nessun dato disponibile.")
    st.stop()

df = df.sort_values("anno")

# ── KPI Row ──────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

latest = df.iloc[-1]
k1.metric("Stazioni monitorate", fmt_num(int(latest["stazioni"])))
k2.metric("Sostanze analizzate", fmt_num(int(latest["sostanze"])))
k3.metric(
    "Rilevazioni positive",
    f"{latest['pct_positive']:.1f}%",
    help=f"{fmt_num(int(latest['rilevazioni_positive']))} su {fmt_num(int(latest['totale_misurazioni']))}",
)
k4.metric(
    "Media positivi",
    f"{latest['media_positivi']:.1f} µg/L",
)

st.divider()

# ── Trend stazioni e sostanze ───────────────────────────────────────────
st.subheader("Evoluzione monitoraggio")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["anno"], y=df["stazioni"],
    name="Stazioni", line=dict(color="#2563eb", width=2), mode="lines+markers",
))
fig.add_trace(go.Scatter(
    x=df["anno"], y=df["sostanze"],
    name="Sostanze", line=dict(color="#059669", width=2), mode="lines+markers",
    yaxis="y2",
))
fig.update_layout(
    height=300, margin={"t": 20, "b": 40},
    yaxis_title="Stazioni", xaxis_title="Anno",
    yaxis2=dict(title="Sostanze", overlaying="y", side="right"),
)
st.plotly_chart(fig, width="stretch")

st.divider()

# ── Trend % positivi ────────────────────────────────────────────────────
st.subheader("Trend rilevazioni positive")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df["anno"], y=df["pct_positive"],
    name="% Positive", line=dict(color="#dc2626", width=3),
    mode="lines+markers",
))
fig2.update_layout(
    height=300, margin={"t": 20, "b": 40},
    yaxis_title="%", xaxis_title="Anno", yaxis_range=[0, 100],
)
st.plotly_chart(fig2, width="stretch")

st.divider()

# ── Tabella ──────────────────────────────────────────────────────────────
st.subheader("Riepilogo annuale")

st.dataframe(
    df[["anno", "stazioni", "sostanze", "totale_misurazioni", "rilevazioni_positive", "pct_positive"]]
    .rename(columns={
        "anno": "Anno", "stazioni": "Stazioni", "sostanze": "Sostanze",
        "totale_misurazioni": "Misurazioni", "rilevazioni_positive": "Positive",
        "pct_positive": "% Positive",
    }),
    width="stretch", hide_index=True,
)

st.caption("Dati: ISPRA — Pesticidi acque sotterranee · Fonte: open-ispra")
