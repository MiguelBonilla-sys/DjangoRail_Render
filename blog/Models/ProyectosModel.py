"""
Modelo para gestionar proyectos y sus colaboradores.

Este modelo administra información de proyectos con soporte para
múltiples integrantes y detalles completos del desarrollo.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from blog.Models.IntegrantesModel import Integrantes
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class Proyectos(models.Model):
    """
    Modelo que representa un proyecto de desarrollo o investigación.
    
    Attributes:
        idproyectos (int): Identificador único del proyecto
        nombre_proyecto (str): Nombre descriptivo del proyecto
        fecha_proyecto (datetime): Fecha de inicio o creación
        link_proyecto (str): URL del repositorio o demo del proyecto
        description_proyecto (str): Descripción detallada y objetivos
        creador (User): Usuario que creó el registro del proyecto
        integrantes (ManyToMany): Integrantes que participan en el proyecto
    """
    
    idproyectos = models.AutoField(
        primary_key=True,
        help_text="Identificador único del proyecto"
    )
    nombre_proyecto = models.CharField(
        max_length=850,
        help_text="Nombre descriptivo del proyecto"
    )
    fecha_proyecto = models.DateTimeField(
        help_text="Fecha de inicio o creación del proyecto"
    )
    link_proyecto = models.URLField(
        max_length=1200,
        validators=[URLValidator()],
        help_text="URL del repositorio, demo o documentación"
    )
    description_proyecto = models.TextField(
        max_length=1200,
        help_text="Descripción detallada, objetivos y tecnologías utilizadas"
    )
    creador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="Usuario que registró el proyecto"
    )
    integrantes = models.ManyToManyField(
        Integrantes, 
        through='ProyectosIntegrantesProyecto',
        help_text="Integrantes que participan en el proyecto"
    )

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-fecha_proyecto', 'nombre_proyecto']
        indexes = [
            models.Index(fields=['fecha_proyecto']),
            models.Index(fields=['creador']),
        ]
        
    def __str__(self):
        """Representación string del objeto."""
        return self.nombre_proyecto
    
    def save(self, *args, **kwargs):
        """Guarda el proyecto con logging y validaciones."""
        if not self.fecha_proyecto:
            self.fecha_proyecto = timezone.now()
            
        logger.info(f"Guardando proyecto: {self.nombre_proyecto}")
        super().save(*args, **kwargs)
    
    @property
    def total_integrantes(self):
        """Retorna el número total de integrantes en el proyecto."""
        return self.integrantes.count()
    
    @property
    def is_recent(self):
        """Verifica si el proyecto fue creado en los últimos 30 días."""
        return (timezone.now() - self.fecha_proyecto).days <= 30
    
    def get_integrantes_activos(self):
        """Retorna solo los integrantes activos del proyecto."""
        return self.integrantes.filter(estado=True)
