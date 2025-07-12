#numeros primos ejercicio 1

from datetime import date

def es_primo(number):
    if number <= 1:
        return False
    for i in range (2,number):
        if number % i == 0:
            return False
    return True


number = int(input("Ingresa un número: "))
if es_primo(number):
    print(f"{number} ES UN NÚMERO PRIMO.")
else:
    print(f"{number} NO ES UN NÚMERO PRIMO.")


#Menu ejercicio 2
option1 = 1
option2 = 2
option3 = 3
resultOption = int(input(f"Escribe el número de la opción que necesites: Frase: {option1}, Fecha: {option2}, Salir:{option3} "))
if resultOption == 1:
    print ("Invertir tiempo en aprender a programar es invertir en mi futuro.")
elif resultOption == 2:
    dateActual = date.today()
    print(f"La fecha de hoy es:{dateActual}")
elif resultOption == 3:
    print ("XSaliendo, Saludos..")
    exit()
else:
    print ("El número ingresado no es correcto. Selecciona una opción valida")