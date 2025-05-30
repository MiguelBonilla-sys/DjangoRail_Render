#!/usr/bin/env python
"""
Verificación rápida del estado del proyecto
"""

import os
import sys

print("🔍 Verificación rápida del proyecto Django")
print("=" * 50)

# 1. Verificar archivos críticos
print("\n📁 Verificando archivos críticos...")
critical_files = [
    'manage.py',
    'mysite/settings.py',
    'mysite/wsgi.py',
    'vercel.json',
    'requirements.txt',
    '.env.example',
    'DEPLOY_INSTRUCTIONS.md'
]

for file in critical_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - FALTANTE")

# 2. Verificar configuración de Vercel
print("\n⚙️ Verificando configuración de Vercel...")
if os.path.exists('vercel.json'):
    with open('vercel.json', 'r') as f:
        content = f.read()
        if '"VERCEL": "1"' in content:
            print("✅ Variable VERCEL configurada")
        else:
            print("❌ Variable VERCEL no encontrada")
        
        if 'maxDuration' in content:
            print("✅ maxDuration configurado")
        else:
            print("❌ maxDuration no configurado")

# 3. Verificar requirements.txt
print("\n📦 Verificando requirements.txt...")
if os.path.exists('requirements.txt'):
    with open('requirements.txt', 'r') as f:
        content = f.read()
        key_packages = ['Django', 'djangorestframework', 'psycopg2-binary', 'whitenoise']
        for package in key_packages:
            if package in content:
                print(f"✅ {package}")
            else:
                print(f"❌ {package} - FALTANTE")

# 4. Verificar estructura de archivos
print("\n🏗️ Verificando estructura del proyecto...")
required_dirs = ['blog', 'mysite']
for dir_name in required_dirs:
    if os.path.isdir(dir_name):
        print(f"✅ Directorio {dir_name}/")
    else:
        print(f"❌ Directorio {dir_name}/ - FALTANTE")

print("\n" + "=" * 50)
print("✅ Verificación completada")
print("\n📋 Próximos pasos:")
print("1. Configurar variables de entorno en Vercel")
print("2. Ejecutar 'vercel --prod' para desplegar")
print("3. Verificar que el despliegue funciona correctamente")
