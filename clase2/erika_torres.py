## 🧪 Ejercicio 1:   Objetos

class Bicicleta:
    """
    Clase Bicicleta:
    Representa una bicicleta con atributos básicos y métodos para simular su uso.
    """
    def __init__(self, marca, tipo, color, velocidad_max):
        self.marca = marca
        self.tipo = tipo  # Montaña, Ruta, Urbana, etc.
        self.color = color
        self.velocidad_max = velocidad_max
        self.velocidad_actual = 0

    def pedalear(self):
        if self.velocidad_actual < self.velocidad_max:
            self.velocidad_actual += 5
            print(f"Pedaleando... 🚴 Velocidad actual: {self.velocidad_actual} km/h")
        else:
            print("🚨 Has alcanzado la velocidad máxima.")

    def frenar(self):
        if self.velocidad_actual > 0:
            self.velocidad_actual -= 5
            print(f"Frenando... ⚠️ Velocidad actual: {self.velocidad_actual} km/h")
        else:
            print("La bicicleta ya está detenida.")

# Crear objeto bicicleta
mi_bici = Bicicleta("Giant", "Montaña", "Roja", 25)

# Usar métodos
mi_bici.pedalear()
mi_bici.pedalear()
mi_bici.frenar()

## 🧪 Ejercicio 2: Listas y diccionarios

# Lista de mis 3 películas favoritas
peliculas = ["El Origen", "Coco", "Intensamente"]

# Diccionario con información de una de ellas
pelicula_favorita = {
    "nombre": "El Origen",
    "género": "Ciencia Ficción",
    "año": 2010
}

# Operaciones
print("🎬 Mis películas favoritas son:", peliculas)
print("🎥 Detalles de la favorita:")
print("Nombre:", pelicula_favorita["nombre"])
print("Género:", pelicula_favorita["género"])
print("Año:", pelicula_favorita["año"])

## 🧪 Ejercicio 3: Trivia con PO

class Pregunta:
    def __init__(self, enunciado, opciones, respuesta_correcta):
        self.enunciado = enunciado
        self.opciones = opciones
        self.respuesta_correcta = respuesta_correcta

    def mostrar(self):
        print("❓", self.enunciado)
        for i, opcion in enumerate(self.opciones, 1):
            print(f"{i}. {opcion}")

    def responder(self, seleccion):
        if self.opciones[seleccion - 1] == self.respuesta_correcta:
            print("✅ ¡Correcto!")
        else:
            print(f"❌ Incorrecto. La respuesta era: {self.respuesta_correcta}")

# Crear pregunta
pregunta1 = Pregunta(
    "¿Cuál es la capital de Ecuador?",
    ["Guayaquil", "Quito", "Cuenca"],
    "Quito"
)

# Mostrar y pedir respuesta
pregunta1.mostrar()
numero = int(input("Ingresa el número de tu respuesta: "))
pregunta1.responder(numero)
