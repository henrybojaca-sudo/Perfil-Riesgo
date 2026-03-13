# 📊 Encuesta de Perfil de Riesgo del Inversionista

Aplicación Streamlit para evaluar el perfil de riesgo de inversionistas, dirigida a estudiantes de posgrado en finanzas.

## 🚀 Demo en vivo

> Despliega en Streamlit Cloud: [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 📋 Características

- **11 preguntas** en 4 dimensiones: reacción al mercado, tolerancia al riesgo, decisiones financieras y sofisticación financiera
- **5 perfiles de riesgo**: Conservador → Agresivo
- **Visualizaciones dinámicas**: velocímetro de riesgo + radar de dimensiones
- **Desglose de respuestas** detallado
- Diseño oscuro tipo Bloomberg Terminal

## ⚙️ Instalación local

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/encuesta-perfil-riesgo.git
cd encuesta-perfil-riesgo

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la app
streamlit run app.py
```

La app abrirá en `http://localhost:8501`

## ☁️ Despliegue en Streamlit Cloud (gratuito)

1. Sube este repositorio a GitHub (público)
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio y el archivo `app.py`
5. Haz clic en **Deploy**

## 📁 Estructura

```
encuesta-perfil-riesgo/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias Python
└── README.md           # Este archivo
```

## 🎯 Perfiles de Riesgo

| Puntaje | Perfil | Descripción |
|---------|--------|-------------|
| 11–14 | 🛡️ Conservador | Preservación del capital, mínima volatilidad |
| 15–24 | ⚓ Moderado-Conservador | Rendimientos moderados, baja volatilidad |
| 25–34 | ⚖️ Moderado | Crecimiento equilibrado |
| 35–44 | 🚀 Moderado-Agresivo | Alto crecimiento, alta volatilidad |
| 45–55 | ⚡ Agresivo | Máximo retorno, máximo riesgo |

---

Desarrollado para el Programa de Posgrado en Finanzas.
