#!/usr/bin/env python3
"""
Script de desarrollo para ejecutar Flask + Bot Telegram
Establece valores por defecto para desarrollo local
"""

import os
import sys
from pathlib import Path

# Establecer variables por defecto para desarrollo
def setup_dev_environment():
    """Configura variables de entorno para desarrollo"""
    
    # Variables por defecto para desarrollo
    defaults = {
        'TELEGRAM_BOT_TOKEN': '7832895832:AAEhmcmADP-DRuOf9Bg7Xbf3sz8Tx50452g',
        'WEB_APP_URL': 'https://dde6b371e9b0.ngrok-free.app/telegram',
        'FLASK_HOST': '0.0.0.0',
        'FLASK_PORT': '5000',
        'FLASK_DEBUG': 'True',
        'SECRET_KEY': 'dev-secret-key-change-in-production'
    }
    
    # Establecer variables solo si no existen
    for key, value in defaults.items():
        if not os.environ.get(key):
            os.environ.setdefault(key, value)
    
    print("🔧 Configuración de desarrollo:")
    print(f"   - Flask: http://{os.environ.get('FLASK_HOST')}:{os.environ.get('FLASK_PORT')}")
    print(f"   - Mini App: {os.environ.get('WEB_APP_URL')}")
    print(f"   - Bot Token: {'✅ Configurado' if os.environ.get('TELEGRAM_BOT_TOKEN') != 'your_bot_token_here' else '⚠️  Usar token real'}")
    print("   - Modo: Desarrollo")
    print()

if __name__ == '__main__':
    print("🚀 Iniciando en modo desarrollo...")
    print()
    
    # Configurar entorno de desarrollo
    setup_dev_environment()
    
    # Verificar si existe .env
    env_file = Path('.env')
    if env_file.exists():
        print("✅ Archivo .env encontrado")
    else:
        print("⚠️  No se encontró archivo .env, usando valores por defecto")
        print("💡 Copia .env.example a .env y configura tus valores reales")
    
    print("📱 Mini App estará disponible en: /telegram")
    print("🤖 Recuerda configurar tu TELEGRAM_BOT_TOKEN real para que funcione!")
    print()
    
    # Importar y ejecutar el script principal
    try:
        from run_combined_v2 import main
        main()
    except KeyboardInterrupt:
        print("\n👋 Desarrollo detenido")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
