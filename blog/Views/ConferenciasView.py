"""
API Views para gestión de conferencias.

Este módulo proporciona endpoints REST para crear, leer, actualizar
y eliminar conferencias, con capacidades avanzadas de filtrado y búsqueda.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
import logging

from blog.Models.ConferenciasModel import Conferencias
from blog.Serializers.ConferenciasSerializer import ConferenciasSerializer
from blog.filters import ConferenciasFilter
from blog.pagination import StandardResultsSetPagination

logger = logging.getLogger(__name__)


class ConferenciasViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar conferencias.
    
    Proporciona operaciones CRUD completas para conferencias con:
    - Filtrado avanzado por nombre, ponente y fechas
    - Búsqueda en texto completo
    - Ordenamiento por múltiples campos
    - Rate limiting por usuario
    - Paginación automática
    
    **Filtros disponibles:**
    - `nombre`: Buscar por nombre de conferencia
    - `ponente`: Buscar por nombre del ponente
    - `fecha_desde`: Conferencias desde una fecha específica
    - `fecha_hasta`: Conferencias hasta una fecha específica
    - `proximas`: Solo conferencias futuras (true/false)
    
    **Búsqueda:**
    Usar el parámetro `search` para buscar en nombre, ponente y descripción.
      **Ordenamiento:**
    Usar `ordering` con campos: fecha_conferencia, nombre_conferencia, ponente_conferencia
    """
    
    serializer_class = ConferenciasSerializer
    queryset = Conferencias.objects.all()
    pagination_class = StandardResultsSetPagination
    filterset_class = ConferenciasFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre_conferencia', 'ponente_conferencia', 'descripcion_conferencia']
    ordering_fields = ['fecha_conferencia', 'nombre_conferencia', 'ponente_conferencia']
    ordering = ['-fecha_conferencia']  # Ordenamiento por defecto
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def perform_create(self, serializer):
        """
        Crear una nueva conferencia asignando el usuario actual como creador.
        
        Args:
            serializer: Serializer con los datos validados
        """
        logger.info(f"Usuario {self.request.user} creando nueva conferencia")
        serializer.save(creador=self.request.user)
    
    def perform_update(self, serializer):
        """
        Actualizar una conferencia existente.
        
        Args:
            serializer: Serializer con los datos validados
        """
        logger.info(f"Usuario {self.request.user} actualizando conferencia {serializer.instance.idconferencia}")
        serializer.save()
    
    def perform_destroy(self, instance):
        """
        Eliminar una conferencia.
        
        Args:
            instance: Instancia de la conferencia a eliminar
        """
        logger.info(f"Usuario {self.request.user} eliminando conferencia {instance.idconferencia}")
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def proximas(self, request):
        """
        Endpoint personalizado para obtener solo conferencias futuras.
        
        Returns:
            Response: Lista de conferencias que aún no han ocurrido
        """
        queryset = self.filter_queryset(
            self.get_queryset().filter(fecha_conferencia__gte=timezone.now())
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Endpoint para obtener estadísticas de conferencias.
        
        Returns:
            Response: Estadísticas básicas sobre las conferencias
        """
        total = self.get_queryset().count()
        proximas = self.get_queryset().filter(fecha_conferencia__gte=timezone.now()).count()
        pasadas = total - proximas
        
        data = {
            'total_conferencias': total,
            'conferencias_proximas': proximas,
            'conferencias_pasadas': pasadas
        }
        
        logger.info(f"Estadísticas solicitadas por {request.user}")
        return Response(data, status=status.HTTP_200_OK)