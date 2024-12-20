def irv_winner(ballots):
    # Extraer lista de todos los candidatos a partir del primer ballot
    # Se asume que todos los ballots tienen el mismo conjunto de candidatos
    candidates = set(ballots[0])

    while True:
        # Contar la cantidad de primeras preferencias para cada candidato aún en la contienda
        counts = {c: 0 for c in candidates}

        for ballot in ballots:
            # Buscar el primer candidato de la boleta que todavía siga en carrera
            for pref in ballot:
                if pref in candidates:
                    counts[pref] += 1
                    break
        
        total_votes = sum(counts.values())
        # Checkear si alguno tiene mayoría (>50%)
        for c, count in counts.items():
            if count > total_votes / 2:
                # Tenemos un ganador con mayoría absoluta
                return c
        
        # Si nadie tiene mayoría, eliminar al candidato menos votado
        # Identificar el mínimo
        min_count = min(counts.values())
        # Identificar todos los candidatos con el mínimo
        least_candidates = [c for c, cnt in counts.items() if cnt == min_count]
        
        # Eliminar al candidato o candidatos con menos votos
        # En IRV tradicional se elimina solo uno. Si hay empates, se puede elegir uno al azar
        # o según algún criterio. Aquí, para simplicidad, eliminamos todos los que empatan en último lugar.
        for lc in least_candidates:
            candidates.remove(lc)
        
        # Si se han eliminado todos menos uno, ese último es el ganador por default.
        if len(candidates) == 1:
            return candidates.pop()


# Ejemplo de uso:
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

winner = irv_winner(ballots)
print(f"El ganador por IRV es: {winner}")
