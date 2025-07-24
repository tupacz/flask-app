#!/usr/bin/env python3
"""
Script para verificar que todas las rutas de navegación funcionen correctamente.
"""

import requests
import sys
from datetime import datetime

def test_routes():
    """Prueba todas las rutas de la aplicación"""
    
    base_url = "http://localhost:5000"
    
    routes = [
        {
            "name": "Pantalla Principal",
            "url": f"{base_url}/",
            "method": "GET",
            "expected_status": 200
        },
        {
            "name": "Pantalla de Ganador",
            "url": f"{base_url}/winner",
            "method": "GET", 
            "expected_status": 200
        },
        {
            "name": "Gestión de Libros",
            "url": f"{base_url}/books-manager",
            "method": "GET",
            "expected_status": 200
        },
        {
            "name": "Ver Votos",
            "url": f"{base_url}/votes",
            "method": "GET",
            "expected_status": 200
        },
        {
            "name": "Mini App Telegram",
            "url": f"{base_url}/telegram",
            "method": "GET",
            "expected_status": 200
        },
        {
            "name": "Telegram - Ganador",
            "url": f"{base_url}/telegram-winner",
            "method": "GET",
            "expected_status": 200
        },
        {
            "name": "Telegram - Gestión Libros",
            "url": f"{base_url}/telegram-books",
            "method": "GET",
            "expected_status": 200
        },
        {
            "name": "API Votos JSON",
            "url": f"{base_url}/votes-json",
            "method": "GET",
            "expected_status": 200
        },
        {
            "name": "API Estadísticas",
            "url": f"{base_url}/vote-stats",
            "method": "GET",
            "expected_status": 200
        }
    ]
    
    print("🧪 Prueba de Rutas del Sistema de Votación")
    print("=" * 50)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL Base: {base_url}")
    print()
    
    results = []
    
    for route in routes:
        try:
            print(f"🔍 Probando: {route['name']}")
            print(f"   URL: {route['url']}")
            
            if route['method'] == 'GET':
                response = requests.get(route['url'], timeout=10)
            else:
                response = requests.post(route['url'], timeout=10)
            
            status = response.status_code
            expected = route['expected_status']
            
            if status == expected:
                print(f"   ✅ OK - Status: {status}")
                results.append({"route": route['name'], "status": "OK", "code": status})
            else:
                print(f"   ❌ ERROR - Expected: {expected}, Got: {status}")
                results.append({"route": route['name'], "status": "ERROR", "code": status})
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ ERROR - No se puede conectar al servidor")
            print(f"   💡 Asegúrate de que la aplicación esté ejecutándose (python run.py)")
            results.append({"route": route['name'], "status": "CONNECTION_ERROR", "code": None})
            
        except requests.exceptions.Timeout:
            print(f"   ❌ ERROR - Timeout")
            results.append({"route": route['name'], "status": "TIMEOUT", "code": None})
            
        except Exception as e:
            print(f"   ❌ ERROR - {str(e)}")
            results.append({"route": route['name'], "status": "EXCEPTION", "code": None})
        
        print()
    
    # Resumen
    print("📊 Resumen de Pruebas")
    print("=" * 50)
    
    ok_count = sum(1 for r in results if r['status'] == 'OK')
    total_count = len(results)
    
    print(f"✅ Rutas OK: {ok_count}/{total_count}")
    print(f"❌ Rutas con errores: {total_count - ok_count}/{total_count}")
    print()
    
    if ok_count == total_count:
        print("🎉 ¡Todas las rutas funcionan correctamente!")
        print()
        print("🧭 Navegación disponible:")
        print("• http://localhost:5000/ - Pantalla principal de votación")
        print("• http://localhost:5000/winner - Ver ganador")
        print("• http://localhost:5000/books-manager - Gestionar libros")
        print("• http://localhost:5000/votes - Ver votos (contraseña: 1234)")
        print()
        print("🎯 Para probar la navegación:")
        print("python demo_navigation.py")
    else:
        print("⚠️  Hay problemas con algunas rutas:")
        for result in results:
            if result['status'] != 'OK':
                print(f"   • {result['route']}: {result['status']}")
        
        print()
        print("💡 Soluciones sugeridas:")
        print("1. Asegúrate de que la aplicación esté ejecutándose:")
        print("   python run.py")
        print("2. Verifica que el puerto 5000 esté libre")
        print("3. Revisa los logs de la aplicación para errores")

if __name__ == "__main__":
    try:
        test_routes()
    except KeyboardInterrupt:
        print("\n\n👋 Pruebas canceladas por el usuario")
        sys.exit(0)
