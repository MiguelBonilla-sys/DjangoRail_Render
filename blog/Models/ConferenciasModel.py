"""
Modelo para gestionar conferencias y eventos académicos.

Este modelo almacena información sobre conferencias, incluyendo detalles
del ponente, fecha, descripción e imagen promocional.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from cloudinary.models import CloudinaryField
import logging

logger = logging.getLogger(__name__)


class Conferencias(models.Model):
    """
    Modelo que representa una conferencia o evento académico.
    
    Attributes:
        idconferencia (int): Identificador único de la conferencia
        nombre_conferencia (str): Nombre descriptivo de la conferencia
        ponente_conferencia (str): Nombre del ponente principal
        fecha_conferencia (datetime): Fecha y hora del evento
        descripcion_conferencia (str): Descripción detallada del contenido
        imagen_conferencia (CloudinaryField): Imagen promocional del evento
        link_conferencia (str): URL para acceso o más información
        creador (User): Usuario que creó el registro
    """
    
    idconferencia = models.AutoField(
        primary_key=True,
        help_text="Identificador único de la conferencia"
    )
    nombre_conferencia = models.CharField(
        max_length=620,
        help_text="Nombre descriptivo de la conferencia"
    )
    ponente_conferencia = models.CharField(
        max_length=250,
        help_text="Nombre del ponente principal"
    )
    fecha_conferencia = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Fecha y hora programada para la conferencia"
    )
    descripcion_conferencia = models.TextField(
        max_length=1200,
        help_text="Descripción detallada del contenido y objetivos"
    )
    imagen_conferencia = CloudinaryField(
        'image', 
        folder='conferencias/',
        help_text="Imagen promocional de la conferencia"
    )
    link_conferencia = models.URLField(
        max_length=1200,
        validators=[URLValidator()],
        help_text="URL para acceso virtual o más información"
    )
    creador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="Usuario que creó este registro"
    )
    
    class Meta:
        verbose_name = "Conferencia"
        verbose_name_plural = "Conferencias"
        ordering = ['-fecha_conferencia']
        
    def __str__(self):
        """Representación string del objeto."""
        return f"{self.nombre_conferencia} - {self.ponente_conferencia}"
    
    def save(self, *args, **kwargs):
        """Guarda el objeto con logging."""
        logger.info(f"Guardando conferencia: {self.nombre_conferencia}")
        super().save(*args, **kwargs)