"""Identidad de quien vota, firmada por Telegram (initData de la Mini App).

Referencia: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
"""
import hashlib
import hmac
import json
import re
import time
from urllib.parse import parse_qsl

from flask import current_app, request


class InitDataInvalido(Exception):
    pass


def validar_init_data(init_data, bot_token, max_edad_seg=86400):
    """Comprueba la firma de initData con el token del bot y devuelve sus campos.
    'user' vuelve como dict. Lanza InitDataInvalido si algo no cierra."""
    if not init_data:
        raise InitDataInvalido("initData vacío")
    if not bot_token:
        raise InitDataInvalido("falta configurar el token del bot")
    try:
        pares = dict(parse_qsl(init_data, keep_blank_values=True, strict_parsing=True))
    except ValueError:
        raise InitDataInvalido("initData mal formado")
    hash_recibido = pares.pop("hash", None)
    if not hash_recibido:
        raise InitDataInvalido("falta hash")
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(pares.items()))
    # Clave = "WebAppData", mensaje = token (invertirlos es el error más común)
    clave_secreta = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    calculado = hmac.new(clave_secreta, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calculado.encode(), hash_recibido.encode()):
        raise InitDataInvalido("hash incorrecto")
    try:
        auth_date = int(pares.get("auth_date", ""))
    except ValueError:
        raise InitDataInvalido("auth_date inválido")
    if max_edad_seg and time.time() - auth_date > max_edad_seg:
        raise InitDataInvalido("initData vencido")
    try:
        pares["user"] = json.loads(pares["user"]) if "user" in pares else None
    except ValueError:
        raise InitDataInvalido("user inválido")
    return pares


def usuario_de_request():
    """El usuario de Telegram que manda el header 'Authorization: tma <initData>', o None."""
    encabezado = request.headers.get('Authorization', '')
    if not encabezado.startswith('tma '):
        return None
    try:
        datos = validar_init_data(encabezado[len('tma '):], current_app.config.get('BOT_TOKEN'))
    except InitDataInvalido as e:
        print(f"initData rechazado: {e}")
        return None
    usuario = datos.get('user')
    if not isinstance(usuario, dict) or not isinstance(usuario.get('id'), int):
        return None
    return usuario


def es_admin_telegram(usuario):
    return bool(usuario) and usuario.get('id') in current_app.config.get('ADMIN_TELEGRAM_IDS', set())


def nombre_para_guardar(usuario):
    """Nombre que se muestra y se guarda en data.txt. Saca lo que rompería el formato de la línea."""
    nombre = f"{usuario.get('first_name', '')} {usuario.get('last_name', '')}"
    nombre = re.sub(r"[;\[\]'\"\r\n\t]", " ", nombre)
    nombre = re.sub(r"\s+", " ", nombre).strip()[:64].strip()
    if nombre:
        return nombre
    if usuario.get('username'):
        return '@' + re.sub(r"[^A-Za-z0-9_]", "", usuario['username'])
    return f"Usuario {usuario.get('id')}"
