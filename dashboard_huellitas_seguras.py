"""
dashboard_huellitas_seguras.py
Dashboard de KPIs de Huellitas Seguras con Streamlit.
Uso: streamlit run dashboard_huellitas_seguras.py
"""

import streamlit as st
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Configuración de página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Huellitas Seguras — Dashboard KPIs",
    page_icon="🐾",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Colores
# ---------------------------------------------------------------------------
VERDE = {
    1: "#E1F5EE",
    2: "#9FE1CB",
    3: "#5DCAA5",
    4: "#1D9E75",
    5: "#0F6E56",
    6: "#085041",
}
GRIS = "#888780"
BORDE = "#EBEBEA"

# ---------------------------------------------------------------------------
# CSS personalizado
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
  @import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css');

  /* Fondo general */
  .stApp {{ background-color: #FAFAF9; }}

  /* Ocultar toolbar de Streamlit */
  [data-testid="stToolbar"] {{ display: none; }}

  /* Header */
  .hs-header {{
    display: flex; align-items: center; gap: 12px;
    padding: 0.5rem 0 1.2rem;
    border-bottom: 1px solid {BORDE};
    margin-bottom: 1.5rem;
  }}
  .hs-logo {{
    width: 42px; height: 42px; border-radius: 50%;
    background: {VERDE[1]}; display: flex;
    align-items: center; justify-content: center;
    font-size: 22px;
  }}
  .hs-title {{ font-size: 18px; font-weight: 600; color: #1A1A1A; margin: 0; }}
  .hs-sub   {{ font-size: 12px; color: {GRIS}; margin: 0; }}

  /* Etiqueta de sección */
  .section-label {{
    font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.07em;
    color: {GRIS}; margin: 1.4rem 0 0.6rem;
  }}

  /* Tarjetas de métricas */
  .metric-card {{
    background: #fff; border: 0.5px solid {BORDE};
    border-radius: 10px; padding: 14px 16px;
  }}
  .metric-label {{ font-size: 12px; color: {GRIS}; margin-bottom: 4px; }}
  .metric-value {{ font-size: 26px; font-weight: 600; color: #1A1A1A; }}
  .metric-meta  {{ font-size: 11px; color: {GRIS}; margin-top: 2px; }}

  /* Tarjetas de mapa de calor */
  .heat-cell {{
    border-radius: 10px; padding: 12px 14px; height: 100%;
  }}
  .heat-label {{ font-size: 13px; font-weight: 600; margin-bottom: 4px; }}
  .heat-desc  {{ font-size: 11px; }}

  /* Escala de calor */
  .heat-scale {{
    display: flex; align-items: center; gap: 6px;
    margin-top: 10px; font-size: 11px; color: {GRIS};
  }}
  .heat-square {{
    width: 16px; height: 10px; border-radius: 2px; display: inline-block;
  }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="hs-header">
  <div class="hs-logo">🐾</div>
  <div>
    <p class="hs-title">Huellitas Seguras — Dashboard de KPIs</p>
    <p class="hs-sub">Prueba de concepto · PMV fase conceptual · Tijuana, Baja California</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Métricas
# ---------------------------------------------------------------------------
METRICAS = [
    ("Inversión total PMV",   "$372K",  "Meta ≤ $372,921 MXN"),
    ("Animales registrados",  ">200",   "Perfiles · meta año 1"),
    ("Tutores activos",       ">200",   "Usuarios/mes"),
    ("Veterinarios activos",  ">15",    "Clínicas registradas"),
]

st.markdown('<p class="section-label">Insumos y productos clave</p>', unsafe_allow_html=True)
cols = st.columns(4)
for col, (label, valor, meta) in zip(cols, METRICAS):
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <p class="metric-label">{label}</p>
          <p class="metric-value">{valor}</p>
          <p class="metric-meta">{meta}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Velocímetros (Gauges)
# ---------------------------------------------------------------------------
GAUGES = [
    ("Casos de extravío resueltos", 20,  "Meta > 20%"),
    ("Tiempo de respuesta",         60,  "Meta < 40 hrs"),
    ("NPS satisfacción del dueño",  60,  "Meta > 60 / 100"),
    ("Cobertura territorial",       15,  "Meta > 15% de colonias"),
]

st.markdown('<p class="section-label">Velocímetros de eficiencia</p>', unsafe_allow_html=True)
gcols = st.columns(4)
for col, (label, pct, meta) in zip(gcols, GAUGES):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={"suffix": "%", "font": {"size": 24, "color": VERDE[4]}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": GRIS, "tickfont": {"size": 10}},
            "bar":  {"color": VERDE[4], "thickness": 0.28},
            "bgcolor": VERDE[1],
            "borderwidth": 0,
            "steps": [{"range": [0, 100], "color": VERDE[1]}],
        },
        domain={"x": [0, 1], "y": [0, 1]},
    ))
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=10),
        height=160,
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "sans-serif"},
    )
    with col:
        st.plotly_chart(fig, width="stretch", key=f"gauge_{label}", config={"displayModeBar": False})
        st.markdown(
            f"<p style='text-align:center;font-size:12px;color:{GRIS};margin-top:-12px;'>"
            f"{label}<br><span style='font-size:10px;'>{meta}</span></p>",
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# CAPEX — Gráfica de barras horizontal
# ---------------------------------------------------------------------------
CAPEX = [
    ("Desarrollo app",          235_000, True),
    ("UX/UI",                    50_000, True),
    ("Autenticación veterinarios",12_000, True),
    ("IMPI Clase 42",             3_126, True),
    ("IMPI Clase 44",             3_126, True),
    ("Google Play",                 437, True),
    ("App Store",                 1_732, True),
    ("Servidor (año 1)",           6_000, True),
    ("Dominio y correo",          1_500, True),
    ("Piloto usuarios",          18_000, False),
    ("Iteraciones post-piloto",  28_000, False),
    ("Asesoría legal",            8_000, False),
    ("Difusión y onboarding",     6_000, False),
]

nombres  = [n for n, _, _   in CAPEX]
montos   = [m for _, m, _   in CAPEX]
colores  = [VERDE[4] if pmv else VERDE[3] for _, _, pmv in CAPEX]
total    = sum(montos)

st.markdown(
    f'<p class="section-label">Desglose de inversión inicial (CAPEX) — Total: ${total:,} MXN</p>',
    unsafe_allow_html=True,
)

# Leyenda
lcol1, lcol2, _ = st.columns([1, 1, 4])
lcol1.markdown(
    f"<span style='font-size:12px;color:{GRIS};'>"
    f"<span style='display:inline-block;width:12px;height:12px;border-radius:3px;"
    f"background:{VERDE[4]};margin-right:5px;vertical-align:middle;'></span>"
    f"PMV — desarrollo y activos</span>",
    unsafe_allow_html=True,
)
lcol2.markdown(
    f"<span style='font-size:12px;color:{GRIS};'>"
    f"<span style='display:inline-block;width:12px;height:12px;border-radius:3px;"
    f"background:{VERDE[3]};margin-right:5px;vertical-align:middle;'></span>"
    f"Validación y pivoteo</span>",
    unsafe_allow_html=True,
)

fig_bar = go.Figure(go.Bar(
    x=montos,
    y=nombres,
    orientation="h",
    marker_color=colores,
    marker_line_width=0,
    hovertemplate="<b>%{y}</b><br>$%{x:,.0f} MXN<extra></extra>",
))
fig_bar.update_layout(
    height=340,
    margin=dict(l=10, r=20, t=10, b=10),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font={"family": "sans-serif", "color": GRIS, "size": 11},
    xaxis=dict(
        tickprefix="$",
        ticksuffix="K",
        tickvals=[0, 50_000, 100_000, 150_000, 200_000, 235_000],
        ticktext=["$0", "$50K", "$100K", "$150K", "$200K", "$235K"],
        gridcolor="rgba(0,0,0,0.06)",
        zeroline=False,
    ),
    yaxis=dict(gridcolor="rgba(0,0,0,0)", autorange="reversed"),
    bargap=0.3,
)
st.plotly_chart(fig_bar, width="stretch", key="capex_bar", config={"displayModeBar": False})

# ---------------------------------------------------------------------------
# Mapa de calor — impacto social
# ---------------------------------------------------------------------------
IMPACTO = [
    ("Mascotas rescatadas",            "Meta: >50 casos/año · Impacto alto",               VERDE[1], VERDE[6], VERDE[5]),
    ("Reducción animales en calle",    "Meta: >5% anual · Zona piloto Tijuana",            VERDE[2], VERDE[6], VERDE[6]),
    ("Cobertura territorial",          "Meta: >15% colonias · Semestral",                  VERDE[3], VERDE[6], VERDE[6]),
    ("Integración con Control Animal", "Meta: >60% interoperabilidad · Trimestral",        VERDE[4], VERDE[1], VERDE[2]),
    ("Historiales médicos actualizados","Meta: >100 ediciones/mes · Veterinarios",         VERDE[5], VERDE[1], VERDE[2]),
    ("Alertas de extravío enviadas",   "Meta: >30 alertas/mes · Tiempo real",              VERDE[6], VERDE[1], VERDE[2]),
]

st.markdown('<p class="section-label">Mapa de calor — impacto social</p>', unsafe_allow_html=True)

row1 = st.columns(3)
row2 = st.columns(3)
filas = [row1, row2]

for i, (titulo, desc, fondo, c_titulo, c_desc) in enumerate(IMPACTO):
    fila = filas[i // 3]
    col  = fila[i % 3]
    with col:
        st.markdown(f"""
        <div class="heat-cell" style="background:{fondo};">
          <p class="heat-label" style="color:{c_titulo};">{titulo}</p>
          <p class="heat-desc"  style="color:{c_desc};">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# Escala
escala_html = "".join(
    f'<span class="heat-square" style="background:{VERDE[i]};'
    f'{"border:0.5px solid " + BORDE + ";" if i == 1 else ""}"></span>'
    for i in range(1, 7)
)
st.markdown(f"""
<div class="heat-scale" style="margin-top:14px;">
  Menor impacto
  <div style="display:flex;gap:3px;">{escala_html}</div>
  Mayor impacto
</div>
""", unsafe_allow_html=True)
