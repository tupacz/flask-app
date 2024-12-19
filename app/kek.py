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
