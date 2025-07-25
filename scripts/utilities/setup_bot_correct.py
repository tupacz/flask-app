from dotenv import load_dotenv
load_dotenv()

import asyncio
import os
from telegram import Bot, MenuButtonWebApp, WebAppInfo
from telegram.error import TelegramError

async def setup_telegram_bot():
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    web_app_url = os.environ.get('WEB_APP_URL')
    
    if not bot_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN no está configurado")
        return
    
    if not web_app_url:
        print("❌ Error: WEB_APP_URL no está configurado")
        return
    
    try:
        bot = Bot(token=bot_token)
        
        # Verificar que el bot funciona
        me = await bot.get_me()
        print(f"✅ Bot conectado: @{me.username}")
        
        # Configurar el Web App como botón del menú
        web_app = WebAppInfo(url=web_app_url)
        menu_button = MenuButtonWebApp(text="📚 Votar Libros", web_app=web_app)
        
        await bot.set_chat_menu_button(menu_button=menu_button)
        print(f"✅ Web App configurado: {web_app_url}")
        
        # Configurar comandos del bot
        from telegram import BotCommand
        commands = [
            BotCommand("start", "Iniciar el bot de votación"),
            BotCommand("votar", "Abrir la aplicación de votación"),
            BotCommand("help", "Mostrar ayuda")
        ]
        
        await bot.set_my_commands(commands)
        print("✅ Comandos configurados")
        
        print(f"\n🎉 ¡Bot configurado exitosamente!")
        print(f"Bot: @{me.username}")
        print(f"Web App URL: {web_app_url}")
        print(f"\n📱 Ahora puedes:")
        print(f"1. Escribir /start a @{me.username}")
        print(f"2. Usar el botón del menú '📚 Votar Libros'")
        
    except TelegramError as e:
        print(f"❌ Error de Telegram: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    asyncio.run(setup_telegram_bot())