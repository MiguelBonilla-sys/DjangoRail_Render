"""
API Views para gestión de ofertas de empleo.

Este módulo proporciona endpoints REST para gestionar ofertas laborales
con filtros avanzados, búsqueda y gestión de expiración automática.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
import logging

from blog.Models.OfertasEmpleoModel import OfertasEmpleo
from blog.Serializers.OfertasSerializer import OfertasEmpleoSerializer
from blog.filters import OfertasEmpleoFilter

logger = logging.getLogger(__name__)


class OfertasEmpleoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar ofertas de empleo.
    
    Proporciona operaciones CRUD completas para ofertas laborales con:
    - Filtrado por título, empresa y vigencia
    - Búsqueda en texto completo
    - Gestión automática de expiración
    - Rate limiting por usuario
    - Paginación automática
    
    **Filtros disponibles:**
    - `titulo`: Buscar por título del empleo
    - `empresa`: Buscar por nombre de empresa
    - `vigentes`: Solo ofertas no expiradas (true/false)
    - `publicado_desde`: Ofertas desde una fecha específica
    
    **Búsqueda:**
    Usar el parámetro `search` para buscar en título, empresa y descripción.
    
    **Ordenamiento:**
    Usar `ordering` con campos: fecha_publicacion, titulo_empleo, empresa
    """
    
    serializer_class = OfertasEmpleoSerializer
    queryset = OfertasEmpleo.objects.all()
    filterset_class = OfertasEmpleoFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['titulo_empleo', 'empresa', 'descripcion_empleo']
    ordering_fields = ['fecha_publicacion', 'titulo_empleo', 'empresa', 'fecha_expiracion']
    ordering = ['-fecha_publicacion']  # Ordenamiento por defecto
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def perform_create(self, serializer):
        """
        Crear una nueva oferta de empleo asignando el usuario actual como creador.
        
        Args:
            serializer: Serializer con los datos validados
        """
        logger.info(f"Usuario {self.request.user} publicando nueva oferta de empleo")
        serializer.save(creador=self.request.user)
    
    def perform_update(self, serializer):
        """
        Actualizar una oferta de empleo existente.
        
        Args:
            serializer: Serializer con los datos validados
        """
        logger.info(f"Usuario {self.request.user} actualizando oferta {serializer.instance.idoferta}")
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def vigentes(self, request):
        """
        Endpoint para obtener solo ofertas vigentes (no expiradas).
        
        Returns:
            Response: Lista de ofertas que aún están activas
        """
        queryset = self.filter_queryset(
            self.get_queryset().filter(fecha_expiracion__gte=timezone.now())
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expiradas(self, request):
        """
        Endpoint para obtener ofertas expiradas.
        
        Returns:
            Response: Lista de ofertas que ya expiraron
        """
        queryset = self.filter_queryset(
            self.get_queryset().filter(fecha_expiracion__lt=timezone.now())
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def limpiar_expiradas(self, request):
        """
        Endpoint para eliminar ofertas expiradas manualmente.
        
        Returns:
            Response: Número de ofertas eliminadas
        """
        if not request.user.is_staff:
            return Response(
                {'error': 'Solo administradores pueden realizar esta acción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        expiradas = self.get_queryset().filter(fecha_expiracion__lt=timezone.now())
        count = expiradas.count()
        expiradas.delete()
        
        logger.info(f"Usuario {request.user} eliminó {count} ofertas expiradas")
        return Response(
            {'mensaje': f'Se eliminaron {count} ofertas expiradas'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Endpoint para obtener estadísticas de ofertas de empleo.
        
        Returns:
            Response: Estadísticas básicas sobre las ofertas
        """
        total = self.get_queryset().count()
        vigentes = self.get_queryset().filter(fecha_expiracion__gte=timezone.now()).count()
        expiradas = total - vigentes
        
        # Empresas más activas
        from django.db.models import Count
        empresas_activas = (self.get_queryset()
                           .values('empresa')
                           .annotate(total=Count('idoferta'))
                           .order_by('-total')[:5])
        
        data = {
            'total_ofertas': total,
            'ofertas_vigentes': vigentes,
            'ofertas_expiradas': expiradas,
            'empresas_mas_activas': list(empresas_activas)
        }
        
        logger.info(f"Estadísticas de ofertas solicitadas por {request.user}")
        return Response(data, status=status.HTTP_200_OK)