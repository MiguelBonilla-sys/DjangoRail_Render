"""
API Views para gestión de proyectos.

Este módulo proporciona endpoints REST para gestionar proyectos
con capacidades avanzadas de filtrado y búsqueda.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import logging

from blog.Models.ProyectosModel import Proyectos
from blog.Serializers.ProyectosSerializer import ProyectosSerializer
from blog.filters import ProyectosFilter

logger = logging.getLogger(__name__)


class ProyectosViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar proyectos.
    
    Proporciona operaciones CRUD completas para proyectos con:
    - Filtrado por nombre y tecnología
    - Búsqueda en texto completo
    - Ordenamiento por múltiples campos
    - Rate limiting por usuario
    - Paginación automática
    
    **Filtros disponibles:**
    - `nombre`: Buscar por nombre del proyecto
    - `tecnologia`: Buscar por tecnología en la descripción
    
    **Búsqueda:**
    Usar el parámetro `search` para buscar en nombre y descripción.
    
    **Ordenamiento:**
    Usar `ordering` con campos: nombre_proyecto, fecha_proyecto
    """
    
    serializer_class = ProyectosSerializer
    queryset = Proyectos.objects.all()
    filterset_class = ProyectosFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre_proyecto', 'descripcion_proyecto']
    ordering_fields = ['nombre_proyecto', 'fecha_proyecto']
    ordering = ['-fecha_proyecto']  # Ordenamiento por defecto
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def perform_create(self, serializer):
        """
        Crear un nuevo proyecto asignando el usuario actual como creador.
        
        Args:
            serializer: Serializer con los datos validados
        """
        logger.info(f"Usuario {self.request.user} creando nuevo proyecto")
        serializer.save(creador=self.request.user)
    
    def perform_update(self, serializer):
        """
        Actualizar un proyecto existente.
        
        Args:
            serializer: Serializer con los datos validados
        """
        logger.info(f"Usuario {self.request.user} actualizando proyecto {serializer.instance.pk}")
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def tecnologias_populares(self, request):
        """
        Endpoint para obtener las tecnologías más populares en proyectos.
        
        Returns:
            Response: Lista de tecnologías mencionadas con frecuencia
        """
        # Análisis simple de palabras clave en descripciones
        tecnologias_comunes = [
            'python', 'django', 'javascript', 'react', 'vue', 'angular',
            'nodejs', 'java', 'spring', 'docker', 'kubernetes', 'aws',
            'postgresql', 'mysql', 'mongodb', 'redis', 'git'
        ]
        
        from django.db.models import Q
        import re
        
        tecnologias_encontradas = {}
        
        proyectos = self.get_queryset()
        for proyecto in proyectos:
            texto = (proyecto.descripcion_proyecto or '').lower()
            for tech in tecnologias_comunes:
                if re.search(r'\b' + tech + r'\b', texto):
                    tecnologias_encontradas[tech] = tecnologias_encontradas.get(tech, 0) + 1
        
        # Ordenar por frecuencia
        tecnologias_ordenadas = sorted(
            tecnologias_encontradas.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        resultado = [{'tecnologia': tech, 'proyectos': count} for tech, count in tecnologias_ordenadas]
        
        logger.info(f"Tecnologías populares solicitadas por {request.user}")
        return Response(resultado, status=status.HTTP_200_OK)