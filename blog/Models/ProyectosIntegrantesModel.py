"""
Modelo intermedio para la relación Many-to-Many entre Proyectos e Integrantes.

Este modelo gestiona la asociación entre proyectos y sus participantes,
permitiendo un control más granular de las relaciones.
"""

from django.db import models
from blog.Models.IntegrantesModel import Integrantes
from blog.Models.ProyectosModel import Proyectos
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class ProyectosIntegrantesProyecto(models.Model):
    """
    Modelo intermedio para gestionar la participación de integrantes en proyectos.
    
    Esta tabla through permite controlar específicamente qué integrantes
    participan en qué proyectos, con la posibilidad de añadir campos
    adicionales en el futuro como rol, fecha de participación, etc.
    
    Attributes:
        proyectos (Proyectos): Referencia al proyecto
        integrantes (Integrantes): Referencia al integrante participante
    """
    
    proyectos = models.OneToOneField(
        Proyectos, 
        on_delete=models.CASCADE, 
        primary_key=True,
        help_text="Proyecto al que pertenece esta relación"
    )
    integrantes = models.ForeignKey(
        Integrantes, 
        on_delete=models.CASCADE,
        help_text="Integrante que participa en el proyecto"
    )
    
    class Meta:
        verbose_name = "Participación en Proyecto"
        verbose_name_plural = "Participaciones en Proyectos"
        unique_together = ['proyectos', 'integrantes']
        
    def __str__(self):
        """Representación string del objeto."""
        return f"{self.integrantes.nombre_integrante} en {self.proyectos.nombre_proyecto}"
    
    def save(self, *args, **kwargs):
        """Guarda la relación con logging."""
        logger.info(f"Asignando {self.integrantes.nombre_integrante} al proyecto {self.proyectos.nombre_proyecto}")
        super().save(*args, **kwargs)
