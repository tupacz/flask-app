#!/usr/bin/env python3
"""
Ejecutor combinado para Flask y Bot de Telegram
Ejecuta ambos servicios simultáneamente usando threading
"""

import os
import sys
import threading
import time
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_flask_app():
    """Ejecuta la aplicación Flask"""
    try:
        logger.info("🌐 Iniciando servidor Flask...")
        
        # Importar después de cargar las variables de entorno
        from app import create_app
        
        app = create_app()
        
        # Configuración del servidor Flask
        host = os.environ.get('FLASK_HOST', '0.0.0.0')
        port = int(os.environ.get('FLASK_PORT', 5000))
        debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
        
        logger.info(f"🌐 Flask ejecutándose en http://{host}:{port}")
        logger.info("📱 Mini App disponible en: /telegram")
        
        # Ejecutar Flask sin reloader para evitar conflictos con threading
        app.run(host=host, port=port, debug=debug, use_reloader=False, threaded=True)
        
    except Exception as e:
        logger.error(f"❌ Error al iniciar Flask: {e}")
        sys.exit(1)

def run_telegram_bot():
    """Ejecuta el bot de Telegram"""
    import asyncio
    
    try:
        # Esperar un poco para que Flask se inicie primero
        time.sleep(2)
        
        logger.info("🤖 Iniciando bot de Telegram...")
        
        # Crear un nuevo event loop para este thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Importar las dependencias del bot
        from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
        from telegram.ext import Application, CommandHandler, ContextTypes
        
        # Verificar token del bot
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            logger.error("❌ Error: TELEGRAM_BOT_TOKEN no está configurado en .env")
            return
        
        # Configurar handlers del bot
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

        # Crear la aplicación del bot
        application = Application.builder().token(bot_token).build()
        
        # Agregar manejadores
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("votar", votar))
        application.add_handler(CommandHandler("help", help_command))
        
        logger.info("🤖 Bot de Telegram iniciado correctamente")
        
        # Función para ejecutar el bot de manera async
        async def run_bot():
            async with application:
                await application.start()
                await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
                # Mantener el bot ejecutándose
                await asyncio.Event().wait()
        
        # Ejecutar el bot en el event loop
        loop.run_until_complete(run_bot())
        
    except Exception as e:
        logger.error(f"❌ Error al iniciar el bot de Telegram: {e}")
        sys.exit(1)
    finally:
        # Cerrar el event loop al finalizar
        try:
            if not loop.is_closed():
                loop.close()
        except:
            pass

def main():
    """Función principal que ejecuta ambos servicios"""
    logger.info("🚀 Iniciando servicios combinados...")
    
    # Verificar variables de entorno críticas
    required_vars = ['TELEGRAM_BOT_TOKEN']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
        logger.error("💡 Asegúrate de tener un archivo .env con las variables necesarias")
        sys.exit(1)
    
    # Mostrar configuración
    logger.info("⚙️  Configuración:")
    logger.info(f"   - Flask Host: {os.environ.get('FLASK_HOST', '0.0.0.0')}")
    logger.info(f"   - Flask Port: {os.environ.get('FLASK_PORT', '5000')}")
    logger.info(f"   - Web App URL: {os.environ.get('WEB_APP_URL', 'http://localhost:5000/telegram')}")
    logger.info(f"   - Bot Token configurado: {'✅' if os.environ.get('TELEGRAM_BOT_TOKEN') else '❌'}")
    
    try:
        # Crear threads para cada servicio
        flask_thread = threading.Thread(target=run_flask_app, daemon=True)
        bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
        
        # Iniciar Flask primero
        flask_thread.start()
        logger.info("🌐 Thread de Flask iniciado")
        
        # Luego iniciar el bot
        bot_thread.start()
        logger.info("🤖 Thread del bot iniciado")
        
        logger.info("✅ Ambos servicios están ejecutándose")
        logger.info("🛑 Presiona Ctrl+C para detener ambos servicios")
        
        # Mantener el programa ejecutándose
        try:
            while True:
                time.sleep(1)
                
                # Verificar si los threads siguen vivos
                if not flask_thread.is_alive():
                    logger.error("❌ Thread de Flask se detuvo inesperadamente")
                    break
                    
                if not bot_thread.is_alive():
                    logger.error("❌ Thread del bot se detuvo inesperadamente")
                    break
                    
        except KeyboardInterrupt:
            logger.info("🛑 Deteniendo servicios...")
            
    except Exception as e:
        logger.error(f"❌ Error al iniciar los servicios: {e}")
        sys.exit(1)
    
    logger.info("👋 Servicios detenidos")

if __name__ == '__main__':
    main()
