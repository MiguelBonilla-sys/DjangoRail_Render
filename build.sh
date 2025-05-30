#!/usr/bin/env bash
# build.sh - Script de construcción para Render

# Salir si hay algún error
set -o errexit

echo "🔧 Iniciando proceso de construcción..."

# Instalar dependencias Python
echo "📦 Instalando dependencias Python..."
pip install -r requirements.txt

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --no-input

# Ejecutar migraciones de base de datos
echo "🗄️ Ejecutando migraciones de base de datos..."
python manage.py migrate

echo "✅ Construcción completada exitosamente!"
