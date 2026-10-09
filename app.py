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
from html import escape

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
    background-color: #f7f5f1;
    color: #1c1a18;
}
.stApp { background-color: #f7f5f1; }
.main .block-container { padding: 2rem 2rem 4rem; max-width: 900px; margin: 0 auto; }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Progress bar */
.stProgress > div > div { background: linear-gradient(90deg, #c9a84c, #f0d080); border-radius: 4px; }
.stProgress > div { background: #e2dfd8; border-radius: 4px; }

/* Radio buttons */
div[data-testid="stRadio"] > label {
    font-family: 'DM Sans', sans-serif;
    color: #6a6865;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
div[data-testid="stRadio"] > div {
    background: #eeeae3;
    border: 1px solid #d5d2cb;
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
    color: #1c1a18 !important;
    font-size: 0.95rem !important;
    line-height: 1.4 !important;
}
div[data-testid="stRadio"] label:hover {
    background: #e2dfd8 !important;
    border-color: #c9a84c !important;
    color: #8a6a10 !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"] input:checked + div {
    background: #c9a84c !important;
}
div[data-testid="stRadio"] label p {
    color: #1c1a18 !important;
}
div[data-testid="stRadio"] label span {
    color: #1c1a18 !important;
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
    color: #1c1a18;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #f0d080, #c9a84c);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(201,168,76,0.35);
}

/* Divider */
hr { border-color: #d8d5ce; }

/* Metric */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #d8d5ce;
    border-radius: 12px;
    padding: 1rem;
}

/* Note box */
.note-box {
    background: #ffffff;
    border-left: 3px solid #c9a84c;
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0 1.25rem 0;
    font-size: 0.85rem;
    color: #6a6560;
    font-style: italic;
}

/* Question card */
.q-card {
    background: #ffffff;
    border: 1px solid #d8d5ce;
    border-top: 3px solid #c9a84c;
    border-radius: 0 0 12px 12px;
    padding: 1.5rem 1.75rem 1.75rem;
    margin-bottom: 0.5rem;
}

/* Section badge */
.section-badge {
    display: inline-block;
    background: rgba(201,168,76,0.12);
    color: #8a6a10;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    border: 1px solid rgba(201,168,76,0.4);
    margin-bottom: 0.75rem;
}

/* Question number */
.q-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 900;
    color: rgba(201,168,76,0.25);
    line-height: 1;
    margin-bottom: 0.25rem;
}

/* Question text */
.q-text {
    font-size: 1.1rem;
    font-weight: 500;
    color: #1c1a18;
    line-height: 1.5;
    margin-bottom: 0.25rem;
}

/* Info card */
.info-card {
    background: #ffffff;
    border: 1px solid #d8d5ce;
    border-top: 3px solid #c9a84c;
    border-radius: 12px;
    padding: 1.5rem 1rem;
    text-align: center;
}
.info-card-icon { font-size: 1.8rem; margin-bottom: 0.6rem; }
.info-card-value {
    font-size: 0.8rem;
    color: #8a6a10;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.2rem;
}
.info-card-label { font-size: 0.8rem; color: #7a7775; }

/* Metric pill */
.metric-pill {
    background: #ffffff;
    border: 1px solid #d8d5ce;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.metric-pill-label {
    font-size: 0.65rem;
    color: #9a9795;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}
.metric-pill-value {
    font-size: 1rem;
    font-weight: 600;
    color: #1c1a18;
}

/* Profile scale row */
.scale-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #f2f0eb;
    border: 1px solid #d8d5ce;
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
    background: #e2dfd8;
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
    color: #9a9795;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    text-align: center;
    margin: 1.25rem 0 0.75rem;
}

/* Input styling */
div[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid #d8d5ce !important;
    border-radius: 8px !important;
    color: #1c1a18 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.6rem 0.85rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #c9a84c !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.2) !important;
}
div[data-testid="stTextInput"] label {
    color: #7a7775 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* Section title (results) */
.sec-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.45rem;
    color: #1c1a18;
    margin: 1.75rem 0 0.25rem;
}
.sec-sub { color: #7a7775; font-size: 0.88rem; margin-bottom: 1rem; }

/* Tip cards */
.tip-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 0.75rem; }
.tip-card {
    background: #ffffff;
    border: 1px solid #d8d5ce;
    border-radius: 12px;
    padding: 1rem 1.1rem 1.1rem;
}
.tip-head { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.45rem; }
.tip-icon { font-size: 1.35rem; }
.tip-title { font-weight: 600; color: #1c1a18; font-size: 0.95rem; line-height: 1.3; }
.tip-body { color: #5a5754; font-size: 0.86rem; line-height: 1.55; }
.tip-tag {
    display: inline-block; font-size: 0.62rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 0.15rem 0.55rem; border-radius: 20px; margin-bottom: 0.45rem;
}

/* Insight banner */
.insight {
    border-radius: 12px; padding: 1rem 1.2rem; margin: 0.75rem 0;
    font-size: 0.9rem; line-height: 1.55; border: 1px solid;
}
.insight b { font-weight: 700; }

/* Big number */
.big-num { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 900; line-height: 1.1; }
.big-lbl { font-size: 0.68rem; color: #9a9795; text-transform: uppercase; letter-spacing: 0.1em; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 0.4rem; }
.stTabs [data-baseweb="tab"] {
    background: #eeeae3; border-radius: 8px 8px 0 0; padding: 0.55rem 1rem;
    font-weight: 600; color: #6a6865;
}
.stTabs [aria-selected="true"] { background: #ffffff; color: #8a6a10; }
</style>
""", unsafe_allow_html=True)

# ─── DATA ────────────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "id": "caida_20",
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
        "id": "sube_25",
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
        "id": "perdida_max",
        "section": "II — Tolerancia al riesgo y objetivos",
        "text": "Tiene un portafolio de COP $100.000.000. ¿Cuál es la máxima caída en un año que soportaría sin cambiar su estrategia?",
        "options": [
            "−5%: ver el portafolio en $95 millones ya me quitaría el sueño.",
            "−10%: aguantaría hasta $90 millones.",
            "−20%: aguantaría hasta $80 millones si el plan es de largo plazo.",
            "−35% o más: podría ver $65 millones y seguir con el plan.",
        ],
        "points": [1, 2, 4, 5],
        "loss": [5, 10, 20, 35],
        "note": "Piense en pesos, no en porcentajes. Así se sienten las caídas en la vida real.",
    },
    {
        "id": "horizonte",
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
        "id": "premio",
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
        "id": "deuda",
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
        "id": "acciones_empresa",
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
    {
        "id": "fondo_emergencia",
        "section": "V — Capacidad financiera",
        "text": "Si mañana perdiera su fuente principal de ingresos, ¿cuántos meses de gastos cubre su fondo de emergencia?",
        "options": [
            "No tengo fondo de emergencia.",
            "Entre 1 y 3 meses.",
            "Entre 3 y 6 meses.",
            "Más de 6 meses.",
        ],
        "points": [1, 2, 4, 5],
        "note": "El fondo de emergencia es dinero líquido y seguro, separado de sus inversiones.",
    },
    {
        "id": "ingresos",
        "section": "V — Capacidad financiera",
        "text": "¿Qué tan estables son sus ingresos?",
        "options": [
            "Inestables: dependo de una sola fuente incierta.",
            "Algo variables: contrato a término, comisiones o trabajo independiente.",
            "Estables: contrato indefinido o pensión.",
            "Muy estables y diversificados: tengo varias fuentes de ingreso.",
        ],
        "points": [1, 2, 4, 5],
        "note": None,
    },
    {
        "id": "impacto_perdida",
        "section": "V — Capacidad financiera",
        "text": "Si perdiera el 30% del dinero que piensa invertir, ¿cómo afectaría su nivel de vida?",
        "options": [
            "Tendría que cambiar mi estilo de vida de forma importante.",
            "Tendría que recortar gastos importantes por un tiempo.",
            "Sería doloroso, pero mi día a día no cambiaría.",
            "No tendría ningún impacto en mi nivel de vida.",
        ],
        "points": [1, 2, 4, 5],
        "note": "Esta pregunta mide su capacidad de asumir riesgo, que es distinta de las ganas de asumirlo.",
    },
    {
        "id": "fomo",
        "section": "VI — Psicología del inversionista",
        "text": "Una criptomoneda subió 300% en un mes y todos en redes sociales hablan de ella. ¿Qué hace?",
        "options": [
            "Nada. Si ya subió tanto, el riesgo es enorme.",
            "La investigo a fondo y, si me convence, invierto máximo el 5% de mi portafolio.",
            "Invierto una parte importante antes de que siga subiendo.",
        ],
        "points": [1, 3, 5],
        "note": None,
    },
    {
        "id": "recesion",
        "section": "VI — Psicología del inversionista",
        "text": "Los noticieros anuncian una posible recesión. Su portafolio todavía no ha caído. ¿Qué hace?",
        "options": [
            "Paso todo a efectivo o CDT de inmediato.",
            "Reduzco un poco la exposición a acciones.",
            "Mantengo mi plan: ya había considerado escenarios así.",
            "Preparo liquidez para comprar más si el mercado cae.",
        ],
        "points": [1, 2, 4, 5],
        "note": None,
    },
    {
        "id": "confianza",
        "section": "VI — Psicología del inversionista",
        "text": "¿Cómo calificaría su habilidad para escoger acciones que le ganen al mercado?",
        "options": [
            "Por debajo del promedio: prefiero fondos indexados o delegar.",
            "Promedio: combino índices con algunas apuestas propias.",
            "Superior: puedo superar al mercado de forma consistente.",
        ],
        "points": [1, 3, 5],
        "note": None,
    },
]

QIDX = {q["id"]: i for i, q in enumerate(QUESTIONS) if "id" in q}
N_Q = len(QUESTIONS)
MIN_SCORE = sum(min(q["points"]) for q in QUESTIONS)
MAX_SCORE = sum(max(q["points"]) for q in QUESTIONS)

# Preguntas que miden la CAPACIDAD de asumir riesgo; el resto (salvo experiencia) mide la DISPOSICIÓN.
CAPACITY_IDS = {"horizonte", "fondo_emergencia", "ingresos", "impacto_perdida"}

DIMENSIONS = {
    "I": "Reacción al\nmercado",
    "II": "Tolerancia y\nobjetivos",
    "III": "Apalancamiento\ny decisiones",
    "IV": "Experiencia",
    "V": "Capacidad\nfinanciera",
    "VI": "Psicología",
}

PROFILES = [
    {
        "cut": 0.15,
        "name": "Conservador",
        "alias": "El Guardián",
        "emoji": "🛡️",
        "color": "#1a6fcc",
        "bg": "#e8f2ff",
        "desc": "Prioriza la preservación del capital por encima de todo. Prefiere instrumentos de renta fija, mercado monetario y depósitos a término. Tiene muy baja tolerancia a la volatilidad y busca certeza sobre el valor de su capital.",
        "strategy": "CDTs, bonos del gobierno, fondos de mercado monetario, cuentas de ahorro de alto rendimiento.",
        "horizon": "Corto plazo (< 3 años)",
        "volatility": "Muy baja",
        "expected_return": "Inflación ± 1%",
        "real_return": 0.005,
        "drawdown": 3,
        "allocation": {"Liquidez": 40, "Renta fija": 60},
        "tips": [
            ("🪜", "Escalera de CDTs", "Divida el capital en 4 CDTs a 3, 6, 9 y 12 meses. Cada trimestre se vence uno: tiene liquidez y reinvierte a la tasa del momento."),
            ("🔎", "Mire la tasa real, no la nominal", "Un CDT al 9% E.A. con inflación del 5% le deja (1,09 / 1,05) − 1 ≈ 3,8% real. Si la tasa real es negativa, está perdiendo poder de compra."),
            ("💧", "Saque la liquidez de la cuenta de ahorros", "Un fondo de inversión colectiva (FIC) a la vista suele pagar más que una cuenta de ahorros y le permite retirar en uno o dos días."),
            ("🧾", "Cuente los costos ocultos", "Revise la retención en la fuente sobre rendimientos y el 4x1000 cada vez que mueva dinero. Mover plata seguido se come el rendimiento."),
            ("🌱", "Una pizca de crecimiento", "Un 5% a 10% en un ETF de índice amplio protege contra la inflación en el largo plazo sin cambiar el carácter de su portafolio."),
        ],
    },
    {
        "cut": 0.38,
        "name": "Moderado-Conservador",
        "alias": "El Navegante",
        "emoji": "⚓",
        "color": "#0e9e73",
        "bg": "#e0f9f3",
        "desc": "Acepta un nivel limitado de riesgo a cambio de rendimientos ligeramente superiores a los del mercado monetario. Prefiere portafolios con predominancia de renta fija y una pequeña exposición a renta variable.",
        "strategy": "70-80% renta fija (bonos grado inversión, CDTs) + 20-30% renta variable diversificada (ETFs de índice).",
        "horizon": "Mediano plazo (3–5 años)",
        "volatility": "Baja",
        "expected_return": "Inflación + 2–3%",
        "real_return": 0.025,
        "drawdown": 10,
        "allocation": {"Liquidez": 5, "Renta fija": 70, "Renta variable": 25},
        "tips": [
            ("🛡️", "Protéjase de la inflación con TES UVR", "Los TES en UVR ajustan el capital por inflación. Son un buen ancla para la parte de renta fija."),
            ("📦", "Renta variable vía ETFs", "Para el 20–30% en acciones use ETFs de índice: diversifica en un solo clic. Busque costos totales (TER) por debajo de 0,3% anual."),
            ("🔁", "Aporte automático cada mes", "Programe un aporte fijo mensual (DCA). Compra más unidades cuando el mercado baja y elimina la tentación de adivinar el momento."),
            ("⚖️", "Rebalanceo una vez al año", "Si la renta variable pasa de 25% a 32% por una subida, venda el exceso y vuelva a su peso objetivo. Es vender caro de forma disciplinada."),
            ("📅", "Calce plazos con metas", "Asigne cada meta a un instrumento con vencimiento parecido: el dinero de la cuota inicial en 2 años no va en acciones."),
        ],
    },
    {
        "cut": 0.62,
        "name": "Moderado",
        "alias": "El Estratega",
        "emoji": "⚖️",
        "color": "#8a6a10",
        "bg": "#fdf8e0",
        "desc": "Busca un crecimiento equilibrado del capital. Tolera fluctuaciones moderadas en el corto plazo y combina renta fija con renta variable en proporciones similares. Su horizonte es de mediano a largo plazo.",
        "strategy": "50% renta variable (acciones, ETFs globales) + 45% renta fija + 5% liquidez. Los fondos balanceados son una forma simple de lograrlo.",
        "horizon": "Mediano-largo plazo (5–10 años)",
        "volatility": "Moderada",
        "expected_return": "Inflación + 4–6%",
        "real_return": 0.05,
        "drawdown": 20,
        "allocation": {"Liquidez": 5, "Renta fija": 45, "Renta variable": 50},
        "tips": [
            ("🌎", "Diversifique fuera de Colombia", "Colombia es una fracción mínima de la capitalización bursátil mundial. Un ETF global (por ejemplo, uno que replique el MSCI ACWI) le da miles de empresas."),
            ("💵", "El dólar como amortiguador", "Tener parte del portafolio en activos en USD suaviza los golpes: cuando hay crisis local, el peso suele devaluarse y esos activos suben en pesos."),
            ("📏", "Rebalanceo por bandas", "Fije bandas de ±5 puntos alrededor de su 50/50. Solo rebalancee cuando una clase de activo se salga de la banda."),
            ("🎯", "Mídase contra un benchmark", "Compare su resultado contra una mezcla simple, por ejemplo 50% índice global de acciones + 50% índice de TES. Si no le gana, indexe."),
            ("🧮", "Use la regla del 72", "Divida 72 por el retorno anual para saber en cuántos años se duplica su dinero: al 8%, en unos 9 años."),
        ],
    },
    {
        "cut": 0.82,
        "name": "Moderado-Agresivo",
        "alias": "El Explorador",
        "emoji": "🚀",
        "color": "#c95f00",
        "bg": "#fff3e0",
        "desc": "Dispuesto a asumir un riesgo considerable para obtener rendimientos superiores al mercado. Entiende y acepta la volatilidad como parte del proceso de inversión. Tiene horizonte de largo plazo.",
        "strategy": "70% renta variable (acciones individuales, ETFs temáticos, REITs) + 30% alternativos y renta fija.",
        "horizon": "Largo plazo (10–20 años)",
        "volatility": "Alta",
        "expected_return": "Inflación + 6–10%",
        "real_return": 0.08,
        "drawdown": 30,
        "allocation": {"Liquidez": 5, "Renta fija": 10, "Renta variable": 70, "Alternativos": 15},
        "tips": [
            ("🪐", "Núcleo y satélites", "Ponga 70% en un núcleo de ETFs de índice y 30% en satélites: acciones individuales, temáticos o factores. Así sus apuestas no hunden el plan."),
            ("✂️", "Tope por posición", "Ninguna acción individual debe pesar más de 5% a 10% del portafolio. Una mala noticia no debe poder borrar un año de trabajo."),
            ("📝", "Escriba su plan de caída hoy", "Deje por escrito qué hará si el portafolio cae 25%: ¿rebalancear, comprar, esperar? Decidir en calma evita decidir en pánico."),
            ("🧪", "Pruebe con factores", "ETFs de value, momentum o quality permiten buscar primas de riesgo documentadas sin elegir acciones una por una."),
            ("🏢", "Alternativos con lupa", "En inmobiliarios, deuda privada o private equity revise siempre la liquidez (¿cuándo puede salir?) y las comisiones totales."),
        ],
    },
    {
        "cut": 1.01,
        "name": "Agresivo",
        "alias": "El Cazador de Alfa",
        "emoji": "⚡",
        "color": "#c4003a",
        "bg": "#ffe8ef",
        "desc": "Alta tolerancia al riesgo. Busca maximizar el retorno absoluto con plena consciencia de las pérdidas potenciales. Invierte en renta variable concentrada, alternativos sofisticados y puede usar apalancamiento.",
        "strategy": "Renta variable concentrada, derivados, private equity, venture capital, hedge funds, activos alternativos.",
        "horizon": "Largo plazo (> 20 años)",
        "volatility": "Muy alta",
        "expected_return": "Inflación + 10%+",
        "real_return": 0.10,
        "drawdown": 45,
        "allocation": {"Liquidez": 5, "Renta fija": 5, "Renta variable": 70, "Alternativos": 20},
        "tips": [
            ("🎲", "Tamaño de posición con Kelly fraccionado", "Use una fracción (¼ o ½) del criterio de Kelly para dimensionar apuestas. El Kelly completo maximiza el crecimiento pero con caídas brutales."),
            ("📉", "Calcule el margin call antes de entrar", "Con apalancamiento 2x, una caída de 50% borra el 100% del capital. Sepa a qué precio le piden garantías antes de abrir la posición."),
            ("🛟", "Compre seguros baratos", "Puts fuera del dinero sobre su posición principal acotan la pérdida máxima. Piense en la prima como el costo de dormir tranquilo."),
            ("📓", "Diario de inversión", "Para cada operación anote la tesis, el precio objetivo y la condición de salida. Revíselo cada trimestre: así se detectan los sesgos propios."),
            ("🧯", "Riesgo total, no solo retorno", "Mida el drawdown máximo y el Sharpe de su portafolio. Ganar 40% con caídas de 60% no es una estrategia repetible."),
        ],
    },
]

GOLDEN_RULES = [
    ("🧱", "Primero el colchón", "Antes de asumir riesgo, tenga de 3 a 6 meses de gastos en algo líquido y seguro. Sin colchón, cualquier emergencia lo obliga a vender en el peor momento."),
    ("💸", "Los costos se componen", "Una comisión de 1% anual durante 30 años se lleva cerca de una cuarta parte del capital final (0,99³⁰ ≈ 0,74). Pregunte siempre el costo total."),
    ("⏳", "El tiempo hace el trabajo pesado", "El interés compuesto premia empezar temprano más que aportar mucho. Diez años antes valen más que el doble de aporte."),
    ("🧭", "Riesgo que no se ve", "Concentrar su sueldo y sus inversiones en la misma empresa o el mismo país duplica el riesgo, aunque no se note en el extracto."),
]

# ─── HELPERS ────────────────────────────────────────────────────────────────
def md(html_str):
    """Renderiza HTML en una sola línea para que Markdown no lo convierta en bloque de código."""
    st.markdown(" ".join(line.strip() for line in html_str.splitlines()), unsafe_allow_html=True)


def norm(score):
    return (score - MIN_SCORE) / (MAX_SCORE - MIN_SCORE)


def profile_index(score):
    p = norm(score)
    for i, prof in enumerate(PROFILES):
        if p < prof["cut"]:
            return i
    return len(PROFILES) - 1


def get_profile(score):
    return PROFILES[profile_index(score)]


def profile_ranges():
    """Rango de puntos (enteros) de cada perfil según el número actual de preguntas."""
    span = MAX_SCORE - MIN_SCORE
    out, lo = [], MIN_SCORE
    for prof in PROFILES:
        hi = min(MAX_SCORE, math.ceil(MIN_SCORE + prof["cut"] * span) - 1)
        out.append((lo, hi))
        lo = hi + 1
    return out


def answer_opt(qid):
    a = st.session_state.answers.get(QIDX[qid])
    return a[0] if a else None


def dimension_scores():
    """Puntaje 0–1 por dimensión, calculado con las respuestas reales."""
    acc = {k: [] for k in DIMENSIONS}
    for i, q in enumerate(QUESTIONS):
        key = q["section"].split("—")[0].strip()
        a = st.session_state.answers.get(i)
        if a:
            lo, hi = min(q["points"]), max(q["points"])
            acc[key].append((a[1] - lo) / (hi - lo))
    return {k: (sum(v) / len(v) if v else 0) for k, v in acc.items()}


def willingness_capacity():
    will, cap = [], []
    for i, q in enumerate(QUESTIONS):
        a = st.session_state.answers.get(i)
        if not a or q["section"].startswith("IV"):
            continue
        lo, hi = min(q["points"]), max(q["points"])
        v = (a[1] - lo) / (hi - lo)
        (cap if q.get("id") in CAPACITY_IDS else will).append(v)
    return (sum(will) / len(will) if will else 0), (sum(cap) / len(cap) if cap else 0)


def bias_insights(profile):
    """Alertas y consejos personalizados según respuestas puntuales."""
    out = []
    o = answer_opt
    if o("fondo_emergencia") == 0:
        out.append(("🧱", "Prioridad número uno: el fondo de emergencia",
                    "Sin colchón, una emergencia lo obliga a vender inversiones en el peor momento. Antes de asumir riesgo, junte 3 a 6 meses de gastos en un FIC a la vista o un CDT corto.",
                    "Capacidad", "#c4003a"))
    if o("caida_20") == 0:
        out.append(("😨", "Aversión a las pérdidas",
                    "Vender después de una caída convierte una pérdida temporal en permanente. Antes de invertir, anote cuánto puede caer su portafolio en un mal año y decida desde ya que esa caída es parte del plan.",
                    "Sesgo", "#c95f00"))
    if o("sube_25") == 0:
        out.append(("🏃", "Efecto disposición",
                    "Tendemos a vender rápido lo que gana y aferrarnos a lo que pierde. Pregúntese: si no lo tuviera, ¿lo compraría hoy a este precio? Decida por fundamentos, no por el precio al que compró.",
                    "Sesgo", "#c95f00"))
    if o("fomo") == 2:
        out.append(("🔥", "FOMO y efecto manada",
                    "Cuando todos hablan de un activo, buena parte de la subida ya ocurrió. Regla práctica: nada especulativo por encima del 5% del portafolio y nunca con dinero que necesite en 3 años.",
                    "Sesgo", "#c95f00"))
    if o("recesion") == 0:
        out.append(("⏱️", "Tentación de adivinar el mercado",
                    "Salir por completo ante una noticia obliga a acertar dos veces: cuándo salir y cuándo volver. Los mejores días del mercado suelen llegar justo después de los peores, y perdérselos reduce mucho el retorno de largo plazo.",
                    "Sesgo", "#c95f00"))
    if o("confianza") == 2:
        out.append(("🦚", "Sobreconfianza",
                    "La gran mayoría de los fondos administrados por profesionales no le gana a su índice en periodos de 15 años, según los informes SPIVA. Ponga sus apuestas propias en un satélite pequeño y mida el resultado.",
                    "Sesgo", "#c95f00"))
    if o("deuda") == 3:
        out.append(("🧨", "Apalancamiento máximo",
                    "Con deuda, las pérdidas también se multiplican: con apalancamiento 2x, una caída del 50% borra todo el capital. Defina un apalancamiento máximo y el precio de margin call antes de entrar.",
                    "Riesgo", "#c4003a"))
    if o("acciones_empresa") == 3:
        out.append(("🏢", "Concentración en su empleador",
                    "Si la empresa tiene problemas, puede perder el empleo y la inversión al mismo tiempo. Limite la exposición a su empleador a una fracción pequeña del patrimonio.",
                    "Riesgo", "#c4003a"))
    if o("premio") == 0:
        out.append(("🔒", "Prima por certeza",
                    "Prefirió el pago seguro aunque las otras opciones tenían mayor valor esperado. Es válido, pero en 20 o 30 años esa preferencia por certeza tiene un costo grande en crecimiento.",
                    "Perfil", "#1a6fcc"))
    tol = answer_opt("perdida_max")
    if tol is not None:
        tol_pct = QUESTIONS[QIDX["perdida_max"]]["loss"][tol]
        if profile["drawdown"] > tol_pct:
            out.append(("📉", "Su portafolio modelo podría caer más de lo que tolera",
                        f"En un año muy malo, un portafolio {profile['name'].lower()} podría caer cerca de {profile['drawdown']}%, y usted dijo que soporta {tol_pct}%. Considere una mezcla un escalón más conservadora o prepárese mentalmente para esa caída.",
                        "Coherencia", "#c4003a"))
    return out


def project(monthly, years, initial, annual_real):
    """Valor futuro (en pesos de hoy) con aportes mensuales al inicio de cada mes."""
    r = (1 + annual_real) ** (1 / 12) - 1
    vals, v = [initial], initial
    for _ in range(int(years * 12)):
        v = (v + monthly) * (1 + r)
        vals.append(v)
    return vals


def fmt_cop(x):
    if abs(x) >= 1e9:
        return f"${x/1e9:,.2f} mil M".replace(",", "X").replace(".", ",").replace("X", ".")
    if abs(x) >= 1e6:
        return f"${x/1e6:,.1f} M".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"${x:,.0f}".replace(",", ".")


def make_gauge(score, profile):
    """Velocímetro de riesgo."""
    fig = plt.figure(figsize=(10, 6), facecolor="#f7f5f1")
    ax = fig.add_subplot(111, facecolor="#f7f5f1")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.6, 1.45)
    ax.set_aspect("equal")
    ax.axis("off")

    for r in np.linspace(1.25, 1.0, 8):
        ax.add_patch(plt.Circle((0, 0), r, color="#c9a84c", alpha=0.02 * (1.35 - r), zorder=0))

    labels = ["Conservador", "Mod-Conservador", "Moderado", "Mod-Agresivo", "Agresivo"]
    cuts = [0] + [min(p["cut"], 1.0) for p in PROFILES]
    active = profile_index(score)

    for i, p in enumerate(PROFILES):
        a0, a1 = 180 - cuts[i] * 180, 180 - cuts[i + 1] * 180
        is_active = i == active
        theta = np.linspace(np.radians(a0), np.radians(a1), 60)
        ax.plot(np.cos(theta), np.sin(theta), color=p["color"],
                linewidth=28 if is_active else 20, alpha=1.0 if is_active else 0.35,
                solid_capstyle="butt", zorder=3)
        mid = np.radians((a0 + a1) / 2)
        ax.text(1.12 * np.cos(mid), 1.12 * np.sin(mid), labels[i], ha="center", va="center",
                fontsize=6.5, color=p["color"] if is_active else "#aaa9a5",
                fontweight="bold" if is_active else "normal", fontfamily="DejaVu Sans")

    theta = np.linspace(np.radians(180), np.radians(0), 120)
    ax.plot(np.cos(theta) * 0.72, np.sin(theta) * 0.72, color="#e2dfd8", linewidth=22, zorder=2)

    needle_rad = np.radians(180 - norm(score) * 180)
    nx, ny = 0.82 * np.cos(needle_rad), 0.82 * np.sin(needle_rad)
    ax.annotate("", xy=(nx * 0.98, ny * 0.98), xytext=(0, -0.04),
                arrowprops=dict(arrowstyle="->, head_width=0.04, head_length=0.04",
                                color="#000000", lw=3, alpha=0.3))
    ax.annotate("", xy=(nx, ny), xytext=(0, -0.04),
                arrowprops=dict(arrowstyle="->, head_width=0.045, head_length=0.045",
                                color="#1c1a18", lw=2.5))
    ax.add_patch(plt.Circle((0, 0), 0.06, color="#c9a84c", zorder=10))
    ax.add_patch(plt.Circle((0, 0), 0.035, color="#f7f5f1", zorder=11))

    ax.text(0, -0.22, str(score), ha="center", va="center", fontsize=42, fontweight="bold",
            color=profile["color"], fontfamily="DejaVu Sans", zorder=12)
    ax.text(0, -0.42, f"puntos de {MAX_SCORE}", ha="center", va="center",
            fontsize=9, color="#9a9795", fontfamily="DejaVu Sans")
    ax.text(0, 1.36, profile["name"].upper(), ha="center", va="center", fontsize=14,
            fontweight="bold", color=profile["color"], fontfamily="DejaVu Sans",
            bbox=dict(boxstyle="round,pad=0.4", facecolor=profile["bg"],
                      edgecolor=profile["color"], alpha=0.9, linewidth=1.5))

    marks = sorted({MIN_SCORE, MAX_SCORE} | {lo for lo, _ in profile_ranges()})
    for val in marks:
        ang = np.radians(180 - norm(val) * 180)
        ax.plot([0.88 * np.cos(ang), 0.95 * np.cos(ang)], [0.88 * np.sin(ang), 0.95 * np.sin(ang)],
                color="#b0aea8", lw=1.5)
        ax.text(0.68 * np.cos(ang), 0.68 * np.sin(ang), str(val), ha="center", va="center",
                fontsize=7, color="#7a7775", fontfamily="DejaVu Sans")

    plt.tight_layout(pad=0)
    return fig


def make_radar(profile):
    """Radar con el puntaje real de cada dimensión."""
    scores = dimension_scores()
    dims = list(DIMENSIONS.values())
    vals = [0.08 + 0.92 * scores[k] for k in DIMENSIONS]

    angles = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
    vals_plot = vals + [vals[0]]
    angles_plot = angles + angles[:1]

    fig = plt.figure(figsize=(5, 5), facecolor="#f7f5f1")
    ax = fig.add_subplot(111, polar=True, facecolor="#eeeae3")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(color="#d8d5ce", linestyle="-", linewidth=0.8, alpha=0.7)
    ax.set_xticks(angles)
    ax.set_xticklabels(dims, size=8, color="#4a4845", fontfamily="DejaVu Sans")
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels([])
    ax.set_ylim(0, 1)

    color = profile["color"]
    ax.fill(angles_plot, vals_plot, color=color, alpha=0.2)
    ax.plot(angles_plot, vals_plot, color=color, linewidth=2.5)
    ax.scatter(angles, vals, s=60, color=color, zorder=5)
    plt.tight_layout()
    return fig


def make_matrix(will, cap, profile):
    """Mapa disposición (eje Y) vs. capacidad (eje X) de asumir riesgo."""
    fig, ax = plt.subplots(figsize=(5, 5), facecolor="#f7f5f1")
    ax.set_facecolor("#f7f5f1")
    quads = [  # (x = capacidad, y = disposición)
        (0, 0, "#e8f2ff", "Protección\nprimero"),
        (0.5, 0, "#e0f9f3", "Espacio\npara crecer"),
        (0, 0.5, "#ffe8ef", "Zona de\nalerta"),
        (0.5, 0.5, "#fff3e0", "Listo para\nel riesgo"),
    ]
    for x0, y0, c, label in quads:
        ax.add_patch(mpatches.Rectangle((x0, y0), 0.5, 0.5, facecolor=c, edgecolor="#f7f5f1", lw=3))
        ax.text(x0 + 0.25, y0 + 0.25, label, ha="center", va="center", fontsize=9,
                color="#6a6865", fontfamily="DejaVu Sans", fontweight="bold", alpha=0.85)
    ax.scatter([cap], [will], s=380, color=profile["color"], edgecolor="white", linewidth=3, zorder=5)
    ax.annotate("Usted", (cap, will), xytext=(0, 18), textcoords="offset points", ha="center",
                fontsize=9, fontweight="bold", color=profile["color"], fontfamily="DejaVu Sans")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([0.08, 0.92])
    ax.set_xticklabels(["Baja", "Alta"], fontsize=8, color="#7a7775")
    ax.set_yticks([0.08, 0.92])
    ax.set_yticklabels(["Baja", "Alta"], fontsize=8, color="#7a7775", rotation=90, va="center")
    ax.set_xlabel("Capacidad de asumir riesgo", fontsize=9, color="#4a4845")
    ax.set_ylabel("Disposición a asumir riesgo", fontsize=9, color="#4a4845")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    plt.tight_layout()
    return fig


ALLOC_COLORS = {"Liquidez": "#9fb8d6", "Renta fija": "#1a6fcc", "Renta variable": "#c9a84c", "Alternativos": "#c4003a"}


def make_donut(profile):
    alloc = profile["allocation"]
    fig, ax = plt.subplots(figsize=(4.6, 4.6), facecolor="#f7f5f1")
    wedges, _ = ax.pie(list(alloc.values()), colors=[ALLOC_COLORS[k] for k in alloc],
                       startangle=90, counterclock=False,
                       wedgeprops=dict(width=0.32, edgecolor="#f7f5f1", linewidth=3))
    for w, (k, v) in zip(wedges, alloc.items()):
        ang = np.radians((w.theta1 + w.theta2) / 2)
        ax.text(0.84 * np.cos(ang), 0.84 * np.sin(ang), f"{v}%", ha="center", va="center",
                fontsize=10, fontweight="bold", color="white", fontfamily="DejaVu Sans")
    ax.text(0, 0.08, profile["alias"], ha="center", va="center", fontsize=11,
            fontweight="bold", color=profile["color"], fontfamily="DejaVu Sans")
    ax.text(0, -0.12, "portafolio modelo", ha="center", va="center", fontsize=8,
            color="#9a9795", fontfamily="DejaVu Sans")
    ax.set_aspect("equal")
    plt.tight_layout()
    return fig


def make_growth(monthly, years, initial, my_idx):
    fig, ax = plt.subplots(figsize=(9, 4), facecolor="#f7f5f1")
    ax.set_facecolor("#f7f5f1")
    months = np.arange(int(years * 12) + 1) / 12
    contrib = [initial + monthly * m * 12 for m in months]
    ax.fill_between(months, 0, np.array(contrib) / 1e6, color="#e2dfd8", alpha=0.8, label="Total aportado")
    for i, p in enumerate(PROFILES):
        vals = np.array(project(monthly, years, initial, p["real_return"])) / 1e6
        mine = i == my_idx
        ax.plot(months, vals, color=p["color"], lw=3.2 if mine else 1.4, alpha=1 if mine else 0.45,
                label=p["name"] + ("  ← usted" if mine else ""))
        if mine:
            ax.scatter([months[-1]], [vals[-1]], color=p["color"], s=60, zorder=5)
    ax.set_xlabel("Años", fontsize=9, color="#4a4845")
    ax.set_ylabel("Millones de COP (pesos de hoy)", fontsize=9, color="#4a4845")
    ax.grid(color="#e2dfd8", lw=0.8)
    ax.tick_params(colors="#7a7775", labelsize=8)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.legend(fontsize=7.5, frameon=False, loc="upper left")
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

    nombre   = escape(_clean(nombre))
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

    personal = [(t, b) for _, t, b, _, _ in bias_insights(profile)]
    tips = personal[:3] + [(t, b) for _, t, b in profile["tips"][:3]]
    tips_html = "".join(
        f'<p style="margin:0 0 10px"><strong style="color:#e2e8f0">{_clean(t)}.</strong> {_clean(b)}</p>'
        for t, b in tips
    )

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
      <div class="score-lbl">Puntaje total · de {MIN_SCORE} a {MAX_SCORE} puntos</div>
    </div>

    <div class="strat">
      <div class="strat-title">📌 Estrategia de portafolio recomendada</div>
      <div class="strat-text">{profile['strategy']}</div>
    </div>

    <div class="strat">
      <div class="strat-title">🎯 Consejos para usted · {profile['alias']}</div>
      <div class="strat-text">{tips_html}</div>
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
                       color:#1c1a18; margin:0; line-height:1.1;">
                Perfil de Riesgo<br>
                <span style="color:#8a6a10;">del Inversionista</span>
            </h1>
            <p style="color:#9a9795; font-size:0.78rem; letter-spacing:0.18em;
                      text-transform:uppercase; margin-top:0.9rem; margin-bottom:0;">
                Posgrado en Finanzas
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Info cards
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-icon">🎯</div>
                <div class="info-card-value">{N_Q} Preguntas</div>
                <div class="info-card-label">{len(DIMENSIONS)} dimensiones</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="info-card">
                <div class="info-card-icon">⏱️</div>
                <div class="info-card-value">~8 minutos</div>
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
        <p style="color:#7a7775; font-size:0.88rem; text-align:center;
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
        if st.button("Comenzar encuesta →", width="stretch"):
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
            <span style="font-size:0.75rem; color:#9a9795; text-transform:uppercase;
                         letter-spacing:0.1em;">Encuesta{name_str}</span>
            <span style="font-size:0.75rem; color:#8a6a10; font-weight:700;
                         background:rgba(201,168,76,0.12); padding:0.2rem 0.7rem;
                         border-radius:20px; border:1px solid rgba(201,168,76,0.4);">
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
                if st.button("← Anterior", width="stretch"):
                    if option_idx is not None:
                        st.session_state.answers[q_idx] = (option_idx, q["points"][option_idx])
                    st.session_state.current_q -= 1
                    st.rerun()
        with col_fwd:
            is_last = q_idx == total - 1
            btn_label = "Ver resultado →" if is_last else "Siguiente →"
            if st.button(btn_label, width="stretch"):
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
def tip_cards(items, color):
    cards = "".join(
        f'<div class="tip-card" style="border-top:3px solid {color};">'
        f'<div class="tip-head"><span class="tip-icon">{icon}</span>'
        f'<span class="tip-title">{title}</span></div>'
        f'<div class="tip-body">{body}</div></div>'
        for icon, title, body in items
    )
    md(f'<div class="tip-grid">{cards}</div>')


def page_result():
    score = sum(v[1] for v in st.session_state.answers.values())
    idx = profile_index(score)
    profile = PROFILES[idx]
    name_str = st.session_state.name or "Estudiante"
    c = profile["color"]

    # Header
    md(f"""
    <div style="text-align:center; padding:1.5rem 0 0.75rem;">
        <p style="color:#9a9795; font-size:0.72rem; text-transform:uppercase;
                  letter-spacing:0.18em; margin-bottom:0.4rem;">Resultado de</p>
        <h2 style="font-family:'Playfair Display',serif; color:#1c1a18;
                   font-size:2rem; margin:0;">{escape(name_str)}</h2>
        <p style="color:{c}; font-weight:600; margin-top:0.35rem;">
            Su arquetipo: {profile['emoji']} {profile['alias']}
        </p>
    </div>
    """)

    # ── Gauge + profile card ────────────────────────────────────────────────
    col_gauge, col_profile = st.columns([3, 2], gap="large")
    with col_gauge:
        fig = make_gauge(score, profile)
        st.pyplot(fig, width="stretch")
        plt.close(fig)
    with col_profile:
        md(f"""
        <div style="background:{profile['bg']}; border:1px solid {c}55;
                    border-left:4px solid {c}; border-radius:14px;
                    padding:1.5rem; box-sizing:border-box;">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">{profile['emoji']}</div>
            <div style="font-size:0.68rem; color:#9a9795; text-transform:uppercase;
                        letter-spacing:0.12em; margin-bottom:0.2rem;">Tu perfil</div>
            <h3 style="font-family:'Playfair Display',serif; color:{c};
                       font-size:1.7rem; margin:0 0 1rem;">{profile['name']}</h3>
            <p style="color:#4a4845; font-size:0.88rem; line-height:1.6; margin:0;">{profile['desc']}</p>
        </div>
        """)

    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
    pills = [
        ("⏱ Horizonte", profile["horizon"]),
        ("〜 Volatilidad", profile["volatility"]),
        ("📈 Retorno esperado", profile["expected_return"]),
        ("🌧 Año muy malo", f"≈ −{profile['drawdown']}%"),
    ]
    for col, (lbl, val) in zip(st.columns(4, gap="small"), pills):
        with col:
            md(f"""
            <div class="metric-pill" style="border-top:3px solid {c};">
                <div class="metric-pill-label">{lbl}</div>
                <div class="metric-pill-value" style="color:{c};">{val}</div>
            </div>
            """)

    insights = bias_insights(profile)
    will, cap = willingness_capacity()

    tab_dna, tab_tips, tab_lab, tab_ans = st.tabs([
        "🧬 Su ADN inversor", f"💡 Consejos ({len(insights) + len(profile['tips'])})",
        "🧮 Laboratorio", "📋 Sus respuestas",
    ])

    # ── TAB 1: ADN ──────────────────────────────────────────────────────────
    with tab_dna:
        md('<div class="sec-title">Seis dimensiones, un inversionista</div>'
           '<div class="sec-sub">Cada eje se calcula con sus respuestas reales. Más lejos del centro = más apetito de riesgo.</div>')
        col_radar, col_matrix = st.columns(2, gap="large")
        with col_radar:
            fig = make_radar(profile)
            st.pyplot(fig, width="stretch")
            plt.close(fig)
        with col_matrix:
            fig = make_matrix(will, cap, profile)
            st.pyplot(fig, width="stretch")
            plt.close(fig)

        gap = will - cap
        if gap > 0.25:
            lower = PROFILES[max(idx - 1, 0)]
            md(f"""<div class="insight" style="background:#ffe8ef; border-color:#c4003a55; color:#5a1020;">
                <b>⚠️ Sus ganas de riesgo superan su capacidad.</b> Usted está dispuesto a asumir más riesgo
                ({will:.0%}) del que su situación financiera soporta ({cap:.0%}). La práctica profesional
                (por ejemplo, el estándar CFA) recomienda que, cuando hay conflicto, mande la capacidad.
                Considere operar como <b>{lower['name']}</b> hasta fortalecer su colchón e ingresos.</div>""")
        elif gap < -0.25:
            md(f"""<div class="insight" style="background:#e0f9f3; border-color:#0e9e7355; color:#0b4a37;">
                <b>🌱 Tiene espacio para crecer.</b> Su situación financiera ({cap:.0%}) le permitiría asumir
                más riesgo del que hoy desea ({will:.0%}). No es obligatorio subirlo, pero entender la volatilidad
                puede ayudarle a no dejar rendimiento sobre la mesa en metas de largo plazo.</div>""")
        else:
            md(f"""<div class="insight" style="background:#fdf8e0; border-color:#c9a84c77; color:#4a3a08;">
                <b>✅ Disposición y capacidad alineadas.</b> Lo que quiere asumir ({will:.0%}) y lo que puede
                asumir ({cap:.0%}) van en la misma dirección. Es la base de un plan que se sostiene en las malas.</div>""")

        md('<div class="sec-title">Su portafolio modelo</div>'
           '<div class="sec-sub">Una mezcla de referencia para su perfil. Es un punto de partida para discutir, no una recomendación personal.</div>')
        col_donut, col_strat = st.columns([2, 3], gap="large")
        with col_donut:
            fig = make_donut(profile)
            st.pyplot(fig, width="stretch")
            plt.close(fig)
        with col_strat:
            legend = "".join(
                f'<div style="display:flex;align-items:center;gap:0.6rem;margin:0.3rem 0;font-size:0.9rem;">'
                f'<span style="width:12px;height:12px;border-radius:3px;background:{ALLOC_COLORS[k]};display:inline-block"></span>'
                f'<span style="flex:1;color:#2a2825">{k}</span><b style="color:#1c1a18">{v}%</b></div>'
                for k, v in profile["allocation"].items()
            )
            md(f"""
            <div style="background:#ffffff; border:1px solid #d8d5ce; border-top:3px solid {c};
                        border-radius:12px; padding:1.25rem 1.5rem;">
                <div style="font-size:0.68rem; color:#8a6a10; font-weight:700; text-transform:uppercase;
                            letter-spacing:0.12em; margin-bottom:0.6rem;">📋 Estrategia sugerida</div>
                <p style="color:#2a2825; font-size:0.92rem; margin:0 0 0.9rem; line-height:1.6;">{profile['strategy']}</p>
                {legend}
            </div>
            """)
            tol = answer_opt("perdida_max")
            if tol is not None:
                tol_pct = QUESTIONS[QIDX["perdida_max"]]["loss"][tol]
                dd = profile["drawdown"]
                ok = dd <= tol_pct
                md(f"""
                <div class="insight" style="background:{'#e0f9f3' if ok else '#fff3e0'};
                     border-color:{'#0e9e7355' if ok else '#c95f0055'}; color:#2a2825;">
                    <b>🧪 Prueba de estrés.</b> En un año muy malo (como 2008), esta mezcla podría caer
                    cerca de <b>{dd}%</b>: sobre $100 millones, unos <b>{fmt_cop(dd * 1e6)}</b>.
                    Usted dijo que tolera <b>{tol_pct}%</b>.
                    {'Su tolerancia cubre el escenario.' if ok else 'La caída posible supera su tolerancia: revise la pestaña Consejos.'}
                </div>""")

    # ── TAB 2: CONSEJOS ─────────────────────────────────────────────────────
    with tab_tips:
        if insights:
            md('<div class="sec-title">Lo que sus respuestas revelan</div>'
               '<div class="sec-sub">Alertas y sesgos detectados a partir de respuestas puntuales. Conocerlos es la mitad de la solución.</div>')
            cards = "".join(
                f'<div class="tip-card" style="border-top:3px solid {col};">'
                f'<span class="tip-tag" style="background:{col}18;color:{col};border:1px solid {col}55">{tag}</span>'
                f'<div class="tip-head"><span class="tip-icon">{icon}</span><span class="tip-title">{title}</span></div>'
                f'<div class="tip-body">{body}</div></div>'
                for icon, title, body, tag, col in insights
            )
            md(f'<div class="tip-grid">{cards}</div>')
        else:
            md("""<div class="insight" style="background:#e0f9f3; border-color:#0e9e7355; color:#0b4a37;">
                <b>🧘 Sin alertas de comportamiento.</b> Sus respuestas no muestran los sesgos más comunes
                (pánico, FOMO, sobreconfianza, apalancamiento extremo). Mantenga esa disciplina por escrito.</div>""")

        md(f'<div class="sec-title">5 jugadas para {profile["alias"]}</div>'
           f'<div class="sec-sub">Consejos prácticos para un perfil {profile["name"].lower()}.</div>')
        tip_cards(profile["tips"], c)

        md('<div class="sec-title">Reglas de oro para cualquier perfil</div>'
           '<div class="sec-sub">Aplican a todos, del Guardián al Cazador de Alfa.</div>')
        tip_cards(GOLDEN_RULES, "#c9a84c")

    # ── TAB 3: LABORATORIO ──────────────────────────────────────────────────
    with tab_lab:
        md('<div class="sec-title">Laboratorio de interés compuesto</div>'
           '<div class="sec-sub">Juegue con los números y vea cuánto pesa el perfil de riesgo en 10, 20 o 30 años. '
           'Los valores están en pesos de hoy (ya descontada la inflación).</div>')
        l1, l2, l3 = st.columns(3)
        with l1:
            initial = st.number_input("Monto inicial (COP)", min_value=0, max_value=5_000_000_000,
                                      value=5_000_000, step=1_000_000, key="lab_initial")
        with l2:
            monthly = st.number_input("Aporte mensual (COP)", min_value=0, max_value=100_000_000,
                                      value=500_000, step=100_000, key="lab_monthly")
        with l3:
            years = st.slider("Años invirtiendo", 1, 40, 20, key="lab_years")

        mine = project(monthly, years, initial, profile["real_return"])[-1]
        safe = project(monthly, years, initial, PROFILES[0]["real_return"])[-1]
        aportado = initial + monthly * 12 * years
        k1, k2, k3 = st.columns(3)
        for col, (lbl, val, colr) in zip((k1, k2, k3), [
            ("Total aportado", fmt_cop(aportado), "#4a4845"),
            (f"Valor final · {profile['name']}", fmt_cop(mine), c),
            ("Diferencia vs. Conservador", ("+" if mine >= safe else "") + fmt_cop(mine - safe), "#0e9e73" if mine >= safe else "#c4003a"),
        ]):
            with col:
                md(f'<div class="metric-pill" style="text-align:left;padding:1rem 1.1rem;">'
                   f'<div class="big-lbl">{lbl}</div><div class="big-num" style="color:{colr}">{val}</div></div>')

        fig = make_growth(monthly, years, initial, idx)
        st.pyplot(fig, width="stretch")
        plt.close(fig)
        assumed = ", ".join(
            "{} {:.1%}".format(p["name"], p["real_return"]).replace(".", ",") for p in PROFILES
        )
        md(f"""<div class="note-box">Retornos reales anuales supuestos: {assumed}.
            Son ilustrativos y no garantizados; el camino real tendrá caídas como la de la prueba de estrés.</div>""")

    # ── TAB 4: RESPUESTAS ───────────────────────────────────────────────────
    with tab_ans:
        section_map = {}
        for i, q in enumerate(QUESTIONS):
            ans = st.session_state.answers.get(i, (0, 0))
            section_map.setdefault(q["section"], []).append({
                "q": i + 1, "text": q["text"], "answer": q["options"][ans[0]], "points": ans[1],
            })
        for section, items in section_map.items():
            st.markdown(f"**{section}**")
            for item in items:
                md(f"""
                <div style="border-left:2px solid #d8d5ce; padding:0.4rem 0.75rem;
                            margin:0.25rem 0; font-size:0.85rem; color:#7a7775;">
                    <span style="color:#8a6a10; font-weight:600;">P{item['q']}</span> {item['text']}<br>
                    <span style="color:#1c1a18;">→ {item['answer']}</span>
                    <span style="color:#8a6a10; float:right;">{item['points']} pts</span>
                </div>""")
            st.markdown("")

    # ── Escala de perfiles ──────────────────────────────────────────────────
    st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
    md('<div class="divider-label">Escala de perfiles de riesgo</div>')
    cards_html = '<div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin-top:0.5rem;">'
    for p, (lo, hi) in zip(PROFILES, profile_ranges()):
        is_me = p["name"] == profile["name"]
        fill_pct = int((hi - lo + 1) / (MAX_SCORE - MIN_SCORE + 1) * 100)
        border = f"2px solid {p['color']}" if is_me else "1px solid #d8d5ce"
        bg = p["bg"] if is_me else "#f2f0eb"
        you_badge = (f'<div style="font-size:0.6rem; color:{p["color"]}; font-weight:700; text-transform:uppercase; '
                     f'letter-spacing:0.1em; margin-bottom:0.3rem;">&#9658; Tú</div>') if is_me else ""
        cards_html += (
            f'<div style="flex:1 1 120px; background:{bg}; border:{border}; border-radius:10px; padding:0.85rem 0.75rem; text-align:center;">'
            f'<div style="font-size:1.4rem;">{p["emoji"]}</div>{you_badge}'
            f'<div style="font-size:0.78rem; font-weight:{"700" if is_me else "400"}; color:{p["color"]}; margin:0.3rem 0 0.1rem; line-height:1.2;">{p["name"]}</div>'
            f'<div style="font-size:0.66rem; color:#9a9795; margin-bottom:0.2rem;">{p["alias"]}</div>'
            f'<div style="font-size:0.68rem; color:#9a9795; margin-bottom:0.5rem;">{lo}&#8211;{hi} pts</div>'
            f'<div style="height:4px; background:#e2dfd8; border-radius:2px; overflow:hidden;">'
            f'<div style="width:{fill_pct}%; height:100%; background:{p["color"]}; opacity:{"1" if is_me else "0.4"}; border-radius:2px;"></div>'
            f'</div></div>'
        )
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
        if st.button("↩ Reiniciar encuesta", width="stretch"):
            st.session_state.page = "welcome"
            st.session_state.answers = {}
            st.session_state.current_q = 0
            st.session_state.name = ""
            st.session_state.user_email = ""
            st.session_state.email_sent = False
            st.rerun()

    md("""
    <p style="text-align:center; color:#9a9795; font-size:0.72rem; margin-top:1rem;">
        Este resultado es orientativo y tiene fines académicos. Consulta con un asesor financiero profesional.
    </p>
    """)


# ─── ROUTER ──────────────────────────────────────────────────────────────────
if st.session_state.page == "welcome":
    page_welcome()
elif st.session_state.page == "survey":
    page_survey()
elif st.session_state.page == "result":
    page_result()
