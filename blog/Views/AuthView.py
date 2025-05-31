from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.sessions.models import Session
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..Serializers.AuthSerializer import (
    LoginSerializer, 
    UserSerializer, 
    LoginResponseSerializer,
    LogoutResponseSerializer
)


@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={
        200: LoginResponseSerializer,
        400: 'Bad Request - Credenciales inválidas',
        500: 'Error interno del servidor'
    },
    operation_description="Endpoint para autenticar usuarios. Requiere username y password.",
    operation_summary="Login de usuario"
)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_view(request):
    """
    Endpoint para autenticar usuarios
    
    POST /auth/login/
    Body: {
        "username": "string",
        "password": "string"
    }
    
    Response: {
        "success": true,
        "message": "Login exitoso",
        "user": {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "full_name": "Admin User",
            "is_staff": true,
            "is_superuser": true,
            "date_joined": "2024-01-01T00:00:00Z"
        },
        "session_id": "abc123..."
    }
    """
    try:
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Autenticar al usuario (crear sesión)
            login(request, user)
            
            # Obtener session key
            session_key = request.session.session_key
            
            # Serializar datos del usuario
            user_serializer = UserSerializer(user)
            
            response_data = {
                'success': True,
                'message': 'Login exitoso',
                'user': user_serializer.data,
                'session_id': session_key
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Credenciales inválidas',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='post',
    responses={
        200: LogoutResponseSerializer,
        401: 'No autenticado'
    },
    operation_description="Endpoint para cerrar sesión del usuario actual",
    operation_summary="Logout de usuario"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Endpoint para cerrar sesión
    
    POST /auth/logout/
    Headers: Authorization: Session <session_id>
    
    Response: {
        "success": true,
        "message": "Logout exitoso"
    }
    """
    try:
        # Cerrar sesión del usuario
        logout(request)
        
        return Response({
            'success': True,
            'message': 'Logout exitoso'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error al cerrar sesión: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    responses={
        200: UserSerializer,
        401: 'No autenticado'
    },
    operation_description="Obtiene la información del usuario autenticado actualmente",
    operation_summary="Perfil del usuario actual"
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Endpoint para obtener información del usuario actual
    
    GET /auth/profile/
    Headers: Authorization: Session <session_id>
    
    Response: {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "full_name": "Admin User",
        "is_staff": true,
        "is_superuser": true,
        "date_joined": "2024-01-01T00:00:00Z"
    }
    """
    try:
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error al obtener perfil: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="Estado de autenticación",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'authenticated': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                    'session_id': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    operation_description="Verifica si el usuario actual está autenticado",
    operation_summary="Verificar estado de autenticación"
)
@api_view(['GET'])
@permission_classes([AllowAny])
def auth_status_view(request):
    """
    Endpoint para verificar el estado de autenticación
    
    GET /auth/status/
    
    Response: {
        "authenticated": true,
        "user": {UserData} | null,
        "session_id": "abc123..." | null
    }
    """
    try:
        if request.user.is_authenticated:
            user_serializer = UserSerializer(request.user)
            return Response({
                'authenticated': True,
                'user': user_serializer.data,
                'session_id': request.session.session_key
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'authenticated': False,
                'user': None,
                'session_id': None
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({
            'authenticated': False,
            'user': None,
            'session_id': None,
            'error': str(e)
        }, status=status.HTTP_200_OK)
