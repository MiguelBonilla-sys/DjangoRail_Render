"""
Modelo para gestionar ofertas de empleo y oportunidades laborales.

Este modelo permite publicar y gestionar ofertas de trabajo con 
expiración automática después de un período determinado.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from datetime import timedelta
from django.utils import timezone
from cloudinary.models import CloudinaryField
import logging

logger = logging.getLogger(__name__)


class OfertasEmpleo(models.Model):
    """
    Modelo que representa una oferta de empleo.
    
    Attributes:
        idoferta (int): Identificador único de la oferta
        titulo_empleo (str): Título del puesto de trabajo
        empresa (str): Nombre de la empresa
        fecha_publicacion (datetime): Fecha de publicación
        descripcion_empleo (str): Descripción detallada del puesto
        imagen (CloudinaryField): Logo de la empresa o imagen promocional
        link_oferta (str): URL para aplicar a la oferta
        fecha_expiracion (datetime): Fecha límite para aplicaciones
        creador (User): Usuario que publicó la oferta
    """
    
    idoferta = models.AutoField(
        primary_key=True,
        help_text="Identificador único de la oferta de empleo"
    )
    titulo_empleo = models.CharField(
        max_length=620,
        help_text="Título del puesto de trabajo"
    )
    empresa = models.CharField(
        max_length=230,
        help_text="Nombre de la empresa que ofrece el puesto"
    )
    fecha_publicacion = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Fecha y hora de publicación de la oferta"
    )
    descripcion_empleo = models.TextField(
        max_length=1200,
        help_text="Descripción detallada del puesto, requisitos y beneficios"
    )
    imagen = CloudinaryField(
        'image', 
        folder='ofertas/',
        help_text="Logo de la empresa o imagen promocional"
    )
    link_oferta = models.URLField(
        max_length=1200,
        validators=[URLValidator()],
        help_text="URL para aplicar a la oferta de empleo"
    )
    fecha_expiracion = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Fecha límite para recibir aplicaciones"
    )
    creador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="Usuario que publicó la oferta"
    )

    class Meta:
        verbose_name = "Oferta de Empleo"
        verbose_name_plural = "Ofertas de Empleo"
        ordering = ['-fecha_publicacion']

    def save(self, *args, **kwargs):
        """
        Guarda la oferta estableciendo fechas automáticas.
        
        Si es una nueva oferta, establece la fecha de publicación actual
        y calcula la fecha de expiración (60 días después).
        """
        if not self.pk:  # Si el objeto es nuevo
            self.fecha_publicacion = timezone.now()
            logger.info(f"Nueva oferta creada: {self.titulo_empleo} - {self.empresa}")
            
        if not self.fecha_expiracion:
            self.fecha_expiracion = self.fecha_publicacion + timedelta(days=60)
            
        super(OfertasEmpleo, self).save(*args, **kwargs)

    def __str__(self):
        """Representación string del objeto."""
        return f"{self.titulo_empleo} - {self.empresa}"
    
    @property
    def is_expired(self):
        """Verifica si la oferta ha expirado."""
        return timezone.now() > self.fecha_expiracion
    