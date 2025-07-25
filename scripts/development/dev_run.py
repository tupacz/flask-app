"""
Development server script with environment variable setup
"""

import os
from app import create_app

# Set development environment variables
os.environ.setdefault('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
os.environ.setdefault('WEB_APP_URL', 'https://your-domain.com/telegram')
os.environ.setdefault('SECRET_KEY', 'dev-secret-key-change-in-production')

app = create_app()

if __name__ == '__main__':
    print("🚀 Starting Flask development server...")
    print("📱 Telegram Mini App will be available at: /telegram")
    print("🌐 Regular web interface available at: /")
    print("⚠️  Remember to set your real TELEGRAM_BOT_TOKEN for production!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
