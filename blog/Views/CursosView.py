"""
API Views para gestión de cursos.

Este módulo proporciona endpoints REST para gestionar cursos
con capacidades avanzadas de filtrado y búsqueda.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import logging

from blog.Models.CursosModel import Cursos
from blog.Serializers.CursosSerializer import CursosSerializer
from blog.filters import CursosFilter

logger = logging.getLogger(__name__)


class CursosViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar cursos.
    
    Proporciona operaciones CRUD completas para cursos con:
    - Filtrado por nombre e instructor
    - Búsqueda en texto completo
    - Ordenamiento por múltiples campos
    - Rate limiting por usuario    - Paginación automática
    
    **Filtros disponibles:**
    - `nombre`: Buscar por nombre del curso
    - `activos`: Solo cursos actualmente en progreso
    
    **Búsqueda:**
    Usar el parámetro `search` para buscar en nombre y descripción.
    
    **Ordenamiento:**
    Usar `ordering` con campos: nombre_curso, fechainicial_curso, fechafinal_curso
    """
    
    serializer_class = CursosSerializer
    queryset = Cursos.objects.all()
    filterset_class = CursosFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre_curso', 'descripcion_curso']
    ordering_fields = ['nombre_curso', 'fechainicial_curso', 'fechafinal_curso']
    ordering = ['-fechainicial_curso']  # Ordenamiento por defecto
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def perform_create(self, serializer):
        """
        Crear un nuevo curso asignando el usuario actual como creador.
        
        Args:
            serializer: Serializer con los datos validados
        """
        logger.info(f"Usuario {self.request.user} creando nuevo curso")
        serializer.save(creador=self.request.user)
    
    def perform_update(self, serializer):
        """
        Actualizar un curso existente.
        
        Args:
            serializer: Serializer con los datos validados        """
        logger.info(f"Usuario {self.request.user} actualizando curso {serializer.instance.pk}")
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """
        Endpoint para obtener cursos actualmente activos.
        
        Returns:
            Response: Lista de cursos en progreso
        """
        from django.utils import timezone
        
        ahora = timezone.now()
        queryset = self.filter_queryset(
            self.get_queryset().filter(
                fechainicial_curso__lte=ahora,
                fechafinal_curso__gte=ahora
            )
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"Cursos activos solicitados por {request.user}")
        return Response(serializer.data, status=status.HTTP_200_OK)