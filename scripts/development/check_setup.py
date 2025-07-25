import os
import asyncio
from telegram import Bot

async def check_bot():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    url = os.environ.get('WEB_APP_URL')
    
    print("🔍 Verificando configuración...")
    print(f"Bot Token: {'✅ Configurado' if token else '❌ Faltante'}")
    print(f"Web App URL: {'✅ ' + url if url else '❌ Faltante'}")
    
    if token:
        try:
            bot = Bot(token)
            me = await bot.get_me()
            print(f"✅ Bot válido: @{me.username}")
        except Exception as e:
            print(f"❌ Error con el bot: {e}")

if __name__ == '__main__':
    asyncio.run(check_bot())