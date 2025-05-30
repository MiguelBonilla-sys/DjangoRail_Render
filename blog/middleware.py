"""
Middleware personalizado para logging y auditoría.

Este módulo contiene middleware que registra automáticamente
las solicitudes HTTP y respuestas para análisis y depuración.
"""

import logging
import time
import json
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger(__name__)

# Detectar si estamos en entorno de producción
IS_PRODUCTION = getattr(settings, 'IS_PRODUCTION', False)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware para registrar todas las solicitudes HTTP.
    
    Registra información detallada sobre cada solicitud incluyendo:
    - Método HTTP y URL
    - Usuario autenticado
    - Dirección IP
    - User-Agent
    - Tiempo de respuesta
    - Código de estado HTTP    """
    
    def process_request(self, request):
        """
        Procesa la solicitud entrante y registra información básica.
        
        Args:
            request: Objeto HttpRequest de Django
        """
        request.start_time = time.time()
          # En entornos de producción, limitamos el logging para mejor performance
        if not IS_PRODUCTION:
            # Obtener información del cliente
            user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
            ip_address = self.get_client_ip(request)
            user = getattr(request, 'user', AnonymousUser())
            
            # Registrar solicitud entrante
            logger.info(
                f"REQUEST: {request.method} {request.get_full_path()} | "
                f"User: {user.username if not isinstance(user, AnonymousUser) else 'Anonymous'} | "
                f"IP: {ip_address} | "
                f"UA: {user_agent[:100]}"
            )
        
        return None
    
    def process_response(self, request, response):
        """
        Procesa la respuesta y registra el resultado.
        
        Args:
            request: Objeto HttpRequest de Django
            response: Objeto HttpResponse de Django
            
        Returns:
            HttpResponse: La respuesta original sin modificar
        """
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            user = getattr(request, 'user', AnonymousUser())
            ip_address = self.get_client_ip(request)
            
            # Determinar el nivel de log basado en el código de estado
            log_level = logging.INFO
            if response.status_code >= 400:
                log_level = logging.WARNING
            if response.status_code >= 500:
                log_level = logging.ERROR
            
            # Registrar respuesta
            logger.log(
                log_level,
                f"RESPONSE: {request.method} {request.get_full_path()} | "
                f"Status: {response.status_code} | "
                f"Duration: {duration:.3f}s | "
                f"User: {user.username if not isinstance(user, AnonymousUser) else 'Anonymous'} | "
                f"IP: {ip_address}"
            )
        
        return response
    
    def process_exception(self, request, exception):
        """
        Procesa excepciones no manejadas.
        
        Args:
            request: Objeto HttpRequest de Django
            exception: La excepción que ocurrió
        """
        user = getattr(request, 'user', AnonymousUser())
        ip_address = self.get_client_ip(request)
        
        logger.error(
            f"EXCEPTION: {request.method} {request.get_full_path()} | "
            f"Error: {str(exception)} | "
            f"Type: {type(exception).__name__} | "
            f"User: {user.username if not isinstance(user, AnonymousUser) else 'Anonymous'} | "
            f"IP: {ip_address}",
            exc_info=True
        )
        
        return None
    
    def get_client_ip(self, request):
        """
        Obtiene la dirección IP real del cliente.
        
        Args:
            request: Objeto HttpRequest de Django
            
        Returns:
            str: Dirección IP del cliente
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class APIUsageMiddleware(MiddlewareMixin):
    """
    Middleware para monitorear el uso de la API.
    
    Registra estadísticas de uso de endpoints específicos
    para análisis de rendimiento y patrones de uso.
    """
    
    def process_response(self, request, response):
        """
        Procesa la respuesta y registra estadísticas de uso de API.
        
        Args:
            request: Objeto HttpRequest de Django
            response: Objeto HttpResponse de Django
            
        Returns:
            HttpResponse: La respuesta original sin modificar
        """
        # Solo registrar para endpoints de API
        if request.path.startswith('/api/'):
            user = getattr(request, 'user', AnonymousUser())
            
            # Registrar uso de API
            api_logger = logging.getLogger('api_usage')
            api_logger.info(
                json.dumps({
                    'timestamp': time.time(),
                    'method': request.method,
                    'endpoint': request.path,
                    'status_code': response.status_code,
                    'user': user.username if not isinstance(user, AnonymousUser) else 'anonymous',
                    'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    'ip_address': self.get_client_ip(request),
                    'query_params': dict(request.GET),
                    'content_length': len(response.content) if hasattr(response, 'content') else 0
                })
            )
        
        return response
    
    def get_client_ip(self, request):
        """Obtiene la dirección IP real del cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware para agregar headers de seguridad.
    
    Agrega headers de seguridad importantes para proteger
    la aplicación contra ataques comunes.
    """
    
    def process_response(self, request, response):
        """
        Agrega headers de seguridad a la respuesta.
        
        Args:
            request: Objeto HttpRequest de Django
            response: Objeto HttpResponse de Django
            
        Returns:
            HttpResponse: La respuesta con headers de seguridad agregados
        """
        # Headers de seguridad básicos
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Solo para HTTPS en producción
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Headers específicos para API
        if request.path.startswith('/api/'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response
