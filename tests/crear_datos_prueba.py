#!/usr/bin/env python3
"""
Script para crear datos de prueba en la base de datos.
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from blog.Models.ConferenciasModel import Conferencias
from blog.Models.IntegrantesModel import Integrantes
from blog.Models.OfertasEmpleoModel import OfertasEmpleo
from blog.Models.NoticiasModel import Noticias
from blog.Models.CursosModel import Cursos
from blog.Models.ProyectosModel import Proyectos

def crear_conferencias():
    """Crear conferencias de prueba."""
    conferencias_data = [
        {
            'titulo': 'Conferencia de Inteligencia Artificial 2025',
            'descripcion': 'Una conferencia sobre los últimos avances en IA y machine learning.',
            'fecha_inicio': datetime.now() + timedelta(days=30),
            'fecha_fin': datetime.now() + timedelta(days=32),
            'ubicacion': 'Centro de Convenciones Ciudad',
            'organizador': 'Tech Institute',
            'contacto_email': 'contact@techinstitute.com',
            'url_sitio_web': 'https://ai-conference-2025.com',
            'imagen_conferencia': 'https://example.com/ai-conference.jpg',
            'activo': True,
        },
        {
            'titulo': 'Simposio de Desarrollo Web Moderno',
            'descripcion': 'Explorando las últimas tecnologías en desarrollo web frontend y backend.',
            'fecha_inicio': datetime.now() + timedelta(days=45),
            'fecha_fin': datetime.now() + timedelta(days=47),
            'ubicacion': 'Universidad Tecnológica',
            'organizador': 'WebDev Community',
            'contacto_email': 'info@webdev.com',
            'url_sitio_web': 'https://webdev-symposium.com',
            'imagen_conferencia': 'https://example.com/webdev-symposium.jpg',
            'activo': True,
        },
        {
            'titulo': 'Conferencia de Ciberseguridad 2025',
            'descripcion': 'Últimas tendencias y técnicas en ciberseguridad empresarial.',
            'fecha_inicio': datetime.now() + timedelta(days=60),
            'fecha_fin': datetime.now() + timedelta(days=61),
            'ubicacion': 'Hotel Convention Center',
            'organizador': 'CyberSec Alliance',
            'contacto_email': 'security@cybersec.org',
            'url_sitio_web': 'https://cybersec-conf.org',
            'imagen_conferencia': 'https://example.com/cybersec.jpg',
            'activo': True,
        },
    ]
    
    for data in conferencias_data:
        conferencia, created = Conferencias.objects.get_or_create(
            titulo=data['titulo'],
            defaults=data
        )
        if created:
            print(f"✅ Conferencia creada: {conferencia.titulo}")
        else:
            print(f"⚠️  Conferencia ya existe: {conferencia.titulo}")

def crear_integrantes():
    """Crear integrantes de prueba."""
    integrantes_data = [
        {
            'nombre': 'Dr. Juan Carlos Pérez',
            'apellido': 'Pérez',
            'email': 'juan.perez@university.edu',
            'telefono': '+1234567890',
            'area_investigacion': 'Inteligencia Artificial',
            'titulo_academico': 'Doctor en Ciencias de la Computación',
            'institucion': 'Universidad Tecnológica Nacional',
            'biografia': 'Experto en machine learning con 15 años de experiencia.',
            'url_linkedin': 'https://linkedin.com/in/juanperez',
            'url_orcid': 'https://orcid.org/0000-0000-0000-0001',
            'imagen_perfil': 'https://example.com/juan-perez.jpg',
            'activo': True,
        },
        {
            'nombre': 'Dra. María González',
            'apellido': 'González',
            'email': 'maria.gonzalez@tech.edu',
            'telefono': '+1234567891',
            'area_investigacion': 'Desarrollo Web',
            'titulo_academico': 'Doctora en Ingeniería de Software',
            'institucion': 'Instituto Tecnológico Superior',
            'biografia': 'Especialista en arquitecturas web modernas y microservicios.',
            'url_linkedin': 'https://linkedin.com/in/mariagonzalez',
            'url_orcid': 'https://orcid.org/0000-0000-0000-0002',
            'imagen_perfil': 'https://example.com/maria-gonzalez.jpg',
            'activo': True,
        },
        {
            'nombre': 'Dr. Carlos Rodríguez',
            'apellido': 'Rodríguez',
            'email': 'carlos.rodriguez@cybersec.org',
            'telefono': '+1234567892',
            'area_investigacion': 'Ciberseguridad',
            'titulo_academico': 'Doctor en Seguridad Informática',
            'institucion': 'Centro de Investigación en Ciberseguridad',
            'biografia': 'Investigador en seguridad de redes y criptografía.',
            'url_linkedin': 'https://linkedin.com/in/carlosrodriguez',
            'url_orcid': 'https://orcid.org/0000-0000-0000-0003',
            'imagen_perfil': 'https://example.com/carlos-rodriguez.jpg',
            'activo': True,
        },
    ]
    
    for data in integrantes_data:
        integrante, created = Integrantes.objects.get_or_create(
            email=data['email'],
            defaults=data
        )
        if created:
            print(f"✅ Integrante creado: {integrante.nombre} {integrante.apellido}")
        else:
            print(f"⚠️  Integrante ya existe: {integrante.nombre} {integrante.apellido}")

def crear_ofertas_empleo():
    """Crear ofertas de empleo de prueba."""
    ofertas_data = [
        {
            'titulo': 'Desarrollador Full Stack Senior',
            'descripcion': 'Buscamos desarrollador con experiencia en React, Node.js y Python.',
            'empresa': 'TechCorp Solutions',
            'ubicacion': 'Madrid, España',
            'modalidad_trabajo': 'remoto',
            'tipo_contrato': 'tiempo_completo',
            'salario_minimo': 45000,
            'salario_maximo': 65000,
            'moneda': 'EUR',
            'requisitos': 'Mínimo 5 años de experiencia, conocimientos en AWS, Docker.',
            'beneficios': 'Seguro médico, trabajo remoto, formación continua.',
            'contacto_email': 'hr@techcorp.com',
            'url_aplicacion': 'https://techcorp.com/jobs/fullstack-senior',
            'fecha_publicacion': datetime.now() - timedelta(days=5),
            'fecha_cierre': datetime.now() + timedelta(days=25),
            'activo': True,
        },
        {
            'titulo': 'Especialista en Inteligencia Artificial',
            'descripcion': 'Posición para trabajar en proyectos de machine learning y deep learning.',
            'empresa': 'AI Innovations Inc.',
            'ubicacion': 'Barcelona, España',
            'modalidad_trabajo': 'hibrido',
            'tipo_contrato': 'tiempo_completo',
            'salario_minimo': 55000,
            'salario_maximo': 80000,
            'moneda': 'EUR',
            'requisitos': 'PhD en Computer Science o similar, experiencia con TensorFlow, PyTorch.',
            'beneficios': 'Excelente ambiente de trabajo, proyectos innovadores, stock options.',
            'contacto_email': 'careers@aiinnovations.com',
            'url_aplicacion': 'https://aiinnovations.com/careers/ai-specialist',
            'fecha_publicacion': datetime.now() - timedelta(days=3),
            'fecha_cierre': datetime.now() + timedelta(days=27),
            'activo': True,
        },
        {
            'titulo': 'Consultor de Ciberseguridad',
            'descripcion': 'Consultor para auditorías de seguridad y implementación de soluciones.',
            'empresa': 'SecureIT Consulting',
            'ubicacion': 'Valencia, España',
            'modalidad_trabajo': 'presencial',
            'tipo_contrato': 'tiempo_completo',
            'salario_minimo': 40000,
            'salario_maximo': 60000,
            'moneda': 'EUR',
            'requisitos': 'Certificaciones CISSP o CEH, experiencia en pentesting.',
            'beneficios': 'Formación certificada, coche de empresa, seguro médico premium.',
            'contacto_email': 'jobs@secureit.com',
            'url_aplicacion': 'https://secureit.com/jobs/cybersecurity-consultant',
            'fecha_publicacion': datetime.now() - timedelta(days=7),
            'fecha_cierre': datetime.now() + timedelta(days=23),
            'activo': True,
        },
    ]
    
    for data in ofertas_data:
        oferta, created = OfertasEmpleo.objects.get_or_create(
            titulo=data['titulo'],
            empresa=data['empresa'],
            defaults=data
        )
        if created:
            print(f"✅ Oferta creada: {oferta.titulo} en {oferta.empresa}")
        else:
            print(f"⚠️  Oferta ya existe: {oferta.titulo} en {oferta.empresa}")

def main():
    """Función principal para crear todos los datos de prueba."""
    print("🚀 Creando datos de prueba...")
    print("="*50)
    
    crear_conferencias()
    print()
    crear_integrantes()
    print()
    crear_ofertas_empleo()
    
    print("="*50)
    print("✅ Datos de prueba creados exitosamente!")
    print("\nPuedes ahora probar las APIs con datos reales:")
    print("- Conferencias:", Conferencias.objects.count())
    print("- Integrantes:", Integrantes.objects.count())
    print("- Ofertas de empleo:", OfertasEmpleo.objects.count())

if __name__ == "__main__":
    main()
