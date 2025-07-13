#Clase1-ejercicios-Lizeth Albacura

if __name__ == "__main__":
    print("Saludos, soy Lizeth Albacura")

#Ejercicio 1: números primos

def es_primo(número):
    if número < 2:
        return False
    for i in range(2, int(número ** 0.5)+1):
        if número % i == 0:
            return False
    return True

n = int(input("Ingrese el número que desee: "))

print(f"números primos del 1 al {n}:")
for i in range(1, n + 1):
    if es_primo(i):
        print(i)

#Ejercicio 2:Menú interactivo

import datetime 
def menú():
    print("Bienvenido a este menú interactivo")
    print("1. Mostrar una frase motivacional")
    print("2. Mostrar la fecha actual")
    print("3. Salir del programa")

    opcion = input("Elige una opción (1-3): ")

    if opcion == "1":
        print("¡Encomienda a Dios tu camino confía en Él, y Él actuará.Salmo 37:5!)")
    elif opcion == "2":
        fecha_actual = datetime.datetime.now()
        print("Fecha actual:", fecha_actual.strftime("%d/%m/%Y %H:%M:%S"))
    elif opcion == "3":
        print("Hasta luego, que tenga un buen día")
        return
    else:
        print("Opción no válida. Intentalo otra vez.")
    
menú()
