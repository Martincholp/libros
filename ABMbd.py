#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''Gestor de base de datos de biblioteca xml'''

from lxml import etree
from clases import *


class BD(object):
    '''Base de datos completa'''

    # La clave del diccionario son los id de cada entrada y el valor el objeto libro
    def __init__(self, archivoXML):
        super(BD, self).__init__()
        self.__archivoXML   = archivoXML                # Nombre de archivo del XML con la base de datos
        self.__BDxml        = etree.parse(archivoXML)   # Estructura de árbol de elementos del xml
        self.__BD           = {}                        # Diccionario con todos los elementos
        self.__modificado   = False                     # Si modifiqué algo del arbol XML lo pongo a True para saber que tengo que actualizar

        for libro in self.__BDxml.findall('libro'):

            # Creo un objeto de tipo Libro() a partir del elemento xml libro
            objLibro = Libro(libro.attrib['archivo'])

            # Completo todos sus atributos          
            objLibro._Libro__id          = int(libro.attrib['id'])  # El id y el archivo siempre van a existir, si
            objLibro._Libro__archivo     = libro.attrib['archivo']  # alguno no existiera el xml estaría mal hecho

            if libro.find('tags') is not None: 
                objLibro._Libro__tags = libro.find('tags').text.split(' ')
            else:
                objLibro._Libro__tags = None

            if libro.find('titulo') is not None: 
                objLibro._Libro__titulo = libro.find('titulo').text
            else:
                objLibro._Libro__titulo = objLibro._Libro__archivo[0:objLibro._Libro__archivo.rfind('.')]  # Si no tiene título, asigno el nombre de archivo, sin la extensión
                etree.SubElement(libro, 'titulo')  #  Creo el elemento titulo en el árbol xml
                libro.find('titulo').text = objLibro._Libro__titulo  # Le asigno el texto al elemento creado
                self.__modificado = True

            if libro.find('autores') is not None: 
                objLibro._Libro__autores = [autor.text for autor in libro.find('autores').findall('autor')]
            else:
                objLibro._Libro__autores = None

            if libro.find('edicion') is not None:
                ed = libro.find('edicion').get('nro')  # La funcion get(key, default=None) busca el atributo del elemento. Si no existe devuelve default
                if ed is not None:
                    ed = int(ed)

                objLibro._Libro__edicion = ed
                objLibro._Libro__strEdicion  = libro.find('edicion').text
            else:
                objLibro._Libro__edicion = None
                objLibro._Libro__strEdicion  = None

            if libro.find('editorial') is not None: 
                objLibro._Libro__editorial = libro.find('editorial').text
            else:
                objLibro._Libro__editorial = None

            if libro.find('isbn') is not None: 
                objLibro._Libro__isbn = libro.find('isbn').text
            else:
                objLibro._Libro__isbn = None

            if libro.find('anio') is not None: 
                objLibro._Libro__anio = int(libro.find('anio').text)
            else:
                objLibro._Libro__anio = None

            if libro.find('tipo') is not None: 
                objLibro._Libro__tipo = libro.find('tipo').text
            else:
                objLibro._Libro__tipo = None

            if libro.find('subtipo') is not None: 
                objLibro._Libro__subtipo = libro.find('subtipo').text
            else:
                objLibro._Libro__subtipo = None

            if libro.find('idioma') is not None: 
                objLibro._Libro__idioma = libro.find('idioma').text
            else:
                objLibro._Libro__idioma = None

            # Agrego el objeto a la clase
            self.__BD[objLibro._Libro__id] = objLibro



    def __getitem__(self, id):
        ''' Permite buscar un libro con la sintaxis BD[id]'''
        return self.__BD[id]

    def __iter__(self):
        # Iterador sobre todos los libros para poder llamar con la sentencia for sin que de error
        return iter(self.__BD.values())

    def __len__(self):
        '''Devuelve la cantidad de libros en la base de datos'''
        return len(self.__BD)


    def obtenerLibro(self, id, default=None):
        '''Devuelve el libro con el id indicado. Si no existe devuelve default'''
        return self.__BD.get(id, default)

    def agregarLibro(self, libro, actualizar=False):
        '''Agrega el libro pasado a la base de datos. Si actualizar es True actualiza el xml inmediatamente'''
        pass    

    def eliminarLibro(self, libro, actualizar=False):
        '''Elimina el libro pasado de la base de datos. Si actualizar es True actualiza el xml inmediatamente'''
        pass    

    def buscar(self, filtro):
        '''Busca los libros que coinciden con el filtro. Devuelve una lista con los libros encontrados.'''
        # tengo que definir como hacer el filtro, para que pueda buscar en distintos campos
        pass

    def obtenerIdDisponible(self):
        '''Devuelve el siguiente id disponible para ser usado. Notar que si se elimina un libro de la base de datos, su id queda disponible para una próxima entrada'''

        # Objeto dict_keys() con todos los ids usados
        ids = self.__BD.keys() 

        disponible = 0

        while disponible in ids:
            disponible += 1

        return disponible

    def requiereActualizarXML(self):
        '''Devuelve True cuando hay cambios en la base de datos que es necesario guardar'''
        return self.__modificado


    def actualizarXML(self):
        '''Actualiza la base de datos, esribiendo los cambios hechos'''
        self.__BDxml.write(self.__archivoXML, pretty_print=True, xml_declaration=True,   encoding="utf-8")
        self.__modificado   = False

