#Tarea Dos
#____________________________________________________________
#Ejercicio número 1
#Ejercicios de tuplas, listas y diccionarios
#____________________________________________________________

class automovil:
    def __init__(self):
        self.marca = ""
        self.modelo = ""
        self.anio = ""
        self.color = ""

    def __init__(self,marca,modelo,anio,color):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.color = color

    def informacion(self):
        print(f"Marca: {self.marca} Modelo: {self.modelo} Año: {self.anio} Color: {self.color}")

    def aceleracion(self):
        print(f"El auto {self.marca} {self.modelo}, tiene un tiempo de aceleracion de 5 segundos de 0/100 Km")

    def cantidad_pasajeros(self):
        print(f"El auto {self.marca} {self.modelo}, tiene la capacidad de 5 pasajeros")

    def sonido(self):
        print(f"El auto {self.marca} {self.modelo} posee android car y Apple Car, con Spotify")

    def seguridad(self):
        print(f"El auto {self.marca} {self.modelo} posee camaras 360° y graba todo el recorrido del viaje")

#____________________________________________________________
#Ejercicio número 2
#Creación de un juego de trivia
#____________________________________________________________
class Pregunta:
    opciones = []
    def __init__(self,pregunta,respuesta,opciones):
        self.pregunta = pregunta
        self.opciones = list(opciones)
        self.respuesta = respuesta

    def mostrar_pregunta(self):
        print(f" {self.pregunta} : ")
        indice = 1
        for opcion in self.opciones:
            print(f" {indice} {opcion}")
            indice += 1

    def validar_respuesta(self,respuesta_usuario):
        if self.respuesta == respuesta_usuario:
            return True
        else:
            return False
    

if __name__ == "__main__":
    
    #Ejercicio número 1
    print("Caracteristicas de Automovil")
    automovil = automovil("Mazda","CX-30","2025","rojo")
    automovil.informacion()
    automovil.aceleracion()
    automovil.cantidad_pasajeros()
    automovil.sonido()
    automovil.seguridad()
    print("\n")
  
    print("Listas y Diccionarios")
    pelicula_1 = {"Nombre":"Lord of the rings : La comunidad del anillo","genero":"acción","Anio":2001}
    pelicula_2 = {"Nombre":"Lord of the rings : Las dos torres","genero":"acción","Anio":2002}
    pelicula_3 = {"Nombre":"Lord of the rings : El retorno del rey","genero":"drama","Anio":2023}

    Listado = [pelicula_1, pelicula_2, pelicula_3]
 
    for pelicula in Listado:
        print(pelicula)

    pelicula_3["genero"]="accion"
    pelicula_3["Anio"] = 2003

    pelicula_4 = {"Nombre":"El hobbit : Un viaje inesperado","genero":"accion","Anio":2012}

    Listado.append(pelicula_4)
    Listado.remove(pelicula_3)
    
    print("\n")
    print("Listado despues de eliminar pelicula 3 y posicionar pelicula 4")
    print("\n")

    for pelicula in Listado:
        print(pelicula)

    print("\n")
    
    
    #Ejercicio número 2
    print("Trivia")
    pregunta = Pregunta("Cuál es la primera pelicula de Lord of the rings", 2, ["EL retorno del rey","La comunindad del anillo","Las dos torres","Un viaje inesperado"])
    
    pregunta.mostrar_pregunta()

    respuesta_correcta = int(input("Su respuesta es (ingrese el número correspondiente):"))

    if pregunta.validar_respuesta(respuesta_correcta):
        print("Respuesta correcta")
    else:
        print("Respuesta Incorrecta")