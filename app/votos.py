"""Lectura y escritura de los votos (data.txt) y del estado de la votación en Telegram.

Formato de cada línea de data.txt (lo leen también voting_condorcet.py, voting_irv.py y kek.py):
    Nombre: Pato García [tg:123456789]; Lista: ['Libro A', 'Libro B']; fecha: 2026-11-20 21:03:11
La marca [tg:<id>] identifica la cuenta de Telegram que votó. Los parsers del conteo descartan el nombre.
"""
import ast
import json
import os
import re
import threading
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))
RUTA_VOTOS = os.path.join(base_dir, 'data', 'data.txt')
RUTA_LIBROS = os.path.join(base_dir, 'data', 'books.json')
# Estado del bot: si la votación está abierta y dónde está la tarjeta del grupo. Ignorado por git.
RUTA_ESTADO = os.path.join(base_dir, 'data', 'telegram.json')
# Copia de cada voto que borra el admin, por si se borró por error. Ignorado por git.
RUTA_BORRADOS = os.path.join(base_dir, 'data', 'votos_borrados.txt')

_MARCA = re.compile(r'^(.*?)\s*\[tg:(\d+)\]$')
# Que nadie agregue un voto mientras otro pedido reescribe el archivo
_candado = threading.Lock()


def separar_marca(nombre):
    """'Pato García [tg:123]' -> ('Pato García', 123). Sin marca -> (nombre, None)."""
    nombre = nombre.strip()
    m = _MARCA.match(nombre)
    if m:
        return m.group(1), int(m.group(2))
    return nombre, None


def _leer_linea(linea):
    """Una línea de data.txt -> {nombre, tg_id, lista, fecha}, o None si no es un voto."""
    linea = linea.strip()
    if not linea.startswith('Nombre: '):
        return None
    partes = linea.split('; ')
    nombre, tg_id = separar_marca(partes[0][len('Nombre: '):])
    fecha = partes[-1][len('fecha: '):].strip() if partes[-1].startswith('fecha: ') else ''
    texto_lista = '; '.join(partes[1:-1])
    lista = []
    if texto_lista.startswith('Lista: '):
        try:
            lista = ast.literal_eval(texto_lista[len('Lista: '):])
        except (ValueError, SyntaxError):
            lista = []
    return {'nombre': nombre, 'tg_id': tg_id, 'lista': lista, 'fecha': fecha}


def leer_votos(ruta=None):
    """Todos los votos, en el orden en que llegaron: [{nombre, tg_id, lista, fecha}]."""
    try:
        with open(ruta or RUTA_VOTOS, 'r', encoding='utf-8') as archivo:
            lineas = archivo.read().splitlines()
    except FileNotFoundError:
        return []
    return [voto for voto in map(_leer_linea, lineas) if voto]


def clave_de(voto):
    """Cómo se identifica un voto para borrarlo: por la cuenta de Telegram o,
    en los votos viejos que no la tienen, por nombre y fecha."""
    if voto['tg_id'] is not None:
        return f"tg:{voto['tg_id']}"
    return f"{voto['nombre']}|{voto['fecha']}"


def nombres_de_votantes(ruta=None):
    """Nombres de quienes ya votaron, sin la marca de Telegram, en el orden en que votaron."""
    return [voto['nombre'] for voto in leer_votos(ruta)]


def voto_de(tg_id, ruta=None):
    """El voto de esa cuenta de Telegram, o None si todavía no votó."""
    for voto in leer_votos(ruta):
        if voto['tg_id'] == tg_id:
            return voto
    return None


def agregar_voto(nombre, tg_id, lista, fechahora, ruta=None):
    with _candado:
        with open(ruta or RUTA_VOTOS, 'a', encoding='utf-8') as archivo:
            archivo.write(f"Nombre: {nombre} [tg:{tg_id}]; Lista: {lista}; fecha: {fechahora}\n")


def borrar_votos(clave=None, ruta=None):
    """Saca de data.txt los votos con esa clave (ver clave_de), o todos si clave es None.
    Devuelve los votos borrados. Las líneas borradas se copian al final de votos_borrados.txt."""
    ruta = ruta or RUTA_VOTOS
    with _candado:
        try:
            # newline='' deja los saltos de línea como están
            with open(ruta, 'r', encoding='utf-8', newline='') as archivo:
                lineas = archivo.readlines()
        except FileNotFoundError:
            return []
        quedan, borradas, borrados = [], [], []
        for linea in lineas:
            voto = _leer_linea(linea)
            if voto and (clave is None or clave_de(voto) == clave):
                borradas.append(linea)
                borrados.append(voto)
            else:
                quedan.append(linea)
        if not borrados:
            return []

        with open(RUTA_BORRADOS, 'a', encoding='utf-8') as archivo:
            archivo.write(f"# Borrado el {datetime.now():%Y-%m-%d %H:%M:%S}\n")
            archivo.writelines(l.rstrip('\r\n') + '\n' for l in borradas)
        # Si la última línea queda sin salto, el próximo voto se pegaría a ella
        if quedan and not quedan[-1].endswith('\n'):
            quedan[-1] += '\n'
        temporal = ruta + '.tmp'
        with open(temporal, 'w', encoding='utf-8', newline='') as archivo:
            archivo.writelines(quedan)
        os.replace(temporal, ruta)
        return borrados


def leer_estado():
    try:
        with open(RUTA_ESTADO, 'r', encoding='utf-8') as archivo:
            estado = json.load(archivo)
            return estado if isinstance(estado, dict) else {}
    except (FileNotFoundError, ValueError):
        return {}


def guardar_estado(estado):
    temporal = RUTA_ESTADO + '.tmp'
    with open(temporal, 'w', encoding='utf-8') as archivo:
        json.dump(estado, archivo, ensure_ascii=False, indent=4)
    os.replace(temporal, RUTA_ESTADO)


def grupo_en_silencio():
    """Con "grupo_en_silencio": true en telegram.json, el bot no manda ni edita nada en grupos (ver telegram_bot.llamar)."""
    return leer_estado().get('grupo_en_silencio') is True


def votacion_abierta():
    """Mientras nadie la cierre (con /cerrar o desde la página de resultados), la votación está abierta."""
    return leer_estado().get('abierta', True) is not False
