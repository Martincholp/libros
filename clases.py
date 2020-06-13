#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import scandir

'''Módulo que define las clases para manejar la biblioteca'''

class Libro(object):
    """Clase que representa un libro"""
    def __init__(self, archivo):
        '''Archivo es el nombre de archivo del libro representado'''

        self.__id          = 0                              # Entero. Identificador único del libro. Debe ser asignado por la aplicación, y no por el usuario
        self.__archivo     = archivo                        # String con el nombre del archivo
        self.__tags        = []                             # Lista de strings con las etiquetas
        self.__titulo      = archivo[0:archivo.rfind('.')]  # String con el título del libro. Por defecto es el nombre del archivo sin la extensión
        self.__autores     = []                             # Lista de strings con el o los autores
        self.__edicion     = 0                              # Entero con el número de edición. Si es 0 entonces no está asignado
        self.__strEdicion  = ''                             # String para identificar la edición. Por ejemplo 'Primera edición'
        self.__editorial   = ''                             # String con el nombre de la editorial que publicó esta edición
        self.__isbn        = ''                             # String con el ISBN del libro
        self.__anio        = 0                              # Entero con el año de publicación. Si es 0 entonces no está asignado
        self.__tipo        = ''                             # String indicando si es novela, texto universitario, biografía, autoayuda, etc.
        self.__subtipo     = ''                             # String indicando un subtipo. Por ejemplo si el tipo es "novela", el subtipo puede
                                                            # ser "ciencia ficción", "histórica", etc. Para el tipo "texto universitario" el 
                                                            # subtipo puede ser la materia de la que trata, como "física", "informática", etc.
                                                            # Cada tipo, tiene sus propios subtitpos, aunque no hay validación. El usuario puede
                                                            # nombrar los tipos y subtipos a su gusto.
        self.__idioma      = ''                             # String indicando el idioma en que está escrito el libro


    # # Todo el manejo de ABM lo debe hacer el otro modulo (ABMbd.py)
    # def agregarTags(self, *tags):
    #     '''Agrega los tags pasados, a la lista de tags del libro'''

    #     for tag in tags:
    #         if not(tag in self.__tags):
    #             self.__tags.append(tag)

    # def quitarTags(self, *tags):
    #     '''Elimina los tags pasados, de la lista de tags del libro'''

    #     for tag in tags:
    #         if tag in self.__tags:
    #             self.__tags.remove(tag)

    # def agregarAutores(self, *autores):
    #     '''Agrega los autores pasados, a la lista de autores del libro'''

    #     for autor in autores:
    #         if not(autor in self.__autores):
    #             self.__autores.append(autor)

    # def quitarAutores(self, *autores):
    #     '''Elimina los autores pasados, de la lista de autores del libro'''

    #     for autor in autores:
    #         if autor in self.__autores:
    #             self.__autores.remove(autor)


    ############################################################################
    ##################   PROPIEDADES  ##########################################
    ############################################################################
    @property
    def id(self):
        '''Número de id del libro'''
        return self.__id
    
    @property
    def archivo(self):
        '''Archivo del libro'''
        return self.__archivo
    
    @property
    def tags(self):
        '''Etiquetas del libro'''
        return self.__tags
    
    @property
    def titulo(self):
        '''Título del libro'''
        return self.__titulo
      
    @property
    def autor(self):
        '''Autores del libro. Devuelve una lista de strings'''
        return self.__autores
       
    @property
    def edicion(self):
        '''Número de edicion del libro'''
        return self.__edicion
    
    @property
    def strEdicion(self):
        '''String representando la edición del libro'''
        return self.__strEdicion
        
    @property
    def editorial(self):
        '''Editorial del libro'''
        return self.__editorial
    
    @property
    def isbn(self):
        '''ISBN del libro'''
        return self.__isbn
    
    @property
    def anio(self):
        '''Año de publicación del libro'''
        return self.__anio

    @property
    def tipo(self):
        '''Tipo del libro (Novela, texto universitario, autoayuda, biografía, etc.)'''
        return self.__tipo
    
    @property
    def subtipo(self):
        '''Subtipo del libro. Por ejemplo si el tipo es "novela", el subtipo puede
        ser "ciencia ficción", "histórica", etc. Para el tipo "texto universitario"
        el subtipo puede ser la materia de la que trata, como "física", "informática", etc.'''
        return self.__subtipo

    @property
    def idioma(self):
        '''Idioma en que está escrito el libro'''
        return self.__idioma
    

    ############################################################################
    ##################   METODOS ESPECIALES  ###################################
    ############################################################################

    def __str__(self):
        return self.titulo

class Directorio(object):
    """Directorio utilizado como biblioteca"""
    def __init__(self, path):
        
        self.__path = path

    @property
    def path(self):
        return self._path
    

    def archivos(self):
    '''Lista con los archivos del directorio actual'''
        return [obj.name for obj in scandir(self.path) if obj.is_file()]