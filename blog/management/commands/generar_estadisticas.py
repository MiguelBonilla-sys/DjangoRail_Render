"""
Comando de gestión para generar reportes de estadísticas del sistema.

Este comando permite generar reportes detallados sobre el uso
y estado del sistema desde la línea de comandos.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta
import json


class Command(BaseCommand):
    """
    Comando para generar reportes de estadísticas del sistema.
    
    Uso:
        python manage.py generar_estadisticas
        python manage.py generar_estadisticas --formato json
        python manage.py generar_estadisticas --dias 30
    """
    
    help = 'Genera un reporte de estadísticas del sistema'
    
    def add_arguments(self, parser):
        """
        Agrega argumentos al comando.
        
        Args:
            parser: ArgumentParser de Django
        """
        parser.add_argument(
            '--formato',
            type=str,
            default='texto',
            choices=['texto', 'json'],
            help='Formato de salida del reporte (texto o json)'
        )
        
        parser.add_argument(
            '--dias',
            type=int,
            default=30,
            help='Número de días hacia atrás para el análisis (default: 30)'
        )
        
        parser.add_argument(
            '--output',
            type=str,
            help='Archivo donde guardar el reporte (opcional)'
        )
    
    def handle(self, *args, **options):
        """
        Ejecuta el comando principal.
        
        Args:
            *args: Argumentos posicionales
            **options: Opciones del comando
        """
        self.stdout.write(
            self.style.SUCCESS('Generando reporte de estadísticas...')
        )
        
        formato = options['formato']
        dias = options['dias']
        output_file = options.get('output')
        
        # Generar estadísticas
        estadisticas = self.generar_estadisticas(dias)
        
        # Formatear salida
        if formato == 'json':
            contenido = json.dumps(estadisticas, indent=2, default=str)
        else:
            contenido = self.formatear_texto(estadisticas)
        
        # Mostrar o guardar resultado
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(contenido)
            self.stdout.write(
                self.style.SUCCESS(f'Reporte guardado en: {output_file}')
            )
        else:
            self.stdout.write(contenido)
    
    def generar_estadisticas(self, dias):
        """
        Genera las estadísticas del sistema.
        
        Args:
            dias (int): Número de días para el análisis
            
        Returns:
            dict: Diccionario con las estadísticas
        """
        from blog.Models.ConferenciasModel import Conferencias
        from blog.Models.IntegrantesModel import Integrantes
        from blog.Models.OfertasEmpleoModel import OfertasEmpleo
        from blog.Models.NoticiasModel import Noticias
        from blog.Models.CursosModel import Cursos
        from blog.Models.ProyectosModel import Proyectos
        from blog.Models.AuditLogModel import AuditLog
        
        ahora = timezone.now()
        fecha_limite = ahora - timedelta(days=dias)
        
        estadisticas = {
            'fecha_generacion': ahora,
            'periodo_analisis_dias': dias,
            'conferencias': {
                'total': Conferencias.objects.count(),
                'proximas': Conferencias.objects.filter(fecha_conferencia__gte=ahora).count(),
                'recientes': Conferencias.objects.filter(fecha_conferencia__gte=fecha_limite).count(),
                'por_mes': list(
                    Conferencias.objects.filter(fecha_conferencia__gte=fecha_limite)
                    .extra({'mes': "date_trunc('month', fecha_conferencia)"})
                    .values('mes')
                    .annotate(total=Count('idconferencia'))
                    .order_by('mes')
                )
            },
            'integrantes': {
                'total': Integrantes.objects.count(),
                'activos': Integrantes.objects.filter(estado=True).count(),
                'inactivos': Integrantes.objects.filter(estado=False).count(),
                'por_semestre': list(
                    Integrantes.objects.values('semestre')
                    .annotate(total=Count('idintegrantes'))
                    .order_by('semestre')
                )
            },
            'ofertas_empleo': {
                'total': OfertasEmpleo.objects.count(),
                'vigentes': OfertasEmpleo.objects.filter(fecha_expiracion__gte=ahora).count(),
                'expiradas': OfertasEmpleo.objects.filter(fecha_expiracion__lt=ahora).count(),
                'publicadas_periodo': OfertasEmpleo.objects.filter(fecha_publicacion__gte=fecha_limite).count(),
                'empresas_activas': list(
                    OfertasEmpleo.objects.filter(fecha_publicacion__gte=fecha_limite)
                    .values('empresa')
                    .annotate(total=Count('idoferta'))
                    .order_by('-total')[:10]
                )
            },
            'noticias': {
                'total': Noticias.objects.count(),
                'recientes': Noticias.objects.filter(fecha_noticia__gte=fecha_limite).count()
            },
            'cursos': {
                'total': Cursos.objects.count(),
                'recientes': Cursos.objects.filter(fecha_curso__gte=fecha_limite).count()
            },
            'proyectos': {
                'total': Proyectos.objects.count(),
                'recientes': Proyectos.objects.filter(fecha_proyecto__gte=fecha_limite).count()
            },
            'auditoria': {
                'total_logs': AuditLog.objects.count(),
                'logs_periodo': AuditLog.objects.filter(timestamp__gte=fecha_limite).count(),
                'acciones_frecuentes': list(
                    AuditLog.objects.filter(timestamp__gte=fecha_limite)
                    .values('accion')
                    .annotate(total=Count('id'))
                    .order_by('-total')[:10]
                )
            }
        }
        
        return estadisticas
    
    def formatear_texto(self, estadisticas):
        """
        Formatea las estadísticas como texto legible.
        
        Args:
            estadisticas (dict): Diccionario con las estadísticas
            
        Returns:
            str: Texto formateado
        """
        texto = []
        texto.append("=" * 60)
        texto.append("REPORTE DE ESTADÍSTICAS DEL SISTEMA")
        texto.append("=" * 60)
        texto.append(f"Fecha de generación: {estadisticas['fecha_generacion']}")
        texto.append(f"Período de análisis: {estadisticas['periodo_analisis_dias']} días")
        texto.append("")
        
        # Conferencias
        conf = estadisticas['conferencias']
        texto.append("CONFERENCIAS:")
        texto.append(f"  Total: {conf['total']}")
        texto.append(f"  Próximas: {conf['proximas']}")
        texto.append(f"  Recientes: {conf['recientes']}")
        texto.append("")
        
        # Integrantes
        int_stats = estadisticas['integrantes']
        texto.append("INTEGRANTES:")
        texto.append(f"  Total: {int_stats['total']}")
        texto.append(f"  Activos: {int_stats['activos']}")
        texto.append(f"  Inactivos: {int_stats['inactivos']}")
        if int_stats['por_semestre']:
            texto.append("  Por semestre:")
            for item in int_stats['por_semestre']:
                texto.append(f"    {item['semestre']}: {item['total']}")
        texto.append("")
        
        # Ofertas de empleo
        ofertas = estadisticas['ofertas_empleo']
        texto.append("OFERTAS DE EMPLEO:")
        texto.append(f"  Total: {ofertas['total']}")
        texto.append(f"  Vigentes: {ofertas['vigentes']}")
        texto.append(f"  Expiradas: {ofertas['expiradas']}")
        texto.append(f"  Publicadas en período: {ofertas['publicadas_periodo']}")
        if ofertas['empresas_activas']:
            texto.append("  Empresas más activas:")
            for item in ofertas['empresas_activas']:
                texto.append(f"    {item['empresa']}: {item['total']}")
        texto.append("")
        
        # Otras secciones
        for seccion in ['noticias', 'cursos', 'proyectos']:
            datos = estadisticas[seccion]
            texto.append(f"{seccion.upper()}:")
            texto.append(f"  Total: {datos['total']}")
            texto.append(f"  Recientes: {datos['recientes']}")
            texto.append("")
        
        # Auditoría
        audit = estadisticas['auditoria']
        texto.append("AUDITORÍA:")
        texto.append(f"  Total logs: {audit['total_logs']}")
        texto.append(f"  Logs en período: {audit['logs_periodo']}")
        if audit['acciones_frecuentes']:
            texto.append("  Acciones más frecuentes:")
            for item in audit['acciones_frecuentes']:
                texto.append(f"    {item['accion']}: {item['total']}")
        
        return "\n".join(texto)
