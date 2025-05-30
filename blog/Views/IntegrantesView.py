"""
API Views para gestión de integrantes del equipo.

Este módulo proporciona endpoints REST para gestionar información
de los integrantes con filtros avanzados y búsqueda.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import logging

from blog.Models.IntegrantesModel import Integrantes
from blog.Serializers.IntegrantesSerializer import IntegrantesSerializer
from blog.filters import IntegrantesFilter

logger = logging.getLogger(__name__)


class IntegrantesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar integrantes del equipo.
    
    Proporciona operaciones CRUD completas para integrantes con:
    - Filtrado por nombre, semestre y estado
    - Búsqueda en texto completo
    - Ordenamiento por múltiples campos
    - Rate limiting por usuario
    - Paginación automática
    
    **Filtros disponibles:**
    - `nombre`: Buscar por nombre del integrante
    - `semestre`: Filtrar por semestre
    - `estado`: Filtrar por estado activo/inactivo
    - `habilidades`: Buscar en la reseña y habilidades
    
    **Búsqueda:**
    Usar el parámetro `search` para buscar en nombre, correo y reseña.
    
    **Ordenamiento:**
    Usar `ordering` con campos: nombre_integrante, semestre, correo
    """
    
    serializer_class = IntegrantesSerializer
    queryset = Integrantes.objects.all()
    filterset_class = IntegrantesFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre_integrante', 'correo', 'reseña', 'semestre']
    ordering_fields = ['nombre_integrante', 'semestre', 'correo']
    ordering = ['nombre_integrante']  # Ordenamiento por defecto
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def perform_create(self, serializer):
        """
        Crear un nuevo integrante asignando el usuario actual como creador.
        
        Args:
            serializer: Serializer con los datos validados
        """
        logger.info(f"Usuario {self.request.user} agregando nuevo integrante")
        serializer.save(creador=self.request.user)
    
    def perform_update(self, serializer):
        """
        Actualizar información de un integrante.
        
        Args:
            serializer: Serializer con los datos validados
        """
        logger.info(f"Usuario {self.request.user} actualizando integrante {serializer.instance.idintegrantes}")
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """
        Endpoint para obtener solo integrantes activos.
        
        Returns:
            Response: Lista de integrantes con estado activo
        """
        queryset = self.filter_queryset(
            self.get_queryset().filter(estado=True)
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_semestre(self, request):
        """
        Endpoint para agrupar integrantes por semestre.
        
        Returns:
            Response: Integrantes agrupados por semestre
        """
        from django.db.models import Count
        
        semestres = (self.get_queryset()
                    .values('semestre')
                    .annotate(total=Count('idintegrantes'))
                    .order_by('semestre'))
        
        logger.info(f"Estadísticas por semestre solicitadas por {request.user}")
        return Response(semestres, status=status.HTTP_200_OK)