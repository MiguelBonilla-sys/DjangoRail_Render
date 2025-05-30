#!/usr/bin/env python
"""
Script de verificación pre-despliegue para Vercel
"""

import os
import django
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command
from django.core.checks import run_checks

def check_environment():
    """Verificar variables de entorno necesarias"""
    print("🔍 Verificando variables de entorno...")
    
    required_vars = [
        'SECRET_KEY',
        'DATABASE_URL',
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY', 
        'CLOUDINARY_API_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables faltantes: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Todas las variables de entorno están configuradas")
        return True

def check_django_config():
    """Verificar configuración de Django"""
    print("\n🔍 Verificando configuración de Django...")
    
    try:
        # Ejecutar checks de Django
        errors = run_checks()
        if errors:
            print(f"❌ Errores encontrados: {len(errors)}")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print("✅ Configuración de Django válida")
            return True
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

def check_static_files():
    """Verificar archivos estáticos"""
    print("\n🔍 Verificando archivos estáticos...")
    
    try:
        # Verificar que collectstatic funcione
        call_command('collectstatic', '--noinput', '--verbosity=0')
        
        # Verificar que existan archivos
        static_root = Path(settings.STATIC_ROOT)
        if static_root.exists() and any(static_root.iterdir()):
            print("✅ Archivos estáticos generados correctamente")
            return True
        else:
            print("❌ No se encontraron archivos estáticos")
            return False
    except Exception as e:
        print(f"❌ Error al generar archivos estáticos: {e}")
        return False

def check_database_connection():
    """Verificar conexión a base de datos"""
    print("\n🔍 Verificando conexión a base de datos...")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✅ Conexión a base de datos exitosa")
                return True
    except Exception as e:
        print(f"❌ Error de conexión a base de datos: {e}")
        print("💡 Asegúrate de que DATABASE_URL esté configurado correctamente")
        return False

def check_vercel_config():
    """Verificar configuración específica de Vercel"""
    print("\n🔍 Verificando configuración de Vercel...")
    
    # Verificar vercel.json
    vercel_config = Path('vercel.json')
    if not vercel_config.exists():
        print("❌ Archivo vercel.json no encontrado")
        return False
    
    # Verificar que IS_VERCEL funcione
    os.environ['VERCEL'] = '1'
    from django.conf import settings
    
    # Recargar settings para verificar configuración
    if hasattr(settings, 'IS_VERCEL'):
        print("✅ Configuración de Vercel detectada correctamente")
        return True
    else:
        print("❌ Variable IS_VERCEL no configurada")
        return False

def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN PRE-DESPLIEGUE PARA VERCEL")
    print("=" * 50)
    
    checks = [
        check_environment,
        check_django_config,
        check_static_files,
        check_database_connection,
        check_vercel_config
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Error inesperado en {check.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    
    if all(results):
        print("🎉 ¡TODO LISTO PARA DESPLEGAR!")
        print("✅ Todas las verificaciones pasaron exitosamente")
        print("\n📋 Próximos pasos:")
        print("1. git add .")
        print("2. git commit -m 'Listo para Vercel'")
        print("3. git push origin main")
        print("4. Conectar repositorio en vercel.com")
        return True
    else:
        failed_count = results.count(False)
        print(f"❌ {failed_count} verificación(es) fallaron")
        print("🔧 Corrige los errores antes de desplegar")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
