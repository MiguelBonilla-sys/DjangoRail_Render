"""
Modelo para gestionar cursos y programas académicos.

Este modelo permite administrar información sobre cursos, incluyendo
fechas, enlaces y descripciones de los programas educativos.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class Cursos(models.Model):
    """
    Modelo que representa un curso o programa académico.
    
    Attributes:
        idcursos (int): Identificador único del curso
        nombre_curso (str): Nombre descriptivo del curso
        fechainicial_curso (datetime): Fecha de inicio del curso
        fechafinal_curso (datetime): Fecha de finalización del curso
        link_curso (str): URL para acceder al curso o más información
        descripcion_curso (str): Descripción detallada del contenido
        creador (User): Usuario que creó el registro del curso
    """
    
    idcursos = models.AutoField(
        primary_key=True,
        help_text="Identificador único del curso"
    )
    nombre_curso = models.CharField(
        max_length=120,
        help_text="Nombre descriptivo del curso o programa"
    )
    fechainicial_curso = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Fecha y hora de inicio del curso"
    )
    fechafinal_curso = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Fecha y hora de finalización del curso"
    )
    link_curso = models.URLField(
        max_length=1200,
        validators=[URLValidator()],
        help_text="URL para acceder al curso o plataforma educativa"
    )
    descripcion_curso = models.TextField(
        max_length=1200,
        help_text="Descripción detallada del contenido, objetivos y metodología"
    )
    creador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="Usuario que registró el curso"
    )

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-fechainicial_curso', 'nombre_curso']
        
    def __str__(self):
        """Representación string del objeto."""
        return self.nombre_curso
    
    def save(self, *args, **kwargs):
        """Guarda el curso con validaciones y logging."""
        if self.fechainicial_curso and self.fechafinal_curso:
            if self.fechainicial_curso >= self.fechafinal_curso:
                raise ValueError("La fecha inicial debe ser anterior a la fecha final")
        
        logger.info(f"Guardando curso: {self.nombre_curso}")
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        """Verifica si el curso está actualmente en progreso."""
        now = timezone.now()
        if self.fechainicial_curso and self.fechafinal_curso:
            return self.fechainicial_curso <= now <= self.fechafinal_curso
        return False
    
    @property
    def duration_days(self):
        """Calcula la duración del curso en días."""
        if self.fechainicial_curso and self.fechafinal_curso:
            delta = self.fechafinal_curso - self.fechainicial_curso
            return delta.days
        return None
