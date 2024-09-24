import numpy as np #Importamos numpy y lo denominamos como una variable "np" para trabajar con ella
import random #importamos random

lista = np.array([i for i in range(11)] * 5)  # Crea un arreglo de 55 valores
random.shuffle(lista)  # Baraja el arreglo

partes = np.array_split(lista, 5)  # Divide el arreglo en 5 partes de 11 valores

# Función para encontrar valores únicos y repetidos
def encontrar_unicos_y_repetidos(arr): #Definimos una funcion que va a buscar todos los valores únicos y repetidos
    conteo = np.unique(arr, return_counts=True) #Realiza con la capacidad unique, dentro del arreglo ingresado [en este caso arr], y me cuenta cuantas veces se repite
    #^ Es decir, en el arreglo, cuentame cuantas veces se repite un valor. 
    #creamos 2 arreglos, uno llamado Unicos y otro llamado repetidos_list, uno me guarda los valores únicos, el otro los repetidos
    unicos = [] 
    repetidos_list = []

    for val, count in zip(conteo[0], conteo[1]): #Realiza dentro de una tupla la comparación de los valores, es decir, en el arreglo, en la posición 1, cuantas veces se repite ese valor en la posición
        if count == 1: #Si el valor se repite 1 sola vez, agrégalo a la lista de unicos
            unicos.append(val) #Dentro del arreglo únicos, agrega el valor guardado en la variable "val"
        elif count > 1: #Si el valor se repite más de una vez, agrégalo a la lista de unicos y repetidos
            unicos.append(val) #Dentro del arreglo únicos, agrega el valor guardado en la variable "val"
            repetidos_list.extend([val] * (count - 1))  # Dentro de arreglo repetidos_list, extiendelo 1 por cada vez que se repita el valor -1
            #^ Es decir, si se repite 2 veces, ingresa 1 vez en repetidos y 1 en únicos
            #^ Si se repite 3 veces, ingresa 2 vez en repetidos y 1 en únicos

    return unicos, repetidos_list #La funcion realizada me devolvera 2 arreglos, unicos y repetidos_list

# Arreglo global para almacenar todos los valores repetidos
todos_repetidos = []

# Procesar cada parte
for i in range(5): #Se repite un ciclo for por un valor de 5 veces *Si fuesemos a tener + contenedores, se modificaria eso y el array*
    unicos, repetidos = encontrar_unicos_y_repetidos(partes[i]) #Unicos y repetidos serán los 2 arreglos en los que almacenaremos los arreglos
    #que iremos a recibir por parte de unicos y repetidos_list *LINEA 26*
    todos_repetidos.extend(repetidos)  # En el arreglo global todos_repetidos, ingresame todo loq ue recibas de repetidos *que recibirá 5 arreglos
    
    print(f"Parte {i + 1}:") #Impresiones en posiciones desde la 1 hasta la N (EN ESTE CASO 5 porque el for se repite 5 veces *LINEA 32)
    print("Valores únicos:", unicos) #Imprime unicos
    print("Valores repetidos:", repetidos) #imprime repetidos
    print("------------------------------------------") #estetica para entender qpasa

print("Todos los valores repetidos acumulados sin organizar:", todos_repetidos) 
todos_repetidos = np.sort(todos_repetidos)  # Ordenar todos_repetidos
print("Todos los valores repetidos acumulados:", todos_repetidos)

# Buscar valores de todos_repetidos en cada parte
for i in range(5):
    # Obtener solo los valores únicos de la parte actual
    unicos_parte = encontrar_unicos_y_repetidos(partes[i])[0] #Como se devuelve una tupla, existen 2 listas dentro de esa tupla
    #^ Unicos y repetidos_list, como usamos la posicion [0], estamos solo obteniendo la primera lista de la tupla, en este caso, unicos
    # Ordenar la parte actual para poder aplicar búsqueda binaria
    partes[i] = np.sort(unicos_parte) #Organiza el arreglo que tenemos
    print(f"Parte {i + 1} ordenada:", partes[i]) #lo imprime xd 
    
    # Agregar los valores de todos_repetidos que no están en la parte actual
    for repetido in todos_repetidos: #Se recorre TODOS_REPETIDOS, y se guarda en "repetido" el valor que esté recibiendo del arreglo
        if repetido not in partes[i]: #Si el valor repetido no está en la parte, agrégalo a la parte
            print(f"El valor {repetido} NO se encontró en la Parte {i + 1}. Agregando a la parte.") #impresion 
            partes[i] = np.append(partes[i], repetido)  # Agregar el valor a la parte 

    # Ordenar la parte después de agregar los valores
    partes[i] = np.sort(partes[i])
    print(f"Parte {i + 1} actualizada:", partes[i])

# Actualizar todos_repetidos eliminando los números que ahora están en partes[i]
for i in range(5): #For que se repite 5 veces, i es el valor que va a tener el contador cada iteración, desde 0 a 4
    for numero in partes[i]: #recorre el arreglo partes, y cada valor recibido, guardalo en una variable numero
        if numero in todos_repetidos: #si el valor del numero está dentro del todos_repetidos, ingrésalo
            todos_repetidos = np.delete(todos_repetidos, np.where(todos_repetidos == numero)[0]) 
            #Se iguala a todos_repetidos una nueva lista, dónde:
            #np.delete guarda 2 valores, el arreglo donde se va a eliminar, y la posición
            #np.where utiliza un algoritmo de búsqueda dentro de todos repetidos, buscando la posicion en la que se encuentre la variable "numero"
            #Y la elimina 😁👍
            #Dando como resultante una nueva lista sin los valores

print("Valores repetidos restantes:", todos_repetidos)