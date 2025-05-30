"""
Django settings para debug - version minima
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Variables de entorno
IS_RAILWAY = os.getenv('RAILWAY_ENVIRONMENT') is not None
IS_RENDER = os.getenv('RENDER') == 'True'
IS_PRODUCTION = IS_RAILWAY or IS_RENDER

print("DEBUG SETTINGS:")
print(f"IS_RAILWAY: {IS_RAILWAY}")
print(f"IS_RENDER: {IS_RENDER}")
print(f"IS_PRODUCTION: {IS_PRODUCTION}")

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key-change-in-production')
DEBUG = not IS_PRODUCTION

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.railway.app', '.onrender.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    'django_celery_beat',
    'blog',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# Base de datos - version simplificada
print(f"Configurando base de datos, IS_PRODUCTION = {IS_PRODUCTION}")

if IS_PRODUCTION:
    print("Modo producción detectado")
    database_url = os.getenv("DATABASE_URL")
    print(f"DATABASE_URL: {database_url}")
    if database_url:
        from urllib.parse import urlparse
        tmpPostgres = urlparse(database_url)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': tmpPostgres.path[1:],
                'USER': tmpPostgres.username,
                'PASSWORD': tmpPostgres.password,
                'HOST': tmpPostgres.hostname,
                'PORT': tmpPostgres.port or 5432,
                'OPTIONS': {
                    'sslmode': 'require',
                },
            }
        }
    else:
        raise ValueError("DATABASE_URL environment variable is required in production")
else:
    print("Modo desarrollo detectado - usando SQLite")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

print(f"DATABASES configurado: {DATABASES}")

# Configuración básica
USE_TZ = True
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework básico
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# CORS básico
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
