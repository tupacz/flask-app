"""Configura el bot de Telegram: webhook, comandos y botón de menú.

Se corre una vez (y de nuevo si cambia la dirección del sitio), desde la raíz del repo:
    python -m app.configurar_bot

Lee el token y demás datos igual que la app (variables de entorno o archivos en app/).
Antes de correrlo, la web app tiene que estar recargada para que el webhook exista.
"""
import json
import sys

from flask import Flask

from app import leer_config_telegram
from app.telegram_bot import llamar


def main():
    config = leer_config_telegram()
    if not config['BOT_TOKEN']:
        sys.exit("Falta el token del bot: creá app/bot_token.txt o definí BOT_TOKEN.")
    if not config['BOT_USERNAME']:
        print("Aviso: falta app/bot_username.txt. Sin eso la tarjeta del grupo no tiene botón para votar.")
    if not config['ADMIN_TELEGRAM_IDS']:
        print("Aviso: app/admin_ids.txt está vacío. Mandale /miid al bot y anotá ahí tu id.")

    sitio = config['SITE_URL']
    # llamar() lee el token de la config de Flask
    app = Flask(__name__)
    app.config.update(config)
    with app.app_context():
        pasos = [
            ('setWebhook', {
                'url': f"{sitio}/telegram/webhook",
                'secret_token': config['WEBHOOK_SECRET'],
                'allowed_updates': ['message'],
                'drop_pending_updates': True,
            }),
            ('setMyCommands', {'commands': [
                {'command': 'votacion', 'description': 'Publicar la tarjeta para votar (organización)'},
                {'command': 'cerrar', 'description': 'Cerrar la votación y anunciar el ganador (organización)'},
                {'command': 'miid', 'description': 'Ver tu id de Telegram'},
            ]}),
            ('setChatMenuButton', {'menu_button': {
                'type': 'web_app', 'text': 'Votar', 'web_app': {'url': f"{sitio}/"},
            }}),
        ]
        for metodo, params in pasos:
            resultado = llamar(metodo, params)
            print(f"{metodo}: {'listo' if resultado is not None else 'falló (mirá el mensaje de arriba)'}")

        info = llamar('getWebhookInfo')
        print("getWebhookInfo:", json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
