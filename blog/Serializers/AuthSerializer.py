from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    """
    Serializer para el endpoint de login
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            if not user:
                raise serializers.ValidationError(
                    'Credenciales inválidas. Verifique su usuario y contraseña.',
                    code='authorization'
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    'Esta cuenta está desactivada.',
                    code='authorization'
                )
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Debe incluir "username" y "password".',
                code='authorization'
            )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para información del usuario
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'is_staff', 'is_superuser', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']

    def get_full_name(self, obj):
        """Retorna el nombre completo del usuario"""
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class LoginResponseSerializer(serializers.Serializer):
    """
    Serializer para la respuesta del login
    """
    success = serializers.BooleanField()
    message = serializers.CharField()
    user = UserSerializer()
    session_id = serializers.CharField()


class LogoutResponseSerializer(serializers.Serializer):
    """
    Serializer para la respuesta del logout
    """
    success = serializers.BooleanField()
    message = serializers.CharField()
