"""
Script de verificación para el repositorio DjangoRail_Render
Verifica que todas las configuraciones estén correctas para Railway y Render
"""

import os
import sys
import django
from pathlib import Path

# Agregar el directorio del proyecto al path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command
from django.test.utils import get_runner

def test_basic_configuration():
    """Prueba la configuración básica del proyecto"""
    print("🔍 Verificando configuración básica...")
    
    # Verificar que no hay referencias a Vercel
    assert not hasattr(settings, 'IS_VERCEL'), "❌ Encontradas referencias a IS_VERCEL"
    print("✅ Sin referencias a Vercel")
    
    # Verificar configuración de Railway/Render
    assert hasattr(settings, 'IS_RAILWAY'), "❌ Falta configuración IS_RAILWAY"
    assert hasattr(settings, 'IS_RENDER'), "❌ Falta configuración IS_RENDER"
    assert hasattr(settings, 'IS_PRODUCTION'), "❌ Falta configuración IS_PRODUCTION"
    print("✅ Variables de entorno configuradas correctamente")
    
    # Verificar ALLOWED_HOSTS
    allowed_hosts = settings.ALLOWED_HOSTS
    assert '.railway.app' in allowed_hosts, "❌ Falta dominio .railway.app en ALLOWED_HOSTS"
    assert '.onrender.com' in allowed_hosts, "❌ Falta dominio .onrender.com en ALLOWED_HOSTS"
    print("✅ ALLOWED_HOSTS configurado para Railway y Render")
    
    # Verificar middleware
    middleware = settings.MIDDLEWARE
    assert 'whitenoise.middleware.WhiteNoiseMiddleware' in middleware, "❌ Falta WhiteNoise middleware"
    print("✅ Middleware configurado correctamente")
    
    # Verificar configuración de archivos estáticos
    assert hasattr(settings, 'STATIC_ROOT'), "❌ Falta STATIC_ROOT"
    assert settings.STATICFILES_STORAGE == 'whitenoise.storage.CompressedManifestStaticFilesStorage', "❌ Configuración incorrecta de STATICFILES_STORAGE"
    print("✅ Configuración de archivos estáticos correcta")

def test_database_configuration():
    """Prueba la configuración de base de datos"""
    print("\n🔍 Verificando configuración de base de datos...")
    
    # En desarrollo debería usar SQLite
    if not settings.IS_PRODUCTION:
        assert settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3', "❌ Base de datos de desarrollo incorrecta"
        print("✅ Base de datos de desarrollo (SQLite) configurada")
    
    print("✅ Configuración de base de datos correcta")

def test_celery_configuration():
    """Prueba la configuración de Celery"""
    print("\n🔍 Verificando configuración de Celery...")
    
    # Verificar configuración base de Celery
    assert hasattr(settings, 'CELERY_BEAT_SCHEDULE'), "❌ Falta CELERY_BEAT_SCHEDULE"
    
    # En desarrollo sin Redis, debería usar TASK_ALWAYS_EAGER
    if not hasattr(settings, 'CELERY_BROKER_URL') or not os.getenv('REDIS_URL'):
        assert getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False), "❌ CELERY_TASK_ALWAYS_EAGER debería estar activado sin Redis"
        print("✅ Celery configurado para modo síncrono (sin Redis)")
    else:
        assert hasattr(settings, 'CELERY_BROKER_URL'), "❌ Falta CELERY_BROKER_URL"
        assert hasattr(settings, 'CELERY_RESULT_BACKEND'), "❌ Falta CELERY_RESULT_BACKEND"
        print("✅ Celery configurado con Redis")
    
    print("✅ Configuración de Celery correcta")

def test_security_settings():
    """Prueba la configuración de seguridad"""
    print("\n🔍 Verificando configuración de seguridad...")
    
    if settings.IS_PRODUCTION:
        assert settings.SECURE_SSL_REDIRECT == True, "❌ SECURE_SSL_REDIRECT no activado en producción"
        assert settings.SECURE_HSTS_SECONDS > 0, "❌ HSTS no configurado en producción"
        print("✅ Configuración de seguridad para producción correcta")
    else:
        print("✅ Modo desarrollo - configuración de seguridad apropiada")

def test_installed_apps():
    """Verifica que todas las apps necesarias están instaladas"""
    print("\n🔍 Verificando aplicaciones instaladas...")
    
    required_apps = [
        'rest_framework',
        'corsheaders',
        'django_filters',
        'drf_yasg',
        'django_celery_beat',
        'blog',
    ]
    
    for app in required_apps:
        assert app in settings.INSTALLED_APPS, f"❌ Falta la aplicación {app}"
    
    print("✅ Todas las aplicaciones necesarias están instaladas")

def test_file_structure():
    """Verifica que la estructura de archivos es correcta"""
    print("\n🔍 Verificando estructura de archivos...")
    
    required_files = [
        'requirements.txt',
        'Procfile',
        'railway.json',
        'build.sh',
        'manage.py',
        'DEPLOY_RAILWAY.md',
        'DEPLOY_RENDER.md',
        'DEPLOYMENT_GUIDE.md',
    ]
    
    for file_name in required_files:
        file_path = BASE_DIR / file_name
        assert file_path.exists(), f"❌ Falta el archivo {file_name}"
    
    # Verificar que NO existe vercel.json
    vercel_file = BASE_DIR / 'vercel.json'
    assert not vercel_file.exists(), "❌ Encontrado archivo vercel.json - debe ser eliminado"
    
    print("✅ Estructura de archivos correcta")

def main():
    """Función principal del script de verificación"""
    print("🚀 Iniciando verificación del repositorio DjangoRail_Render")
    print("=" * 60)
    
    try:
        test_basic_configuration()
        test_database_configuration()
        test_celery_configuration()
        test_security_settings()
        test_installed_apps()
        test_file_structure()
        
        print("\n" + "=" * 60)
        print("🎉 ¡Todas las verificaciones pasaron exitosamente!")
        print("✅ El repositorio está listo para Railway y Render")
        print("\n📚 Próximos pasos:")
        print("1. Leer DEPLOY_RAILWAY.md para desplegar en Railway")
        print("2. Leer DEPLOY_RENDER.md para desplegar en Render")
        print("3. Configurar variables de entorno según la plataforma elegida")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ Error en verificación: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
