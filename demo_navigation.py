#!/usr/bin/env python3
"""
Demo script para mostrar las funcionalidades de navegación del sistema de votación de libros.
"""

import webbrowser
import time
import sys

def demo_navigation():
    """Demostración de las funcionalidades de navegación"""
    
    print("🚀 Demo del Sistema de Votación de Libros")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    pages = [
        {
            "name": "🗳️ Pantalla Principal - Votar",
            "url": f"{base_url}/",
            "description": "Interfaz para ordenar y votar por libros"
        },
        {
            "name": "🏆 Pantalla de Ganador",
            "url": f"{base_url}/winner",
            "description": "Resultados usando el método Condorcet"
        },
        {
            "name": "📚 Gestión de Libros", 
            "url": f"{base_url}/books-manager",
            "description": "Agregar, editar y eliminar libros"
        },
        {
            "name": "📊 Ver Votos (Protegida)",
            "url": f"{base_url}/votes",
            "description": "Vista administrativa (contraseña: 1234)"
        }
    ]
    
    print("Asegúrate de que la aplicación esté ejecutándose (python run.py)")
    print()
    
    for i, page in enumerate(pages, 1):
        print(f"{i}. {page['name']}")
        print(f"   📝 {page['description']}")
        print(f"   🔗 {page['url']}")
        
        response = input(f"\n   ¿Abrir esta página? (s/n/q para salir): ").lower()
        
        if response == 'q':
            print("\n👋 Demo terminada!")
            break
        elif response == 's':
            print(f"   🌐 Abriendo {page['name']}...")
            try:
                webbrowser.open(page['url'])
                time.sleep(2)
            except Exception as e:
                print(f"   ❌ Error al abrir: {e}")
        
        print("-" * 50)
    
    print("\n✨ Características destacadas:")
    print("• Navegación con barra fija en la parte superior")
    print("• Botón activo resaltado según la página actual")
    print("• Protección por contraseña para la vista de votos")
    print("• Diseño responsive para móviles y desktop")
    print("• Interfaz intuitiva con emojis y colores")
    
    print("\n🔐 Credenciales de acceso:")
    print("• Contraseña para ver votos: 1234")
    
    print("\n🎯 Próximos pasos:")
    print("1. Probar la votación desde la pantalla principal")
    print("2. Agregar libros desde la gestión de libros")
    print("3. Ver resultados en la pantalla de ganador")
    print("4. Revisar datos en la vista de votos (con contraseña)")

if __name__ == "__main__":
    try:
        demo_navigation()
    except KeyboardInterrupt:
        print("\n\n👋 Demo cancelada por el usuario")
        sys.exit(0)
