from rest_framework import serializers
from blog.Models.IntegrantesModel import Integrantes
# Convierte el modelo Integrantes(Python) en un JSON para ser
# Consumido por la API
class IntegrantesSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField()
    class Meta:
        model = Integrantes
        fields = '__all__'