from rest_framework import serializers
from blog.Models.OfertasEmpleoModel import OfertasEmpleo
import base64
import binascii
# Convierte el modelo OfertasEmpleo(Python) en un JSON para ser
# Consumido por la API
class OfertasEmpleoSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField()
    class Meta:
        model = OfertasEmpleo
        fields = '__all__'