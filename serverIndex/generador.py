#TIENES QUE INSTALAR NUMPY PARA PODER HACER ESTO
#pip install numpy 😁

import numpy as np
import random
# Lista original
lista = np.array([i for i in range(11)] * 5) #Tomo una lista de 11 indices, luego, multiplico la cantidad de instrucciones a repetir por 5 para tener los 55 valores
random.shuffle(lista) #con el shuffle lista lo que hago simplemente es barajar el arreglo, para que los numeros se vuelvan aleatorios
# Dividir en 5 partes
partes = np.array_split(lista, 5) #divido el arreglo de 55 valores en un arreglo que guarde en cada espacio valores de 11 en 11
#Si quieres manipular y verificar, te toca imprimir las partes de la siguiente forma:
print(partes)
print(partes[0]) #Primeros 11 numeros
print(partes[1]) #Segundos 11 numeros
print(partes[4]) #Ultimos 11 numeros
print(partes[-1]) #Si utilizas esta instrucción te devuelve el ultimo valor del arreglo, es decir, los ultimos 11 
print(np.sort(partes[-1])) #Resulta que dentro de numpy existe un sort integrado para ordenar los números, esta instrucción me organiza los ultimos 11 numeros



