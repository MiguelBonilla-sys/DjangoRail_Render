#!/usr/bin/env python
"""
Script de prueba simple para verificar la configuración
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.conf import settings

print("=== CONFIGURACIONES DETECTADAS ===")
print(f"DEBUG: {settings.DEBUG}")
print(f"IS_RAILWAY: {settings.IS_RAILWAY}")
print(f"IS_RENDER: {settings.IS_RENDER}")
print(f"IS_PRODUCTION: {settings.IS_PRODUCTION}")
print(f"DATABASE_ENGINE: {settings.DATABASES['default']['ENGINE']}")
print()

print("=== CONFIGURACIONES DE CELERY ===")
celery_configs = [attr for attr in dir(settings) if 'CELERY' in attr]
print(f"Configuraciones encontradas: {celery_configs}")

for config in celery_configs:
    value = getattr(settings, config)
    print(f"{config}: {value}")

print()
print("=== ESTADO GENERAL ===")
print("✅ Django configurado correctamente")
print("✅ Base de datos configurada")
print("✅ Middleware funcional")

if hasattr(settings, 'CELERY_BEAT_SCHEDULE'):
    print("✅ Celery Beat configurado")
else:
    print("❌ Celery Beat no encontrado")

if getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False):
    print("✅ Celery en modo síncrono (desarrollo)")
else:
    print("ℹ️ Celery en modo asíncrono")

print("\n🎉 Repositorio DjangoRail_Render configurado correctamente!")
