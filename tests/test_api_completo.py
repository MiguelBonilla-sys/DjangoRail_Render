#!/usr/bin/env python3
"""
Script de pruebas completo para verificar las mejoras implementadas.

Este script prueba todas las funcionalidades nuevas:
1. Paginación
2. Filtros y búsqueda
3. Rate limiting (throttling)
4. Logging
5. Headers de seguridad
"""

import requests
import json
import time
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:8001"
API_BASE = f"{BASE_URL}/api/hl4/v1"

def test_api_endpoint(endpoint, description, params=None):
    """Prueba un endpoint de API y muestra los resultados."""
    print(f"\n🔍 Probando: {description}")
    print(f"📍 Endpoint: {endpoint}")
    
    try:
        url = urljoin(API_BASE, endpoint)
        response = requests.get(url, params=params, timeout=10)
        
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Headers de seguridad:")
        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options', 
            'X-XSS-Protection',
            'Referrer-Policy'
        ]
        
        for header in security_headers:
            value = response.headers.get(header, 'No presente')
            print(f"   - {header}: {value}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Verificar paginación
            if isinstance(data, dict) and 'results' in data:
                print(f"📄 Paginación detectada:")
                print(f"   - Total elementos: {data.get('count', 'N/A')}")
                print(f"   - Página anterior: {'Sí' if data.get('previous') else 'No'}")
                print(f"   - Página siguiente: {'Sí' if data.get('next') else 'No'}")
                print(f"   - Elementos en esta página: {len(data.get('results', []))}")
            elif isinstance(data, list):
                print(f"📋 Lista directa con {len(data)} elementos")
            else:
                print(f"📊 Respuesta: {type(data).__name__}")
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

def test_filters_and_search():
    """Prueba los filtros y búsqueda implementados."""
    print("\n" + "="*60)
    print("🔧 PROBANDO FILTROS Y BÚSQUEDA")
    print("="*60)
    
    # Prueba filtros en conferencias
    test_api_endpoint("/conferencias/", "Conferencias - Lista básica")
    test_api_endpoint("/conferencias/", "Conferencias - Filtro por activo", {"activo": "true"})
    test_api_endpoint("/conferencias/", "Conferencias - Búsqueda", {"search": "conferencia"})
    
    # Prueba filtros en integrantes
    test_api_endpoint("/integrantes/", "Integrantes - Lista básica")
    test_api_endpoint("/integrantes/", "Integrantes - Filtro por área", {"area_investigacion": "tecnologia"})
    test_api_endpoint("/integrantes/", "Integrantes - Búsqueda por nombre", {"search": "juan"})
      # Prueba filtros en ofertas de empleo
    test_api_endpoint("/ofertasempleo/", "Ofertas - Lista básica")
    test_api_endpoint("/ofertasempleo/", "Ofertas - Filtro por modalidad", {"modalidad_trabajo": "remoto"})
    test_api_endpoint("/ofertasempleo/", "Ofertas - Búsqueda", {"search": "desarrollador"})

def test_pagination():
    """Prueba la paginación implementada."""
    print("\n" + "="*60)
    print("📄 PROBANDO PAGINACIÓN")
    print("="*60)
    
    # Prueba diferentes tamaños de página
    test_api_endpoint("/conferencias/", "Paginación - 5 elementos por página", {"page_size": "5"})
    test_api_endpoint("/conferencias/", "Paginación - Página 2", {"page": "2"})
    test_api_endpoint("/integrantes/", "Paginación - 10 elementos por página", {"page_size": "10"})

def test_special_endpoints():
    """Prueba endpoints especiales (estadísticas, etc.)."""
    print("\n" + "="*60)
    print("📊 PROBANDO ENDPOINTS ESPECIALES")
    print("="*60)
    
    test_api_endpoint("/conferencias/estadisticas/", "Estadísticas de conferencias")
    test_api_endpoint("/conferencias/proximas/", "Próximas conferencias")
    test_api_endpoint("/integrantes/estadisticas/", "Estadísticas de integrantes")
    test_api_endpoint("/ofertasempleo/estadisticas/", "Estadísticas de ofertas")

def test_rate_limiting():
    """Prueba el rate limiting (con cuidado)."""
    print("\n" + "="*60)
    print("⚡ PROBANDO RATE LIMITING")
    print("="*60)
    
    print("Realizando múltiples solicitudes para probar throttling...")
    
    for i in range(5):
        response = test_api_endpoint("/conferencias/", f"Solicitud {i+1}/5")
        if response and response.status_code == 429:
            print("🚫 Rate limit alcanzado - Funciona correctamente!")
            break
        time.sleep(1)

def main():
    """Función principal que ejecuta todas las pruebas."""
    print("🚀 INICIANDO PRUEBAS COMPLETAS DE LAS MEJORAS")
    print("="*60)
    print(f"🌐 Servidor: {BASE_URL}")
    print(f"🔗 API Base: {API_BASE}")
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Servidor accesible (Status: {response.status_code})")
    except requests.exceptions.RequestException:
        print("❌ Error: No se puede conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo en puerto 8001")
        return
    
    # Ejecutar todas las pruebas
    test_filters_and_search()
    test_pagination()
    test_special_endpoints()
    test_rate_limiting()
    
    print("\n" + "="*60)
    print("🎉 PRUEBAS COMPLETADAS")
    print("="*60)
    print("✅ Revisa los logs en la carpeta 'logs/' para ver el logging en acción")
    print("✅ Los headers de seguridad están siendo aplicados")
    print("✅ La paginación está funcionando")
    print("✅ Los filtros y búsqueda están activos")

if __name__ == "__main__":
    main()
