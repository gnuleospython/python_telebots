from datetime import datetime

def verificar_primo(num):
    if num <= 1:
        return False
    for divisor in range(2, num):
        if num % divisor == 0:
            return False
    return True

def listar_primos(limite):
    return [numero for numero in range(2, limite + 1) if verificar_primo(numero)]

def mostrar_menu():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Mostrar una frase motivacional")
        print("2. Mostrar la fecha actual")
        print("3. Salir del programa")

        opcion = input("Selecciona una opción (1-3): ")

        if opcion == '1':
            print("La vida es un viaje, no un destino..")
        elif opcion == '2':
            ahora = datetime.now()
            print("La Fecha y hora actual es:", ahora.strftime("%d/%m/%Y %H:%M:%S"))
        elif opcion == '3':
            print("¡CHAIIITOO!")
            break
        else:
            print("La Opción no es válida. Ingresa una opción valida.")

if __name__ == "__main__":
    print("Iniciando ...")
    try:
        numero_usuario = int(input("Ingresa un número positivo mayor que 1: "))
        if numero_usuario > 1:
            lista_primos = listar_primos(numero_usuario)
            print(f"Los números primos hasta {numero_usuario} son: {lista_primos}")
        else:
            print("El número debe ser mayor que 1.")
    except ValueError:
        print("Debe ingresar un número entero válido.")

    mostrar_menu()