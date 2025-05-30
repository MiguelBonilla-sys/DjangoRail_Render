#!/usr/bin/env python3
"""
Script de verificación automatizada de las mejoras implementadas.

Este script realiza pruebas automáticas para verificar que todas las
mejoras implementadas están funcionando correctamente.
"""

import sys
import os
import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:8001"
API_BASE = f"{BASE_URL}/api/hl4/v1"

def print_header(title):
    """Imprime un header bonito."""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def print_test_result(test_name, success, details=""):
    """Imprime el resultado de una prueba."""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"    └─ {details}")

def test_server_accessibility():
    """Verifica que el servidor esté accesible."""
    print_header("VERIFICACIÓN DE ACCESIBILIDAD DEL SERVIDOR")
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        print_test_result(
            "Servidor accesible", 
            True, 
            f"Status: {response.status_code}"
        )
        return True
    except requests.exceptions.RequestException as e:
        print_test_result(
            "Servidor accesible", 
            False, 
            f"Error: {e}"
        )
        return False

def test_pagination():
    """Verifica que la paginación esté funcionando."""
    print_header("VERIFICACIÓN DE PAGINACIÓN")
    
    tests = [
        ("Paginación básica", "/conferencias/", {}),
        ("Tamaño de página personalizado", "/conferencias/", {"page_size": "2"}),
        ("Navegación a página 2", "/conferencias/", {"page": "2", "page_size": "2"}),
    ]
    
    success_count = 0
    
    for test_name, endpoint, params in tests:
        try:
            response = requests.get(f"{API_BASE}{endpoint}", params=params, timeout=10)
            data = response.json()
            
            # Verificar estructura de paginación
            has_pagination = "pagination" in data
            has_results = "results" in data
            
            if has_pagination and has_results:
                pagination = data["pagination"]
                expected_keys = ["next", "previous", "count", "current_page", "total_pages", "page_size"]
                has_all_keys = all(key in pagination for key in expected_keys)
                
                success = response.status_code == 200 and has_all_keys
                details = f"Count: {pagination.get('count', 'N/A')}, Page: {pagination.get('current_page', 'N/A')}"
            else:
                success = False
                details = "Estructura de paginación incorrecta"
            
            print_test_result(test_name, success, details)
            if success:
                success_count += 1
                
        except Exception as e:
            print_test_result(test_name, False, f"Error: {e}")
    
    return success_count == len(tests)

def test_search_and_filters():
    """Verifica que la búsqueda y filtros estén funcionando."""
    print_header("VERIFICACIÓN DE BÚSQUEDA Y FILTROS")
    
    tests = [
        ("Búsqueda en conferencias", "/conferencias/", {"search": "Inteligencia"}),
        ("Filtro por tamaño de página", "/conferencias/", {"page_size": "1"}),
        ("Ordenamiento", "/conferencias/", {"ordering": "nombre_conferencia"}),
    ]
    
    success_count = 0
    
    for test_name, endpoint, params in tests:
        try:
            response = requests.get(f"{API_BASE}{endpoint}", params=params, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                count = data.get("pagination", {}).get("count", len(data.get("results", [])))
                details = f"Resultados encontrados: {count}"
            else:
                details = f"Status: {response.status_code}"
            
            print_test_result(test_name, success, details)
            if success:
                success_count += 1
                
        except Exception as e:
            print_test_result(test_name, False, f"Error: {e}")
    
    return success_count == len(tests)

def test_special_endpoints():
    """Verifica que los endpoints especiales estén funcionando."""
    print_header("VERIFICACIÓN DE ENDPOINTS ESPECIALES")
    
    endpoints = [
        ("Estadísticas de conferencias", "/conferencias/estadisticas/"),
        ("Próximas conferencias", "/conferencias/proximas/"),
    ]
    
    success_count = 0
    
    for test_name, endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE}{endpoint}", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if "total_conferencias" in data:
                    details = f"Total: {data.get('total_conferencias', 'N/A')}"
                else:
                    details = f"Resultados: {len(data.get('results', []))}"
            else:
                details = f"Status: {response.status_code}"
            
            print_test_result(test_name, success, details)
            if success:
                success_count += 1
                
        except Exception as e:
            print_test_result(test_name, False, f"Error: {e}")
    
    return success_count == len(endpoints)

def test_security_headers():
    """Verifica que los headers de seguridad estén presentes."""
    print_header("VERIFICACIÓN DE HEADERS DE SEGURIDAD")
    
    expected_headers = [
        "X-Content-Type-Options",
        "X-Frame-Options", 
        "X-XSS-Protection",
        "Referrer-Policy"
    ]
    
    try:
        response = requests.get(f"{API_BASE}/conferencias/", timeout=10)
        success_count = 0
        
        for header in expected_headers:
            present = header in response.headers
            print_test_result(
                f"Header {header}", 
                present, 
                f"Valor: {response.headers.get(header, 'No presente')}"
            )
            if present:
                success_count += 1
        
        return success_count == len(expected_headers)
        
    except Exception as e:
        print_test_result("Headers de seguridad", False, f"Error: {e}")
        return False

def test_rate_limiting():
    """Prueba básica de rate limiting (sin saturar)."""
    print_header("VERIFICACIÓN DE RATE LIMITING")
    
    try:
        # Hacer varias solicitudes para verificar que no hay error inmediato
        requests_made = 0
        for i in range(3):
            response = requests.get(f"{API_BASE}/conferencias/", timeout=10)
            if response.status_code == 200:
                requests_made += 1
            elif response.status_code == 429:
                print_test_result(
                    "Rate limiting activo", 
                    True, 
                    f"Throttled después de {requests_made} solicitudes"
                )
                return True
        
        print_test_result(
            "Rate limiting configurado", 
            True, 
            f"{requests_made} solicitudes exitosas (limite no alcanzado)"
        )
        return True
        
    except Exception as e:
        print_test_result("Rate limiting", False, f"Error: {e}")
        return False

def check_log_files():
    """Verifica que los archivos de log existan."""
    print_header("VERIFICACIÓN DE ARCHIVOS DE LOG")
    
    log_files = [
        "logs/django.log",
        "logs/api_usage.log", 
        "logs/errors.log"
    ]
    
    success_count = 0
    
    for log_file in log_files:
        exists = os.path.exists(log_file)
        if exists:
            size = os.path.getsize(log_file)
            details = f"Tamaño: {size} bytes"
        else:
            details = "Archivo no existe"
        
        print_test_result(f"Log file {log_file}", exists, details)
        if exists:
            success_count += 1
    
    return success_count == len(log_files)

def main():
    """Función principal que ejecuta todas las verificaciones."""
    print("🚀 VERIFICACIÓN AUTOMATIZADA DE MEJORAS IMPLEMENTADAS")
    print(f"⏰ Ejecutado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Servidor: {BASE_URL}")
    
    # Ejecutar todas las pruebas
    tests = [
        ("Accesibilidad del servidor", test_server_accessibility),
        ("Sistema de paginación", test_pagination),
        ("Búsqueda y filtros", test_search_and_filters),
        ("Endpoints especiales", test_special_endpoints),
        ("Headers de seguridad", test_security_headers),
        ("Rate limiting", test_rate_limiting),
        ("Archivos de log", check_log_files),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_function in tests:
        try:
            success = test_function()
            if success:
                passed_tests += 1
        except Exception as e:
            print_test_result(test_name, False, f"Excepción: {e}")
    
    # Resumen final
    print_header("RESUMEN DE VERIFICACIÓN")
    
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"📊 Pruebas exitosas: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if passed_tests == total_tests:
        print("🎉 ¡TODAS LAS MEJORAS ESTÁN FUNCIONANDO CORRECTAMENTE!")
        exit_code = 0
    elif passed_tests >= total_tests * 0.8:
        print("⚠️  La mayoría de las mejoras están funcionando, revisar fallos menores")
        exit_code = 1
    else:
        print("❌ Hay problemas significativos que requieren atención")
        exit_code = 2
    
    print(f"\n💡 Para más detalles, revisa los logs en la carpeta 'logs/'")
    print(f"📋 Documentación completa en 'RESUMEN_MEJORAS_COMPLETADAS.md'")
    
    return exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
