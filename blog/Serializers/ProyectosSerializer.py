from rest_framework import serializers
from blog.Models.ProyectosModel import Proyectos

# Convierte el modelo Proyectos(Python) en un JSON para ser
# Consumido por la API
class ProyectosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyectos
        fields = '__all__'