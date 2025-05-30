# DjangoRail_Render

Un proyecto Django profesional optimizado específicamente para despliegue en **Railway** y **Render**, completamente libre de dependencias de Vercel.

## 🚀 Características

- **Django 5.1.5** con Django REST Framework
- **Celery** con Redis para tareas asíncronas
- **PostgreSQL** para producción, SQLite para desarrollo
- **WhiteNoise** para servir archivos estáticos
- **Gunicorn** como servidor WSGI
- **Cloudinary** para almacenamiento de media files
- **API REST completa** con documentación Swagger/OpenAPI
- **Sistema de logging** robusto
- **Middleware personalizado** para seguridad y auditoría
- **Tests comprehensivos**

## 📁 Estructura del Proyecto

```
DjangoRail_Render/
├── blog/                    # Aplicación principal
│   ├── Models/             # Modelos de datos
│   ├── Views/              # Vistas de API
│   ├── Serializers/        # Serializers de DRF
│   ├── middleware.py       # Middleware personalizado
│   ├── filters.py          # Filtros para API
│   └── tasks.py           # Tareas de Celery
├── mysite/                 # Configuración del proyecto
│   ├── settings.py        # Configuración optimizada para Railway/Render
│   ├── celery.py          # Configuración de Celery
│   └── urls.py            # URLs principales
├── tests/                  # Tests del proyecto
├── logs/                   # Archivos de log (desarrollo)
├── requirements.txt        # Dependencias Python
├── Procfile               # Configuración para Railway
├── railway.json           # Configuración específica de Railway
├── build.sh              # Script de build para Render
├── DEPLOY_RAILWAY.md     # Guía de despliegue en Railway
├── DEPLOY_RENDER.md      # Guía de despliegue en Render
└── DEPLOYMENT_GUIDE.md   # Guía comparativa
```

## 🛠️ Instalación Local

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd DjangoRail_Render
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   Crear archivo `.env`:
   ```env
   SECRET_KEY=tu-secret-key-aqui
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   REDIS_URL=redis://localhost:6379/0
   
   # Cloudinary (opcional para desarrollo)
   CLOUDINARY_CLOUD_NAME=tu-cloud-name
   CLOUDINARY_API_KEY=tu-api-key
   CLOUDINARY_API_SECRET=tu-api-secret
   ```

5. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

## 🚀 Despliegue

### Railway
Lee la guía completa: [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md)

### Render
Lee la guía completa: [DEPLOY_RENDER.md](DEPLOY_RENDER.md)

### Comparación
Para decidir entre Railway y Render: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 📊 API Endpoints

- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`
- **API Schema**: `/swagger.json`

### Principales endpoints:
- `/api/noticias/` - Gestión de noticias
- `/api/conferencias/` - Gestión de conferencias
- `/api/cursos/` - Gestión de cursos
- `/api/proyectos/` - Gestión de proyectos
- `/api/integrantes/` - Gestión de integrantes
- `/api/ofertas-empleo/` - Gestión de ofertas de empleo
- `/api/audit-log/` - Logs de auditoría

## 🔧 Configuración de Producción

### Variables de Entorno Requeridas

```env
# Django
SECRET_KEY=tu-secret-key-muy-seguro
DEBUG=False

# Base de datos
DATABASE_URL=postgresql://usuario:password@host:puerto/database

# Redis (opcional pero recomendado)
REDIS_URL=redis://usuario:password@host:puerto

# Cloudinary
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret

# Dominio personalizado (opcional)
CUSTOM_DOMAIN=tu-dominio.com

# Frontend (para CORS)
FRONTEND_URL=https://tu-frontend.com
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests específicos
python manage.py test blog.tests

# Con pytest
pytest

# Verificar configuración del proyecto
python verify_railway_render.py
```

## 📝 Logging

- **Desarrollo**: Logs en archivos en `/logs/`
- **Producción**: Logs en consola para mejor integración con plataformas cloud

## 🔒 Seguridad

- Configuración HTTPS forzado en producción
- Headers de seguridad configurados
- CORS configurado apropiadamente
- Variables sensibles en variables de entorno
- Validación robusta en API

## 📚 Tecnologías Utilizadas

- **Backend**: Django 5.1.5, Django REST Framework
- **Base de datos**: PostgreSQL (prod), SQLite (dev)
- **Cache/Queue**: Redis, Celery
- **Servidor**: Gunicorn
- **Archivos estáticos**: WhiteNoise
- **Media files**: Cloudinary
- **Documentación**: drf-yasg (Swagger/OpenAPI)
- **Testing**: pytest, pytest-django

## 🆚 Diferencias con Versión Vercel

Esta versión ha sido completamente reescrita para Railway y Render:

- ❌ **Eliminado**: Todas las referencias a Vercel
- ❌ **Eliminado**: `vercel.json` y configuraciones serverless
- ✅ **Añadido**: `Procfile` para Railway
- ✅ **Añadido**: `railway.json` con configuración específica
- ✅ **Añadido**: `build.sh` para Render
- ✅ **Mejorado**: `settings.py` optimizado para Railway/Render
- ✅ **Mejorado**: Configuración de base de datos más robusta
- ✅ **Mejorado**: Logging optimizado para plataformas cloud

## 📞 Soporte

Si tienes problemas con el despliegue:

1. Revisa los logs de tu plataforma
2. Verifica que todas las variables de entorno estén configuradas
3. Consulta las guías específicas de despliegue
4. Ejecuta el script de verificación local

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Nota**: Este repositorio está optimizado específicamente para Railway y Render. Para Vercel, usar el repositorio original.
