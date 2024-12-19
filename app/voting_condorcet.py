def condorcet_winner(ballots):
    # Obtener los candidatos de la primera boleta
    candidates = ballots[0]
    num_candidates = len(candidates)

    # Crear un índice para los candidatos
    candidate_index = {c: i for i, c in enumerate(candidates)}
    # Inicializar la matriz de conteo de preferencias
    preference_counts = [[0] * num_candidates for _ in range(num_candidates)]

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
    # Contador de victorias de cada candidato en enfrentamientos directos
    wins_count = [0] * num_candidates
    respuesta = ""
    # Contar las victorias de cada candidato en enfrentamientos directos
    for i in range(num_candidates):
        for j in range(i + 1, num_candidates):
            votes_i_over_j = preference_counts[i][j]
            votes_j_over_i = preference_counts[j][i]

            if votes_i_over_j > votes_j_over_i:
                wins_count[i] += 1
                respuesta += f"{candidates[i]} le gana a {candidates[j]}\n"
                print(f"{candidates[i]} le gana a {candidates[j]}")
            elif votes_j_over_i > votes_i_over_j:
                wins_count[j] += 1
                respuesta += f"{candidates[j]} le gana a {candidates[i]}\n"
                print(f"{candidates[j]} le gana a {candidates[i]}")

    # Imprimir el número de contiendas ganadas por cada candidato
    for i, c in enumerate(candidates):
        respuesta += f"El candidato {c} ganó {wins_count[i]} contiendas.\n"
        print(f"El candidato {c} ganó {wins_count[i]} contiendas.")

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
            return respuesta

    return None


# Ejemplo de uso:
ballots = [
    ["A", "B", "C"],
    ["B", "C", "A"],
    ["B", "C", "A"],
    ["B", "C", "A"],
    ["B", "C", "A"]
]

winner = condorcet_winner(ballots)
if winner:
    print(f"\nEl ganador de Condorcet es: {winner}")
else:
    print("\nNo existe un ganador de Condorcet")