#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  tarea2.py
#  
#  Copyright 2025 edisontana <ltanav@tutanota.com>
#
# Tarea 2. 
# Ejercicio1: Defina un clase Pais con dos metodos
# Ejercicio2: Listas y diccionarios
# Ejercicio3: Trivia con POO

from datetime import datetime

class Pais:

    def __init__(self, nombreES, nombreEN, codigoISOA3):
            """
            Crea un constructor 
            """
            self.nombreES = nombreES
            self.nombreEN = nombreEN
            self.codigoISOA3 = codigoISOA3
                
    def verArea(self, pais):
        """
        Visuliza el area superficial del pais
        """
        # Diccionario de áreas de países (puedes expandir este diccionario)
        self.areas = {
            'ecuador': 256370,
            'colombia': 1141748,
            'peru': 1285216,
            'argentina': 2780400,
            'chile': 756102
        }
        
        strPais = pais.lower()
        if strPais in self.areas:
            return self.areas[strPais]
        else:
            return f"No se encontró información para el país {pais}"

        
    def verCapital(self, pais):
        """
        Muestra la capital del pais
        """
        self.capitales = {
            'ecuador': 'Quito',
            'colombia': 'Bogota',
            'peru': 'Lima',
            'argentina': 'Buenos Aires',
                'chile': 'Santiago'
        }          
        strPais = pais.lower()
        if strPais in self.capitales:
            return self.capitales[strPais]
        else:
            return f"No se encontró información para el país {pais}"

# Ejercicio2: Defina un clase Pais con dos metodos

class Pelicula:
    def __init__(self, anio, nombre, genero):
        """
        Constructor de la clase Pelicula
        
        Args:
            anio (int): Año de producción
            nombre (str): Nombre de la pelicula
            genero (str): Género de la pelicula
        """
        self.anio = anio
        self.nombre = nombre
        self.genero = genero
    
    def __str__(self):
        """
        Representación en cadena de la película
        """
        return f"{self.nombre} ({self.anio}) - {self.genero}"

class PeliculasFavoritas:
    def __init__(self):
        """
        Constructor de la clase PeliculasFavoritas
        """
        self.peliculas = []
    
    def agregapelicula(self, anio, nombre, genero):
        """
        Agrega una nueva película a la lista
        
        Args:
            anio (int): Año de producción
            nombre (str): Nombre de la pelicula
            genero (str): Género de la pelicula
        """
        nuevapelicula = Pelicula(anio, nombre, genero)
        self.peliculas.append(nuevapelicula)
        print(f"Se agregó {nombre}")
    
    def buscaporanio(self, anio):
        """
        Busca una pelicula por su año de producción
        
        Args:
            anio (int): Año a buscar
        
        Returns:
            Pelicula or str: Pelicula encontrada o mensaje de no encontrado
        """
        for pelicula in self.peliculas:
            if pelicula.anio == anio:
                return pelicula
        return f"No se encontró pelicula en el {anio}"
    
    def muestratodaspeliculas(self):
        """
        Muestra todas las peliculas en la lista
        """
        if not self.peliculas:
            print("El catálogo está vacío.")
            return 0
        
        print("\n--- Catálogo de Películas ---")
        for pelicula in self.peliculas:
            print(pelicula)

def main():
    """
    Función principal para demostrar el catálogo de películas
    """
    # Crear instancia del catálogo
    favorita1 = PeliculasFavoritas()
    
    # Agregar películas al catálogo
    favorita1.agregapelicula(2010, "Inception", "Ciencia Ficción")
    favorita1.agregapelicula(1972, "El Padrino", "Drama")
    favorita1.agregapelicula(1999, "Matrix", "Ciencia Ficción")
    
    # Mostrar películas
    favorita1.muestratodaspeliculas()

# Ejercicio3: Defina un clase Pais con dos metodos
class Pregunta:

    def __init__(self, enunciado, opciones, respuesta):
        """
        Constructor de la clase Pregunta
        
        Args:
            enunciado (str): cadena de texto del enunciado
            opciones (int): numero de opcion
            respuesta (int): respuesta correcta
        """
        self.enunciado = enunciado
        self.opciones = opciones
        self.respuesta = respuesta
    
    def __str__(self):
        """
        Representación en cadena de la pregunta
        """
        return f"{self.enunciado}"
    
    def visualizaopciones(self):
        """
        Muestra las opciones de respuesta
        """
        print(self.enunciado)
        for i, opcion in enumerate(self.opciones, 1):
            print(f"{i}. {opcion}")
    
    def verificarespuesta(self, respuesta_usuario):
        """
        Verifica si la respuesta del usuario es correcta
        
        Args:
            respuesta_usuario (int): respuesta seleccionada por el usuario
        
        Returns:
            bool: True si la respuesta es correcta, False en caso contrario
        """
        # Ajustar el índice para que coincida con la lista (restar 1)
        return respuesta_usuario - 1 == self.respuesta
    
    def obtienerespuestacorrecta(self):
        """
        Devuelve la respuesta correcta
        
        Returns:
            str: Opción correcta
        """
        return self.opciones[self.respuesta]

# Ejemplo de pregunta
def main3():
    # Crear una pregunta
    pregunta1 = Pregunta(
        "¿Cuál es la capital de Francia?", 
        ["Londres", "Berlín", "París", "Madrid"], 
        2  # París es la respuesta correcta (índice 2)
    )
    
    # Mostrar la pregunta y sus opciones
    pregunta1.visualizaopciones()
    
    # Solicitar respuesta del usuario
    try:
        respuestausuario = int(input("^.^ Ingrese el número de su respuesta: "))
        
        # Verificar la respuesta
        if pregunta1.verificarespuesta(respuestausuario):
            print("¡Respuesta correcta!")
        else:
            print(f"Respuesta incorrecta. La respuesta correcta es: {pregunta1.obtienerespuestacorrecta()}")
    
    except ValueError:
        print("Por favor, ingrese un número válido.")
        
if __name__ == '__main__':
    
    print("Programa de la Tarea 2")
    print("Realizado por 2025 Edison TANA")
    print("Enunciado 1")
    pais1 = Pais('Ecuador','Ecuador','ECU')
    pais2 = Pais('Colombia','Colombia','COL')
    print(f" >> Pais: {pais1.nombreES}")
    print(pais1.verCapital(pais1.nombreES))    
    print(f"{pais1.verArea(pais1.nombreES)} km²")
    print(f" >> Pais: {pais2.nombreES}")
    print(pais2.verCapital(pais2.nombreES))    
    print(f"{pais2.verArea(pais2.nombreES)} km²")
    print("Enunciado 2")
    main()
    print("Enunciado 3")
    main3()    
    print("Fin del programa")
