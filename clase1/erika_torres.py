## 🧪 Ejercicio 1: Números primos

def es_primo(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def mostrar_primos_hasta_n(n):
    print(f"Números primos del 1 al {n}:")
    for i in range(1, n + 1):
        if es_primo(i):
            print(i, end=" ")

# Programa principal
try:
    n = int(input("Ingresa un número entero positivo: "))
    if n < 1:
        print("Por favor, ingresa un número mayor o igual a 1.")
    else:
        mostrar_primos_hasta_n(n)
except ValueError:
    print("Entrada inválida. Por favor ingresa un número entero.")

## 🧪 Ejercicio 2: Menú interactivo 

import datetime

def mostrar_menu():
    print("\n📋 MENÚ PRINCIPAL")
    print("1. Mostrar una frase motivacional")
    print("2. Mostrar la fecha actual")
    print("3. Salir del programa")

while True:
    mostrar_menu()
    opcion = input("Elige una opción (1, 2 o 3): ")

    if opcion == "1":
        print("\n💬 Frase motivacional:")
        print("✨ El éxito es la suma de pequeños esfuerzos repetidos día tras día.")
    elif opcion == "2":
        fecha_actual = datetime.datetime.now()
        print(f"\n📅 Fecha actual: {fecha_actual.strftime('%d/%m/%Y - %H:%M:%S')}")
    elif opcion == "3":
        print("\n👋 ¡Gracias por usar el programa! Hasta pronto.")
        break
    else:
        print("⚠️ Opción no válida. Por favor, elige 1, 2 o 3.")
