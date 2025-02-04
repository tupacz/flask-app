def condorcet_winner(ballots):
    resultado = {
        "candidatos": [],
        "tabla_enfrentamientos": "",
        "get_votes": None,
        "ganador_condorcet": "",
        "respuesta_escrita": "",
        "half": 0
    }
    # Obtener los candidatos de la primera boleta
    candidates = ballots[0]
    resultado["candidatos"] = candidates
    num_candidates = len(candidates)

    # Crear un índice para los candidatos
    candidate_index = {c: i for i, c in enumerate(candidates)}
    # Inicializar la matriz de conteo de preferencias
    preference_counts = [[0] * num_candidates for _ in range(num_candidates)]
    resultado["get_votes"] = preference_counts

    # Contar las preferencias de cada boleta
    for ballot in ballots:
        positions = {candidate: pos for pos, candidate in enumerate(ballot)}

        for i in range(num_candidates):
            for j in range(num_candidates):
                if i != j:
                    if positions[candidates[i]] < positions[candidates[j]]:
                        preference_counts[i][j] += 1

    # Número total de boletas
    num_ballots = len(ballots)
    # Mitad del número total de boletas
    half = num_ballots / 2.0
    resultado["half"] = half
    # Contador de victorias de cada candidato en enfrentamientos directos
    wins_count = [0] * num_candidates

    # Generar el "fixture" o tabla de enfrentamientos
    resultado["tabla_enfrentamientos"] = fixture_maker(candidates, num_candidates, preference_counts)

    respuesta = ""
    # Contar las victorias de cada candidato en enfrentamientos directos
    for i in range(num_candidates):
        for j in range(i + 1, num_candidates):
            votes_i_over_j = preference_counts[i][j]
            votes_j_over_i = preference_counts[j][i]

            if votes_i_over_j > votes_j_over_i:
                wins_count[i] += 1
                respuesta += f"{candidates[i]} le gana a {candidates[j]}\n"
            elif votes_j_over_i > votes_i_over_j:
                wins_count[j] += 1
                respuesta += f"{candidates[j]} le gana a {candidates[i]}\n"

    # Imprimir el número de contiendas ganadas por cada candidato
    for i, c in enumerate(candidates):
        respuesta += f"El candidato {c} ganó {wins_count[i]} contiendas.\n"

    # Determinar si hay un ganador de Condorcet
    for i in range(num_candidates):
        wins_all = True
        for j in range(num_candidates):
            if i != j:
                if preference_counts[i][j] <= half:
                    wins_all = False
                    break
        if wins_all:
            respuesta += f"El ganador de Condorcet es: {candidates[i]}\n"
            resultado["ganador_condorcet"] = candidates[i]
            

    respuesta += f"El ganador de Condorcet es: None\n"
    
    # desempate por quién gana más contiendas y quién gana por más votos
    max_wins = max(wins_count)
    max_wins_indices = [i for i, wins in enumerate(wins_count) if wins == max_wins]
    
    if len(max_wins_indices) == 1:
        max_wins_index = max_wins_indices[0]
        if max_wins > half:
            respuesta += f"El ganador de Condorcet es: {candidates[max_wins_index]}\n"
            resultado["ganador_condorcet"] = candidates[max_wins_index]
            return respuesta
    else:
        # Manejar el caso de empate
        respuesta += "Hay un empate entre los siguientes candidatos:\n"
        for index in max_wins_indices:
            respuesta += f"{candidates[index]}\n"
        
        # Se realiza entonces desempate por cantidad de votos entre los candidatos que empataron, eso se puede hacer con preference_counts
        max_votes = -1
        condorcet_winner = None
        for i in max_wins_indices:
            total_votes = sum(preference_counts[i])
            if total_votes > max_votes:
                max_votes = total_votes
                condorcet_winner = candidates[i]
        
        if condorcet_winner:
            respuesta += f"El ganador de Condorcet por desempate es: {condorcet_winner}\n"
            resultado["ganador_condorcet"] = condorcet_winner
        else:
            respuesta += "No se pudo determinar un ganador de Condorcet por desempate.\n"
            resultado["ganador_condorcet"] = None
    
    resultado["respuesta_escrita"] = respuesta
    return resultado

def fixture_maker(candidates, num_candidates, preference_counts):
    output = []
    output.append("\nTabla de enfrentamientos:")
    header = [";"] + candidates
    output.append(";".join(header))
    for i in range(num_candidates):
        row = [candidates[i]]
        for j in range(num_candidates):
            if i == j:
                row.append("-")  # Sin enfrentamiento consigo mismo
            else:
                row.append(str(preference_counts[i][j]))
        output.append(";".join(row))
    return "\n".join(output)

def get_condorcet_winner(ruta_archivo: str):
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
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

    ballots = data

    winner = condorcet_winner(ballots)
    if winner:
        return winner
    else:
        return "No existe un ganador de Condorcet"

# Ejemplo de uso:

if __name__ == '__main__':
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

    ballots = data


    winner = condorcet_winner(ballots)
    if winner:
        print(f"\n{winner}")
    else:
        print("\nNo existe un ganador de Condorcet")