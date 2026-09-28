"""Balneazione — Deep dive: qualità acque di balneazione."""

import plotly.graph_objects as go
import streamlit as st
from sources import fmt_num, load_mart_bathw

st.title("🏖️ Balneazione — Qualità acque")

# ── Load data ────────────────────────────────────────────────────────────
df = load_mart_bathw("mart_sintesi_anno")

if df.empty:
    st.warning("Nessun dato disponibile.")
    st.stop()

df = df.sort_values("anno")

# ── Warning: breakpoint metodologico 2013 ───────────────────────────────
st.warning(
    "⚠️ **Cambio metodologico nel 2013**: prima del 2013 la classificazione "
    "era binaria (eccellente/scadente). Dal 2013 è stata introdotta la scala "
    "a 4 livelli (eccellente/buona/sufficiente/scadente) della Direttiva UE "
    "2006/7/CE. I dati pre-2013 e post-2013 **non sono direttamente comparabili** "
    "per le colonne 'buona' e 'sufficiente'."
)

# ── Split by era ─────────────────────────────────────────────────────────
df_pre = df[df["anno"] < 2013]
df_post = df[df["anno"] >= 2013]

# ── KPI Row (post-2013 only) ────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

if not df_post.empty:
    latest = df_post.iloc[-1]
    first = df_post.iloc[0]
    k1.metric("Siti totali (ultimo anno)", fmt_num(int(latest["totale_siti"])))
    k2.metric(
        "Eccellenti + Buone",
        f"{latest['pct_eccellente_buona']:.1f}%",
        delta=f"{latest['pct_eccellente_buona'] - first['pct_eccellente_buona']:+.1f} pp vs {int(first['anno'])}",
        delta_color="normal",
    )
    k3.metric(
        "Almeno sufficiente",
        f"{latest['pct_almeno_sufficiente']:.1f}%",
    )
    k4.metric(
        "Periodo",
        f"{int(first['anno'])}–{int(latest['anno'])}",
        help="Dati post-2013 (scala 4 livelli)",
    )
else:
    k1.metric("Siti totali", "—")
    k2.metric("Eccellenti + Buone", "—")
    k3.metric("Almeno sufficiente", "—")
    k4.metric("Periodo", "—")

st.divider()

# ── Stacked area: solo post-2013 ────────────────────────────────────────
st.subheader("Distribuzione qualità nel tempo (2013–2024)")

if not df_post.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_post["anno"], y=df_post["eccellente"],
        name="Eccellente", stackgroup="one", line=dict(color="#059669"),
    ))
    fig.add_trace(go.Scatter(
        x=df_post["anno"], y=df_post["buona"],
        name="Buona", stackgroup="one", line=dict(color="#2563eb"),
    ))
    fig.add_trace(go.Scatter(
        x=df_post["anno"], y=df_post["sufficiente"],
        name="Sufficiente", stackgroup="one", line=dict(color="#d97706"),
    ))
    fig.add_trace(go.Scatter(
        x=df_post["anno"], y=df_post["scadente"],
        name="Scadente", stackgroup="one", line=dict(color="#dc2626"),
    ))
    fig.update_layout(
        height=400, margin={"t": 20, "b": 40},
        yaxis_title="N° siti", xaxis_title="Anno",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, width="stretch")
else:
    st.info("Nessun dato post-2013 disponibile.")

st.divider()

# ── Trend % eccellente + buona ──────────────────────────────────────────
st.subheader("Trend qualità ottima (% eccellente + buona)")

if not df_post.empty:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df_post["anno"], y=df_post["pct_eccellente_buona"],
        name="% Eccellente + Buona", line=dict(color="#059669", width=3),
        mode="lines+markers",
    ))
    fig2.add_hline(
        y=df_post["pct_eccellente_buona"].mean(), line_dash="dash",
        line_color="#6b7280", annotation_text=f"Media: {df_post['pct_eccellente_buona'].mean():.1f}%",
    )
    fig2.update_layout(
        height=300, margin={"t": 20, "b": 40},
        yaxis_title="%", xaxis_title="Anno", yaxis_range=[0, 100],
    )
    st.plotly_chart(fig2, width="stretch")

st.divider()

# ── Serie storica completa (solo eccellente + scadente, binaria) ─────────
st.subheader("Serie storica completa (1990–2012, classificazione binaria)")

st.caption("Prima del 2013: solo eccellente e scadente. I dati non sono comparabili con il post-2013.")

if not df_pre.empty:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_pre["anno"], y=df_pre["eccellente"],
        name="Eccellente", stackgroup="one", line=dict(color="#059669"),
    ))
    fig3.add_trace(go.Scatter(
        x=df_pre["anno"], y=df_pre["scadente"],
        name="Scadente", stackgroup="one", line=dict(color="#dc2626"),
    ))
    fig3.update_layout(
        height=300, margin={"t": 20, "b": 40},
        yaxis_title="N° siti", xaxis_title="Anno",
    )
    st.plotly_chart(fig3, width="stretch")

st.divider()

# ── Tabella riepilogativa ───────────────────────────────────────────────
st.subheader("Riepilogo annuale")

st.dataframe(
    df[["anno", "totale_siti", "eccellente", "buona", "sufficiente", "scadente", "pct_eccellente_buona"]]
    .rename(columns={
        "anno": "Anno", "totale_siti": "Siti",
        "eccellente": "Eccellente", "buona": "Buona",
        "sufficiente": "Sufficiente", "scadente": "Scadente",
        "pct_eccellente_buona": "% Ottima",
    }),
    use_container_width=True, hide_index=True,
)

st.caption("Dati: ISPRA — Qualità acque di balneazione · Fonte: open-ispra")
