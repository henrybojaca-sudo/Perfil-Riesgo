#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# setup_github.sh  —  Sube el proyecto a GitHub en un solo paso
#
# USO:
#   chmod +x setup_github.sh
#   ./setup_github.sh TU_USUARIO_GITHUB encuesta-perfil-riesgo
# ─────────────────────────────────────────────────────────────────────────────

GITHUB_USER=${1:-"TU_USUARIO"}
REPO_NAME=${2:-"encuesta-perfil-riesgo"}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " 📊 Encuesta Perfil Riesgo — Setup GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Init git
git init
git add .
git commit -m "feat: encuesta perfil de riesgo inversionista - initial commit"

# 2. Rename branch to main
git branch -M main

# 3. Conectar con GitHub (requiere repo ya creado en github.com)
echo ""
echo "⚠️  Antes de continuar, crea el repositorio en:"
echo "    https://github.com/new"
echo "    Nombre: $REPO_NAME"
echo "    Visibilidad: Public (para Streamlit Cloud gratis)"
echo ""
read -p "¿Ya creaste el repo? Presiona Enter para continuar..."

git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
git push -u origin main

echo ""
echo "✅ Código subido a: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " ☁️  Despliega GRATIS en Streamlit Cloud:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " 1. Ve a https://share.streamlit.io"
echo " 2. Inicia sesión con tu cuenta de GitHub"
echo " 3. New app → Selecciona $REPO_NAME"
echo " 4. Main file: app.py"
echo " 5. Deploy!"
echo ""
