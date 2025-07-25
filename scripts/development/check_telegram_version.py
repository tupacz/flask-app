try:
    import telegram
    print(f"✅ python-telegram-bot versión: {telegram.__version__}")
    
    # Verificar si WebApp está disponible
    try:
        from telegram import WebApp
        print("✅ WebApp disponible")
    except ImportError:
        print("❌ WebApp no disponible - actualiza python-telegram-bot")
        
    # Verificar otras características
    try:
        from telegram.ext import Application
        print("✅ Application disponible (versión moderna)")
    except ImportError:
        print("❌ Application no disponible - versión muy antigua")
        
except ImportError:
    print("❌ python-telegram-bot no está instalado")
    print("Instala con: pip install python-telegram-bot>=20.0")