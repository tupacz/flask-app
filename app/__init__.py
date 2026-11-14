import os
import secrets
from datetime import timedelta

from flask import Flask

base_dir = os.path.dirname(os.path.abspath(__file__))


def _leer_secreto(nombre_env, archivo, generar=False):
    """Lee un secreto de una variable de entorno o de un archivo (ignorado por git).
    Si generar=True y no existe, lo crea con un valor aleatorio."""
    valor = os.environ.get(nombre_env)
    if valor:
        return valor
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            valor = f.read().strip()
        if valor:
            return valor
    if generar:
        valor = secrets.token_hex(32)
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(valor)
        return valor
    return None


def create_app():
    app = Flask(__name__)

    # Clave para firmar la cookie de sesión (la del admin). Se genera sola la primera vez.
    app.secret_key = _leer_secreto('SECRET_KEY', os.path.join(base_dir, 'secret_key.txt'), generar=True)
    # Contraseña del admin: variable ADMIN_PASSWORD o archivo app/admin_password.txt
    app.config['ADMIN_PASSWORD'] = _leer_secreto('ADMIN_PASSWORD', os.path.join(base_dir, 'admin_password.txt'))
    # El navegador del admin lo recuerda durante un año
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Registrar las rutas
    from .routes import main
    app.register_blueprint(main)

    return app
