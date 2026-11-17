"""El bot del grupo: publica la tarjeta para votar, la actualiza y anuncia el ganador.

Telegram manda cada mensaje al webhook (/telegram/webhook) y este módulo responde
llamando a la Bot API con urllib, sin bibliotecas extra.
Referencia: https://core.telegram.org/bots/api
"""
import json
import urllib.error
import urllib.request

from flask import current_app

try:
    from app import votos
    from app.voting_condorcet import get_condorcet_winner
except ImportError:
    import votos
    from voting_condorcet import get_condorcet_winner


def llamar(metodo, params=None, token=None):
    """Llama a un método de la Bot API. Devuelve 'result' o None si algo falla. Nunca lanza."""
    token = token or current_app.config.get('BOT_TOKEN')
    if not token:
        print(f"Telegram {metodo}: falta configurar el token del bot")
        return None
    pedido = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/{metodo}",
        data=json.dumps(params or {}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
    )
    try:
        with urllib.request.urlopen(pedido, timeout=5) as respuesta:
            datos = json.load(respuesta)
    except urllib.error.HTTPError as e:
        try:
            datos = json.load(e)
        except Exception:
            datos = {'ok': False, 'description': str(e)}
    except Exception as e:
        print(f"Telegram {metodo}: {e}")
        return None
    if not datos.get('ok'):
        print(f"Telegram {metodo}: {datos.get('description')}")
        return None
    return datos.get('result')


# ---------- Textos ----------

def unir_nombres(nombres):
    """['Ana', 'Beto', 'Caro'] -> 'Ana, Beto y Caro'"""
    if len(nombres) <= 1:
        return ''.join(nombres)
    return ', '.join(nombres[:-1]) + ' y ' + nombres[-1]


def _personas(cantidad):
    return f"{cantidad} {'persona' if cantidad == 1 else 'personas'}"


def texto_tarjeta(nombres, abierta=True, ganador=None):
    if not abierta:
        texto = f"📚 La votación terminó. Votaron {_personas(len(nombres))}"
        return texto + (f" y ganó {ganador} 🏆" if ganador else ".")
    texto = ("📚 Elegimos el próximo libro del club.\n"
             "Tocá Votar y ordená los libros, del que más querés leer al que menos.\n\n")
    if not nombres:
        return texto + "Todavía no votó nadie."
    if len(nombres) == 1:
        return texto + f"Ya votó {nombres[0]}."
    return texto + f"Ya votaron {len(nombres)} personas: {unir_nombres(nombres)}."


def boton_votar():
    usuario_bot = current_app.config.get('BOT_USERNAME')
    if not usuario_bot:
        return None
    return {'inline_keyboard': [[{'text': '🗳️ Votar', 'url': f"https://t.me/{usuario_bot}?startapp"}]]}


def definir_ganador(resultado):
    """(ganador, empatados). Si el desempate por votos también empata, no hay ganador:
    condorcet_winner elegiría al primero de la lista, que no dice nada sobre las preferencias."""
    candidatos = resultado.get('candidatos') or []
    if not candidatos:
        return None, []
    duelos = resultado.get('duelos_ganados') or [0] * len(candidatos)
    matriz = resultado.get('get_votes') or [[0] * len(candidatos) for _ in candidatos]
    maximo = max(duelos)
    empatados = [i for i, ganados in enumerate(duelos) if ganados == maximo]
    if len(empatados) > 1:
        sumas = {i: sum(matriz[i]) for i in empatados}
        mejor = max(sumas.values())
        finalistas = [candidatos[i] for i in empatados if sumas[i] == mejor]
        if len(finalistas) > 1:
            return None, finalistas
    return (resultado.get('ganador_condorcet') or None), []


def texto_anuncio(resultado, cantidad_votos):
    candidatos = resultado.get('candidatos') or []
    duelos = resultado.get('duelos_ganados') or [0] * len(candidatos)
    total = max(len(candidatos) - 1, 0)
    ganador, empatados = definir_ganador(resultado)

    lineas = []
    if ganador:
        lineas.append(f"🏆 Ganó {ganador}.")
        if duelos[candidatos.index(ganador)] == total:
            lineas.append("Le ganó el mano a mano a todos los demás libros.")
        elif duelos.count(max(duelos)) > 1:
            lineas.append("Ningún libro le ganó a todos. Hubo empate en duelos ganados "
                          "y se desempató por la cantidad de votos en esos duelos.")
        else:
            lineas.append("Ningún libro le ganó a todos, así que ganó el que se impuso en más duelos.")
    elif empatados:
        lineas.append(f"🤝 Empataron {unir_nombres(empatados)}.")
        lineas.append("Quedaron iguales en duelos ganados y también en votos. Hace falta desempatar entre esos libros.")
    else:
        lineas.append("No hubo un ganador claro. Quien organiza puede ver la tabla completa para decidir.")

    lineas.append("")
    lineas.append("Duelos ganados por cada libro:")
    for titulo, ganados in sorted(zip(candidatos, duelos), key=lambda par: -par[1]):
        lineas.append(f"{titulo}: {ganados} de {total}")
    lineas.append("")
    lineas.append(f"Votaron {_personas(cantidad_votos)}.")
    return "\n".join(lineas)


# ---------- Tarjeta del grupo ----------

def actualizar_tarjeta(nombres, abierta=True, ganador=None):
    """Edita la tarjeta publicada con /votacion. Si no hay tarjeta o falla, no pasa nada."""
    estado = votos.leer_estado()
    if not estado.get('chat_id') or not estado.get('message_id'):
        return
    params = {
        'chat_id': estado['chat_id'],
        'message_id': estado['message_id'],
        'text': texto_tarjeta(nombres, abierta, ganador),
    }
    if abierta and boton_votar():
        params['reply_markup'] = boton_votar()
    llamar('editMessageText', params)


# ---------- Comandos ----------

def _responder(mensaje, texto, **extra):
    params = {
        'chat_id': mensaje['chat']['id'],
        'text': texto,
        'reply_parameters': {'message_id': mensaje['message_id'], 'allow_sending_without_reply': True},
    }
    params.update(extra)
    return llamar('sendMessage', params)


def _abrir_votacion(mensaje):
    if mensaje['chat'].get('type') == 'private':
        _responder(mensaje, "Este comando se usa en el grupo del club, así la tarjeta para votar queda ahí.")
        return
    params = {'chat_id': mensaje['chat']['id'], 'text': texto_tarjeta(votos.nombres_de_votantes())}
    if boton_votar():
        params['reply_markup'] = boton_votar()
    tarjeta = llamar('sendMessage', params)
    if not tarjeta:
        return
    estado = votos.leer_estado()
    estado.update({'abierta': True, 'chat_id': tarjeta['chat']['id'], 'message_id': tarjeta['message_id']})
    votos.guardar_estado(estado)
    # Solo funciona si el bot es admin del grupo con permiso para fijar mensajes
    llamar('pinChatMessage', {'chat_id': tarjeta['chat']['id'], 'message_id': tarjeta['message_id'],
                              'disable_notification': True})


def _cerrar_votacion(mensaje):
    nombres = votos.nombres_de_votantes()
    if not nombres:
        _responder(mensaje, "Todavía no votó nadie, así que no hay nada que cerrar.")
        return
    try:
        resultado = get_condorcet_winner(votos.RUTA_VOTOS)
    except Exception as e:
        print(f"No se pudo contar los votos: {e}")
        _responder(mensaje, "No pude contar los votos. Revisá el archivo de votos desde la página de admin.")
        return

    estado = votos.leer_estado()
    estado['abierta'] = False
    votos.guardar_estado(estado)

    ganador, _ = definir_ganador(resultado)
    anuncio = texto_anuncio(resultado, len(nombres))
    chat_tarjeta = estado.get('chat_id')
    if chat_tarjeta and chat_tarjeta != mensaje['chat']['id']:
        llamar('sendMessage', {'chat_id': chat_tarjeta, 'text': anuncio})
        _responder(mensaje, "Listo, cerré la votación y anuncié el resultado en el grupo.")
    else:
        _responder(mensaje, anuncio)
    actualizar_tarjeta(nombres, abierta=False, ganador=ganador)


def _bienvenida(mensaje):
    url = current_app.config.get('SITE_URL', '') + '/'
    _responder(mensaje, "¡Hola! Acá se vota el próximo libro del club. Tocá el botón para abrir la votación.",
               reply_markup={'inline_keyboard': [[{'text': '📚 Abrir votación', 'web_app': {'url': url}}]]})


def procesar_update(update):
    """Atiende un update que Telegram manda al webhook. Solo reacciona a comandos."""
    mensaje = update.get('message') or {}
    texto = mensaje.get('text') or ''
    if not texto.startswith('/') or 'chat' not in mensaje:
        return

    comando, _, destinatario = texto.split()[0][1:].partition('@')
    usuario_bot = current_app.config.get('BOT_USERNAME') or ''
    if destinatario and destinatario.lower() != usuario_bot.lower():
        return  # es un comando para otro bot del grupo
    comando = comando.lower()

    usuario = mensaje.get('from') or {}
    es_admin = usuario.get('id') in current_app.config.get('ADMIN_TELEGRAM_IDS', set())

    if comando == 'start':
        if mensaje['chat'].get('type') == 'private':
            _bienvenida(mensaje)
    elif comando == 'miid':
        _responder(mensaje, f"Tu id de Telegram es {usuario.get('id')}. "
                            "Si organizás la votación, tiene que estar en admin_ids.txt del servidor.")
    elif comando in ('votacion', 'cerrar'):
        if not es_admin:
            _responder(mensaje, "Solo quien organiza la votación puede hacer eso.")
        elif comando == 'votacion':
            _abrir_votacion(mensaje)
        else:
            _cerrar_votacion(mensaje)
