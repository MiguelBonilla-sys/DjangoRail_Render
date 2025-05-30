from rest_framework import serializers
from blog.Models.AuditLogModel import AuditLog

# Convierte el modelo AuditLog(Python) en un JSON para ser
# Consumido por la API 
class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'