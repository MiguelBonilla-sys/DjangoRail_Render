"""
Modelo para auditoría y registro de cambios en el sistema.

Este modelo registra todas las operaciones realizadas en la base de datos
para mantener un historial completo de modificaciones.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class AuditLog(models.Model):
    """
    Modelo que registra cambios y operaciones en el sistema.
    
    Attributes:
        timestamp (datetime): Marca de tiempo de la operación
        user (User): Usuario que realizó la operación
        table_name (str): Nombre de la tabla afectada
        change_type (str): Tipo de cambio (CREATE, UPDATE, DELETE)
        affected_record_id (int): ID del registro afectado
        modified_data (JSON): Datos modificados en formato JSON
    """
    
    CHANGE_TYPES = [
        ('CREATE', 'Creación'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
    ]
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de la operación"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING,
        help_text="Usuario que realizó la operación"
    )
    table_name = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z_][a-zA-Z0-9_]*$',
                message='Nombre de tabla debe ser alfanumérico'
            )
        ],
        help_text="Nombre de la tabla de base de datos afectada"
    )
    change_type = models.CharField(
        max_length=6,
        choices=CHANGE_TYPES,
        help_text="Tipo de operación realizada"
    )
    affected_record_id = models.IntegerField(
        blank=True, 
        null=True,
        help_text="ID del registro afectado por la operación"
    )
    modified_data = models.JSONField(
        blank=True, 
        null=True,
        help_text="Datos modificados en formato JSON"
    )

    class Meta:
        verbose_name = "Log de Auditoría"
        verbose_name_plural = "Logs de Auditoría"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['user']),
            models.Index(fields=['table_name']),
        ]

    def __str__(self):
        """Representación string del objeto."""
        return f"{self.user.username} - {self.change_type} en {self.table_name}"
    
    def save(self, *args, **kwargs):
        """Guarda el log con validaciones adicionales."""
        logger.info(f"Registrando operación de auditoría: {self.change_type} en {self.table_name}")
        super().save(*args, **kwargs)