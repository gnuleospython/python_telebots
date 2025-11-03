import datetime

#Tarea Uno
#____________________________________________________________
#Ejercicio número 1
#Determinar si un número ingresado es primo
#____________________________________________________________

def numero_primo(numero):
    if numero % 2 == 0:
        return False
    for i in range(3, int(numero ** 0.5) + 1, 2):
        if numero % i == 0:
            return False
    return True

def numeros_primos(numero):
    primos = []
    for i in range(2, numero + 1):
        if numero_primo(i):
            primos.append(i)
    return primos

#____________________________________________________________
#Ejercicio número 2
#Menú interactivo
#____________________________________________________________

def menu():
    print("--- Bienvenido al menú interactivo ---")
    print("|1| Frase motivacional")
    print("|2| Fecha actual")
    print("|3| Salir")
    opcion = input("Ingrese una opcion: ")
    if opcion == "1":
        print("🎯 El éxito es la suma de pequeños esfuerzos repetidos día tras día.")
    elif opcion == "2":
        fecha_actual = print(" 🗓️ La fecha actual es: ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        print("👋🏼 Fin del programa, Hasta pronto.")


if __name__ == "__main__":

    #Ejercicio número 1
    numero = int(input("Ingrese un número mayor a 2: "))
    if numero <= 2:
        print("Por favor, ingrese un número mayor a 2.")
    else:
        primos = numeros_primos(numero)
        print(f"Numeros primos hasta {numero}: {primos}")
    
    #Ejercicio número 2
    menu()