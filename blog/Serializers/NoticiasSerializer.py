from rest_framework import serializers
from blog.Models.NoticiasModel import Noticias

class NoticiasSerializer(serializers.ModelSerializer):
    imagen_noticia = serializers.ImageField()

    class Meta:
        model = Noticias
        fields = '__all__'