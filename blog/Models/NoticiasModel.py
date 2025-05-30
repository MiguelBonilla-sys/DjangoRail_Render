"""
Modelo para gestionar noticias y artículos informativos.

Este modelo permite administrar un sistema de noticias con soporte
para imágenes, fuentes y contenido multimedia.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from cloudinary.models import CloudinaryField
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class Noticias(models.Model):
    """
    Modelo que representa una noticia o artículo informativo.
    
    Attributes:
        idnoticia (int): Identificador único de la noticia
        nombre_noticia (str): Título principal de la noticia
        fecha_noticia (datetime): Fecha de publicación
        link_noticia (str): URL de la noticia original o fuente
        description_noticia (str): Descripción y contenido detallado
        creador (User): Usuario que publicó la noticia
        fuente (str): Nombre de la fuente o medio de comunicación
        imagen_noticia (CloudinaryField): Imagen principal de la noticia
    """
    
    idnoticia = models.AutoField(
        primary_key=True,
        help_text="Identificador único de la noticia"
    )
    nombre_noticia = models.CharField(
        max_length=600,
        help_text="Título principal de la noticia"
    )
    fecha_noticia = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de publicación"
    )
    link_noticia = models.URLField(
        max_length=250,
        validators=[URLValidator()],
        help_text="URL de la noticia original o fuente externa"
    )
    description_noticia = models.TextField(
        max_length=1450,
        help_text="Contenido detallado y descripción de la noticia"
    )
    creador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="Usuario que publicó la noticia"
    )
    fuente = models.CharField(
        max_length=250, 
        blank=True, 
        null=True,
        help_text="Nombre del medio de comunicación o fuente"
    )
    imagen_noticia = CloudinaryField(
        'image', 
        folder='noticias/',
        help_text="Imagen principal o thumbnail de la noticia"
    )

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ['-fecha_noticia']
        indexes = [
            models.Index(fields=['fecha_noticia']),
            models.Index(fields=['creador']),
        ]
        
    def __str__(self):
        """Representación string del objeto."""
        return self.nombre_noticia[:50] + "..." if len(self.nombre_noticia) > 50 else self.nombre_noticia
    
    def save(self, *args, **kwargs):
        """Guarda la noticia con logging y validaciones."""
        logger.info(f"Guardando noticia: {self.nombre_noticia}")
        super().save(*args, **kwargs)
    
    @property
    def is_recent(self):
        """Verifica si la noticia fue publicada en los últimos 7 días."""
        return (timezone.now() - self.fecha_noticia).days <= 7
    
    @property
    def summary(self):
        """Retorna un resumen corto de la descripción."""
        if len(self.description_noticia) > 150:
            return self.description_noticia[:150] + "..."
        return self.description_noticia

