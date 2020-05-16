#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''Módulo que define las clases para manejar la biblioteca'''

class Libro(object):
    """Clase que representa un libro"""
    def __init__(self, archivo):
        '''Archivo es el nombre de archivo del libro representado'''

        self.__archivo     = archivo  # El nombre del archivo
        self.__tags        = []       # Lista de strings con las etiquetas
        self.__titulo      = archivo[0:archivo.rfind('.')]  # Por defecto es el nombre del archivo sin la extensión
        self.__autores     = []       # Lista de strings. Puede haber mas de un autor
        self.__edicion     = None     # Debe ser un entero con el número de edición
        self.__strEdicion  = ''       # Un string para identificar la edición. Por ejemplo 'Primera edición'
        self.__editorial   = ''       # Editorial que publicó esta edición
        self.__isbn        = ''       # String con el ISBN del libro
        self.__ano         = None     # Debe ser en entero con el año de publicación.
        self.__tipo        = ''       # String indicando si es novela, texto universitario, biografía, autoayuda, etc.
        self.__subtipo     = ''       # String indicando un subtipo. Por ejemplo si el tipo es "novela", el subtipo puede
                                      # ser "ciencia ficción", "histórica", etc. Para el tipo "texto universitario" el 
                                      # subtipo puede ser la materia de la que trata, como "física", "informática", etc.
                                      # Cada tipo, tiene sus propios subtitpos, aunque no hay validación. El usuario puede
                                      # nombrar los tipos y subtipos a su gusto.
        self.__idioma      = ''       # Idioma en que está escrito el libro


    def agregarTags(self, *tags):
        '''Agrega los tags pasados, a la lista de tags del libro'''

        for tag in tags:
            if not(tag in self.__tags):
                self.__tags.append(tag)

    def quitarTags(self, *tags):
        '''Elimina los tags pasados, de la lista de tags del libro'''

        for tag in tags:
            if tag in self.__tags:
                self.__tags.remove(tag)

    def agregarAutores(self, *autores):
        '''Agrega los autores pasados, a la lista de autores del libro'''

        for autor in autores:
            if not(autor in self.__autores):
                self.__autores.append(autor)

    def quitarAutores(self, *autores):
        '''Elimina los autores pasados, de la lista de autores del libro'''

        for autor in autores:
            if autor in self.__autores:
                self.__autores.remove(autor)

