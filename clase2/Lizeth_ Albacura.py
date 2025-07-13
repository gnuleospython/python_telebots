#CLASE2-Lizeth Albacura

#EJERCICIO 1: Objetos

#Este objeto representa una plancha alisadora de cabello. 
# Tiene propiedades como marca, modelo, color y temperatura máxima.
#Puede encenderse, ajustar la temperatura, y apagarse. 
# Elegí este objeto porque es útil y común, especialmente en rutinas personales.

"""
Plancha de Cabello:
- Marca
- Modelo
- Color
- Temperatura máxima

Métodos:
- encender()
- ajustar_temperatura()
- apagar()
"""

class PlanchaCabello:
    def __init__(self, marca, modelo, color, temp_max):
        self.marca = marca
        self.modelo = modelo
        self.color = color
        self.temp_max = temp_max
        self.encendida = False
        self.temperatura_actual = 0

    def encender(self):
        self.encendida = True
        self.temperatura_actual = 180  # temperatura inicial
        print(f"La plancha {self.marca} está encendida a {self.temperatura_actual}°C.")

    def ajustar_temperatura(self, nueva_temp):
        if self.encendida:
            if nueva_temp <= self.temp_max:
                self.temperatura_actual = nueva_temp
                print(f"Temperatura ajustada a {nueva_temp}°C.")
            else:
                print(f"La temperatura máxima es {self.temp_max}°C.")

    def apagar(self):
        self.encendida = False
        self.temperatura_actual = 0
        print(f"La plancha {self.marca} está apagada.")


mi_plancha = PlanchaCabello("Revlon", "NV9193", "Lila", 200)


mi_plancha.encender()
mi_plancha.ajustar_temperatura(200)
mi_plancha.apagar()


print("Marca:", mi_plancha.marca)
print("Modelo:", mi_plancha.modelo)
print("Color:", mi_plancha.color)
print("Temperatura máxima:", mi_plancha.temp_max, "°C")

#EJERCICIO 2: Listas y diccionarios

#Películas favoritas

peliculas_favoritas = ["El diario de Bridget Jones", "Legalmente rubia", "La Momia", "V de venganza"]

#Diccionario con información de cada película
info_peliculas = {
    "El diario de Bridget Jones": {
        "Género": "Comedia romántica",
        "Año": 2001
    },
    "Legalmente rubia": {
        "Género": "Comedia",
        "Año": 2001
    },
    "La Momia": {
        "Género": "Acción / Aventura",
        "Año": 1999
    },
    "V de venganza": {
        "Género": "Ciencia ficción",
        "Año": 2005
    }
}

#Imprimir las operaciones
print("\nMis películas favoritas son:\n")
for pelicula in peliculas_favoritas:
    print("-", pelicula)

print("\nDetalles de las películas:\n")
for nombre in peliculas_favoritas:
    datos = info_peliculas[nombre]
    print(f"{nombre}:\nGénero:{datos['Género']}, \nAño: {datos['Año']}\n")

#EJERCICIO 3-Trivia con POO

class Pregunta:
    def __init__(self, enunciado, opciones, respuesta_correcta):
        self.enunciado = enunciado
        self.opciones = opciones
        self.respuesta_correcta = respuesta_correcta

    def mostrar(self):
        print(self.enunciado)
        for i, opcion in enumerate(self.opciones, 1):
            print(f"{i}. {opcion}")

    def verificar_respuesta(self, seleccion_usuario):
        try:
            indice = int(seleccion_usuario) - 1
            if self.opciones[indice].lower() == self.respuesta_correcta.lower():
                print("✅ ¡Respuesta correcta!")
            else:
                print(f"❌ Respuesta incorrecta. La correcta es: {self.respuesta_correcta}")
        except (IndexError, ValueError):
            print("Opción inválida. Intenta con otro número")

# Preguntas disponibles
preguntas = {
    1: Pregunta(
        "¿Cuál es el nevado más grande del Ecuador?",
        ["Cotopaxi", "Chimborazo", "Cayambe", "Antisana"],
        "Chimborazo"
    ),
    2: Pregunta(
        "¿Cuál es la capital de Napo?",
        ["Quito", "Ambato", "Nueva Loja", "Tena"],
        "Tena"
    ),
    3: Pregunta(
        "¿En qué provincia se encuentra el Parque Nacional Cajas?",
        ["Azuay", "Loja", "El Oro", "Pichincha"],
        "Azuay"
    )
}

# Opciones
print("\nPreguntas disponibles:")
for num in preguntas:
    print(f"{num}. {preguntas[num].enunciado}")

# Selección del usuario
numero = int(input("\nIngrese el número de la pregunta (1-3): "))

if numero in preguntas:
    preguntas[numero].mostrar()
    respuesta = input("Tu respuesta (número): ")
    preguntas[numero].verificar_respuesta(respuesta)
else:
    print("Número de pregunta no válido")
