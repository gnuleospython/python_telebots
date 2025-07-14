"""
Autor: Santiago Calvopiña
Descripción: Archivo con ejercicios de objetos, listas/diccionarios y POO con trivia en Python.
"""

#  ////////////////////////////////// Ejercicio 1: Objetos //////////////////////////////////

# Objeto: Computadora

""" Atributos:
- marca: fabricante de la computadora
- sistema_operativo: sistema operativo instalado
- ram: memoria RAM en GB
- almacenamiento: capacidad del disco en GB

Métodos:
- encender(): imprime que la computadora está encendida
- apagar(): imprime que la computadora se está apagando
- mostrar_info(): muestra detalles de la computadora

Este objeto fue elegido porque es algo que usamos a diario y es fácil de relacionar con atributos y acciones reales. """



class Computadora:
    def __init__(self, marca, sistema_operativo, ram, almacenamiento):
        self.marca = marca
        self.sistema_operativo = sistema_operativo
        self.ram = ram
        self.almacenamiento = almacenamiento

    def encender(self):
        print(f"La computadora {self.marca} se está encendiendo...")

    def apagar(self):
        print(f"La computadora {self.marca} se está apagando...")

    def mostrar_info(self):
        print(f"Marca: {self.marca}")
        print(f"Sistema Operativo: {self.sistema_operativo}")
        print(f"RAM: {self.ram} GB")
        print(f"Almacenamiento: {self.almacenamiento} GB")

# ////////////////////////////////// Ejercicio 2: Listas y Diccionarios //////////////////////////////////

peliculas_favoritas = ["Interestelar", "Coco", "Matrix"]

info_peliculas = [
    {"titulo": "Interestelar", "genero": "Ciencia Ficción", "anio": 2014},
    {"titulo": "Coco", "genero": "Animación", "anio": 2017},
    {"titulo": "Matrix", "genero": "Acción", "anio": 1999}
]

print("\n Mis películas favoritas:")
print(peliculas_favoritas)

print("\n Información de las películas:")
for peli in info_peliculas:
    print(peli)

# Operaciones
print("\n Operaciones con diccionarios:")
info_peliculas[1]["anio"] = 2018
nueva_pelicula = {"titulo": "Inception", "genero": "Ciencia Ficción", "anio": 2010}
info_peliculas.append(nueva_pelicula)
info_peliculas.pop(0)

print("Después de las modificaciones:")
for peli in info_peliculas:
    print(peli)

#  ////////////////////////////////// Ejercicio 3: Trivia con POO //////////////////////////////////

class Pregunta:
    def __init__(self, enunciado, opciones, respuesta_correcta):
        self.enunciado = enunciado
        self.opciones = opciones
        self.respuesta_correcta = respuesta_correcta

    def mostrar(self):
        print(f"\n {self.enunciado}")
        for i, opcion in enumerate(self.opciones, start=1):
            print(f"{i}. {opcion}")

    def verificar(self, eleccion_usuario):
        return eleccion_usuario == self.respuesta_correcta

# Pregunta de ejemplo
pregunta = Pregunta(
    "¿Cuál es el lenguaje que se ejecuta en el navegador?",
    ["Python", "C++", "JavaScript", "Java"],
    3
)

pregunta.mostrar()
respuesta_usuario = int(input("Elige la opción correcta (1-4): "))

if pregunta.verificar(respuesta_usuario):
    print(" ¡Respuesta correcta!")
else:
    print(" Respuesta incorrecta.")

# Impresión clase Computadora
print("\n Objeto Computadora:")
mi_pc = Computadora("Lenovo", "Windows 11", 16, 512)
mi_pc.mostrar_info()
mi_pc.encender()
mi_pc.apagar()