#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  tarea1.py
#  
#  Copyright 2025 edisontana <ltanav@tutanota.com>
#
# Tarea 1. 
# Programa que solicita al usuario un número n y visualiza todos los números primos del 1 al n.

from datetime import datetime

def esprimo(inumero):
    """
    Funcion para saber si un numero es primo.
    """
    if inumero <= 1:
        False
    for i in range( 2, int( inumero ** 0.5) + 1):
        if inumero % i == 0:
            return False
    return True    

def evaluanumeros(n):
    listaprimos = []
    icontador = 1
    x = 1
    while True:
        if icontador <= n:
            if esprimo(x):
                listaprimos.append(x)
                icontador = icontador + 1
            x = x + 1 
        else:
            break
    print(f"Resultado: Los {n} numeros  primos son: ")
    print(listaprimos)
    
    
def visualizafrase():
    texto = "Los buenos equipos incorporan el trabajo en grupo \n a la cultura, creando así los pilares del éxito."
    frase = f"{texto:>50}"
    texto2 = "Ted Sundquist"
    autor = f"{texto2:>50}"
    print(frase)
    print(autor)    
    print("")
    
def visualizafechaactual():
    print(datetime.now())
    
def muestramenu(opcion):
    if opcion == 1:
        visualizafrase()
    elif opcion == 2:
        visualizafechaactual()
    else:
        quit()

if __name__ == '__main__':
    print("Programa para hallar 'n' numero primos")
    print("Realizado por 2025 Edison TANA")
    n = int(input("¿Cuantos números primos desea, por favor digite aquí? (numero): "))
    evaluanumeros(n)
    print("------------------")
    print("Menu interactivo")
    print("1. Ver frase motivacional")
    print("2. Ver hora actual")
    print("3. Salir")
    eleccion = int(input("Por favor digite su opcion (1-3): "))
    muestramenu(eleccion)
    print("Fin del programa")
        

