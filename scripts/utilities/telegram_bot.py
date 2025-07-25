"""
Telegram Bot to set up the Mini App
This script helps you create a bot and set up the Web App URL
"""

from dotenv import load_dotenv
load_dotenv()  # Cargar variables del .env

import asyncio
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebApp
from telegram.ext import Application, CommandHandler, ContextTypes

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get bot token from environment or ask user
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
WEB_APP_URL = os.environ.get('WEB_APP_URL', 'https://your-domain.com/telegram')

if not BOT_TOKEN:
    print("Please set TELEGRAM_BOT_TOKEN environment variable or edit this script")
    print("Get your bot token from @BotFather on Telegram")
    sys.exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    web_app_url = os.environ.get('WEB_APP_URL', 'https://example.ngrok.io/telegram')
    
    # Crear botón con Web App
    keyboard = [
        [InlineKeyboardButton("📚 Votar Libros", web_app=WebApp(url=web_app_url))]
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

async def vote(update, context: ContextTypes.DEFAULT_TYPE):
    """Open the voting web app."""
    web_app = WebAppInfo(url=WEB_APP_URL)
    await update.message.reply_text(
        "🗳️ Haz clic en el botón para abrir la aplicación de votación:",
        reply_markup={
            "inline_keyboard": [[{
                "text": "📚 Votar por Libros",
                "web_app": {"url": WEB_APP_URL}
            }]]
        }
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

async def setup_menu_button(application):
    """Set up the menu button for the web app."""
    try:
        bot = application.bot
        web_app_info = WebAppInfo(url=WEB_APP_URL)
        menu_button = MenuButtonWebApp(text="📚 Votar Libros", web_app=web_app_info)
        
        await bot.set_chat_menu_button(menu_button=menu_button)
        print("Menu button set successfully!")
    except Exception as e:
        print(f"Error setting menu button: {e}")

def main():
    """Start the bot."""
    if not WEB_APP_URL.startswith('https://'):
        print("WARNING: WEB_APP_URL should start with https:// for Telegram Web Apps")
        print(f"Current URL: {WEB_APP_URL}")
    
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN no está configurado")
        return
    
    # Create the Application
    application = Application.builder().token(bot_token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("vote", vote))
    application.add_handler(CommandHandler("votar", votar))
    application.add_handler(CommandHandler("help", help_command))

    # Set up the menu button
    asyncio.get_event_loop().run_until_complete(setup_menu_button(application))

    print("Bot is starting...")
    print(f"Web App URL: {WEB_APP_URL}")
    print("Send /start to your bot to test it!")
    print("🤖 Bot iniciado. Presiona Ctrl+C para detener.")
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=["message", "inline_query", "chosen_inline_result"])

if __name__ == '__main__':
    main()
