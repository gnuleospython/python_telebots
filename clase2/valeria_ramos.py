
# # Objeto Televisión
# """
# Estudiante:
# - edad
# - año    
# - nota
# Metodos:
# - información
# - aprobar 
# """

#EJERCICIO 1 OBJETOS
# ¿Qué es un objeto?
# Un objeto es como una cosa o persona en la vida real, pero en programación. Tiene datos que lo describen y cosas que puede hacer.

# ¿Qué hace el objeto Estudiante?
# Este objeto representa a un estudiante, con su nombre, edad, nota y curso. Además, puede mostrar su información y decir si aprobó o no.

# ¿Por qué elegí Estudiante?
# Porque es fácil de entender y es algo que todos conocemos. Así puedo practicar cómo guardar información y usarla para hacer cosas, como decir si el estudiante pasó la materia.

class Estudiante:
    def __init__(self, nombre, edad, nota, curso):
        self.nombre = nombre
        self.edad = edad
        self.nota = nota
        self.curso = curso       
        
    def informacion (self):
        print (f"Nombre:{nombre}")
        print (f"Edad:{edad}")
        print (f"Nota:{nota}")
        print (f"curso:{curso}")
        
    def aprobar (self):
        if self.nota>=7:
            print(f"{self.nombre} Felicidades! aprobaste.")
        else:
            print(f"{self.nombre} No aprobaste." )
        
#se pide los datos     
nombre = input ("Ingresa tu nombre:")
edad = int ( input ("Ingresa tu edad:"))
nota = float(input("Ingresa tu nota:"))
curso = input("Ingrea tu curso:")
        

#creación de objeto
est1 = Estudiante(nombre, edad, nota, curso)

#uso de métodos
est1.informacion()
est1.aprobar()

# Ejercicio2: LISTAS Y DICCIONARIOS
#lista
pelis_fav = ["voces inocentes", "crepusculo", "Yo antes de ti"]

print(f"Mi pelis favoritas son: {pelis_fav}")

#dicionario

peliculas = [
    {"nombre": "Voces Inocentes","genero": "Drama", "año": 2004 },
    {"nombre":"Crepúsculo", "genero": "Fantasía", "año": 2000},
    {"nombre": "Yo antes de ti", "genero":"Romance", "año":2005}
]

for peli in peliculas:
    print("Nombre:", peli["nombre"])
    print("Género:", peli["genero"])
    print("Año:", peli["año"])
    print("---")
    

#EJERCICIO 3: TRIVIA CON PPO

class Pregunta:
    def __init__(self, enunciado, opciones, respuesta):
        self.enunciado = enunciado
        self.opciones = opciones
        self.respuesta = respuesta
        
    
    def mostrar(self):
        print(self.enunciado)
        for i, opcion in enumerate(self.opciones, 1):
            print(f"{i}. {opcion}")
    
    def verificar(self, respuesta):
        return respuesta == self.respuesta
    


# Objectos de clase pregunta
p1 = Pregunta("¿Cuál es la capital de Francia?", ["Madrid", "París", "Londres"], 2)
p2 = Pregunta("¿Qué planeta es conocido como el Planeta Rojo?", ["Venus", "Marte", "Júpiter"], 2)
p3 = Pregunta("¿Cuántos continentes hay en el mundo?", ["5", "6", "7", "8"], 3)

# Los ponemos en una lista
lista_preguntas = [p1, p2, p3]

# Recorremos la lista para jugar la trivia
for pregunta in lista_preguntas:
    pregunta.mostrar()
    respuesta = int(input("Escribe el número de la opción correcta: "))
    if pregunta.verificar(respuesta):
        print("¡Correcto!\n")
    else:
        print(f"Incorrecto. La respuesta correcta era la opción {pregunta.respuesta}\n")
        