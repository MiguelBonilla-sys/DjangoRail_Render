"""
Modelo para gestionar los integrantes del equipo o organización.

Este modelo almacena información personal y académica de los miembros,
incluyendo semestre, contacto y reseña profesional.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, EmailValidator
from cloudinary.models import CloudinaryField
import logging

logger = logging.getLogger(__name__)


class Integrantes(models.Model):
    """
    Modelo que representa un integrante del equipo.
    
    Attributes:
        idintegrantes (int): Identificador único del integrante
        nombre_integrante (str): Nombre completo del integrante
        semestre (str): Semestre académico actual
        correo (str): Dirección de correo electrónico
        link_git (str): Enlace al perfil de GitHub
        imagen (CloudinaryField): Foto de perfil
        creador (User): Usuario que creó el registro
        estado (bool): Estado activo/inactivo del integrante
        reseña (str): Descripción profesional o académica
    """
    
    idintegrantes = models.AutoField(
        primary_key=True,
        help_text="Identificador único del integrante"
    )
    nombre_integrante = models.CharField(
        max_length=220,
        help_text="Nombre completo del integrante"
    )
    semestre = models.CharField(
        max_length=50,
        help_text="Semestre académico actual"
    )
    correo = models.EmailField(
        max_length=550,
        validators=[EmailValidator()],
        help_text="Dirección de correo electrónico válida"
    )
    link_git = models.URLField(
        max_length=650,
        validators=[
            RegexValidator(
                regex=r'^https://github\.com/[\w\-\.]+/?$',
                message='Debe ser una URL válida de GitHub'
            )
        ],
        help_text="Enlace al perfil de GitHub"
    )
    imagen = CloudinaryField(
        'image', 
        folder='integrantes/',
        help_text="Foto de perfil del integrante"
    )
    creador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="Usuario que creó este registro"
    )
    estado = models.BooleanField(
        default=True,
        help_text="Estado activo (True) o inactivo (False) del integrante"
    )
    reseña = models.TextField(
        help_text="Descripción profesional, habilidades y experiencia"
    )
    
    class Meta:
        verbose_name = "Integrante"
        verbose_name_plural = "Integrantes"
        ordering = ['nombre_integrante']
        
    def __str__(self):
        """Representación string del objeto."""
        return f"{self.nombre_integrante} ({self.semestre})"
    
    def save(self, *args, **kwargs):
        """Guarda el objeto con logging."""
        logger.info(f"Guardando integrante: {self.nombre_integrante}")
        super().save(*args, **kwargs)
