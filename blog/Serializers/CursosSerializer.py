from rest_framework import serializers
from blog.Models.CursosModel import Cursos

# Convierte el modelo Cursos(Python) en un JSON para ser
# Consumido por la API 
class CursosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cursos
        fields = '__all__'