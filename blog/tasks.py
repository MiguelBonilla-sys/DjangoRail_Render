"""
Tareas asíncronas para el blog usando Celery.

Este módulo contiene tareas que se ejecutan en segundo plano
para mantener la integridad y limpieza de los datos.
"""

from celery import shared_task
from django.utils import timezone
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


@shared_task
def eliminar_ofertas_expiradas():
    """
    Tarea programada para eliminar ofertas de empleo expiradas.
    
    Esta tarea se ejecuta periódicamente para limpiar la base de datos
    de ofertas que ya han superado su fecha de expiración.
    
    Returns:
        dict: Resultado de la operación con el número de ofertas eliminadas
    """
    from blog.Models.OfertasEmpleoModel import OfertasEmpleo
    
    try:
        ahora = timezone.now()
        ofertas_expiradas = OfertasEmpleo.objects.filter(fecha_expiracion__lt=ahora)
        count = ofertas_expiradas.count()
        
        if count > 0:
            ofertas_expiradas.delete()
            logger.info(f"Eliminadas {count} ofertas de empleo expiradas")
            return {
                'status': 'success',
                'eliminadas': count,
                'mensaje': f'Se eliminaron {count} ofertas expiradas'
            }
        else:
            logger.info("No hay ofertas expiradas para eliminar")
            return {
                'status': 'success',
                'eliminadas': 0,
                'mensaje': 'No hay ofertas expiradas'
            }
            
    except Exception as e:
        logger.error(f"Error al eliminar ofertas expiradas: {str(e)}")
        return {
            'status': 'error',
            'mensaje': f'Error: {str(e)}'
        }


@shared_task
def generar_reporte_estadisticas():
    """
    Tarea para generar un reporte de estadísticas del sistema.
    
    Esta tarea recopila estadísticas generales sobre todos los
    componentes del sistema para análisis y monitoreo.
    
    Returns:
        dict: Diccionario con estadísticas del sistema
    """
    try:
        from blog.Models.ConferenciasModel import Conferencias
        from blog.Models.IntegrantesModel import Integrantes
        from blog.Models.OfertasEmpleoModel import OfertasEmpleo
        from blog.Models.NoticiasModel import Noticias
        from blog.Models.CursosModel import Cursos
        from blog.Models.ProyectosModel import Proyectos
        
        ahora = timezone.now()
        
        estadisticas = {
            'fecha_reporte': ahora.isoformat(),
            'conferencias': {
                'total': Conferencias.objects.count(),
                'proximas': Conferencias.objects.filter(fecha_conferencia__gte=ahora).count()
            },
            'integrantes': {
                'total': Integrantes.objects.count(),
                'activos': Integrantes.objects.filter(estado=True).count()
            },
            'ofertas_empleo': {
                'total': OfertasEmpleo.objects.count(),
                'vigentes': OfertasEmpleo.objects.filter(fecha_expiracion__gte=ahora).count()
            },
            'noticias': {
                'total': Noticias.objects.count()
            },
            'cursos': {
                'total': Cursos.objects.count()
            },
            'proyectos': {
                'total': Proyectos.objects.count()
            }
        }
        
        logger.info("Reporte de estadísticas generado exitosamente")
        return {
            'status': 'success',
            'estadisticas': estadisticas
        }
        
    except Exception as e:
        logger.error(f"Error al generar reporte de estadísticas: {str(e)}")
        return {
            'status': 'error',
            'mensaje': f'Error: {str(e)}'
        }


@shared_task
def limpiar_logs_antiguos(dias=30):
    """
    Tarea para limpiar logs antiguos del sistema.
    
    Args:
        dias (int): Número de días de antigüedad para eliminar logs
        
    Returns:
        dict: Resultado de la operación de limpieza
    """
    try:
        import os
        from datetime import timedelta
        from django.conf import settings
        
        fecha_limite = timezone.now() - timedelta(days=dias)
        logs_dir = os.path.join(settings.BASE_DIR, 'logs')
        
        if not os.path.exists(logs_dir):
            return {
                'status': 'success',
                'mensaje': 'Directorio de logs no existe'
            }
        
        archivos_eliminados = 0
        for archivo in os.listdir(logs_dir):
            ruta_archivo = os.path.join(logs_dir, archivo)
            if os.path.isfile(ruta_archivo):
                fecha_modificacion = timezone.datetime.fromtimestamp(
                    os.path.getmtime(ruta_archivo),
                    tz=timezone.get_current_timezone()
                )
                
                if fecha_modificacion < fecha_limite:
                    os.remove(ruta_archivo)
                    archivos_eliminados += 1
        
        logger.info(f"Eliminados {archivos_eliminados} archivos de log antiguos")
        return {
            'status': 'success',
            'archivos_eliminados': archivos_eliminados,
            'mensaje': f'Se eliminaron {archivos_eliminados} archivos de log'
        }
        
    except Exception as e:
        logger.error(f"Error al limpiar logs antiguos: {str(e)}")
        return {
            'status': 'error',
            'mensaje': f'Error: {str(e)}'
        }