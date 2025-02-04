from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import os

try:
    from app import voting_condorcet
except ImportError:
    import voting_condorcet

# Crear un Blueprint
main = Blueprint('main', __name__)

# Ruta para la página principal
@main.route('/')
def index():
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

    # Construir una ruta absoluta al archivo
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene la carpeta actual
    file_path_data = os.path.join(base_dir, 'data', 'data.txt')
    file_path_winner = os.path.join(base_dir, 'data', 'winner.txt')
    file_path_winnerHistorico = os.path.join(base_dir, 'data', 'winnerHistorico.txt')

    if name != 'kek':
        try:
            # Crear carpeta si no existe
            os.makedirs(os.path.dirname(file_path_data), exist_ok=True)
            os.makedirs(os.path.dirname(file_path_winner), exist_ok=True)
            os.makedirs(os.path.dirname(file_path_winnerHistorico), exist_ok=True)
            print(base_dir)
            print(file_path_data)
            with open(file_path_data, 'a') as file:
                file.write(f"Nombre: {name}; Lista: {ordered_list}; fecha: {fechahora}\n")

        except Exception as e:
            return (jsonify({'message': f'Error al guardar los datos: {str(e)}'}), 500)

    # Armo un array de arrays llamados Lista de data.txt
    #Obtengo un array de arrays del archivo data.txt
    with open(file_path_data, 'r') as file:
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
    with open(file_path_winner, 'w') as file:
        file.write(f"{winner}")

    with open(file_path_winnerHistorico, 'a') as file:
        file.write(f"{fechahora}\n{winner}\n\n")

    return jsonify({'message': 'Datos guardados correctamente'}), 200
    return jsonify({'message': 'Datos guardados correctamente', 'winner': winner}), 200