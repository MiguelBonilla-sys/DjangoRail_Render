"""
Clases de paginación personalizadas para las APIs del blog.

Este módulo define diferentes tipos de paginación para optimizar
la respuesta de la API según el tipo de contenido.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """
    Paginación estándar para la mayoría de endpoints.
    
    Proporciona 20 elementos por página con información adicional
    sobre la paginación en la respuesta.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """
        Respuesta personalizada con metadatos de paginación.
        
        Args:
            data: Datos serializados de la página actual
            
        Returns:
            Response: Respuesta con datos y metadatos de paginación
        """
        return Response({
            'pagination': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'count': self.page.paginator.count,
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'page_size': self.get_page_size(self.request)
            },
            'results': data
        })


class LargeResultsSetPagination(PageNumberPagination):
    """
    Paginación para conjuntos grandes de datos.
    
    Útil para endpoints que manejan grandes volúmenes de información
    como logs de auditoría o históricos.
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200
    
    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'count': self.page.paginator.count,
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'page_size': self.get_page_size(self.request)
            },
            'results': data
        })


class SmallResultsSetPagination(PageNumberPagination):
    """
    Paginación para conjuntos pequeños de datos.
    
    Ideal para endpoints con pocos elementos como integrantes
    o configuraciones.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    
    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'count': self.page.paginator.count,
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'page_size': self.get_page_size(self.request)
            },
            'results': data
        })
