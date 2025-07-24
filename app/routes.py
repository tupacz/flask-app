import os
import random
from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime

from app.voting_condorcet import get_condorcet_winner, condorcet_winner
from app.telegram_auth import validate_telegram_data, get_user_name
from app.voting_manager import VotingManager

try:
    from app import voting_condorcet
    from app import Book
except ImportError:
    import voting_condorcet
    import Book

# Crear un Blueprint
main = Blueprint('main', __name__)

# Inicializar el gestor de votaciones
voting_manager = VotingManager('votes.json')

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

# Nueva ruta para Telegram Mini App
@main.route('/telegram')
def telegram_app():
    books_to_send = Book.BooksDAO(file_path_books).load_books()
    random.shuffle(books_to_send)
    return render_template('telegram_index.html', books=books_to_send)

# Nuevas rutas específicas para Telegram Mini App
@main.route('/telegram-winner')
def telegram_winner():
    # Obtener todos los rankings para el cálculo de Condorcet
    rankings = voting_manager.get_rankings_for_condorcet()
    
    if not rankings:
        return render_template('telegram_winner.html', 
                             winner="No hay votos aún", 
                             total_votes=0)
    
    # Usar el sistema de votación Condorcet existente
    try:
        # Usar la función condorcet_winner directamente con los rankings
        winner_result = condorcet_winner(rankings)
        total_votes = voting_manager.get_vote_count()
        
        return render_template('telegram_winner.html', 
                             winner=winner_result, 
                             total_votes=total_votes,
                             telegram_votes=voting_manager.get_telegram_votes_count(),
                             web_votes=voting_manager.get_web_votes_count())
    except Exception as e:
        print(f"Error calculando ganador: {e}")
        return render_template('telegram_winner.html', 
                             winner="Error calculando resultado", 
                             total_votes=voting_manager.get_vote_count())

@main.route('/telegram-books')
def telegram_books():
    books_dao = Book.BooksDAO(file_path_books)
    return render_template('telegram_books.html', books=books_dao.load_books())

# Endpoint para validar autenticación de Telegram
@main.route('/telegram-auth', methods=['POST'])
def telegram_auth():
    try:
        data = request.get_json()
        init_data = data.get('initData')
        
        if not init_data:
            return jsonify({'valid': False, 'error': 'No init data provided'}), 400
        
        is_valid, user_data = validate_telegram_data(init_data, current_app.config['TELEGRAM_BOT_TOKEN'])
        
        if is_valid:
            user_name = get_user_name(user_data)
            return jsonify({
                'valid': True, 
                'user': user_data,
                'userName': user_name
            }), 200
        else:
            return jsonify({'valid': False, 'error': 'Invalid Telegram data'}), 401
            
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500

@main.route('/books-manager')
def books_manager():
    books_dao = Book.BooksDAO(file_path_books)
    return render_template('books-manager.html', books=books_dao.load_books())

@main.route('/winner')
def winner():
    # Obtener todos los rankings para el cálculo de Condorcet
    rankings = voting_manager.get_rankings_for_condorcet()
    
    if not rankings:
        return render_template('winner.html', 
                             winner="No hay votos aún", 
                             total_votes=0)
    
    # Usar el sistema de votación Condorcet existente
    try:
        # Usar la función condorcet_winner directamente con los rankings
        winner_result = condorcet_winner(rankings)
        total_votes = voting_manager.get_vote_count()
        
        return render_template('winner.html', 
                             winner=winner_result, 
                             total_votes=total_votes,
                             telegram_votes=voting_manager.get_telegram_votes_count(),
                             web_votes=voting_manager.get_web_votes_count())
    except Exception as e:
        print(f"Error calculando ganador: {e}")
        return render_template('winner.html', 
                             winner="Error calculando resultado", 
                             total_votes=voting_manager.get_vote_count())

@main.route('/votes')
def votes():
    # Obtener resumen de votos usando el nuevo sistema
    summary = voting_manager.export_votes_summary()
    
    # Para compatibilidad con la vista existente, convertir a texto
    data_text = ""
    for vote_detail in summary['vote_details']:
        timestamp = vote_detail['timestamp']
        display_name = vote_detail['display_name']
        ranking = vote_detail['ranking']
        source = vote_detail['source']
        
        data_text += f"[{source.upper()}] {display_name}; Lista: {ranking}; fecha: {timestamp}\n"
    
    return render_template('votes.html', 
                         data=data_text, 
                         summary=summary)

@main.route('/votes-json')
def votes_json():
    """Endpoint para obtener votos en formato JSON"""
    summary = voting_manager.export_votes_summary()
    return jsonify(summary)

@main.route('/vote-stats')
def vote_stats():
    """Endpoint para obtener estadísticas de votación"""
    summary = voting_manager.export_votes_summary()
    
    stats = {
        'total_votes': summary['total_votes'],
        'telegram_votes': summary['telegram_votes'],
        'web_votes': summary['web_votes'],
        'last_vote_time': summary['vote_details'][-1]['timestamp'] if summary['vote_details'] else None
    }
    
    return jsonify(stats)


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

    # Check if this is a Telegram request
    if 'initData' in data:
        # Validate Telegram authentication
        is_valid, user_data = validate_telegram_data(data['initData'], current_app.config['TELEGRAM_BOT_TOKEN'])
        if not is_valid:
            return jsonify({'message': 'Autenticación de Telegram inválida'}), 401
        
        if not data or 'orderedList' not in data:
            return jsonify({'message': 'Datos inválidos'}), 400
        
        # Extract data for Telegram user
        ordered_list = data['orderedList']
        telegram_user_id = user_data.get('id') if user_data else None
        
        # Add vote using voting manager
        success, message = voting_manager.add_vote(
            ranking=ordered_list,
            telegram_user_id=str(telegram_user_id) if telegram_user_id else None,
            telegram_user_data=user_data
        )
        
        if not success:
            return jsonify({'message': message}), 400
            
    else:
        # Regular web form submission
        if not data or 'name' not in data or 'orderedList' not in data:
            return jsonify({'message': 'Datos inválidos'}), 400

        name = data['name']
        ordered_list = data['orderedList']
        
        # Special case for test user
        if name == 'kek':
            return jsonify({'message': 'Voto de prueba ignorado'}), 200
        
        # Add vote using voting manager
        success, message = voting_manager.add_vote(
            ranking=ordered_list,
            username=name
        )
        
        if not success:
            return jsonify({'message': message}), 400
        
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
