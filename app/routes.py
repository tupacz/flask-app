import os
import hmac
import random
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, current_app
from datetime import datetime

from app.voting_condorcet import get_condorcet_winner

try:
    from app import voting_condorcet
    from app import Book
except ImportError:
    import voting_condorcet
    import Book

# Crear un Blueprint
main = Blueprint('main', __name__)

books = [ Book.Book("Cien años de soledad", "Gabriel García Márquez", "La obra cumbre del realismo mágico que consolidó a García Márquez como una figura central de la literatura mundial.")
    ]


# Construir una ruta absoluta al archivo
base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene la carpeta actual
file_path_data = os.path.join(base_dir, 'data', 'data.txt')
file_path_books = os.path.join(base_dir, 'data', 'books.json')

# Ruta para la página principal
@main.route('/')
def index():
    books_to_send = Book.BooksDAO(file_path_books).load_books()
    random.shuffle(books_to_send)
    return render_template('index.html', books=books_to_send)

@main.route('/books-manager')
def books_manager():
    books_dao = Book.BooksDAO(file_path_books)
    return render_template('books-manager.html', books=books_dao.load_books())

def es_admin():
    return session.get('admin') is True

def nombres_de_votantes(ruta_archivo):
    """Nombres de quienes ya votaron, en el orden en que votaron."""
    nombres = []
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        for linea in file:
            if linea.startswith('Nombre: '):
                nombres.append(linea.split('; ')[0][len('Nombre: '):].strip())
    return nombres

# Páginas a las que se puede volver después de ingresar como admin
DESTINOS_ADMIN = {'/votes', '/winner'}

@main.route('/winner')
def winner():
    nombres = nombres_de_votantes(file_path_data)
    if not es_admin() or not nombres:
        # El público solo ve quién votó; el resultado completo es solo para el admin
        return render_template('winner_publico.html', nombres=nombres, admin=es_admin())
    winner = get_condorcet_winner(file_path_data)
    return render_template('winner.html', winner=winner, cantidad_votos=len(nombres))

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
    with open(file_path_data, 'r', encoding='utf-8') as file:
        data = file.read()
    return render_template('votes.html', data=data)


@main.route('/submit-data', methods=['POST'])
def cambiar_data():
    if not es_admin():
        return jsonify({'message': 'Solo el admin puede cambiar los votos. Ingresá de nuevo en /votes.'}), 403
    try:
        data = request.get_json()
        print('JSON recibido:', data)  # Imprime el JSON recibido
    except Exception as e:
        return jsonify({'message': f'Error al procesar JSON: {str(e)}'}), 400
    
    with open(file_path_data, 'w', encoding='utf-8') as file:
        file.write(data)

    return jsonify({'message': 'Datos guardados correctamente'}), 200

@main.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        print('JSON recibido:', data)  # Imprime el JSON recibido
    except Exception as e:
        return jsonify({'message': f'Error al procesar JSON: {str(e)}'}), 400

    if not data or 'name' not in data or 'orderedList' not in data:
        return jsonify({'message': 'Datos inválidos'}), 400

    name = data['name']
    ordered_list = data['orderedList']
    fechahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if name != 'kek':
        try:
            with open(file_path_data, 'a+', encoding='utf-8') as file:
                file.seek(0)  # Move the cursor to the beginning of the file
                file_contents = file.read()
                
                search_string = name
                if search_string in file_contents:
                    fecha_previa = buscar_fecha_de_voto(file_contents, name)
                    if fecha_previa:
                        mensaje = f"{name.strip()} ya votó el {fecha_legible(fecha_previa)}. Si sos otra persona, probá con otro nombre (por ejemplo, sumando tu apellido)."
                    else:
                        mensaje = f'El nombre "{name.strip()}" ya figura en los votos. Probá con otro nombre (por ejemplo, sumando tu apellido).'
                    return jsonify({'message': mensaje, 'yaVoto': True, 'fecha': fecha_previa}), 409
                else:
                    print(f"'{search_string}' not found in file.")

                file.write(f"Nombre: {name}; Lista: {ordered_list}; fecha: {fechahora}\n")
        except Exception as e:
            return (jsonify({'message': f'Error al guardar los datos: {str(e)}'}), 500)

    return jsonify({'message': 'Datos guardados correctamente', 'fecha': fechahora}), 200

def buscar_fecha_de_voto(contenido, nombre):
    """Devuelve la fecha del voto cuyo nombre coincide exactamente (sin importar mayúsculas ni espacios), o None."""
    buscado = nombre.strip().lower()
    for linea in contenido.splitlines():
        if not linea.startswith('Nombre: ') or 'fecha: ' not in linea:
            continue
        nombre_linea = linea.split('; ')[0][len('Nombre: '):]
        if nombre_linea.strip().lower() == buscado:
            return linea.rsplit('fecha: ', 1)[1].strip()
    return None

def fecha_legible(fecha):
    """'2026-06-28 22:35:19' -> '28/06 a las 22:35'"""
    try:
        d = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        return f"{d:%d/%m} a las {d:%H:%M}"
    except ValueError:
        return fecha

@main.route('/submit-book', methods=['POST'])
def submit_books():
    try:
        data = request.get_json()
        print('JSON recibido:', data)  # Imprime el JSON recibido
    except Exception as e:
        return jsonify({'message': f'Error al procesar JSON: {str(e)}'}), 400
    
    # Data es un array que contiene diccionarios con los datos del libro
    books2 = []
    for book in data:
        if 'title' not in book or 'author' not in book or 'description' not in book:
            return jsonify({'message': 'Datos inválidos'}), 400
        title = book['title']
        author = book['author']
        description = book['description']
        books2.append(Book.Book(title, author, description))

    books_dao = Book.BooksDAO(file_path_books)
    books_dao.save_books(books=books2)
    
    return jsonify({'message': 'Datos guardados correctamente'}), 200
