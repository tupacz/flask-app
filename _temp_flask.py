
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
