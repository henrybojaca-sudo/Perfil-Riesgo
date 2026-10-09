# 📊 Encuesta de Perfil de Riesgo del Inversionista

Aplicación Streamlit para evaluar el perfil de riesgo de inversionistas, dirigida a estudiantes de posgrado en finanzas.

**App en vivo:** https://perfil-riesgo-jxjrb6pmb6b29skm7xuetu.streamlit.app/

---

## 📋 Características

- **18 preguntas** en 6 dimensiones: reacción al mercado, tolerancia y objetivos, apalancamiento, experiencia, capacidad financiera y psicología del inversionista
- **5 perfiles con arquetipo**: Conservador (El Guardián) → Agresivo (El Cazador de Alfa)
- **Velocímetro de riesgo** y **radar de 6 dimensiones** calculado con las respuestas reales
- **Mapa disposición × capacidad**: separa las ganas de asumir riesgo de la capacidad financiera para asumirlo y alerta cuando no coinciden
- **Portafolio modelo** por perfil con **prueba de estrés**: compara la caída posible en un año muy malo con la pérdida que el estudiante dijo tolerar
- **Detector de sesgos**: aversión a las pérdidas, efecto disposición, FOMO, market timing, sobreconfianza, apalancamiento y concentración
- **Consejos prácticos**: 5 por perfil + reglas de oro para todos
- **Laboratorio de interés compuesto**: proyección en pesos de hoy para los 5 perfiles
- **Correo automático** con el perfil, la estrategia y los consejos personalizados

## ⚙️ Instalación local

```bash
pip install -r requirements.txt
streamlit run app.py
```

La app abrirá en `http://localhost:8501`

## ✉️ Envío de correo

Configure en Streamlit Cloud → **Settings → Secrets**:

```toml
[smtp]
sender = "tu@gmail.com"
password = "app_password_de_16_caracteres"
host = "smtp.gmail.com"
port = 587
```

## 🎯 Perfiles de Riesgo

El perfil se asigna según el puntaje normalizado (0% = todas las respuestas más conservadoras, 100% = todas las más arriesgadas). Con 18 preguntas el puntaje va de 18 a 90.

| Puntaje | Perfil | Arquetipo | Caída en un año muy malo |
|---------|--------|-----------|--------------------------|
| 18–28 | 🛡️ Conservador | El Guardián | ≈ −3% |
| 29–45 | ⚓ Moderado-Conservador | El Navegante | ≈ −10% |
| 46–62 | ⚖️ Moderado | El Estratega | ≈ −20% |
| 63–77 | 🚀 Moderado-Agresivo | El Explorador | ≈ −30% |
| 78–90 | ⚡ Agresivo | El Cazador de Alfa | ≈ −45% |

Los retornos y caídas son referencias ilustrativas con fines académicos.

---

Desarrollado para el Programa de Posgrado en Finanzas.
