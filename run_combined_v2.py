#!/usr/bin/env python3
"""
Ejecutor combinado para Flask y Bot de Telegram - Versión Simplificada
Ejecuta ambos servicios usando multiprocessing en lugar de threading
"""

import os
import sys
import subprocess
import signal
import time
import logging
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_flask_script():
    """Crea un script temporal para ejecutar Flask"""
    flask_script = '''
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Importar después de cargar las variables de entorno
from app import create_app

app = create_app()

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🌐 Flask ejecutándose en http://{host}:{port}")
    print("📱 Mini App disponible en: /telegram")
    
    app.run(host=host, port=port, debug=debug, use_reloader=False, threaded=True)
'''
    
    with open('_temp_flask.py', 'w', encoding='utf-8') as f:
        f.write(flask_script)
    
    return '_temp_flask.py'

def create_bot_script():
    """Crea un script temporal para ejecutar el bot"""
    bot_script = '''
import os
import asyncio
import logging
from dotenv import load_dotenv

load_dotenv()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /start"""
    web_app_url = os.environ.get('WEB_APP_URL', 'http://localhost:5000/telegram')
    
    # Crear botón con Web App
    web_app = WebAppInfo(url=web_app_url)
    keyboard = [
        [InlineKeyboardButton("📚 Votar Libros", web_app=web_app)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = """
🎉 ¡Bienvenido al Bot de Votación de Libros!

📖 Aquí puedes votar por tus libros favoritos arrastrando y soltando para ordenarlos según tu preferencia.

🗳️ Haz clic en el botón de abajo para comenzar a votar:
"""
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup
    )

async def votar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /votar"""
    await start(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /help"""
    help_text = """
🤖 *Bot de Votación de Libros*

📚 *Comandos disponibles:*
/start - Iniciar el bot
/votar - Abrir la votación
/help - Mostrar esta ayuda

🗳️ *Cómo votar:*
1. Haz clic en "📚 Votar Libros"
2. Arrastra los libros para ordenarlos
3. El primer libro es tu favorito
4. Haz clic en "Enviar Voto"

✨ *Tu voto se cuenta usando el método Condorcet para encontrar el ganador más justo!*
"""
    
    await update.message.reply_text(
        help_text,
        parse_mode='Markdown'
    )

def main():
    """Función principal del bot"""
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        logger.error("❌ Error: TELEGRAM_BOT_TOKEN no está configurado en .env")
        return
    
    logger.info("🤖 Iniciando bot de Telegram...")
    
    # Crear la aplicación del bot
    application = Application.builder().token(bot_token).build()
    
    # Agregar manejadores
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("votar", votar))
    application.add_handler(CommandHandler("help", help_command))
    
    logger.info("🤖 Bot de Telegram iniciado correctamente")
    
    # Ejecutar el bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
'''
    
    with open('_temp_bot.py', 'w', encoding='utf-8') as f:
        f.write(bot_script)
    
    return '_temp_bot.py'

def cleanup_temp_files():
    """Limpia los archivos temporales"""
    for file in ['_temp_flask.py', '_temp_bot.py']:
        try:
            if os.path.exists(file):
                os.remove(file)
        except:
            pass

def main():
    """Función principal que ejecuta ambos servicios"""
    logger.info("🚀 Iniciando servicios combinados...")
    
    # Verificar variables de entorno críticas
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        logger.error("❌ Error: TELEGRAM_BOT_TOKEN no está configurado en .env")
        logger.error("💡 Asegúrate de tener un archivo .env con las variables necesarias")
        sys.exit(1)
    
    # Mostrar configuración
    logger.info("⚙️  Configuración:")
    logger.info(f"   - Flask Host: {os.environ.get('FLASK_HOST', '0.0.0.0')}")
    logger.info(f"   - Flask Port: {os.environ.get('FLASK_PORT', '5000')}")
    logger.info(f"   - Web App URL: {os.environ.get('WEB_APP_URL', 'http://localhost:5000/telegram')}")
    logger.info(f"   - Bot Token configurado: ✅")
    
    # Crear scripts temporales
    flask_script = create_flask_script()
    bot_script = create_bot_script()
    
    flask_process = None
    bot_process = None
    
    try:
        # Iniciar Flask
        logger.info("🌐 Iniciando servidor Flask...")
        flask_process = subprocess.Popen([sys.executable, flask_script])
        
        # Esperar un poco para que Flask se inicie
        time.sleep(3)
        
        # Iniciar Bot de Telegram
        logger.info("🤖 Iniciando bot de Telegram...")
        bot_process = subprocess.Popen([sys.executable, bot_script])
        
        logger.info("✅ Ambos servicios están ejecutándose")
        logger.info("🛑 Presiona Ctrl+C para detener ambos servicios")
        
        # Esperar a que terminen los procesos
        while True:
            # Verificar si los procesos siguen vivos
            if flask_process.poll() is not None:
                logger.error("❌ Proceso de Flask se detuvo inesperadamente")
                break
                
            if bot_process.poll() is not None:
                logger.error("❌ Proceso del bot se detuvo inesperadamente")
                break
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 Deteniendo servicios...")
        
    except Exception as e:
        logger.error(f"❌ Error al iniciar los servicios: {e}")
        
    finally:
        # Terminar procesos
        if flask_process:
            try:
                flask_process.terminate()
                flask_process.wait(timeout=5)
            except:
                try:
                    flask_process.kill()
                except:
                    pass
        
        if bot_process:
            try:
                bot_process.terminate()
                bot_process.wait(timeout=5)
            except:
                try:
                    bot_process.kill()
                except:
                    pass
        
        # Limpiar archivos temporales
        cleanup_temp_files()
        
        logger.info("👋 Servicios detenidos")

if __name__ == '__main__':
    main()
