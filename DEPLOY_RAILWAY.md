# 🚂 Despliegue en Railway - RECOMENDADO

## ¿Por qué Railway es perfecto para tu backend Django?

✅ **Soporte nativo para Django** con PostgreSQL y Redis incluidos  
✅ **Celery workers** funcionan perfectamente  
✅ **Precio competitivo** - $5/mes con generosos límites  
✅ **GitHub integration** automática  
✅ **Variables de entorno** fáciles de configurar  
✅ **Logs en tiempo real** y monitoreo integrado  

---

## 📋 PASO A PASO

### 1. Preparar archivos de configuración

#### **Procfile** (crear en la raíz del proyecto)
```bash
web: gunicorn mysite.wsgi --bind 0.0.0.0:$PORT
worker: celery -A mysite worker --loglevel=info
beat: celery -A mysite beat --loglevel=info
```

#### **railway.json** (crear en la raíz del proyecto)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "sleepApplication": false,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

#### **requirements.txt** (agregar gunicorn)
```bash
# Agregar estas líneas al final de requirements.txt
gunicorn==21.2.0
whitenoise[brotli]==6.6.0
```

### 2. Configurar Railway

#### **Crear cuenta y proyecto:**
1. Ve a [railway.app](https://railway.app)
2. Conecta tu cuenta de GitHub
3. Clic en "New Project" → "Deploy from GitHub repo"
4. Selecciona tu repositorio Django

#### **Agregar servicios necesarios:**
1. **PostgreSQL**: Clic en "+ Add Service" → "Database" → "PostgreSQL"
2. **Redis**: Clic en "+ Add Service" → "Database" → "Redis"

### 3. Variables de Entorno

En el dashboard de Railway, ve a tu proyecto Django → "Variables":

```bash
SECRET_KEY=tu_clave_secreta_django_super_larga_y_segura_aqui
DEBUG=False
ALLOWED_HOSTS=*.railway.app,tu-dominio-personalizado.com
DJANGO_SETTINGS_MODULE=mysite.settings

# Se generan automáticamente cuando agregas los servicios:
DATABASE_URL=postgresql://user:pass@host:port/db  # Auto-generada
REDIS_URL=redis://default:pass@host:port  # Auto-generada

# Cloudinary (para archivos)
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key  
CLOUDINARY_API_SECRET=tu_api_secret

# Configuración específica Railway
RAILWAY_ENVIRONMENT=production
PORT=8000
```

### 4. Configurar múltiples servicios

Railway puede ejecutar múltiples procesos. Crea estos servicios:

#### **Servicio Web (Django API)**
- Comando: `gunicorn mysite.wsgi --bind 0.0.0.0:$PORT`
- Puerto: 8000
- Público: Sí

#### **Servicio Worker (Celery)**
- Comando: `celery -A mysite worker --loglevel=info`
- Puerto: No aplica
- Público: No

#### **Servicio Beat (Tareas programadas)**
- Comando: `celery -A mysite beat --loglevel=info`
- Puerto: No aplica  
- Público: No

### 5. Comandos post-deploy

Railway ejecutará automáticamente:
```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

---

## 🔧 CONFIGURACIÓN AVANZADA

### **Dominios personalizados**
1. Ve a tu servicio web → "Settings" → "Custom Domain"
2. Agrega tu dominio (ej: `api.tuapp.com`)
3. Configura DNS apuntando a Railway

### **Monitoreo y Logs**
```bash
# Ver logs en tiempo real
railway logs --service web
railway logs --service worker

# Ejecutar comandos Django
railway run python manage.py createsuperuser
railway run python manage.py shell
```

### **Escalado automático**
Railway escala automáticamente basado en uso:
- CPU > 80% → Escala hacia arriba
- CPU < 20% → Escala hacia abajo

---

## 💰 COSTOS

### **Plan Hobby (Recomendado para inicio)**
- **$5/mes** por servicio activo
- **500 horas** de ejecución incluidas
- **PostgreSQL gratuito** (500MB)
- **Redis gratuito** (25MB)

### **Estimación para tu proyecto:**
- Web service: $5/mes
- Worker service: $5/mes  
- Beat service: $5/mes
- **Total: ~$15/mes** (muy competitivo)

---

## 🚀 DESPLIEGUE

### **Comandos para deploy:**
```powershell
# Instalar Railway CLI
npm install -g @railway/cli

# Login y deploy
railway login
railway link
railway up
```

### **URL de tu API:**
Tu API estará disponible en:
```
https://tu-proyecto-production.up.railway.app/api/hl4/v1/
```

---

## ✅ VENTAJAS vs Vercel

| Característica | Railway | Vercel |
|---|---|---|
| **Django nativo** | ✅ Excelente | ⚠️ Limitado |
| **PostgreSQL** | ✅ Incluido gratis | ❌ Externo |
| **Redis/Celery** | ✅ Funciona perfecto | ❌ Complicado |
| **Workers background** | ✅ Nativo | ❌ No soportado |
| **Logs y monitoreo** | ✅ Tiempo real | ⚠️ Básico |
| **Costo** | ✅ $15/mes | ⚠️ Funciones limitadas |

---

## 🔗 INTEGRACIÓN CON NEXTJS

### **En tu frontend NextJS:**
```javascript
// .env.local
NEXT_PUBLIC_API_BASE_URL=https://tu-proyecto-production.up.railway.app

// utils/api.js
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

export const fetchConferencias = async () => {
  const response = await fetch(`${API_BASE}/api/hl4/v1/conferencias/`);
  return response.json();
};
```

**Railway es la opción ideal para tu backend Django** - es robusto, escalable y perfecto para trabajar con NextJS frontend! 🎯
