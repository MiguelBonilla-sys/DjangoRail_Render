"""
API Views para gestión de noticias.

Este módulo proporciona endpoints REST para gestionar noticias
con capacidades avanzadas de filtrado y búsqueda.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
import logging

from blog.Models.NoticiasModel import Noticias
from blog.Serializers.NoticiasSerializer import NoticiasSerializer
from blog.filters import NoticiasFilter

logger = logging.getLogger(__name__)


class NoticiasViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar noticias.
    
    Proporciona operaciones CRUD completas para noticias con:
    - Filtrado por título y fechas
    - Búsqueda en texto completo
    - Ordenamiento por múltiples campos
    - Rate limiting por usuario
    - Paginación automática
    
    **Filtros disponibles:**
    - `titulo`: Buscar por título de la noticia
    - `fecha_desde`: Noticias desde una fecha específica
    
    **Búsqueda:**
    Usar el parámetro `search` para buscar en título y descripción.
      **Ordenamiento:**
    Usar `ordering` con campos: fecha_noticia, nombre_noticia
    """
    
    serializer_class = NoticiasSerializer
    queryset = Noticias.objects.all()
    filterset_class = NoticiasFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre_noticia', 'description_noticia', 'fuente']
    ordering_fields = ['fecha_noticia', 'nombre_noticia']
    ordering = ['-fecha_noticia']  # Ordenamiento por defecto
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def perform_create(self, serializer):
        """
        Crear una nueva noticia asignando el usuario actual como creador.
        
        Args:
            serializer: Serializer con los datos validados
        """
        logger.info(f"Usuario {self.request.user} creando nueva noticia")
        serializer.save(creador=self.request.user)
    
    def perform_update(self, serializer):
        """
        Actualizar una noticia existente.
        
        Args:
            serializer: Serializer con los datos validados
        """
        logger.info(f"Usuario {self.request.user} actualizando noticia {serializer.instance.pk}")
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def recientes(self, request):
        """
        Endpoint para obtener las noticias más recientes.
        
        Returns:
            Response: Lista de las últimas 10 noticias
        """
        from datetime import timedelta
        
        fecha_limite = timezone.now() - timedelta(days=30)
        queryset = self.filter_queryset(
            self.get_queryset().filter(fecha_noticia__gte=fecha_limite)
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)