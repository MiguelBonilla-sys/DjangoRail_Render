# Instrucciones de Despliegue en Vercel

## 📋 Configuración Previa

### 1. Variables de Entorno en Vercel
Configura las siguientes variables en tu dashboard de Vercel:

```bash
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura
DATABASE_URL=postgresql://usuario:password@host:puerto/nombre_db
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
VERCEL_ENV=production
```

### 2. Base de Datos PostgreSQL
Recomendado usar servicios como:
- **Neon** (gratuito): https://neon.tech/
- **Supabase** (gratuito): https://supabase.com/
- **Railway**: https://railway.app/

### 3. Almacenamiento de Archivos
Configurar cuenta en **Cloudinary**:
1. Crear cuenta en https://cloudinary.com/
2. Obtener credenciales del dashboard
3. Agregar las variables de entorno

## 🚀 Proceso de Despliegue

### 1. Preparar el Proyecto
```bash
# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Verificar configuración
python manage.py check
```

### 2. Subir a GitHub
```bash
git add .
git commit -m "Configuración para Vercel"
git push origin main
```

### 3. Conectar con Vercel
1. Ir a https://vercel.com/
2. Importar proyecto desde GitHub
3. Vercel detectará automáticamente la configuración
4. Agregar las variables de entorno
5. Desplegar

## 🔧 Configuraciones Específicas

### Logging en Producción
- ✅ Solo usa consola (sin archivos)
- ✅ Logs optimizados para serverless
- ✅ Diferentes niveles según el entorno

### Celery en Producción
- ✅ Deshabilitado automáticamente en Vercel
- ✅ Tareas ejecutadas síncronamente
- ✅ Configuración condicional por entorno

### CORS y Seguridad
- ✅ Headers de seguridad configurados
- ✅ CORS configurado para tu dominio
- ✅ Rate limiting implementado

## 📊 URLs de tu API

Una vez desplegado, tu API estará disponible en:
```
https://tu-proyecto.vercel.app/hl4/v1/
```

### Endpoints principales:
- `/hl4/v1/conferencias/` - Gestión de conferencias
- `/hl4/v1/cursos/` - Gestión de cursos
- `/hl4/v1/noticias/` - Gestión de noticias
- `/hl4/v1/proyectos/` - Gestión de proyectos
- `/hl4/v1/integrantes/` - Gestión de integrantes
- `/hl4/v1/ofertasempleo/` - Ofertas de empleo
- `/docs/` - Documentación Swagger

## 🛠️ Solución de Problemas

### Error de Logging
Si ves errores relacionados con archivos de log:
- ✅ **SOLUCIONADO**: Configuración condicional implementada

### Error de Celery
Si hay problemas con Redis/Celery:
- ✅ **SOLUCIONADO**: Celery deshabilitado en producción

### Error de Archivos Estáticos
```bash
# Ejecutar antes de cada despliegue
python manage.py collectstatic --noinput
```

### Error de Base de Datos
Asegurar que `DATABASE_URL` esté correctamente configurado en formato:
```
postgresql://usuario:password@host:puerto/nombre_db
```
