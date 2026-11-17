"""Pruebas de la Mini App sin Telegram real: initData firmado con un token falso y la Bot API simulada.

Desde la raíz del repo, con el venv activado:
    python pruebas/probar_telegram.py

Trabaja sobre copias temporales de los datos: no toca app/data/ ni llama a Telegram.
"""
import hashlib
import hmac
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlencode

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

TOKEN = '123456:TEST-token'
os.environ.update({
    'BOT_TOKEN': TOKEN, 'BOT_USERNAME': 'ClubTestBot', 'TELEGRAM_WEBHOOK_SECRET': 'secreto-test',
    'ADMIN_TELEGRAM_IDS': '111, 999', 'SECRET_KEY': 'clave-de-prueba', 'ADMIN_PASSWORD': 'pw',
})

from app import create_app, votos, telegram_bot  # noqa: E402
from app.telegram_auth import validar_init_data, InitDataInvalido, nombre_para_guardar  # noqa: E402

tmp = tempfile.mkdtemp()
votos.RUTA_VOTOS = os.path.join(tmp, 'data.txt')
votos.RUTA_LIBROS = os.path.join(tmp, 'books.json')
votos.RUTA_ESTADO = os.path.join(tmp, 'telegram.json')
open(votos.RUTA_VOTOS, 'w', encoding='utf-8').close()
LIBROS = ['Cien años de soledad', "El túnel", 'Rayuela']
with open(votos.RUTA_LIBROS, 'w', encoding='utf-8') as f:
    json.dump([{'title': t, 'author': 'A', 'description': 'D'} for t in LIBROS], f, ensure_ascii=False)

LLAMAR_REAL = telegram_bot.llamar
llamadas = []
def llamar_falso(metodo, params=None, token=None):
    llamadas.append((metodo, params or {}))
    if metodo == 'sendMessage':
        return {'message_id': 77, 'chat': {'id': params['chat_id']}}
    return True
telegram_bot.llamar = llamar_falso


def init_data(user, token=TOKEN, auth_date=None):
    campos = {'auth_date': str(auth_date or int(time.time())), 'query_id': 'AAHdF6IQAAAAAN0XohDhrOrc',
              'user': json.dumps(user, separators=(',', ':'), ensure_ascii=False)}
    dcs = '\n'.join(f'{k}={v}' for k, v in sorted(campos.items()))
    clave = hmac.new(b'WebAppData', token.encode(), hashlib.sha256).digest()
    campos['hash'] = hmac.new(clave, dcs.encode(), hashlib.sha256).hexdigest()
    return urlencode(campos)

def tma(user, **kw):
    return {'Authorization': 'tma ' + init_data(user, **kw)}

ANA = {'id': 222, 'first_name': 'Ana', 'last_name': "O'Brien; [x]", 'username': 'ana'}
MARIANA = {'id': 333, 'first_name': 'Mariana'}
ADMIN = {'id': 111, 'first_name': 'Pato', 'last_name': 'García'}

fallas = []
def chequear(condicion, descripcion):
    print(('OK   ' if condicion else 'FALLA ') + descripcion)
    if not condicion:
        fallas.append(descripcion)

# ---------- Validador ----------
datos = validar_init_data(init_data(ANA), TOKEN)
chequear(datos['user']['id'] == 222, 'validador acepta initData bien firmado')
for desc, valor, token in [
    ('token incorrecto', init_data(ANA), 'otro:token'),
    ('datos alterados', init_data(ANA).replace('Ana', 'Eva'), TOKEN),
    ('vencido', init_data(ANA, auth_date=int(time.time()) - 90000), TOKEN),
    ('vacío', '', TOKEN),
]:
    try:
        validar_init_data(valor, token)
        chequear(False, f'validador rechaza {desc}')
    except InitDataInvalido:
        chequear(True, f'validador rechaza {desc}')
chequear(nombre_para_guardar(ANA) == "Ana O Brien x", f'nombre saneado: {nombre_para_guardar(ANA)!r}')
chequear(nombre_para_guardar({'id': 5, 'first_name': ' ', 'username': 'pepe'}) == '@pepe', 'nombre vacío usa @username')

app = create_app()
app.config['ADMIN_TELEGRAM_IDS'] = {111, 999}
cliente = app.test_client()

# ---------- Página y sesión ----------
r = cliente.get('/')
chequear(r.status_code == 200 and b'telegram-web-app.js' in r.data and b'sortablejs@1.15.6' in r.data, 'GET / renderiza la Mini App')
chequear(cliente.post('/sesion-telegram').status_code == 401, '/sesion-telegram sin header -> 401')
r = cliente.post('/sesion-telegram', headers=tma(ANA))
chequear(r.status_code == 200 and r.json == {'nombre': 'Ana', 'voto': None, 'abierta': True, 'esAdmin': False}, f'/sesion-telegram de Ana: {r.json}')
chequear(cliente.get('/votes').data.count(b'name="password"') == 1, 'Ana no queda como admin')

# ---------- Votar ----------
orden = ['Rayuela', 'Cien años de soledad', 'El túnel']
chequear(cliente.post('/submit', json={'orderedList': orden}).status_code == 401, '/submit sin header -> 401')
chequear(cliente.post('/submit', json={'orderedList': orden}, headers=tma(ANA, token='otro:token')).status_code == 401, '/submit con firma falsa -> 401')
chequear(cliente.post('/submit', json={'orderedList': orden[:2]}, headers=tma(ANA)).status_code == 400, '/submit con lista incompleta -> 400')
chequear(cliente.post('/submit', json={'orderedList': orden + ['Otro']}, headers=tma(ANA)).status_code == 400, '/submit con libro de más -> 400')
chequear(cliente.post('/submit', json={'nada': 1}, headers=tma(ANA)).status_code == 400, '/submit sin orderedList -> 400')

# Tarjeta publicada antes para ver que se actualiza
votos.guardar_estado({'abierta': True, 'chat_id': -100, 'message_id': 77})
llamadas.clear()
r = cliente.post('/submit', json={'orderedList': orden}, headers=tma(ANA))
chequear(r.status_code == 200 and r.json['voto']['lista'] == orden, '/submit válido -> 200')
contenido = open(votos.RUTA_VOTOS, encoding='utf-8').read()
chequear(contenido.startswith("Nombre: Ana O Brien x [tg:222]; Lista: ['Rayuela', 'Cien años de soledad', 'El túnel']; fecha: "), f'línea en data.txt: {contenido.strip()}')
chequear(any(m == 'editMessageText' and 'Ya votó Ana O Brien x.' in p['text'] for m, p in llamadas), 'la tarjeta se actualiza después del voto')
r = cliente.post('/submit', json={'orderedList': orden}, headers=tma(ANA))
chequear(r.status_code == 409 and r.json.get('yaVoto') and r.json['voto']['lista'] == orden, 'segundo voto de Ana -> 409 con su boleta')
# "Ana" ya no bloquea a "Mariana" (antes era una búsqueda por subcadena)
r = cliente.post('/submit', json={'orderedList': list(reversed(orden))}, headers=tma(MARIANA))
chequear(r.status_code == 200, 'Mariana puede votar aunque "Ana" ya figure')
r = cliente.post('/sesion-telegram', headers=tma(ANA))
chequear(r.json['voto'] and r.json['voto']['lista'] == orden, '/sesion-telegram devuelve el voto de Ana')

# ---------- Admin por Telegram ----------
admin = app.test_client()
r = admin.post('/sesion-telegram', headers=tma(ADMIN))
chequear(r.json['esAdmin'] is True, 'admin reconocido por id')
r = admin.get('/winner')
chequear(r.status_code == 200 and b'Duelos mano a mano' in r.data, 'admin ve /winner completo')
chequear(admin.get('/votes').status_code == 200 and b'[tg:222]' in admin.get('/votes').data, 'admin ve /votes')
chequear(admin.get('/books-manager').status_code == 200 and b'Libros de la votaci' in admin.get('/books-manager').data, 'admin ve /books-manager')
chequear(b'Libros de la votaci' not in cliente.get('/books-manager').data, '/books-manager pide login a quien no es admin')
chequear(cliente.post('/submit-book', json=[]).status_code == 403, '/submit-book rechaza a quien no es admin')
r = cliente.get('/winner')
chequear(r.status_code == 200 and 'Quiénes votaron'.encode() in r.data and b'[tg:' not in r.data, '/winner público sin marcas')
chequear(b'Duelos mano a mano' not in r.data and b'Tu boleta' in r.data, '/winner con la votación abierta: sin resultado, con lugar para la boleta')
chequear(b'data-volver' in r.data and b'id="barra-admin" hidden' in r.data, '/winner abierta: vuelve a votar y no muestra organización')
chequear(b'const ABIERTA = true' in cliente.get('/').data, 'GET / sabe que la votación está abierta')
chequear(cliente.get('/login').status_code == 200, '/login renderiza')

# ---------- Webhook ----------
def update(texto, usuario, chat_id=-100, tipo='supergroup'):
    return {'update_id': 1, 'message': {'message_id': 5, 'from': usuario, 'chat': {'id': chat_id, 'type': tipo}, 'text': texto}}
SECRETO = {'X-Telegram-Bot-Api-Secret-Token': 'secreto-test'}

chequear(cliente.post('/telegram/webhook', json=update('/votacion', ADMIN)).status_code == 403, 'webhook sin secreto -> 403')
chequear(cliente.post('/telegram/webhook', json=update('/votacion', ADMIN), headers={'X-Telegram-Bot-Api-Secret-Token': 'mal'}).status_code == 403, 'webhook con secreto incorrecto -> 403')

llamadas.clear()
cliente.post('/telegram/webhook', json=update('/votacion', ANA), headers=SECRETO)
chequear(llamadas and 'Solo quien organiza' in llamadas[0][1]['text'], '/votacion de alguien que no organiza se rechaza')

llamadas.clear()
cliente.post('/telegram/webhook', json=update('/votacion@ClubTestBot', ADMIN, chat_id=-200), headers=SECRETO)
metodos = [m for m, _ in llamadas]
chequear(metodos == ['sendMessage', 'pinChatMessage'], f'/votacion publica y fija la tarjeta: {metodos}')
tarjeta = llamadas[0][1]
chequear(tarjeta['reply_markup']['inline_keyboard'][0][0]['url'] == 'https://t.me/ClubTestBot?startapp', 'el botón de la tarjeta abre la Main Mini App')
print('     tarjeta:', repr(tarjeta['text']))
chequear(votos.leer_estado() == {'abierta': True, 'chat_id': -200, 'message_id': 77}, 'estado guardado con la tarjeta nueva')

llamadas.clear()
cliente.post('/telegram/webhook', json=update('/votacion@OtroBot', ADMIN), headers=SECRETO)
chequear(not llamadas, 'comandos para otro bot se ignoran')

llamadas.clear()
cliente.post('/telegram/webhook', json=update('/miid', ANA, chat_id=222, tipo='private'), headers=SECRETO)
chequear(llamadas and 'Tu id de Telegram es 222' in llamadas[0][1]['text'], '/miid responde el id')

llamadas.clear()
cliente.post('/telegram/webhook', json=update('/start', ANA, chat_id=222, tipo='private'), headers=SECRETO)
chequear(llamadas and llamadas[0][1]['reply_markup']['inline_keyboard'][0][0]['web_app']['url'] == 'https://tupac.pythonanywhere.com/', '/start en privado manda el botón web_app')

llamadas.clear()
cliente.post('/telegram/webhook', json=update('/cerrar', ADMIN, chat_id=-200), headers=SECRETO)
metodos = [m for m, _ in llamadas]
chequear(metodos == ['sendMessage', 'editMessageText'], f'/cerrar anuncia y cierra la tarjeta: {metodos}')
print('     anuncio:\n' + '\n'.join('       ' + l for l in llamadas[0][1]['text'].splitlines()))
print('     tarjeta cerrada:', repr(llamadas[1][1]['text']))
chequear('Empataron' in llamadas[0][1]['text'] and 'ganó' not in llamadas[1][1]['text'], 'dos votos opuestos: empate, sin ganador en la tarjeta')
boton_cerrada = llamadas[1][1]['reply_markup']['inline_keyboard'][0][0]
chequear(boton_cerrada['text'] == '🏆 Ver el resultado' and boton_cerrada['url'] == 'https://t.me/ClubTestBot?startapp', 'la tarjeta cerrada lleva al resultado')
chequear(votos.votacion_abierta() is False, 'la votación queda cerrada')
chequear(b'const ABIERTA = false' in cliente.get('/').data, 'GET / sabe que cerró (y la página lleva al resultado)')
r = cliente.get('/winner')
chequear(r.status_code == 200 and b'Duelos mano a mano' in r.data and b'Tu boleta' in r.data, 'cerrada: cualquiera ve el resultado completo y su boleta')
chequear('Quiénes votaron'.encode() in r.data and b'Ana O Brien x' in r.data and b'[tg:' not in r.data, 'cerrada: el resultado también lista quiénes votaron')
chequear(b'data-volver' not in r.data, 'cerrada: el resultado es la pantalla de inicio, sin Atrás')
chequear(b'id="barra-admin" hidden' in r.data, 'cerrada: quien no organiza no ve la organización')
chequear(b'Reabrir la votaci' in admin.get('/winner').data, 'cerrada: el admin puede reabrir desde el resultado')
r = cliente.post('/submit', json={'orderedList': orden}, headers=tma({'id': 444, 'first_name': 'Beto'}))
chequear(r.status_code == 409 and r.json.get('cerrada'), '/submit con la votación cerrada -> 409')
r = cliente.post('/sesion-telegram', headers=tma({'id': 444, 'first_name': 'Beto'}))
chequear(r.json['abierta'] is False, '/sesion-telegram avisa que cerró')

# /cerrar con data.txt vacío
open(votos.RUTA_VOTOS, 'w').close()
llamadas.clear()
cliente.post('/telegram/webhook', json=update('/cerrar', ADMIN), headers=SECRETO)
chequear(llamadas and 'Todavía no votó nadie' in llamadas[0][1]['text'], '/cerrar sin votos lo dice')
chequear(admin.get('/winner').status_code == 200, '/winner con data.txt vacío no falla')

# /votacion reabre
cliente.post('/telegram/webhook', json=update('/votacion', ADMIN), headers=SECRETO)
chequear(votos.votacion_abierta() is True, '/votacion reabre la votación')

# ---------- Cerrar y reabrir desde la página de resultados ----------
def cambiar_estado(abierta, quien=None, cliente_http=None):
    return (cliente_http or app.test_client()).post('/estado-votacion', json={'abierta': abierta},
                                                    headers=tma(quien) if quien else {})

chequear(cambiar_estado(False).status_code == 403, '/estado-votacion sin identidad -> 403')
chequear(cambiar_estado(False, ANA).status_code == 403, '/estado-votacion de quien no organiza -> 403')
chequear(app.test_client().post('/estado-votacion', json={'abierta': 'no'}, headers=tma(ADMIN)).status_code == 400, '/estado-votacion con datos inválidos -> 400')
r = cambiar_estado(False, ADMIN)
chequear(r.status_code == 409 and 'Todavía no votó nadie' in r.json['message'] and votos.votacion_abierta(), 'no se puede cerrar sin votos')

with open(votos.RUTA_VOTOS, 'w', encoding='utf-8') as f:
    for i, orden_i in enumerate([orden, orden, list(reversed(orden))]):
        f.write(f"Nombre: Persona {i} [tg:{i + 500}]; Lista: {orden_i}; fecha: 2026-11-20 21:0{i}:00\n")
chequear(b'Cerrar la votaci' in admin.get('/winner').data, 'abierta: el admin ve el botón para cerrar')

llamadas.clear()
r = cambiar_estado(False, ADMIN)  # admin por initData, sin cookie (como en Telegram Web)
metodos = [m for m, _ in llamadas]
chequear(r.status_code == 200 and r.json['abierta'] is False and not votos.votacion_abierta(), f'el admin cierra desde la app: {r.json}')
chequear(metodos == ['sendMessage', 'editMessageText'] and llamadas[0][1]['chat_id'] == -100 and 'Ganó Rayuela' in llamadas[0][1]['text'],
         f'al cerrar desde la app, el bot anuncia en el grupo de la tarjeta: {metodos}')
llamadas.clear()
r = cambiar_estado(False, cliente_http=admin)  # admin por cookie
chequear(r.status_code == 200 and 'ya estaba cerrada' in r.json['message'] and not llamadas, 'cerrar dos veces no anuncia de nuevo')
r = cliente.get('/winner')
chequear(b'Duelos mano a mano' in r.data and 'Rayuela</div>'.encode() in r.data, 'cerrada desde la app: el resultado es público')

llamadas.clear()
r = cambiar_estado(True, ADMIN)
chequear(r.status_code == 200 and votos.votacion_abierta(), 'el admin reabre desde la app')
chequear([m for m, _ in llamadas] == ['editMessageText'] and llamadas[0][1]['reply_markup']['inline_keyboard'][0][0]['text'] == '🗳️ Votar',
         'al reabrir, la tarjeta vuelve a tener el botón Votar')
chequear(b'Duelos mano a mano' not in cliente.get('/winner').data, 'reabierta: el resultado se oculta otra vez')

# Sin tarjeta publicada, cerrar desde la app avisa que no pudo anunciar
votos.guardar_estado({'abierta': True})
llamadas.clear()
r = cambiar_estado(False, ADMIN)
chequear(r.status_code == 200 and 'No pude avisar en el grupo' in r.json['message'] and not llamadas, 'sin tarjeta: cierra y avisa que no anunció')
votos.guardar_estado({'abierta': True})

# ---------- Anuncio sin ganador estricto (ciclo A>B>C>A) ----------
from app.voting_condorcet import condorcet_winner  # noqa: E402
ciclo = condorcet_winner([['A', 'B', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B']])
texto = telegram_bot.texto_anuncio(ciclo, 3)
print('     anuncio en ciclo:\n' + '\n'.join('       ' + l for l in texto.splitlines()))
chequear('Empataron A, B y C' in texto and 'Ganó' not in texto, 'ciclo perfecto: anuncia empate, no un ganador')
fuerte = condorcet_winner([['A', 'B', 'C'], ['A', 'C', 'B'], ['B', 'A', 'C']])
texto = telegram_bot.texto_anuncio(fuerte, 3)
chequear(texto.startswith('🏆 Ganó A.\nLe ganó el mano a mano'), 'ganador de Condorcet estricto')
chequear(telegram_bot.texto_tarjeta(['Ana'], abierta=False, ganador=None) == '📚 La votación terminó. Votaron 1 persona.', 'tarjeta cerrada sin ganador')

# ---------- Scripts de conteo con marcas [tg:id] ----------
carpeta = os.path.join(tmp, 'scripts', 'app', 'data')
os.makedirs(carpeta)
with open(os.path.join(carpeta, 'data.txt'), 'w', encoding='utf-8') as f:
    for i, orden_i in enumerate([orden, orden, list(reversed(orden))]):
        f.write(f"Nombre: Persona {i} [tg:{i}]; Lista: {orden_i}; fecha: 2026-11-20 21:0{i}:00\n")
for script in ['voting_condorcet.py', 'voting_irv.py']:
    p = subprocess.run([sys.executable, os.path.join(REPO, 'app', script)], cwd=os.path.join(tmp, 'scripts'),
                       capture_output=True, text=True, encoding='utf-8')
    salida = (p.stdout + p.stderr).strip().splitlines()
    chequear(p.returncode == 0, f'{script} corre con marcas [tg:id]: {salida[-1] if salida else ""}')

# ---------- Reintentos ante fallas de red (el proxy de PythonAnywhere a veces responde 503) ----------
import io  # noqa: E402
import urllib.error  # noqa: E402
import urllib.request  # noqa: E402

urlopen_original, sleep_original = urllib.request.urlopen, telegram_bot.time.sleep
intentos = []

def falla_dos_veces(pedido, timeout=None):
    intentos.append(1)
    if len(intentos) < 3:
        raise urllib.error.URLError('Tunnel connection failed: 503 Service Unavailable')
    return io.BytesIO(b'{"ok": true, "result": {"message_id": 1}}')

def falla_siempre(pedido, timeout=None):
    intentos.append(1)
    raise urllib.error.URLError('Tunnel connection failed: 503 Service Unavailable')

def telegram_dice_400(pedido, timeout=None):
    intentos.append(1)
    raise urllib.error.HTTPError(pedido.full_url, 400, 'Bad Request', {},
                                 io.BytesIO(b'{"ok": false, "description": "Bad Request: chat not found"}'))

telegram_bot.time.sleep = lambda segundos: None
try:
    with app.app_context():
        urllib.request.urlopen = falla_dos_veces
        chequear(LLAMAR_REAL('getMe') == {'message_id': 1} and len(intentos) == 3, 'reintenta si el proxy falla y después anda')
        intentos.clear()
        urllib.request.urlopen = falla_siempre
        chequear(LLAMAR_REAL('getMe') is None and len(intentos) == telegram_bot.INTENTOS, 'se rinde después de los reintentos sin lanzar')
        intentos.clear()
        urllib.request.urlopen = telegram_dice_400
        chequear(LLAMAR_REAL('sendMessage', {'chat_id': 1, 'text': 'x'}) is None and len(intentos) == 1, 'no reintenta los errores que responde Telegram')
finally:
    urllib.request.urlopen, telegram_bot.time.sleep = urlopen_original, sleep_original

shutil.rmtree(tmp, ignore_errors=True)
print()
print('TODO BIEN' if not fallas else f'{len(fallas)} FALLAS: {fallas}')
sys.exit(1 if fallas else 0)
