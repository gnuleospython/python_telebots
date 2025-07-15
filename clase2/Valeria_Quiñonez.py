# clase 2-Estructuras y POO
Valeria Beatriz Quiñonez Rodriguez
# Ejercicio 1: Objetos
# Definimos la clase Laptop
class Laptop:
    def __init__(self, marca, modelo, año, color, almacenamiento, memoria_ram=8):
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.color = color
        self.almacenamiento = almacenamiento
        self.memoria_ram = memoria_ram
        self.estado = "apagado"

    def encender(self):
        self.estado = "encendido"
        print(f"La laptop {self.marca} {self.modelo} está {self.estado}.")

    def apagar(self):
        self.estado = "apagado"
        print(f"La laptop {self.marca} {self.modelo} está {self.estado}.")
    def reiniciar(self):
        if self.estado == "encendido":
            print(f"La laptop {self.marca} {self.modelo} se está reiniciando.")
        else:
            print(f"No se puede reiniciar la laptop {self.marca} {self.modelo} porque está apagada.")
#Ejercicio 2: Listas y Diccionarios
#Lista con tus 3 peliculas favoritas
peliculas_favoritas = ["Legalmente Rubia", "Rasputia", "Shrek"]
#Imprimir lista
print("Mis películas favoritas son:")
for pelicula in peliculas_favoritas:
    print(f"- {pelicula}")
    #Diccionario con mis datos
    mi_info = {
        "nombre": "Valeria ",
        "edad": 17,
        "genero": "Femenino"
    }
    #Imprimir diccionario
print("\nMis datos:")
for clave, valor in mi_info.items():
    print(f"{clave.capitalize()}: {valor}")
#Ejercicio 3: Trivia con POO
class Pregunta:
    def __init__(self, pregunta, respuesta_correcta, respuestas_incorrectas):
        self.pregunta = pregunta
        self.respuesta_correcta = respuesta_correcta
        self.respuestas_incorrectas = respuestas_incorrectas
    def mostrar_pregunta(self):
        print(f"Pregunta: {self.pregunta}")
        print("Respuestas posibles:")
        for i, respuesta in enumerate(self.respuestas_incorrectas, start=1):
            print(f"{i}. {respuesta}")
        print(f"Respuesta correcta: {self.respuesta_correcta}")
        print("¿Cuál de los siguientes son factores predisponentes para los cálculos de colesterol?:")
        print("1. Fibrosis quística")
        print("2. Hemólisis crónica")
        print("3. Cirrosis alcohólica")
        print("4. Ayuno")
def responder(self, numero):
        if self.opciones[numero - 4].lower() == self.respuesta.lower():
            print("✅ Respuesta correcta.")
        else:
            print("❌ Respuesta incorrecta: 1, 2 y 3 son incorrectas.")
            print(f"La respuesta correcta era: 4 {self.respuesta}")
            # mostrat pregunta
pregunta1 = Pregunta(
    "¿Cuál de los siguientes son factores predisponentes para los cálculos de colesterol?",
    "Ayuno",
    ["Fibrosis quística", "Hemólisis crónica", "Cirrosis alcohólica", "Ayuno"]
)
pregunta1.mostrar_pregunta()
# Responder a la pregunta
respuesta_usuario = int(input("Selecciona el número de tu respuesta: "))
pregunta1.responder(respuesta_usuario)
elif respuesta_usuario == 1 or respuesta_usuario == 2 or respuesta_usuario == 3:
 print("⚠️ Entrada inválida. Debes escribir un número válido de las opciones.")
