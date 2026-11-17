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


def _leer_ids(texto):
    """'123, 456\n789' -> {123, 456, 789}. Ignora lo que no sea un número."""
    ids = set()
    for parte in (texto or '').replace(',', '\n').split():
        if parte.strip().lstrip('-').isdigit():
            ids.add(int(parte))
    return ids


def leer_config_telegram():
    """Secretos y datos del bot. Los usan la app y el script configurar_bot."""
    return {
        # Token que da @BotFather: variable BOT_TOKEN o archivo app/bot_token.txt
        'BOT_TOKEN': _leer_secreto('BOT_TOKEN', os.path.join(base_dir, 'bot_token.txt')),
        # Usuario del bot sin @, por ejemplo ClubLecturaBot
        'BOT_USERNAME': (_leer_secreto('BOT_USERNAME', os.path.join(base_dir, 'bot_username.txt')) or '').lstrip('@'),
        # Clave que Telegram manda en cada llamada al webhook. Se genera sola la primera vez.
        'WEBHOOK_SECRET': _leer_secreto('TELEGRAM_WEBHOOK_SECRET', os.path.join(base_dir, 'webhook_secret.txt'), generar=True),
        # Cuentas de Telegram que organizan la votación (las da el comando /miid)
        'ADMIN_TELEGRAM_IDS': _leer_ids(_leer_secreto('ADMIN_TELEGRAM_IDS', os.path.join(base_dir, 'admin_ids.txt'))),
        # Dirección pública del sitio. Con el bot de desarrollo, la del túnel (cloudflared).
        'SITE_URL': (os.environ.get('SITE_URL') or 'https://tupac.pythonanywhere.com').rstrip('/'),
    }


def create_app():
    app = Flask(__name__)

    # Clave para firmar la cookie de sesión (la del admin). Se genera sola la primera vez.
    app.secret_key = _leer_secreto('SECRET_KEY', os.path.join(base_dir, 'secret_key.txt'), generar=True)
    # Contraseña del admin: variable ADMIN_PASSWORD o archivo app/admin_password.txt
    app.config['ADMIN_PASSWORD'] = _leer_secreto('ADMIN_PASSWORD', os.path.join(base_dir, 'admin_password.txt'))
    app.config.update(leer_config_telegram())
    # El navegador del admin lo recuerda durante un año
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Registrar las rutas
    from .routes import main
    app.register_blueprint(main)

    return app
