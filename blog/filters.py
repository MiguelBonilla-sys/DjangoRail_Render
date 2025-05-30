"""
Filtros personalizados para las APIs del blog.

Este módulo define filtros avanzados para mejorar las capacidades
de búsqueda y filtrado de las diferentes entidades.
"""

import django_filters
from django.db import models
from django.utils import timezone
from .Models.ConferenciasModel import Conferencias
from .Models.IntegrantesModel import Integrantes
from .Models.OfertasEmpleoModel import OfertasEmpleo
from .Models.NoticiasModel import Noticias
from .Models.CursosModel import Cursos
from .Models.ProyectosModel import Proyectos


class ConferenciasFilter(django_filters.FilterSet):
    """
    Filtro personalizado para conferencias.
    
    Permite filtrar por nombre, ponente, rango de fechas y búsqueda general.
    """
    
    nombre = django_filters.CharFilter(
        field_name='nombre_conferencia',
        lookup_expr='icontains',
        help_text="Buscar por nombre de conferencia (insensible a mayúsculas)"
    )
    
    ponente = django_filters.CharFilter(
        field_name='ponente_conferencia',
        lookup_expr='icontains',
        help_text="Buscar por nombre del ponente"
    )
    
    fecha_desde = django_filters.DateTimeFilter(
        field_name='fecha_conferencia',
        lookup_expr='gte',
        help_text="Conferencias desde esta fecha"
    )
    
    fecha_hasta = django_filters.DateTimeFilter(
        field_name='fecha_conferencia',
        lookup_expr='lte',
        help_text="Conferencias hasta esta fecha"
    )
    
    proximas = django_filters.BooleanFilter(
        method='filter_proximas',
        help_text="Mostrar solo conferencias futuras"
    )

    class Meta:
        model = Conferencias
        fields = ['nombre', 'ponente', 'fecha_desde', 'fecha_hasta', 'proximas']

    def filter_proximas(self, queryset, name, value):
        """Filtra conferencias futuras."""
        if value:
            return queryset.filter(fecha_conferencia__gte=timezone.now())
        return queryset


class IntegrantesFilter(django_filters.FilterSet):
    """
    Filtro personalizado para integrantes.
    
    Permite filtrar por nombre, semestre, estado y búsqueda en reseña.
    """
    
    nombre = django_filters.CharFilter(
        field_name='nombre_integrante',
        lookup_expr='icontains',
        help_text="Buscar por nombre del integrante"
    )
    
    semestre = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text="Filtrar por semestre"
    )
    
    estado = django_filters.BooleanFilter(
        help_text="Filtrar por estado activo/inactivo"
    )
    
    habilidades = django_filters.CharFilter(
        field_name='reseña',
        lookup_expr='icontains',
        help_text="Buscar en la reseña y habilidades"
    )

    class Meta:
        model = Integrantes
        fields = ['nombre', 'semestre', 'estado', 'habilidades']


class OfertasEmpleoFilter(django_filters.FilterSet):
    """
    Filtro personalizado para ofertas de empleo.
    
    Permite filtrar por título, empresa, estado de expiración y fechas.
    """
    
    titulo = django_filters.CharFilter(
        field_name='titulo_empleo',
        lookup_expr='icontains',
        help_text="Buscar por título del empleo"
    )
    
    empresa = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text="Buscar por nombre de empresa"
    )
    
    vigentes = django_filters.BooleanFilter(
        method='filter_vigentes',
        help_text="Mostrar solo ofertas vigentes (no expiradas)"
    )
    
    publicado_desde = django_filters.DateTimeFilter(
        field_name='fecha_publicacion',
        lookup_expr='gte',
        help_text="Ofertas publicadas desde esta fecha"
    )

    class Meta:
        model = OfertasEmpleo
        fields = ['titulo', 'empresa', 'vigentes', 'publicado_desde']

    def filter_vigentes(self, queryset, name, value):
        """Filtra ofertas no expiradas."""
        if value:
            return queryset.filter(fecha_expiracion__gte=timezone.now())
        return queryset


class NoticiasFilter(django_filters.FilterSet):
    """Filtro personalizado para noticias."""
    
    titulo = django_filters.CharFilter(
        field_name='nombre_noticia',
        lookup_expr='icontains',
        help_text="Buscar por título de la noticia"
    )
    
    fuente = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text="Buscar por fuente de la noticia"
    )
    
    fecha_desde = django_filters.DateTimeFilter(
        field_name='fecha_noticia',
        lookup_expr='gte',
        help_text="Noticias desde esta fecha"
    )
    
    recientes = django_filters.BooleanFilter(
        method='filter_recientes',
        help_text="Mostrar solo noticias de los últimos 7 días"
    )

    class Meta:
        model = Noticias
        fields = ['titulo', 'fuente', 'fecha_desde', 'recientes']
    
    def filter_recientes(self, queryset, name, value):
        """Filtra noticias recientes."""
        if value:
            from datetime import timedelta
            fecha_limite = timezone.now() - timedelta(days=7)
            return queryset.filter(fecha_noticia__gte=fecha_limite)
        return queryset


class CursosFilter(django_filters.FilterSet):
    """Filtro personalizado para cursos."""
    
    nombre = django_filters.CharFilter(
        field_name='nombre_curso',
        lookup_expr='icontains',
        help_text="Buscar por nombre del curso"
    )
    
    descripcion = django_filters.CharFilter(
        field_name='descripcion_curso',
        lookup_expr='icontains',
        help_text="Buscar en la descripción del curso"
    )
    
    activos = django_filters.BooleanFilter(
        method='filter_activos',
        help_text="Mostrar solo cursos actualmente en progreso"
    )

    class Meta:
        model = Cursos
        fields = ['nombre', 'descripcion', 'activos']
    
    def filter_activos(self, queryset, name, value):
        """Filtra cursos actualmente activos."""
        if value:
            now = timezone.now()
            return queryset.filter(
                fechainicial_curso__lte=now,
                fechafinal_curso__gte=now
            )
        return queryset


class ProyectosFilter(django_filters.FilterSet):
    """Filtro personalizado para proyectos."""
    
    nombre = django_filters.CharFilter(
        field_name='nombre_proyecto',
        lookup_expr='icontains',
        help_text="Buscar por nombre del proyecto"
    )
    
    tecnologia = django_filters.CharFilter(
        field_name='descripcion_proyecto',
        lookup_expr='icontains',
        help_text="Buscar por tecnología en la descripción"
    )

    class Meta:
        model = Proyectos
        fields = ['nombre', 'tecnologia']
