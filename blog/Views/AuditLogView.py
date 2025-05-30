"""
API Views para gestión de logs de auditoría.

Este módulo proporciona endpoints REST para consultar logs de auditoría
con capacidades avanzadas de filtrado para monitoreo y análisis.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from datetime import timedelta
import logging

from blog.Models.AuditLogModel import AuditLog
from blog.Serializers.AuditLogSerializer import AuditLogSerializer
from blog.pagination import LargeResultsSetPagination

logger = logging.getLogger(__name__)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultar logs de auditoría (solo lectura).
    
    Los logs de auditoría son de solo lectura para mantener la integridad
    del registro histórico. Proporciona capacidades avanzadas de filtrado
    para análisis y monitoreo del sistema.
    
    **Permisos:**
    Solo usuarios staff pueden acceder a los logs de auditoría.
    
    **Filtros disponibles:**
    - `accion`: Tipo de acción realizada
    - `usuario`: Usuario que realizó la acción
    - `fecha_desde`: Logs desde una fecha específica
    - `fecha_hasta`: Logs hasta una fecha específica
    
    **Búsqueda:**
    Usar el parámetro `search` para buscar en detalles y acciones.
    
    **Ordenamiento:**
    Usar `ordering` con campos: timestamp, accion, usuario
    """
    
    serializer_class = AuditLogSerializer
    queryset = AuditLog.objects.all()
    permission_classes = [permissions.IsAdminUser]  # Solo staff
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['accion', 'detalles', 'usuario__username']
    ordering_fields = ['timestamp', 'accion', 'usuario__username']
    ordering = ['-timestamp']  # Ordenamiento por defecto
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    pagination_class = LargeResultsSetPagination
    
    @action(detail=False, methods=['get'])
    def resumen_actividad(self, request):
        """
        Endpoint para obtener un resumen de actividad del sistema.
        
        Returns:
            Response: Estadísticas de actividad por periodo
        """
        from django.db.models import Count
        
        # Actividad de las últimas 24 horas
        hace_24h = timezone.now() - timedelta(hours=24)
        actividad_24h = (self.get_queryset()
                        .filter(timestamp__gte=hace_24h)
                        .values('accion')
                        .annotate(total=Count('id'))
                        .order_by('-total'))
        
        # Actividad de la última semana
        hace_7d = timezone.now() - timedelta(days=7)
        actividad_7d = (self.get_queryset()
                       .filter(timestamp__gte=hace_7d)
                       .values('accion')
                       .annotate(total=Count('id'))
                       .order_by('-total'))
        
        # Usuarios más activos
        usuarios_activos = (self.get_queryset()
                           .filter(timestamp__gte=hace_7d)
                           .values('usuario__username')
                           .annotate(total=Count('id'))
                           .order_by('-total')[:10])
        
        data = {
            'actividad_24_horas': list(actividad_24h),
            'actividad_7_dias': list(actividad_7d),
            'usuarios_mas_activos': list(usuarios_activos),
            'total_logs': self.get_queryset().count()
        }
        
        logger.info(f"Resumen de actividad solicitado por {request.user}")
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def errores_recientes(self, request):
        """
        Endpoint para obtener errores recientes del sistema.
        
        Returns:
            Response: Lista de errores y fallos recientes
        """
        hace_24h = timezone.now() - timedelta(hours=24)
        
        errores = (self.get_queryset()
                  .filter(
                      timestamp__gte=hace_24h,
                      accion__icontains='error'
                  )
                  .order_by('-timestamp'))
        
        page = self.paginate_queryset(errores)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(errores, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def limpiar_logs_antiguos(self, request):
        """
        Endpoint para limpiar logs antiguos (solo superusuarios).
        
        Returns:
            Response: Resultado de la operación de limpieza
        """
        if not request.user.is_superuser:
            return Response(
                {'error': 'Solo superusuarios pueden realizar esta acción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        dias = request.data.get('dias', 90)  # Por defecto 90 días
        fecha_limite = timezone.now() - timedelta(days=dias)
        
        logs_antiguos = self.get_queryset().filter(timestamp__lt=fecha_limite)
        count = logs_antiguos.count()
        logs_antiguos.delete()
        
        logger.info(f"Superusuario {request.user} eliminó {count} logs antiguos")
        return Response(
            {'mensaje': f'Se eliminaron {count} logs antiguos'},
            status=status.HTTP_200_OK
        )
    