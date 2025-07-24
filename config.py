import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sk_test_abc123def456')
    
    # Telegram Bot Token - You'll need to get this from @BotFather
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    # Telegram Web App URL - Replace with your domain when deployed
    WEB_APP_URL = os.environ.get('WEB_APP_URL')
    
    @staticmethod
    def validate():
        if not Config.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN no está configurado en el archivo .env")
        if not Config.WEB_APP_URL:
            raise ValueError("WEB_APP_URL no está configurado en el archivo .env")
        return True
