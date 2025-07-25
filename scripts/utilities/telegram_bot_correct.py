from dotenv import load_dotenv
load_dotenv()

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /start"""
    web_app_url = os.environ.get('WEB_APP_URL', 'https://example.ngrok.io/telegram')
    
    # Crear botón con Web App usando WebAppInfo
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
        print("❌ Error: TELEGRAM_BOT_TOKEN no está configurado en .env")
        return
    
    print(f"🤖 Iniciando bot...")
    
    # Crear la aplicación
    application = Application.builder().token(bot_token).build()
    
    # Agregar manejadores
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("votar", votar))
    application.add_handler(CommandHandler("help", help_command))
    
    print("🤖 Bot iniciado. Presiona Ctrl+C para detener.")
    
    # Ejecutar el bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()