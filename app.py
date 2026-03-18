import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
from matplotlib.patches import FancyArrowPatch
import math
import smtplib
from email.message import EmailMessage
import email.policy

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Perfil de Riesgo del Inversionista",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0b0f1a;
    color: #e8e6e0;
}
.stApp { background-color: #0b0f1a; }
.main .block-container { padding: 2rem 2rem 4rem; max-width: 900px; margin: 0 auto; }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Progress bar */
.stProgress > div > div { background: linear-gradient(90deg, #c9a84c, #f0d080); border-radius: 4px; }
.stProgress > div { background: #1e2435; border-radius: 4px; }

/* Radio buttons */
div[data-testid="stRadio"] > label {
    font-family: 'DM Sans', sans-serif;
    color: #b0aaa0;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
div[data-testid="stRadio"] > div {
    background: #1e2a40;
    border: 1px solid #3a4560;
    border-radius: 12px;
    padding: 0.5rem;
    gap: 4px;
}
div[data-testid="stRadio"] label {
    background: transparent !important;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 0.75rem 1rem !important;
    margin: 2px 0;
    transition: all 0.2s ease;
    cursor: pointer;
    color: #e8e4dc !important;
    font-size: 0.95rem !important;
    line-height: 1.4 !important;
}
div[data-testid="stRadio"] label:hover {
    background: #1e2a40 !important;
    border-color: #c9a84c !important;
    color: #f0d080 !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"] input:checked + div {
    background: #c9a84c !important;
}
div[data-testid="stRadio"] label p {
    color: #e8e4dc !important;
}
div[data-testid="stRadio"] label span {
    color: #e8e4dc !important;
}
/* Buttons */
.stButton > button {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 0.85rem;
    border-radius: 8px;
    border: none;
    padding: 0.75rem 2.5rem;
    transition: all 0.2s ease;
    cursor: pointer;
}
.stButton > button[kind="primary"], .stButton > button {
    background: linear-gradient(135deg, #c9a84c, #f0d080);
    color: #0b0f1a;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #f0d080, #c9a84c);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(201,168,76,0.35);
}

/* Divider */
hr { border-color: #2a3050; }

/* Metric */
[data-testid="metric-container"] {
    background: #131929;
    border: 1px solid #2a3050;
    border-radius: 12px;
    padding: 1rem;
}

/* Note box */
.note-box {
    background: #131929;
    border-left: 3px solid #c9a84c;
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0 1.25rem 0;
    font-size: 0.85rem;
    color: #9a9080;
    font-style: italic;
}

/* Question card */
.q-card {
    background: #131929;
    border: 1px solid #2a3050;
    border-top: 3px solid #c9a84c;
    border-radius: 0 0 12px 12px;
    padding: 1.5rem 1.75rem 1.75rem;
    margin-bottom: 0.5rem;
}

/* Section badge */
.section-badge {
    display: inline-block;
    background: rgba(201,168,76,0.12);
    color: #c9a84c;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    border: 1px solid rgba(201,168,76,0.3);
    margin-bottom: 0.75rem;
}

/* Question number */
.q-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 900;
    color: rgba(201,168,76,0.2);
    line-height: 1;
    margin-bottom: 0.25rem;
}

/* Question text */
.q-text {
    font-size: 1.1rem;
    font-weight: 500;
    color: #e8e6e0;
    line-height: 1.5;
    margin-bottom: 0.25rem;
}

/* Info card */
.info-card {
    background: #131929;
    border: 1px solid #2a3050;
    border-top: 3px solid #c9a84c;
    border-radius: 12px;
    padding: 1.5rem 1rem;
    text-align: center;
}
.info-card-icon { font-size: 1.8rem; margin-bottom: 0.6rem; }
.info-card-value {
    font-size: 0.8rem;
    color: #c9a84c;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.2rem;
}
.info-card-label { font-size: 0.8rem; color: #555; }

/* Metric pill */
.metric-pill {
    background: #0b0f1a;
    border: 1px solid #2a3050;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.metric-pill-label {
    font-size: 0.65rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}
.metric-pill-value {
    font-size: 1rem;
    font-weight: 600;
    color: #e8e6e0;
}

/* Profile scale row */
.scale-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #0d1117;
    border: 1px solid #2a3050;
    border-radius: 8px;
    padding: 0.65rem 1rem;
    margin: 0.25rem 0;
}
.scale-row.active {
    border-left: 4px solid;
}
.scale-bar-track {
    flex: 1;
    height: 4px;
    background: #1e2435;
    border-radius: 2px;
    overflow: hidden;
}
.scale-bar-fill {
    height: 100%;
    border-radius: 2px;
    opacity: 0.8;
}

/* Divider label */
.divider-label {
    font-size: 0.68rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    text-align: center;
    margin: 1.25rem 0 0.75rem;
}

/* Input styling */
div[data-testid="stTextInput"] input {
    background: #131929 !important;
    border: 1px solid #2a3050 !important;
    border-radius: 8px !important;
    color: #e8e6e0 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.6rem 0.85rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #c9a84c !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
}
div[data-testid="stTextInput"] label {
    color: #888 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
</style>
""", unsafe_allow_html=True)

# ─── DATA ────────────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "section": "I — Reacciones ante el mercado",
        "text": "60 días después de realizar la inversión, esta cae aproximadamente un 20%. ¿Qué decisión tomaría?",
        "options": [
            "Vender para evitar pérdidas adicionales.",
            "No hacer nada y esperar que la inversión recupere su precio inicial.",
            "Comprar más; si antes era una buena inversión, al precio actual es aún mejor.",
        ],
        "points": [1, 3, 5],
        "note": None,
    },
    {
        "section": "I — Reacciones ante el mercado",
        "text": "La misma inversión que cayó 20% se usa para un objetivo de inversión. ¿Qué haría según el horizonte de tiempo?",
        "options": [
            "Vender en todos los escenarios (5, 15 y 30 años).",
            "No hacer nada en los escenarios de 15 y 30 años; vender a 5 años.",
            "Comprar más a 15 y 30 años; no hacer nada a 5 años.",
            "Comprar más en todos los escenarios.",
        ],
        "points": [1, 2, 4, 5],
        "note": "Considere la caída del 20% como permanente hasta nuevo aviso y evalúe su reacción en función del plazo.",
    },
    {
        "section": "I — Reacciones ante el mercado",
        "text": "El precio de su inversión para retiro subió 25% al cabo de un mes. El panorama económico se mantiene igual. ¿Qué haría?",
        "options": [
            "Vender y asegurar las ganancias.",
            "Mantener la posición y esperar mayores ganancias.",
            "Comprar más; los fundamentos siguen siendo sólidos.",
        ],
        "points": [1, 3, 5],
        "note": None,
    },
    {
        "section": "II — Tolerancia al riesgo y objetivos",
        "text": "Usted está invirtiendo para retiro en 15 años. ¿Qué asignación de activos preferiría?",
        "options": [
            "100% mercado monetario / renta fija de corto plazo: protege el capital, renuncia al crecimiento.",
            "50% bonos / 50% acciones: crecimiento moderado con cobertura ante fluctuaciones.",
            "70% renta variable / 30% alternativos: alta volatilidad anual, máximo retorno a largo plazo.",
        ],
        "points": [1, 3, 5],
        "note": None,
    },
    {
        "section": "II — Tolerancia al riesgo y objetivos",
        "text": "¿Cuál es su principal objetivo de inversión?",
        "options": [
            "Preservar el capital a cualquier costo, aunque el rendimiento real sea negativo.",
            "Obtener rendimientos similares a inflación +2%, con baja volatilidad.",
            "Superar el benchmark del mercado en el largo plazo, aceptando periodos de pérdida.",
            "Maximizar el retorno absoluto sin restricciones de riesgo ni benchmark.",
        ],
        "points": [1, 2, 4, 5],
        "note": None,
    },
    {
        "section": "II — Tolerancia al riesgo y objetivos",
        "text": "¿Cuánto tiempo podría mantener una inversión sin necesitar liquidarla?",
        "options": [
            "Menos de 1 año: necesito liquidez inmediata o de corto plazo.",
            "Entre 1 y 3 años: podría esperar, pero prefiero plazos medianos.",
            "Entre 3 y 10 años: tengo horizonte de inversión de mediano-largo plazo.",
            "Más de 10 años: no requiero liquidez en el corto plazo.",
        ],
        "points": [1, 2, 4, 5],
        "note": None,
    },
    {
        "section": "III — Decisiones financieras y apalancamiento",
        "text": "Acaba de ganar un premio. ¿Cuál prefiere?",
        "options": [
            "COP $2.000.000 en efectivo, de forma segura.",
            "COP $5.000.000 con probabilidad del 50% de ganar. (VE: $2.500.000)",
            "COP $15.000.000 con probabilidad del 20% de ganar. (VE: $3.000.000)",
        ],
        "points": [1, 3, 5],
        "note": "VE = Valor Esperado (pago × probabilidad). Las opciones B y C tienen mayor VE, pero mayor riesgo.",
    },
    {
        "section": "III — Decisiones financieras y apalancamiento",
        "text": "Se presenta una oportunidad atractiva de inversión, pero requiere endeudamiento. ¿Tomaría el préstamo?",
        "options": [
            "No, nunca invertiría con capital prestado.",
            "Solo si el costo de la deuda es significativamente inferior al retorno esperado y el riesgo es bajo.",
            "Sí, si el análisis financiero muestra que el apalancamiento mejora el retorno ajustado por riesgo.",
            "Sí, maximizaría el apalancamiento para capturar el mayor retorno posible.",
        ],
        "points": [1, 2, 4, 5],
        "note": None,
    },
    {
        "section": "III — Decisiones financieras y apalancamiento",
        "text": "Su empresa ofrece acciones a empleados con un lock-up de 3 años, sin dividendos, pero con potencial de crecer 10x. ¿Cuánto invertiría?",
        "options": [
            "Nada: no me siento cómodo con la iliquidez ni la incertidumbre.",
            "2 meses de salario: participo con una fracción pequeña.",
            "5 meses de salario: la oportunidad justifica el riesgo y la iliquidez.",
            "Más de 5 meses de salario: concentraría una parte significativa de mi patrimonio.",
        ],
        "points": [1, 2, 4, 5],
        "note": None,
    },
    {
        "section": "IV — Conocimiento y experiencia",
        "text": "¿Con cuáles instrumentos tiene experiencia de inversión real (no solo académica)?",
        "options": [
            "Solo cuentas de ahorro, CDTs o mercado monetario.",
            "Fondos mutuos, ETFs y/o bonos corporativos o gubernamentales.",
            "Acciones individuales, derivados (opciones, futuros) o REITs.",
            "Alternativos: private equity, venture capital, hedge funds, criptoactivos o materias primas.",
        ],
        "points": [1, 2, 4, 5],
        "note": None,
    },
    {
        "section": "IV — Conocimiento y experiencia",
        "text": "¿Cómo describiría su comprensión de los conceptos de riesgo-retorno en finanzas?",
        "options": [
            "Comprendo conceptualmente que mayor riesgo implica mayor retorno potencial.",
            "Puedo calcular desviación estándar, Sharpe ratio y beta de un portafolio.",
            "Manejo análisis de VaR, simulaciones Monte Carlo y optimización de portafolio.",
            "Diseño e implemento estrategias de cobertura (hedging) con derivados.",
        ],
        "points": [1, 2, 4, 5],
        "note": None,
    },
]

PROFILES = [
    {
        "range": (11, 14),
        "name": "Conservador",
        "emoji": "🛡️",
        "color": "#4a9eff",
        "bg": "#0a1a2e",
        "desc": "Prioriza la preservación del capital por encima de todo. Prefiere instrumentos de renta fija, mercado monetario y depósitos a término. Tiene muy baja tolerancia a la volatilidad y busca certeza sobre el valor de su capital.",
        "strategy": "CDTs, bonos del gobierno, fondos de mercado monetario, cuentas de ahorro de alto rendimiento.",
        "horizon": "Corto plazo (< 3 años)",
        "volatility": "Muy baja",
        "expected_return": "Inflación ± 1%",
    },
    {
        "range": (15, 24),
        "name": "Moderado-Conservador",
        "emoji": "⚓",
        "color": "#38d9a9",
        "bg": "#0a2520",
        "desc": "Acepta un nivel limitado de riesgo a cambio de rendimientos ligeramente superiores a los del mercado monetario. Prefiere portafolios con predominancia de renta fija y una pequeña exposición a renta variable.",
        "strategy": "70-80% renta fija (bonos grado inversión, CDTs) + 20-30% renta variable diversificada (ETFs de índice).",
        "horizon": "Mediano plazo (3–5 años)",
        "volatility": "Baja",
        "expected_return": "Inflación + 2–3%",
    },
    {
        "range": (25, 34),
        "name": "Moderado",
        "emoji": "⚖️",
        "color": "#f0d080",
        "bg": "#1e1a08",
        "desc": "Busca un crecimiento equilibrado del capital. Tolera fluctuaciones moderadas en el corto plazo y combina renta fija con renta variable en proporciones similares. Su horizonte es de mediano a largo plazo.",
        "strategy": "50% renta fija + 50% renta variable (acciones, ETFs globales, fondos balanceados).",
        "horizon": "Mediano-largo plazo (5–10 años)",
        "volatility": "Moderada",
        "expected_return": "Inflación + 4–6%",
    },
    {
        "range": (35, 44),
        "name": "Moderado-Agresivo",
        "emoji": "🚀",
        "color": "#ff9a3c",
        "bg": "#1e1208",
        "desc": "Dispuesto a asumir un riesgo considerable para obtener rendimientos superiores al mercado. Entiende y acepta la volatilidad como parte del proceso de inversión. Tiene horizonte de largo plazo.",
        "strategy": "70% renta variable (acciones individuales, ETFs temáticos, REITs) + 30% alternativos y renta fija.",
        "horizon": "Largo plazo (10–20 años)",
        "volatility": "Alta",
        "expected_return": "Inflación + 6–10%",
    },
    {
        "range": (45, 55),
        "name": "Agresivo",
        "emoji": "⚡",
        "color": "#ff4d6d",
        "bg": "#1e0810",
        "desc": "Alta tolerancia al riesgo. Busca maximizar el retorno absoluto con plena consciencia de las pérdidas potenciales. Invierte en renta variable concentrada, alternativos sofisticados y puede usar apalancamiento.",
        "strategy": "Renta variable concentrada, derivados, private equity, venture capital, hedge funds, activos alternativos.",
        "horizon": "Largo plazo (> 20 años)",
        "volatility": "Muy alta",
        "expected_return": "Inflación + 10%+",
    },
]

# ─── HELPERS ────────────────────────────────────────────────────────────────
def get_profile(score):
    for p in PROFILES:
        if p["range"][0] <= score <= p["range"][1]:
            return p
    return PROFILES[-1]


def make_gauge(score, profile):
    """Generate a creative gauge/speedometer chart."""
    fig = plt.figure(figsize=(10, 6), facecolor="#0b0f1a")
    ax = fig.add_subplot(111, facecolor="#0b0f1a")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.6, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── background glow ──
    for r in np.linspace(1.25, 1.0, 8):
        alpha = 0.02 * (1.35 - r)
        circle = plt.Circle((0, 0), r, color="#c9a84c", alpha=alpha, zorder=0)
        ax.add_patch(circle)

    # ── arc segments (5 zones) ──
    colors = ["#4a9eff", "#38d9a9", "#f0d080", "#ff9a3c", "#ff4d6d"]
    labels = ["Conservador", "Mod-Conservador", "Moderado", "Mod-Agresivo", "Agresivo"]
    ranges = [(11, 14), (15, 24), (25, 34), (35, 44), (45, 55)]
    total = 44  # 55-11

    theta_start = 180
    theta_end = 0

    segment_angles = []
    for rng in ranges:
        span = rng[1] - rng[0]
        angle_span = (span / total) * 180
        segment_angles.append(angle_span)

    current_angle = 180
    for i, (color, angle_span) in enumerate(zip(colors, segment_angles)):
        is_active = ranges[i][0] <= score <= ranges[i][1]
        alpha = 1.0 if is_active else 0.35
        lw = 28 if is_active else 20

        theta = np.linspace(
            np.radians(current_angle),
            np.radians(current_angle - angle_span),
            60,
        )
        x = np.cos(theta)
        y = np.sin(theta)
        ax.plot(x, y, color=color, linewidth=lw, alpha=alpha,
                solid_capstyle="butt", zorder=3)

        # label
        mid_angle = np.radians(current_angle - angle_span / 2)
        lx = 1.12 * np.cos(mid_angle)
        ly = 1.12 * np.sin(mid_angle)
        ax.text(lx, ly, labels[i], ha="center", va="center",
                fontsize=6.5, color=color if is_active else "#666",
                fontweight="bold" if is_active else "normal",
                fontfamily="DejaVu Sans")

        current_angle -= angle_span

    # ── inner arc (track) ──
    theta = np.linspace(np.radians(180), np.radians(0), 120)
    ax.plot(np.cos(theta) * 0.72, np.sin(theta) * 0.72,
            color="#1e2435", linewidth=22, zorder=2)

    # ── needle ──
    needle_angle = 180 - ((score - 11) / 44) * 180
    needle_rad = np.radians(needle_angle)
    nx = 0.82 * np.cos(needle_rad)
    ny = 0.82 * np.sin(needle_rad)

    # shadow
    ax.annotate("", xy=(nx * 0.98, ny * 0.98), xytext=(0, -0.04),
                arrowprops=dict(arrowstyle="->, head_width=0.04, head_length=0.04",
                                color="#000000", lw=3, alpha=0.3))
    # main needle
    ax.annotate("", xy=(nx, ny), xytext=(0, -0.04),
                arrowprops=dict(arrowstyle="->, head_width=0.045, head_length=0.045",
                                color="#ffffff", lw=2.5))

    # center pin
    pin = plt.Circle((0, 0), 0.06, color="#c9a84c", zorder=10)
    pin_inner = plt.Circle((0, 0), 0.035, color="#0b0f1a", zorder=11)
    ax.add_patch(pin)
    ax.add_patch(pin_inner)

    # ── score text ──
    ax.text(0, -0.22, str(score), ha="center", va="center",
            fontsize=42, fontweight="bold", color=profile["color"],
            fontfamily="DejaVu Sans", zorder=12)
    ax.text(0, -0.42, "puntos de 55", ha="center", va="center",
            fontsize=9, color="#666", fontfamily="DejaVu Sans")

    # ── profile name ──
    ax.text(0, 1.22, f"{profile['emoji']}  {profile['name'].upper()}", ha="center",
            va="center", fontsize=14, fontweight="bold", color=profile["color"],
            fontfamily="DejaVu Sans",
            bbox=dict(boxstyle="round,pad=0.4", facecolor=profile["bg"],
                      edgecolor=profile["color"], alpha=0.9, linewidth=1.5))

    # ── scale marks ──
    for val in [11, 20, 30, 40, 55]:
        ang = np.radians(180 - ((val - 11) / 44) * 180)
        x0, y0 = 0.88 * np.cos(ang), 0.88 * np.sin(ang)
        x1, y1 = 0.95 * np.cos(ang), 0.95 * np.sin(ang)
        ax.plot([x0, x1], [y0, y1], color="#444", lw=1.5)
        ax.text(0.68 * np.cos(ang), 0.68 * np.sin(ang), str(val),
                ha="center", va="center", fontsize=7, color="#555",
                fontfamily="DejaVu Sans")

    plt.tight_layout(pad=0)
    return fig


def make_radar(score, profile):
    """Creative radar/spider chart showing dimension scores."""
    dims = ["Reacción\nMercado", "Tolerancia\nRiesgo", "Horizonte\nTemporal",
            "Apalancamiento", "Experiencia"]
    base = (score - 11) / 44  # 0-1
    np.random.seed(score)
    vals = np.clip(base + np.random.uniform(-0.15, 0.15, 5), 0, 1)
    vals = vals / vals.max() * base + 0.1  # rescale

    angles = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
    vals_plot = vals.tolist() + [vals[0]]
    angles += angles[:1]

    fig = plt.figure(figsize=(5, 5), facecolor="#0b0f1a")
    ax = fig.add_subplot(111, polar=True, facecolor="#0b0f1a")

    ax.set_facecolor("#0d1320")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(color="#2a3050", linestyle="-", linewidth=0.8, alpha=0.5)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dims, size=8, color="#888", fontfamily="DejaVu Sans")
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["", "", "", ""], size=0)
    ax.set_ylim(0, 1)

    color = profile["color"]
    ax.fill(angles, vals_plot, color=color, alpha=0.2)
    ax.plot(angles, vals_plot, color=color, linewidth=2.5)
    ax.scatter(angles[:-1], vals, s=60, color=color, zorder=5)

    plt.tight_layout()
    return fig


# ─── SESSION STATE ───────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "name" not in st.session_state:
    st.session_state.name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

# ─── EMAIL ───────────────────────────────────────────────────────────────────
def _clean(s: str) -> str:
    """Reemplaza caracteres problemáticos para SMTP ASCII."""
    return (s.replace('\xa0', ' ')   # non-breaking space
             .replace('\u2019', "'") # comilla derecha
             .replace('\u2018', "'") # comilla izquierda
             .replace('\u201c', '"') # comilla doble izquierda
             .replace('\u201d', '"') # comilla doble derecha
             .replace('\u2013', '-') # en dash
             .replace('\u2014', '-') # em dash
             .strip())


def send_results_email(to_email: str, nombre: str, score: int, profile: dict) -> bool:
    try:
        smtp_user = st.secrets["smtp"]["sender"].replace('\xa0', '').strip()
        smtp_pass = st.secrets["smtp"]["password"].replace('\xa0', '').strip()
        smtp_host = st.secrets["smtp"].get("host", "smtp.gmail.com").replace('\xa0', '').strip()
        smtp_port = int(st.secrets["smtp"].get("port", 587))
    except Exception as e:
        return False, f"Secrets no encontrados: {e}"

    nombre   = _clean(nombre)
    to_email = to_email.replace('\xa0', '').replace(' ', '').strip()

    section_rows = ""
    section_map = {}
    for i, q in enumerate(QUESTIONS):
        s = q["section"].split("—")[0].strip()
        if s not in section_map:
            section_map[s] = []
        ans = st.session_state.answers.get(i, (0, 0))
        raw_text = _clean(q["text"])
        raw_ans  = _clean(q["options"][ans[0]])
        section_map[s].append({
            "text": raw_text[:70] + ("…" if len(raw_text) > 70 else ""),
            "answer": raw_ans,
            "points": ans[1],
        })

    for section, items in section_map.items():
        section_rows += f"""
        <tr><td colspan="2" style="padding:10px 16px 4px;font-size:11px;
            color:#c9a84c;font-weight:700;text-transform:uppercase;
            letter-spacing:.1em;background:#0d1117">{section}</td></tr>"""
        for item in items:
            section_rows += f"""
        <tr>
          <td style="padding:6px 16px;font-size:12px;color:#94a3b8;
              border-bottom:1px solid #1e293b">{item['text']}<br>
            <span style="color:#e2e8f0">→ {item['answer']}</span>
          </td>
          <td style="padding:6px 16px;font-size:13px;font-weight:700;
              color:{profile['color']};text-align:right;
              border-bottom:1px solid #1e293b">{item['points']} pts</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8">
<style>
  body{{font-family:'Segoe UI',Arial,sans-serif;background:#0b0f1a;margin:0;padding:0;}}
  .wrap{{max-width:620px;margin:32px auto;background:#0b0f1a;border-radius:16px;
         overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.5);
         border:1px solid rgba(201,168,76,.2);}}
  .header{{background:linear-gradient(135deg,#0b0f1a,#1a1f2e);
           border-bottom:2px solid {profile['color']};padding:32px 32px 24px;text-align:center;}}
  .header h1{{color:#c9a84c;font-size:22px;margin:0 0 6px;font-weight:800;}}
  .header p{{color:rgba(255,255,255,.5);font-size:13px;margin:0;}}
  .body{{padding:28px 32px;}}
  .greeting{{color:#e2e8f0;font-size:15px;margin-bottom:24px;line-height:1.6;}}
  .profile-box{{background:rgba(255,255,255,.04);border:2px solid {profile['color']};
                border-radius:14px;padding:24px;margin-bottom:22px;text-align:center;}}
  .profile-emoji{{font-size:52px;display:block;margin-bottom:10px;}}
  .profile-label{{color:rgba(255,255,255,.45);font-size:11px;text-transform:uppercase;
                  letter-spacing:.12em;margin-bottom:4px;}}
  .profile-name{{color:{profile['color']};font-size:26px;font-weight:800;margin:0 0 12px;}}
  .profile-desc{{color:#94a3b8;font-size:13px;line-height:1.75;text-align:left;}}
  .meta-row{{display:flex;gap:8px;margin:14px 0 0;flex-wrap:wrap;justify-content:center;}}
  .meta-pill{{background:rgba(255,255,255,.06);border-radius:20px;padding:4px 12px;
              font-size:11px;color:#64748b;}}
  .meta-pill span{{color:{profile['color']};font-weight:700;}}
  .score-box{{background:rgba(255,255,255,.05);border-radius:10px;padding:18px;
              text-align:center;margin-bottom:22px;}}
  .score-val{{font-size:42px;font-weight:800;color:{profile['color']};}}
  .score-lbl{{font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:.08em;}}
  .strat{{background:rgba(201,168,76,.07);border:1px solid rgba(201,168,76,.25);
          border-radius:10px;padding:14px 18px;margin-bottom:22px;}}
  .strat-title{{color:#c9a84c;font-size:11px;font-weight:700;text-transform:uppercase;
                letter-spacing:.1em;margin-bottom:6px;}}
  .strat-text{{color:#94a3b8;font-size:13px;line-height:1.6;}}
  .footer{{border-top:1px solid rgba(255,255,255,.07);padding:18px 32px;
           text-align:center;color:#334155;font-size:11px;}}
  table{{width:100%;border-collapse:collapse;margin-bottom:22px;
         background:#0d1117;border-radius:10px;overflow:hidden;}}
</style>
</head>
<body>
<div class="wrap">
  <div class="header">
    <h1>📊 Tu Perfil de Riesgo del Inversionista</h1>
    <p>Encuesta · Posgrado en Finanzas</p>
  </div>
  <div class="body">
    <p class="greeting">Hola <strong style="color:#e2e8f0">{nombre}</strong>,<br>
    completaste la <strong style="color:#c9a84c">Encuesta de Perfil de Riesgo</strong>.
    Aquí están tus resultados:</p>

    <div class="profile-box">
      <span class="profile-emoji">{profile['emoji']}</span>
      <div class="profile-label">Tu perfil de riesgo</div>
      <div class="profile-name">{profile['name']}</div>
      <p class="profile-desc">{profile['desc']}</p>
      <div class="meta-row">
        <div class="meta-pill">⏱ Horizonte: <span>{profile['horizon']}</span></div>
        <div class="meta-pill">〜 Volatilidad: <span>{profile['volatility']}</span></div>
        <div class="meta-pill">📈 Retorno esperado: <span>{profile['expected_return']}</span></div>
      </div>
    </div>

    <div class="score-box">
      <div class="score-val">{score}</div>
      <div class="score-lbl">Puntaje total · de 11 a 55 puntos</div>
    </div>

    <div class="strat">
      <div class="strat-title">📌 Estrategia de portafolio recomendada</div>
      <div class="strat-text">{profile['strategy']}</div>
    </div>

    <table>
      {section_rows}
    </table>
  </div>
  <div class="footer">
    Posgrado en Finanzas · Encuesta de Perfil de Riesgo &nbsp;·&nbsp;
    Este correo fue generado automáticamente a partir de tus respuestas.
  </div>
</div>
</body>
</html>"""

    msg = EmailMessage(policy=email.policy.SMTP)
    msg["Subject"] = f"Perfil {profile['name']} - Encuesta de Perfil de Riesgo - Posgrado en Finanzas"
    msg["From"]    = smtp_user
    msg["To"]      = to_email
    msg.set_content(f"Tu perfil de riesgo: {profile['name']}. Puntaje: {score}.")
    msg.add_alternative(html, subtype="html")

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True, None
    except Exception as e:
        return False, str(e)


# ─── WELCOME PAGE ────────────────────────────────────────────────────────────
def page_welcome():
    # Center column layout
    _, center, _ = st.columns([1, 3, 1])
    with center:
        st.markdown("""
        <div style="text-align:center; padding: 2.5rem 0 1.5rem;">
            <div style="font-size:3.5rem; margin-bottom:0.75rem;">📊</div>
            <h1 style="font-family:'Playfair Display',serif; font-size:2.6rem;
                       color:#e8e6e0; margin:0; line-height:1.1;">
                Perfil de Riesgo<br>
                <span style="color:#c9a84c;">del Inversionista</span>
            </h1>
            <p style="color:#555; font-size:0.78rem; letter-spacing:0.18em;
                      text-transform:uppercase; margin-top:0.9rem; margin-bottom:0;">
                Posgrado en Finanzas
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Info cards
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            <div class="info-card">
                <div class="info-card-icon">🎯</div>
                <div class="info-card-value">11 Preguntas</div>
                <div class="info-card-label">4 dimensiones</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="info-card">
                <div class="info-card-icon">⏱️</div>
                <div class="info-card-value">~5 minutos</div>
                <div class="info-card-label">Sin límite de tiempo</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
            <div class="info-card">
                <div class="info-card-icon">🏆</div>
                <div class="info-card-value">5 Perfiles</div>
                <div class="info-card-label">Resultado inmediato</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <p style="color:#666; font-size:0.88rem; text-align:center;
                  margin: 1.75rem 0 1.5rem; line-height:1.6;">
            Responde con honestidad según tu situación actual.<br>
            No hay respuestas correctas ni incorrectas.
        </p>
        """, unsafe_allow_html=True)

        # Form
        fa, fb = st.columns(2)
        with fa:
            name = st.text_input("Nombre completo", placeholder="Ej. Juan García")
        with fb:
            email = st.text_input("Correo electrónico", placeholder="Ej. juan@ejemplo.com")

        st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
        if st.button("Comenzar encuesta →", use_container_width=True):
            n = name.replace('\xa0', ' ').strip()
            e = email.replace('\xa0', '').replace(' ', '').strip()
            if not n:
                st.error("Por favor ingresa tu nombre.")
            elif not e or "@" not in e or "." not in e.split("@")[-1]:
                st.error("Por favor ingresa un correo válido.")
            else:
                st.session_state.name = n
                st.session_state.user_email = e
                st.session_state.page = "survey"
                st.session_state.current_q = 0
                st.session_state.answers = {}
                st.session_state.email_sent = False
                st.rerun()


# ─── SURVEY PAGE ─────────────────────────────────────────────────────────────
def page_survey():
    q_idx = st.session_state.current_q
    q = QUESTIONS[q_idx]
    total = len(QUESTIONS)
    progress = q_idx / total

    _, center, _ = st.columns([1, 3, 1])
    with center:
        name_str = f"  ·  {st.session_state.name}" if st.session_state.name else ""
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center;
                    margin-bottom:0.75rem;">
            <span style="font-size:0.75rem; color:#555; text-transform:uppercase;
                         letter-spacing:0.1em;">Encuesta{name_str}</span>
            <span style="font-size:0.75rem; color:#c9a84c; font-weight:700;
                         background:rgba(201,168,76,0.1); padding:0.2rem 0.7rem;
                         border-radius:20px; border:1px solid rgba(201,168,76,0.3);">
                {q_idx + 1} / {total}
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.progress(progress)
        st.markdown("<div style='margin-bottom:1.25rem'></div>", unsafe_allow_html=True)

        # Question card
        st.markdown(f"""
        <div class="q-card">
            <div class="section-badge">{q["section"]}</div>
            <div class="q-num">{str(q_idx + 1).zfill(2)}</div>
            <div class="q-text">{q["text"]}</div>
        </div>
        """, unsafe_allow_html=True)

        if q["note"]:
            st.markdown(f'<div class="note-box">💡 {q["note"]}</div>',
                        unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

        default_idx = st.session_state.answers.get(q_idx, None)
        if default_idx is not None:
            default_idx = default_idx[0]
        else:
            default_idx = None

        option_idx = st.radio(
            "Selecciona una opción:",
            options=range(len(q["options"])),
            format_func=lambda i: q["options"][i],
            index=default_idx,
            key=f"radio_{q_idx}",
            label_visibility="collapsed",
        )

        st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

        col_back, col_fwd = st.columns([1, 2])
        with col_back:
            if q_idx > 0:
                if st.button("← Anterior", use_container_width=True):
                    if option_idx is not None:
                        st.session_state.answers[q_idx] = (option_idx, q["points"][option_idx])
                    st.session_state.current_q -= 1
                    st.rerun()
        with col_fwd:
            is_last = q_idx == total - 1
            btn_label = "Ver resultado →" if is_last else "Siguiente →"
            if st.button(btn_label, use_container_width=True):
                if option_idx is None:
                    st.error("Por favor selecciona una opción para continuar.")
                else:
                    st.session_state.answers[q_idx] = (option_idx, q["points"][option_idx])
                    if is_last:
                        st.session_state.page = "result"
                    else:
                        st.session_state.current_q += 1
                    st.rerun()


# ─── RESULT PAGE ─────────────────────────────────────────────────────────────
def page_result():
    score = sum(v[1] for v in st.session_state.answers.values())
    profile = get_profile(score)
    name_str = st.session_state.name or "Estudiante"

    # Header
    st.markdown(f"""
    <div style="text-align:center; padding:1.5rem 0 0.75rem;">
        <p style="color:#555; font-size:0.72rem; text-transform:uppercase;
                  letter-spacing:0.18em; margin-bottom:0.4rem;">Resultado de</p>
        <h2 style="font-family:'Playfair Display',serif; color:#e8e6e0;
                   font-size:2rem; margin:0;">{name_str}</h2>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1: Gauge (left) + Profile summary (right) ──────────────────────
    col_gauge, col_profile = st.columns([3, 2], gap="large")

    with col_gauge:
        fig_gauge = make_gauge(score, profile)
        st.pyplot(fig_gauge, use_container_width=True)
        plt.close(fig_gauge)

    with col_profile:
        st.markdown(f"""
        <div style="background:{profile['bg']}; border:1px solid {profile['color']}55;
                    border-left:4px solid {profile['color']}; border-radius:14px;
                    padding:1.5rem; height:100%; box-sizing:border-box;">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">{profile['emoji']}</div>
            <div style="font-size:0.68rem; color:#666; text-transform:uppercase;
                        letter-spacing:0.12em; margin-bottom:0.2rem;">Tu perfil</div>
            <h3 style="font-family:'Playfair Display',serif; color:{profile['color']};
                       font-size:1.7rem; margin:0 0 1rem;">
                {profile['name']}
            </h3>
            <p style="color:#b0aca4; font-size:0.88rem; line-height:1.6; margin:0;">
                {profile['desc']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

    # ── Row 2: 3 metric pills ───────────────────────────────────────────────
    m1, m2, m3 = st.columns(3, gap="small")
    with m1:
        st.markdown(f"""
        <div class="metric-pill" style="border-top:3px solid {profile['color']};">
            <div class="metric-pill-label">⏱ Horizonte</div>
            <div class="metric-pill-value" style="color:{profile['color']};">
                {profile['horizon']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-pill" style="border-top:3px solid {profile['color']};">
            <div class="metric-pill-label">〜 Volatilidad</div>
            <div class="metric-pill-value" style="color:{profile['color']};">
                {profile['volatility']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-pill" style="border-top:3px solid {profile['color']};">
            <div class="metric-pill-label">📈 Retorno esperado</div>
            <div class="metric-pill-value" style="color:{profile['color']};">
                {profile['expected_return']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

    # ── Row 3: Strategy + Radar ─────────────────────────────────────────────
    col_strat, col_radar = st.columns([3, 2], gap="large")

    with col_strat:
        st.markdown(f"""
        <div style="background:#131929; border:1px solid #2a3050;
                    border-top:3px solid {profile['color']}; border-radius:12px;
                    padding:1.25rem 1.5rem;">
            <div style="font-size:0.68rem; color:#c9a84c; font-weight:700;
                        text-transform:uppercase; letter-spacing:0.12em; margin-bottom:0.6rem;">
                📋 Estrategia de portafolio sugerida
            </div>
            <p style="color:#c8c4bc; font-size:0.92rem; margin:0; line-height:1.6;">
                {profile['strategy']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

        # Answer breakdown
        with st.expander("Ver desglose de respuestas"):
            section_map = {}
            for i, q in enumerate(QUESTIONS):
                s = q["section"].split("—")[0].strip()
                if s not in section_map:
                    section_map[s] = []
                ans = st.session_state.answers.get(i, (0, 0))
                section_map[s].append({
                    "q": i + 1,
                    "text": q["text"][:60] + "…",
                    "answer": q["options"][ans[0]],
                    "points": ans[1],
                })

            for section, items in section_map.items():
                st.markdown(f"**{section}**")
                for item in items:
                    st.markdown(f"""
                    <div style="border-left:2px solid #2a3050; padding:0.4rem 0.75rem;
                                margin:0.25rem 0; font-size:0.85rem; color:#888;">
                        <span style="color:#c9a84c; font-weight:600;">P{item['q']}</span>
                        {item['text']}<br>
                        <span style="color:#e8e6e0;">→ {item['answer']}</span>
                        <span style="color:#c9a84c; float:right;">{item['points']} pts</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("")

    with col_radar:
        st.markdown("""
        <div class="divider-label">Dimensiones evaluadas</div>
        """, unsafe_allow_html=True)
        fig_radar = make_radar(score, profile)
        st.pyplot(fig_radar, use_container_width=True)
        plt.close(fig_radar)

    # ── Profiles scale ──────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="divider-label">Escala de perfiles de riesgo</div>',
                unsafe_allow_html=True)

    total_range = 44  # 55 - 11
    cards_html = '<div style="display:flex; gap:0.5rem; margin-top:0.5rem;">'
    for p in PROFILES:
        is_me = p["name"] == profile["name"]
        fill_pct = int(((p["range"][1] - p["range"][0]) / total_range) * 100)
        border = f"2px solid {p['color']}" if is_me else "1px solid #2a3050"
        bg = p["bg"] if is_me else "#0d1117"
        you_badge = f'<div style="font-size:0.6rem; color:{p["color"]}; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.3rem;">&#9658; Tú</div>' if is_me else ""
        fw = "700" if is_me else "400"
        op = "1" if is_me else "0.4"
        cards_html += f'''<div style="flex:1; background:{bg}; border:{border}; border-radius:10px; padding:0.85rem 0.75rem; text-align:center;">
  <div style="font-size:1.4rem;">{p["emoji"]}</div>
  {you_badge}
  <div style="font-size:0.78rem; font-weight:{fw}; color:{p["color"]}; margin:0.3rem 0 0.2rem; line-height:1.2;">{p["name"]}</div>
  <div style="font-size:0.68rem; color:#888; margin-bottom:0.5rem;">{p["range"][0]}&#8211;{p["range"][1]} pts</div>
  <div style="height:4px; background:#1e2435; border-radius:2px; overflow:hidden;">
    <div style="width:{fill_pct}%; height:100%; background:{p["color"]}; opacity:{op}; border-radius:2px;"></div>
  </div>
</div>'''
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    # ── Email ───────────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
    if not st.session_state.email_sent:
        with st.spinner("Enviando resultados a tu correo..."):
            ok, err_msg = send_results_email(
                to_email=st.session_state.user_email,
                nombre=name_str,
                score=score,
                profile=profile,
            )
        if ok:
            st.session_state.email_sent = True
            st.success(f"📧 Resultados enviados a **{st.session_state.user_email}**")
        else:
            st.warning(f"⚠️ No se pudo enviar el correo: `{err_msg}`")

    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([2, 3, 2])
    with btn_col:
        if st.button("↩ Reiniciar encuesta", use_container_width=True):
            st.session_state.page = "welcome"
            st.session_state.answers = {}
            st.session_state.current_q = 0
            st.session_state.name = ""
            st.session_state.user_email = ""
            st.session_state.email_sent = False
            st.rerun()

    st.markdown("""
    <p style="text-align:center; color:#333; font-size:0.72rem; margin-top:1rem;">
        Este resultado es orientativo. Consulta con un asesor financiero profesional.
    </p>
    """, unsafe_allow_html=True)


# ─── ROUTER ──────────────────────────────────────────────────────────────────
if st.session_state.page == "welcome":
    page_welcome()
elif st.session_state.page == "survey":
    page_survey()
elif st.session_state.page == "result":
    page_result()
