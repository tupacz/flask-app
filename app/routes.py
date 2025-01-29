from flask import Blueprint, render_template, request, jsonify
from datetime import datetime

from app import Book
try:
    from app import voting_condorcet
except ImportError:
    import voting_condorcet

# Crear un Blueprint
main = Blueprint('main', __name__)

# Ruta para la página principal
@main.route('/')
def index():
    books = [ Book("Cien años de soledad", "Gabriel García Márquez", "La obra cumbre del realismo mágico que consolidó a García Márquez como una figura central de la literatura mundial.")
    ]
    return render_template('index.html')

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
            with open('app/data/data.txt', 'a') as file:
                file.write(f"Nombre: {name}; Lista: {ordered_list}; fecha: {fechahora}\n")
        except Exception as e:
            return (jsonify({'message': f'Error al guardar los datos: {str(e)}'}), 500)

    # Armo un array de arrays llamados Lista de data.txt
    #Obtengo un array de arrays del archivo data.txt
    with open('app/data/data.txt', 'r') as file:
        data = []
        for line in file:
            if line.strip():
                name, ordered_list, fechahora = line.strip().split('; ')
                #Obtengo dentro de ordered list los valores que están entre ''
                ordered_list = ordered_list.split(': ')[1]
                ordered_list = ordered_list[1:-1].split("', '")
                # Dentro de cada item en ordered_list, elimino las comillas simples y dobles
                for i in range(len(ordered_list)):
                    ordered_list[i] = ordered_list[i].replace("'", "")
                    ordered_list[i] = ordered_list[i].replace('"', "")
                data.append(ordered_list)
    
    # Obtengo el ganador Condorcet
    winner = voting_condorcet.condorcet_winner(data)

    # Escribo el ganador en un archivo. Debe borrar el contenido y escribir
    with open('app/data/winner.txt', 'w') as file:
        file.write(f"{winner}")

    with open('app/data/winnerHistorico.txt', 'a') as file:
        file.write(f"{fechahora}\n{winner}\n\n")

    return jsonify({'message': 'Datos guardados correctamente', 'winner': winner}), 200