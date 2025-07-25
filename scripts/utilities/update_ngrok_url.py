import os
import re
from dotenv import load_dotenv, set_key

def update_ngrok_url():
    """Actualiza la URL de ngrok en el archivo .env"""
    print("🔄 Actualizando URL de ngrok...")
    
    # Pedir la nueva URL
    new_url = input("📝 Ingresa la nueva URL de ngrok (ej: https://abc123.ngrok.io): ").strip()
    
    if not new_url:
        print("❌ URL vacía. Cancelando...")
        return
    
    # Validar formato básico
    if not re.match(r'https://[\w-]+\.ngrok\.io', new_url):
        print("⚠️  Formato de URL no válido. Debería ser como: https://abc123.ngrok.io")
        confirm = input("¿Continuar de todas formas? (y/N): ")
        if confirm.lower() != 'y':
            return
    
    # Agregar el path /telegram si no lo tiene
    if not new_url.endswith('/telegram'):
        new_url += '/telegram'
    
    # Actualizar el archivo .env
    env_file = '.env'
    set_key(env_file, 'WEB_APP_URL', new_url)
    
    print(f"✅ URL actualizada en {env_file}: {new_url}")
    print("🤖 Ahora ejecuta 'python setup_bot.py' para actualizar el bot")

if __name__ == '__main__':
    update_ngrok_url()