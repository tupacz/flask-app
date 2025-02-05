import os
from flask import Blueprint, render_template, request, jsonify
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
    books_dao = Book.BooksDAO(file_path_books)
    return render_template('index.html', books=books_dao.load_books())

@main.route('/books-manager')
def books_manager():
    books_dao = Book.BooksDAO(file_path_books)
    return render_template('books-manager.html', books=books_dao.load_books())

@main.route('/winner')
def winner():
    winner = get_condorcet_winner(file_path_data)
    return render_template('winner.html', winner=winner)

@main.route('/votes')
def votes():
    # obtengo todo un string de data.txt
    with open(file_path_data, 'r', encoding='utf-8') as file:
        data = file.read()
    return render_template('votes.html', data=data, password='1234')


@main.route('/submit-data', methods=['POST'])
def cambiar_data():
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
                    raise Exception(f"{search_string} ya votó.")
                else:
                    print(f"'{search_string}' not found in file.")

                file.write(f"Nombre: {name}; Lista: {ordered_list}; fecha: {fechahora}\n")
        except Exception as e:
            return (jsonify({'message': f'Error al guardar los datos: {str(e)}'}), 500)
        
    return jsonify({'message': 'Datos guardados correctamente'}), 200

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
