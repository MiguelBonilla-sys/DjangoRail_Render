# 🚀 Integración Backend Django + Frontend Next.js

## 🎯 Visión General del Proyecto H4ck3r L4bs

**H4ck3r L4bs** es una plataforma completa de ciberseguridad y hacking ético que combina un robusto **backend Django** con un **frontend Next.js dual**. El sistema está diseñado para proporcionar dos experiencias distintas: una **parte pública** para la comunidad y una **parte administrativa** para la gestión de contenido.

### 🌐 **ESTRUCTURA DUAL DEL FRONTEND**

#### **🌍 PARTE PÚBLICA** - Sin Autenticación

> **Para visitantes y miembros de la comunidad**

- ✅ **Acceso libre** - Sin necesidad de login o registro
- ✅ **Solo lectura** - Únicamente métodos GET a la API
- ✅ **SEO optimizado** - Server-side rendering para mejor indexación
- ✅ **Responsive design** - Adaptado a móviles y tablets
- ✅ **Performance** - Carga rápida con optimizaciones de Next.js

**Rutas Públicas:**

```text
🏠 /                    - Landing page con últimas noticias
📚 /cursos              - Lista de todos los cursos disponibles
📚 /cursos/[id]         - Detalle completo de un curso específico
📰 /noticias            - Feed de noticias de ciberseguridad
📰 /noticias/[id]       - Artículo completo de noticia
🚀 /proyectos           - Showcase de proyectos de la comunidad
🚀 /proyectos/[id]      - Detalle del proyecto con tecnologías
👥 /integrantes         - Equipo de H4ck3r L4bs con perfiles
💼 /ofertas             - Ofertas de empleo en ciberseguridad
🎤 /conferencias        - Eventos y conferencias programadas
```

#### **🔐 PARTE ADMIN** - Con Autenticación

> **Para administradores del sistema**

- 🔒 **Autenticación requerida** - Login con **Username y Password** de Django
- 🛠️ **CRUD completo** - Create, Read, Update, Delete operations
- 📊 **Dashboard estadístico** - Métricas y analytics en tiempo real
- 🔍 **Gestión avanzada** - Filtros, búsqueda, ordenamiento
- 🗂️ **Gestión de archivos** - Upload de imágenes a Cloudinary

**Rutas Admin:**

```text
🏠 /admin                     - Dashboard principal con estadísticas
🔑 /admin/login               - Autenticación con credenciales Django
📚 /admin/cursos              - Gestión completa de cursos
📰 /admin/noticias            - Gestión de noticias
🚀 /admin/proyectos           - Gestión de proyectos
👥 /admin/integrantes         - Gestión del equipo
💼 /admin/ofertas             - Gestión de ofertas laborales
🎤 /admin/conferencias        - Gestión de eventos
```

### 🔐 **Sistema de Autenticación Django**

El frontend admin utiliza el **sistema de autenticación nativo de Django** que ya está configurado en el backend:

- **Username + Password** - Credenciales estándar de Django
- **Token Authentication** - JWT/Token para API calls
- **Sesiones persistentes** - Cookies seguras para mantener login
- **Roles y permisos** - Sistema de usuarios de Django

---

## 📋 Descripción del Backend Django

El proyecto **H4ck3r L4bs Backend** es una API REST completa desarrollada con Django 5.1.5 y Django REST Framework, optimizada para el ecosistema de ciberseguridad y hacking ético. Está desplegado en **Railway** en la URL: `https://apihack3r-production.up.railway.app`

### 🏗️ Arquitectura del Backend

```
DjangoRail_Render/
├── blog/                    # App principal de la API
│   ├── Models/             # 7 modelos de datos
│   │   ├── AuditLogModel.py        # Logs de auditoría
│   │   ├── ConferenciasModel.py    # Conferencias y eventos
│   │   ├── CursosModel.py          # Cursos de formación
│   │   ├── IntegrantesModel.py     # Miembros del equipo
│   │   ├── NoticiasModel.py        # Noticias de ciberseguridad
│   │   ├── OfertasEmpleoModel.py   # Ofertas laborales
│   │   └── ProyectosModel.py       # Proyectos de la comunidad
│   ├── Views/              # ViewSets de la API REST
│   ├── Serializers/        # Serializers para JSON
│   ├── filters.py          # Filtros avanzados
│   └── middleware.py       # Middleware personalizado
├── mysite/                 # Configuración del proyecto
└── static/                 # Archivos estáticos
```

### 🌐 API Endpoints Disponibles

#### **Base URL**: `https://apihack3r-production.up.railway.app/api/hl4/v1/`

| Endpoint | Descripción | Métodos | Funcionalidades |
|----------|-------------|---------|-----------------|
| `/auditlog/` | Logs de auditoría del sistema | GET | Solo lectura (admin) |
| `/conferencias/` | Gestión de conferencias | GET, POST, PUT, DELETE | CRUD completo |
| `/cursos/` | Gestión de cursos | GET, POST, PUT, DELETE | CRUD + filtros |
| `/integrantes/` | Miembros del equipo | GET, POST, PUT, DELETE | CRUD + filtros |
| `/noticias/` | Noticias de ciberseguridad | GET, POST, PUT, DELETE | CRUD + búsqueda |
| `/ofertasempleo/` | Ofertas laborales | GET, POST, PUT, DELETE | CRUD + expiración |
| `/proyectos/` | Proyectos de la comunidad | GET, POST, PUT, DELETE | CRUD + tecnologías |

#### **Documentación API**:
- **Swagger UI**: `https://apihack3r-production.up.railway.app/api/docs/`
- **ReDoc**: `https://apihack3r-production.up.railway.app/redoc/`

---

## 🔗 Modelos de Datos Detallados

### 1. **Cursos** (`/api/hl4/v1/cursos/`)
```typescript
interface Curso {
  idcursos: number;
  nombre_curso: string;
  fechainicial_curso?: string; // ISO datetime
  fechafinal_curso?: string;   // ISO datetime
  link_curso: string;          // URL
  descripcion_curso: string;
  creador: number;             // User ID
}
```

**Endpoints especiales:**
- `GET /cursos/activos/` - Cursos actualmente en progreso

### 2. **Noticias** (`/api/hl4/v1/noticias/`)
```typescript
interface Noticia {
  idnoticia: number;
  nombre_noticia: string;
  fecha_noticia: string;       // ISO datetime (auto)
  link_noticia: string;        // URL
  description_noticia: string;
  creador: number;             // User ID
  fuente?: string;
  imagen_noticia: string;      // Cloudinary URL
}
```

**Endpoints especiales:**
- `GET /noticias/recientes/` - Noticias de los últimos 7 días

### 3. **Proyectos** (`/api/hl4/v1/proyectos/`)
```typescript
interface Proyecto {
  idproyectos: number;
  nombre_proyecto: string;
  fecha_proyecto: string;      // ISO datetime
  link_proyecto: string;       // URL
  description_proyecto: string;
  creador: number;             // User ID
  integrantes: number[];       // IDs de integrantes
}
```

**Endpoints especiales:**
- `GET /proyectos/tecnologias_populares/` - Top 10 tecnologías

### 4. **Integrantes** (`/api/hl4/v1/integrantes/`)
```typescript
interface Integrante {
  idintegrantes: number;
  nombre_integrante: string;
  semestre: string;
  correo: string;              // Email válido
  link_git: string;            // GitHub URL
  imagen: string;              // Cloudinary URL
  creador: number;             // User ID
  estado: boolean;             // Activo/Inactivo
  reseña: string;
}
```

**Endpoints especiales:**
- `GET /integrantes/activos/` - Solo integrantes activos
- `GET /integrantes/por_semestre/` - Agrupados por semestre

### 5. **Ofertas de Empleo** (`/api/hl4/v1/ofertasempleo/`)
```typescript
interface OfertaEmpleo {
  idoferta: number;
  titulo_empleo: string;
  empresa: string;
  descripcion_empleo: string;
  fecha_publicacion: string;   // ISO datetime (auto)
  fecha_expiracion?: string;   // ISO datetime
  salario_min?: number;
  salario_max?: number;
  ubicacion: string;
  modalidad: 'presencial' | 'remoto' | 'hibrido';
  imagen: string;              // Cloudinary URL
  creador: number;             // User ID
}
```

**Endpoints especiales:**
- `GET /ofertasempleo/vigentes/` - Ofertas no expiradas
- `GET /ofertasempleo/expiradas/` - Ofertas expiradas
- `POST /ofertasempleo/limpiar_expiradas/` - Eliminar expiradas
- `GET /ofertasempleo/estadisticas/` - Estadísticas

### 6. **Conferencias** (`/api/hl4/v1/conferencias/`)
```typescript
interface Conferencia {
  idconferencia: number;
  nombre_conferencia: string;
  fecha_conferencia: string;   // ISO datetime
  ponente_conferencia: string;
  descripcion_conferencia: string;
  imagen_conferencia: string;  // Cloudinary URL
  creador: number;             // User ID
}
```

**Endpoints especiales:**
- `GET /conferencias/proximas/` - Conferencias futuras
- `GET /conferencias/estadisticas/` - Estadísticas

---

## 🔧 Funcionalidades Avanzadas de la API

### **Filtros y Búsqueda**
Todos los endpoints soportan:
- **Filtrado**: `?nombre=valor`
- **Búsqueda**: `?search=término`
- **Ordenamiento**: `?ordering=-fecha`
- **Paginación**: `?page=1&page_size=20`

### **Autenticación**
```typescript
// Headers requeridos para operaciones POST/PUT/DELETE
const headers = {
  'Authorization': 'Token <user-token>',
  'Content-Type': 'application/json',
}
```

### **Rate Limiting**
- **Usuarios anónimos**: 100 requests/hora
- **Usuarios autenticados**: 1000 requests/hora

---

## 🔐 Sistema de Administración Django

El proyecto incluye un **Django Admin** completamente funcional accesible en:
`https://apihack3r-production.up.railway.app/admin/`

### **Características del Admin:**
- ✅ **CRUD completo** para todos los modelos
- ✅ **Filtros avanzados** por fechas, usuarios, estados
- ✅ **Búsqueda** en tiempo real
- ✅ **Validaciones** automáticas
- ✅ **Logs de auditoría** integrados
- ✅ **Gestión de usuarios** y permisos
- ✅ **Interfaz responsiva**

---

## 🚀 Integración con Next.js - Panel de Administración

### **Paso 1: Configuración Base**

#### 1.1 Instalar Dependencias
```bash
cd frontend_hack3rlabs
npm install axios @types/axios
npm install @tanstack/react-query
npm install react-hook-form @hookform/resolvers zod
npm install lucide-react
npm install js-cookie @types/js-cookie
```

#### 1.2 Configurar Variables de Entorno
```env
# .env.local
NEXT_PUBLIC_API_BASE_URL=https://apihack3r-production.up.railway.app/api/hl4/v1
NEXT_PUBLIC_API_DOCS_URL=https://apihack3r-production.up.railway.app/api/docs
```

### **Paso 2: Estructura del Panel Admin**

```
app/
├── admin/                   # Panel de administración
│   ├── layout.tsx          # Layout del admin
│   ├── page.tsx            # Dashboard principal
│   ├── cursos/             # Gestión de cursos
│   │   ├── page.tsx
│   │   ├── nuevo/page.tsx
│   │   └── [id]/edit/page.tsx
│   ├── noticias/           # Gestión de noticias
│   ├── proyectos/          # Gestión de proyectos
│   ├── integrantes/        # Gestión de integrantes
│   ├── ofertas/            # Gestión de ofertas
│   └── login/              # Autenticación admin
│       └── page.tsx
├── components/
│   ├── admin/              # Componentes del admin
│   │   ├── AdminSidebar.tsx
│   │   ├── AdminHeader.tsx
│   │   ├── DataTable.tsx
│   │   ├── FormFields.tsx
│   │   └── StatsCards.tsx
│   └── ui/                 # Componentes base
│       ├── Button.tsx
│       ├── Input.tsx
│       ├── Modal.tsx
│       └── Toast.tsx
├── lib/
│   ├── api.ts              # Cliente API
│   ├── auth.ts             # Autenticación
│   └── utils.ts            # Utilidades
└── types/
    ├── api.ts              # Tipos de la API
    └── auth.ts             # Tipos de auth
```

### **Paso 3: Cliente API**

#### 3.1 Cliente Base (`lib/api.ts`)
```typescript
import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { getCookie } from 'js-cookie';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Interceptor para agregar token automáticamente
    this.client.interceptors.request.use((config) => {
      const token = getCookie('auth_token');
      if (token) {
        config.headers.Authorization = `Token ${token}`;
      }
      return config;
    });

    // Interceptor para manejar errores
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Redirect a login
          window.location.href = '/admin/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Métodos genéricos
  async get<T>(endpoint: string, params?: any): Promise<T> {
    const response: AxiosResponse<T> = await this.client.get(endpoint, { params });
    return response.data;
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    const response: AxiosResponse<T> = await this.client.post(endpoint, data);
    return response.data;
  }

  async put<T>(endpoint: string, data: any): Promise<T> {
    const response: AxiosResponse<T> = await this.client.put(endpoint, data);
    return response.data;
  }

  async delete<T>(endpoint: string): Promise<T> {
    const response: AxiosResponse<T> = await this.client.delete(endpoint);
    return response.data;
  }

  // Métodos específicos para cada endpoint
  
  // CURSOS
  async getCursos(params?: { search?: string; page?: number }) {
    return this.get<PaginatedResponse<Curso>>('/cursos/', params);
  }

  async getCurso(id: number) {
    return this.get<Curso>(`/cursos/${id}/`);
  }

  async createCurso(data: Omit<Curso, 'idcursos'>) {
    return this.post<Curso>('/cursos/', data);
  }

  async updateCurso(id: number, data: Partial<Curso>) {
    return this.put<Curso>(`/cursos/${id}/`, data);
  }

  async deleteCurso(id: number) {
    return this.delete(`/cursos/${id}/`);
  }

  // NOTICIAS
  async getNoticias(params?: { search?: string; page?: number }) {
    return this.get<PaginatedResponse<Noticia>>('/noticias/', params);
  }

  async getNoticia(id: number) {
    return this.get<Noticia>(`/noticias/${id}/`);
  }

  async createNoticia(data: Omit<Noticia, 'idnoticia'>) {
    return this.post<Noticia>('/noticias/', data);
  }

  async updateNoticia(id: number, data: Partial<Noticia>) {
    return this.put<Noticia>(`/noticias/${id}/`, data);
  }

  async deleteNoticia(id: number) {
    return this.delete(`/noticias/${id}/`);
  }

  // PROYECTOS
  async getProyectos(params?: { search?: string; page?: number }) {
    return this.get<PaginatedResponse<Proyecto>>('/proyectos/', params);
  }

  async getProyecto(id: number) {
    return this.get<Proyecto>(`/proyectos/${id}/`);
  }

  async createProyecto(data: Omit<Proyecto, 'idproyectos'>) {
    return this.post<Proyecto>('/proyectos/', data);
  }

  async updateProyecto(id: number, data: Partial<Proyecto>) {
    return this.put<Proyecto>(`/proyectos/${id}/`, data);
  }

  async deleteProyecto(id: number) {
    return this.delete(`/proyectos/${id}/`);
  }

  // INTEGRANTES
  async getIntegrantes(params?: { search?: string; page?: number }) {
    return this.get<PaginatedResponse<Integrante>>('/integrantes/', params);
  }

  async getIntegrante(id: number) {
    return this.get<Integrante>(`/integrantes/${id}/`);
  }

  async createIntegrante(data: Omit<Integrante, 'idintegrantes'>) {
    return this.post<Integrante>('/integrantes/', data);
  }

  async updateIntegrante(id: number, data: Partial<Integrante>) {
    return this.put<Integrante>(`/integrantes/${id}/`, data);
  }

  async deleteIntegrante(id: number) {
    return this.delete(`/integrantes/${id}/`);
  }

  // OFERTAS DE EMPLEO
  async getOfertas(params?: { search?: string; page?: number }) {
    return this.get<PaginatedResponse<OfertaEmpleo>>('/ofertasempleo/', params);
  }

  async getOferta(id: number) {
    return this.get<OfertaEmpleo>(`/ofertasempleo/${id}/`);
  }

  async createOferta(data: Omit<OfertaEmpleo, 'idoferta'>) {
    return this.post<OfertaEmpleo>('/ofertasempleo/', data);
  }

  async updateOferta(id: number, data: Partial<OfertaEmpleo>) {
    return this.put<OfertaEmpleo>(`/ofertasempleo/${id}/`, data);
  }

  async deleteOferta(id: number) {
    return this.delete(`/ofertasempleo/${id}/`);
  }

  // AUTENTICACIÓN
  async login(username: string, password: string) {
    return this.post<{ token: string; user: User }>('/auth/login/', {
      username,
      password,
    });
  }

  async logout() {
    return this.post('/auth/logout/', {});
  }

  async getProfile() {
    return this.get<User>('/auth/profile/');
  }
}

export const apiClient = new APIClient();
```

#### 3.2 Tipos TypeScript (`types/api.ts`)
```typescript
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
  is_superuser: boolean;
}

export interface Curso {
  idcursos: number;
  nombre_curso: string;
  fechainicial_curso?: string;
  fechafinal_curso?: string;
  link_curso: string;
  descripcion_curso: string;
  creador: number;
}

export interface Noticia {
  idnoticia: number;
  nombre_noticia: string;
  fecha_noticia: string;
  link_noticia: string;
  description_noticia: string;
  creador: number;
  fuente?: string;
  imagen_noticia: string;
}

export interface Proyecto {
  idproyectos: number;
  nombre_proyecto: string;
  fecha_proyecto: string;
  link_proyecto: string;
  description_proyecto: string;
  creador: number;
  integrantes: number[];
}

export interface Integrante {
  idintegrantes: number;
  nombre_integrante: string;
  semestre: string;
  correo: string;
  link_git: string;
  imagen: string;
  creador: number;
  estado: boolean;
  reseña: string;
}

export interface OfertaEmpleo {
  idoferta: number;
  titulo_empleo: string;
  empresa: string;
  descripcion_empleo: string;
  fecha_publicacion: string;
  fecha_expiracion?: string;
  salario_min?: number;
  salario_max?: number;
  ubicacion: string;
  modalidad: 'presencial' | 'remoto' | 'hibrido';
  imagen: string;
  creador: number;
}

export interface Conferencia {
  idconferencia: number;
  nombre_conferencia: string;
  fecha_conferencia: string;
  ponente_conferencia: string;
  descripcion_conferencia: string;
  imagen_conferencia: string;
  creador: number;
}
```

### **Paso 4: Sistema de Autenticación**

#### 4.1 Hook de Autenticación (`lib/auth.ts`)
```typescript
'use client';

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { setCookie, deleteCookie, getCookie } from 'js-cookie';
import { apiClient } from './api';
import { User } from '@/types/api';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

export const useAuth = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (username: string, password: string) => {
        set({ isLoading: true });
        try {
          const response = await apiClient.login(username, password);
          const { token, user } = response;

          setCookie('auth_token', token, { expires: 7 }); // 7 días
          set({
            user,
            token,
            isAuthenticated: true,
            isLoading: false,
          });

          return true;
        } catch (error) {
          set({ isLoading: false });
          console.error('Login failed:', error);
          return false;
        }
      },

      logout: () => {
        deleteCookie('auth_token');
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },

      checkAuth: async () => {
        const token = getCookie('auth_token');
        if (!token) {
          set({ isAuthenticated: false });
          return;
        }

        try {
          const user = await apiClient.getProfile();
          set({
            user,
            token,
            isAuthenticated: true,
          });
        } catch (error) {
          // Token inválido
          deleteCookie('auth_token');
          set({
            user: null,
            token: null,
            isAuthenticated: false,
          });
        }
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
```

### **Paso 5: Componentes del Panel Admin**

#### 5.1 Layout del Admin (`app/admin/layout.tsx`)
```typescript
'use client';

import { useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import AdminSidebar from '@/components/admin/AdminSidebar';
import AdminHeader from '@/components/admin/AdminHeader';

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, checkAuth, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/admin/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-500"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      <AdminSidebar />
      <div className="lg:pl-64">
        <AdminHeader />
        <main className="py-6">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
```

#### 5.2 Dashboard Principal (`app/admin/page.tsx`)
```typescript
'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api';
import StatsCards from '@/components/admin/StatsCards';
import { Users, BookOpen, Newspaper, Briefcase } from 'lucide-react';

interface DashboardStats {
  totalCursos: number;
  totalNoticias: number;
  totalProyectos: number;
  totalIntegrantes: number;
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalCursos: 0,
    totalNoticias: 0,
    totalProyectos: 0,
    totalIntegrantes: 0,
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [cursos, noticias, proyectos, integrantes] = await Promise.all([
          apiClient.getCursos({ page: 1 }),
          apiClient.getNoticias({ page: 1 }),
          apiClient.getProyectos({ page: 1 }),
          apiClient.getIntegrantes({ page: 1 }),
        ]);

        setStats({
          totalCursos: cursos.count,
          totalNoticias: noticias.count,
          totalProyectos: proyectos.count,
          totalIntegrantes: integrantes.count,
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Panel de Administración
        </h1>
        <p className="mt-2 text-sm text-gray-300">
          Gestiona el contenido de H4ck3r L4bs
        </p>
      </div>

      <StatsCards
        stats={[
          {
            title: 'Total Cursos',
            value: stats.totalCursos,
            icon: BookOpen,
            color: 'blue',
            href: '/admin/cursos',
          },
          {
            title: 'Total Noticias',
            value: stats.totalNoticias,
            icon: Newspaper,
            color: 'green',
            href: '/admin/noticias',
          },
          {
            title: 'Total Proyectos',
            value: stats.totalProyectos,
            icon: Briefcase,
            color: 'purple',
            href: '/admin/proyectos',
          },
          {
            title: 'Total Integrantes',
            value: stats.totalIntegrantes,
            icon: Users,
            color: 'orange',
            href: '/admin/integrantes',
          },
        ]}
      />

      {/* Gráficos y estadísticas adicionales */}
      <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
            Actividad Reciente
          </h3>
          {/* Aquí puedes agregar una lista de actividad reciente */}
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
            Enlaces Útiles
          </h3>
          <div className="space-y-2">
            <a
              href={process.env.NEXT_PUBLIC_API_DOCS_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="block text-green-600 hover:text-green-700 dark:text-green-400"
            >
              📚 Documentación de la API
            </a>
            <a
              href="https://apihack3r-production.up.railway.app/admin/"
              target="_blank"
              rel="noopener noreferrer"
              className="block text-green-600 hover:text-green-700 dark:text-green-400"
            >
              🔧 Django Admin
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
```

#### 5.3 Página de Login (`app/admin/login/page.tsx`)
```typescript
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { Eye, EyeOff } from 'lucide-react';

export default function AdminLogin() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { login, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/admin');
    }
  }, [isAuthenticated, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    const success = await login(username, password);

    if (success) {
      router.push('/admin');
    } else {
      setError('Credenciales inválidas. Verifica tu usuario y contraseña.');
    }

    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-green-900 to-gray-900">
      <div className="max-w-md w-full space-y-8 p-8">
        <div className="bg-black/20 backdrop-blur-md rounded-xl p-8 border border-green-500/20">
          <div className="text-center">
            <h2 className="mt-6 text-3xl font-extrabold text-white">
              Admin H4ck3r L4bs
            </h2>
            <p className="mt-2 text-sm text-gray-300">
              Acceso al panel de administración
            </p>
          </div>

          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3">
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            )}

            <div>
              <label htmlFor="username" className="sr-only">
                Usuario
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white rounded-lg bg-gray-800/50 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder="Usuario"
              />
            </div>

            <div className="relative">
              <label htmlFor="password" className="sr-only">
                Contraseña
              </label>
              <input
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="relative block w-full px-3 py-2 pr-10 border border-gray-600 placeholder-gray-400 text-white rounded-lg bg-gray-800/50 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder="Contraseña"
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <EyeOff className="h-5 w-5 text-gray-400" />
                ) : (
                  <Eye className="h-5 w-5 text-gray-400" />
                )}
              </button>
            </div>

            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-lg text-black bg-green-500 hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
              </button>
            </div>
          </form>

          <div className="mt-6">
            <div className="text-center">
              <p className="text-sm text-gray-400">
                ¿No tienes acceso?{' '}
                <a
                  href="mailto:admin@hack3rlabs.com"
                  className="text-green-400 hover:text-green-300"
                >
                  Contacta al administrador
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

### **Paso 6: Gestión de Cursos (Ejemplo Completo)**

#### 6.1 Lista de Cursos (`app/admin/cursos/page.tsx`)
```typescript
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { Curso, PaginatedResponse } from '@/types/api';
import DataTable from '@/components/admin/DataTable';
import { Plus, Search, Edit, Trash2 } from 'lucide-react';

export default function CursosAdminPage() {
  const [cursos, setCursos] = useState<PaginatedResponse<Curso>>({
    count: 0,
    next: null,
    previous: null,
    results: [],
  });
  const [search, setSearch] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [isLoading, setIsLoading] = useState(true);

  const router = useRouter();

  const fetchCursos = async () => {
    setIsLoading(true);
    try {
      const data = await apiClient.getCursos({
        search: search || undefined,
        page: currentPage,
      });
      setCursos(data);
    } catch (error) {
      console.error('Error fetching cursos:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCursos();
  }, [search, currentPage]);

  const handleDelete = async (id: number) => {
    if (confirm('¿Estás seguro de que quieres eliminar este curso?')) {
      try {
        await apiClient.deleteCurso(id);
        fetchCursos(); // Refrescar la lista
      } catch (error) {
        console.error('Error deleting curso:', error);
        alert('Error al eliminar el curso');
      }
    }
  };

  const columns = [
    {
      key: 'nombre_curso',
      title: 'Nombre',
      render: (value: string) => (
        <div className="font-medium text-gray-900 dark:text-white">{value}</div>
      ),
    },
    {
      key: 'fechainicial_curso',
      title: 'Fecha Inicio',
      render: (value: string) => (
        <div className="text-sm text-gray-600 dark:text-gray-400">
          {value ? new Date(value).toLocaleDateString() : '-'}
        </div>
      ),
    },
    {
      key: 'fechafinal_curso',
      title: 'Fecha Fin',
      render: (value: string) => (
        <div className="text-sm text-gray-600 dark:text-gray-400">
          {value ? new Date(value).toLocaleDateString() : '-'}
        </div>
      ),
    },
    {
      key: 'actions',
      title: 'Acciones',
      render: (_: any, item: Curso) => (
        <div className="flex space-x-2">
          <button
            onClick={() => router.push(`/admin/cursos/${item.idcursos}/edit`)}
            className="text-blue-600 hover:text-blue-700 dark:text-blue-400"
          >
            <Edit className="h-4 w-4" />
          </button>
          <button
            onClick={() => handleDelete(item.idcursos)}
            className="text-red-600 hover:text-red-700 dark:text-red-400"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Gestión de Cursos
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Administra los cursos de formación
          </p>
        </div>
        <button
          onClick={() => router.push('/admin/cursos/nuevo')}
          className="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        >
          <Plus className="h-4 w-4 mr-2" />
          Nuevo Curso
        </button>
      </div>

      <div className="mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            placeholder="Buscar cursos..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10 pr-4 py-2 w-full border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>
      </div>

      <DataTable
        data={cursos.results}
        columns={columns}
        isLoading={isLoading}
        pagination={{
          current: currentPage,
          total: Math.ceil(cursos.count / 20),
          onPageChange: setCurrentPage,
        }}
      />
    </div>
  );
}
```

#### 6.2 Formulario de Curso (`app/admin/cursos/nuevo/page.tsx`)
```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { apiClient } from '@/lib/api';
import { Save, ArrowLeft } from 'lucide-react';

const cursoSchema = z.object({
  nombre_curso: z.string().min(1, 'El nombre es requerido').max(120),
  fechainicial_curso: z.string().optional(),
  fechafinal_curso: z.string().optional(),
  link_curso: z.string().url('Debe ser una URL válida'),
  descripcion_curso: z.string().min(1, 'La descripción es requerida').max(1200),
});

type CursoForm = z.infer<typeof cursoSchema>;

export default function NuevoCursoPage() {
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CursoForm>({
    resolver: zodResolver(cursoSchema),
  });

  const onSubmit = async (data: CursoForm) => {
    setIsLoading(true);
    try {
      // Obtener el ID del usuario actual (deberías tenerlo en el contexto de auth)
      await apiClient.createCurso({
        ...data,
        creador: 1, // Este debería ser el ID del usuario actual
      });
      router.push('/admin/cursos');
    } catch (error) {
      console.error('Error creating curso:', error);
      alert('Error al crear el curso');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <button
          onClick={() => router.back()}
          className="inline-flex items-center text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200 mb-4"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Volver
        </button>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Nuevo Curso
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Crea un nuevo curso de formación
        </p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Nombre del Curso *
            </label>
            <input
              {...register('nombre_curso')}
              type="text"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
              placeholder="Ej: Introducción a la Ciberseguridad"
            />
            {errors.nombre_curso && (
              <p className="mt-1 text-sm text-red-600">{errors.nombre_curso.message}</p>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Fecha de Inicio
              </label>
              <input
                {...register('fechainicial_curso')}
                type="datetime-local"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
              {errors.fechainicial_curso && (
                <p className="mt-1 text-sm text-red-600">{errors.fechainicial_curso.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Fecha de Fin
              </label>
              <input
                {...register('fechafinal_curso')}
                type="datetime-local"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
              {errors.fechafinal_curso && (
                <p className="mt-1 text-sm text-red-600">{errors.fechafinal_curso.message}</p>
              )}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Enlace del Curso *
            </label>
            <input
              {...register('link_curso')}
              type="url"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
              placeholder="https://ejemplo.com/curso"
            />
            {errors.link_curso && (
              <p className="mt-1 text-sm text-red-600">{errors.link_curso.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Descripción *
            </label>
            <textarea
              {...register('descripcion_curso')}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
              placeholder="Describe el contenido, objetivos y metodología del curso..."
            />
            {errors.descripcion_curso && (
              <p className="mt-1 text-sm text-red-600">{errors.descripcion_curso.message}</p>
            )}
          </div>

          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => router.back()}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Save className="h-4 w-4 mr-2" />
              {isLoading ? 'Guardando...' : 'Guardar Curso'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

---

## 🔗 Integración con el Sistema Existente

### **Actualizar el Header Principal**
En tu componente `Header.tsx` existente, agrega un enlace al panel admin:

```typescript
// En components/Header.tsx
const navigation = [
  { name: 'Inicio', href: '/' },
  { name: 'Cursos', href: '/cursos' },
  { name: 'Proyectos', href: '/proyectos' },
  { name: 'Noticias', href: '/noticias' },
  { name: 'Ofertas', href: '/ofertas' },
  { name: 'Admin', href: '/admin' }, // ← Nuevo enlace
];
```

### **Sincronización de Datos**
Para que tu frontend muestre datos reales del backend:

1. **Reemplaza los datos estáticos** en cada sección con llamadas a la API
2. **Usa React Query** para caché y sincronización automática
3. **Implementa SSR/ISR** para mejor SEO

### **Ejemplo de Integración en Cursos:**
```typescript
// En app/cursos/components/CursosContent.tsx
'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api';
import { Curso } from '@/types/api';

export default function CursosContent() {
  const [cursos, setCursos] = useState<Curso[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCursos = async () => {
      try {
        const data = await apiClient.getCursos();
        setCursos(data.results);
      } catch (error) {
        console.error('Error fetching cursos:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCursos();
  }, []);

  if (loading) {
    return <div>Cargando cursos...</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {cursos.map((curso) => (
        <div key={curso.idcursos} className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold mb-2">{curso.nombre_curso}</h3>
          <p className="text-gray-600 mb-4">{curso.descripcion_curso}</p>
          {curso.fechainicial_curso && (
            <p className="text-sm text-gray-500">
              Inicio: {new Date(curso.fechainicial_curso).toLocaleDateString()}
            </p>
          )}
          <a
            href={curso.link_curso}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block mt-4 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Ver Curso
          </a>
        </div>
      ))}
    </div>
  );
}
```

---

## 🚀 Comandos para Implementar

### **1. Instalar Dependencias**
```bash
cd frontend_hack3rlabs
npm install axios @types/axios @tanstack/react-query react-hook-form @hookform/resolvers zod lucide-react js-cookie @types/js-cookie zustand
```

### **2. Crear Estructura de Carpetas**
```bash
mkdir -p app/admin/{cursos,noticias,proyectos,integrantes,ofertas,login}
mkdir -p components/admin
mkdir -p lib
mkdir -p types
```

### **3. Variables de Entorno**
```bash
echo "NEXT_PUBLIC_API_BASE_URL=https://apihack3r-production.up.railway.app/api/hl4/v1" >> .env.local
echo "NEXT_PUBLIC_API_DOCS_URL=https://apihack3r-production.up.railway.app/api/docs" >> .env.local
```

---

## 📝 Próximos Pasos

1. **Implementar el cliente API** siguiendo el código proporcionado
2. **Crear el sistema de autenticación** con el backend Django
3. **Desarrollar el panel de administración** página por página
4. **Integrar los datos reales** en el frontend existente
5. **Agregar funcionalidades avanzadas** como upload de imágenes
6. **Implementar notificaciones** y feedback de usuario
7. **Optimizar el rendimiento** con caché y lazy loading

---

## 🔧 Soporte y Mantenimiento

- **API Documentación**: https://apihack3r-production.up.railway.app/api/docs/
- **Django Admin**: https://apihack3r-production.up.railway.app/admin/
- **Backend Repo**: Tu repositorio actual
- **Frontend Repo**: Tu repositorio de Next.js

---

Esta integración te permitirá tener un **sistema completo** donde:
- ✅ El **backend Django** maneja toda la lógica de negocio y datos
- ✅ El **frontend Next.js** consume la API y muestra el contenido
- ✅ El **panel de administración** permite gestionar todo el contenido
- ✅ Los **datos son consistentes** entre todas las plataformas
- ✅ La **escalabilidad** está garantizada con esta arquitectura

¿Te gustaría que implemente alguna sección específica o necesitas aclaración sobre algún punto?
