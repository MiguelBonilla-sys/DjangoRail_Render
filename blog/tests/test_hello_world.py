import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
'''
@pytest.mark.django_db
def test_hello_world(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert b'Hello, World!' in response.content
    '''
'''
@pytest.mark.django_db
def test_conferencias_list(client):
    url = reverse('conferencias-list')  # Ajustar al nombre de la ruta real
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_conferencias_detail(client):
    # Asumiendo que ya existe una conferencia con pk=1
    url = reverse('conferencias-detail', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 200
'''



'''
@pytest.mark.django_db
def test_conferencias_create(client):
    print("Iniciando prueba de creación de conferencias")
    
    # Crear un usuario para el campo 'creador'
    user = User.objects.create_user(username='testuser', password='12345')
    
    url = reverse('conferencias-list')
    print(f"URL generada: {url}")
    
    # Crear un archivo simulado para 'imagen_conferencia'
    image_content = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff'
        b'\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    image = SimpleUploadedFile("test_image.gif", image_content, content_type="image/gif")
    
    data = {
        'nombre_conferencia': 'Nueva conf',
        'ponente_conferencia': 'Ponente',
        'fecha_conferencia': '2023-10-10T10:00:00Z',
        'descripcion_conferencia': 'Descripción de la conferencia',
        'imagen_conferencia': image,
        'link_conferencia': 'http://link.com',
        'creador': user.id  # ID del usuario creador
    }
    
    response = client.post(url, data=data, format='multipart')
    print(f"Respuesta del servidor: {response.status_code}")
    print(f"Contenido de la respuesta: {response.content}")
    assert response.status_code in (200, 201)
    print("Éxito: Los datos se guardaron correctamente.")
'''
'''
@pytest.mark.django_db
def test_cursos_list(client):
    url = reverse('cursos-list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_cursos_detail(client):
    # Asumiendo que ya existe un curso con pk=1
    url = reverse('cursos-detail', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_cursos_create(client):
    url = reverse('cursos-list')
    data = {
        'nombre_curso': 'Nuevo curso',
        'descripcion_curso': 'Descripción del curso',
        # ...más campos necesarios...
    }
    response = client.post(url, data=data)
    assert response.status_code in (200, 201)
    '''