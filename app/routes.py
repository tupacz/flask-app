import hmac
import random
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, current_app
from datetime import datetime

from app.voting_condorcet import get_condorcet_winner

try:
    from app import Book
    from app import votos
    from app import telegram_bot
    from app.telegram_auth import usuario_de_request, es_admin_telegram, nombre_para_guardar
except ImportError:
    import Book
    import votos
    import telegram_bot
    from telegram_auth import usuario_de_request, es_admin_telegram, nombre_para_guardar

# Crear un Blueprint
main = Blueprint('main', __name__)


# Ruta para la página principal: la Mini App de votación
@main.route('/')
def index():
    books_to_send = Book.BooksDAO(votos.RUTA_LIBROS).load_books()
    random.shuffle(books_to_send)
    return render_template('index.html', books=books_to_send,
                           bot_username=current_app.config.get('BOT_USERNAME'))

def es_admin():
    return session.get('admin') is True

# Páginas a las que se puede volver después de ingresar como admin
DESTINOS_ADMIN = {'/votes', '/winner', '/books-manager'}

@main.route('/books-manager')
def books_manager():
    if not es_admin():
        return render_template('login.html', error=None, next='/books-manager')
    books_dao = Book.BooksDAO(votos.RUTA_LIBROS)
    return render_template('books-manager.html', books=books_dao.load_books())

@main.route('/winner')
def winner():
    nombres = votos.nombres_de_votantes()
    if not es_admin() or not nombres:
        # El público solo ve quién votó; el resultado completo es solo para el admin
        return render_template('winner_publico.html', nombres=nombres, admin=es_admin())
    winner = get_condorcet_winner(votos.RUTA_VOTOS)
    ganador, empatados = telegram_bot.definir_ganador(winner)
    return render_template('winner.html', winner=winner, ganador=ganador, empatados=empatados,
                           cantidad_votos=len(nombres), abierta=votos.votacion_abierta())

@main.route('/login', methods=['GET', 'POST'])
def login():
    destino = request.values.get('next', '/votes')
    if destino not in DESTINOS_ADMIN:
        destino = '/votes'
    if request.method == 'GET':
        if es_admin():
            return redirect(destino)
        return render_template('login.html', error=None, next=destino)

    clave = current_app.config.get('ADMIN_PASSWORD')
    ingresada = request.form.get('password', '')
    if clave and hmac.compare_digest(ingresada.encode('utf-8'), clave.encode('utf-8')):
        session.clear()
        session['admin'] = True
        session.permanent = True
        return redirect(destino)
    error = 'Contraseña incorrecta.' if clave else 'Falta configurar la contraseña de admin en el servidor.'
    return render_template('login.html', error=error, next=destino), 401

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@main.route('/votes')
def votes():
    if not es_admin():
        return render_template('login.html', error=None, next='/votes')
    # obtengo todo un string de data.txt
    with open(votos.RUTA_VOTOS, 'r', encoding='utf-8') as file:
        data = file.read()
    return render_template('votes.html', data=data)


@main.route('/submit-data', methods=['POST'])
def cambiar_data():
    if not es_admin():
        return jsonify({'message': 'Solo el admin puede cambiar los votos. Ingresá de nuevo en /votes.'}), 403
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'message': f'Error al procesar JSON: {str(e)}'}), 400
    if not isinstance(data, str):
        return jsonify({'message': 'Datos inválidos'}), 400

    with open(votos.RUTA_VOTOS, 'w', encoding='utf-8') as file:
        file.write(data)

    return jsonify({'message': 'Cambios guardados.'}), 200


def _voto_para_mostrar(voto):
    return {'lista': voto['lista'], 'fecha': voto['fecha']} if voto else None

def _saludo(usuario):
    return (usuario.get('first_name') or '').strip() or nombre_para_guardar(usuario)

MENSAJE_SIN_IDENTIDAD = 'No pudimos confirmar quién sos. Cerrá la votación y volvé a abrirla desde Telegram.'

@main.route('/sesion-telegram', methods=['POST'])
def sesion_telegram():
    """Al abrir la Mini App: quién es, si ya votó, si la votación sigue abierta y si organiza."""
    usuario = usuario_de_request()
    if not usuario:
        return jsonify({'message': MENSAJE_SIN_IDENTIDAD}), 401
    admin = es_admin_telegram(usuario)
    if admin:
        # Misma sesión que el login con contraseña: habilita /winner, /votes y /books-manager
        session['admin'] = True
        session.permanent = True
    return jsonify({
        'nombre': _saludo(usuario),
        'voto': _voto_para_mostrar(votos.voto_de(usuario['id'])),
        'abierta': votos.votacion_abierta(),
        'esAdmin': admin,
    })

@main.route('/submit', methods=['POST'])
def submit():
    usuario = usuario_de_request()
    if not usuario:
        return jsonify({'message': MENSAJE_SIN_IDENTIDAD}), 401

    data = request.get_json(silent=True)
    ordered_list = data.get('orderedList') if isinstance(data, dict) else None
    if not isinstance(ordered_list, list) or not all(isinstance(t, str) for t in ordered_list):
        return jsonify({'message': 'Datos inválidos'}), 400

    if not votos.votacion_abierta():
        return jsonify({'message': 'La votación ya cerró.', 'cerrada': True}), 409

    titulos = [book.title for book in Book.BooksDAO(votos.RUTA_LIBROS).load_books()]
    if sorted(ordered_list) != sorted(titulos):
        return jsonify({'message': 'La lista de libros cambió mientras votabas. '
                                   'Cerrá la votación y volvé a abrirla para ver la lista nueva.'}), 400

    previo = votos.voto_de(usuario['id'])
    if previo:
        return jsonify({'message': f"Ya votaste el {fecha_legible(previo['fecha'])}.",
                        'yaVoto': True, 'voto': _voto_para_mostrar(previo)}), 409

    fechahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        votos.agregar_voto(nombre_para_guardar(usuario), usuario['id'], ordered_list, fechahora)
    except Exception as e:
        return jsonify({'message': f'Error al guardar el voto: {str(e)}'}), 500

    # La tarjeta del grupo muestra quién votó. Si Telegram no responde, el voto igual quedó guardado.
    telegram_bot.actualizar_tarjeta(votos.nombres_de_votantes())
    voto = {'lista': ordered_list, 'fecha': fechahora}
    return jsonify({'message': 'Voto guardado', 'fecha': fechahora, 'voto': voto}), 200

@main.route('/telegram/webhook', methods=['POST'])
def telegram_webhook():
    secreto = current_app.config.get('WEBHOOK_SECRET') or ''
    recibido = request.headers.get('X-Telegram-Bot-Api-Secret-Token', '')
    if not secreto or not hmac.compare_digest(recibido.encode('utf-8'), secreto.encode('utf-8')):
        return jsonify({'ok': False}), 403
    try:
        telegram_bot.procesar_update(request.get_json(silent=True) or {})
    except Exception as e:
        # Si respondemos error, Telegram reintenta el mismo update una y otra vez
        print(f"Error procesando update de Telegram: {e}")
    return jsonify({'ok': True})

def fecha_legible(fecha):
    """'2026-06-28 22:35:19' -> '28/06 a las 22:35'"""
    try:
        d = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        return f"{d:%d/%m} a las {d:%H:%M}"
    except ValueError:
        return fecha

@main.route('/submit-book', methods=['POST'])
def submit_books():
    if not es_admin():
        return jsonify({'message': 'Solo el admin puede cambiar los libros.'}), 403
    data = request.get_json(silent=True)
    if not isinstance(data, list):
        return jsonify({'message': 'Datos inválidos'}), 400

    # Data es un array que contiene diccionarios con los datos del libro
    books2 = []
    for book in data:
        if not isinstance(book, dict) or 'title' not in book or 'author' not in book or 'description' not in book:
            return jsonify({'message': 'Datos inválidos'}), 400
        title = str(book['title']).strip()
        author = str(book['author']).strip()
        description = str(book['description']).strip()
        if not title:
            return jsonify({'message': 'Hay un libro sin título.'}), 400
        books2.append(Book.Book(title, author, description))

    if len({b.title for b in books2}) != len(books2):
        return jsonify({'message': 'Hay dos libros con el mismo título.'}), 400

    books_dao = Book.BooksDAO(votos.RUTA_LIBROS)
    books_dao.save_books(books=books2)

    return jsonify({'message': 'Libros guardados.'}), 200
