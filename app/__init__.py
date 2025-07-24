from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registrar las rutas
    from .routes import main
    app.register_blueprint(main)

    return app
