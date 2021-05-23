#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

'''Módulo para crear y manipular archivos de log simples'''

class ArchivoLog(object):

    """Clase que representa un archivo de registro"""

    def __init__(self, archivo):

        self.__archivo = archivo   # Ruta al archivo de texto que contie el log
        self.__regs = []           # Lista con todos los registros del archivo.
        self.__regsNuevos = []     # Lista con los registros creados recientemente y que todavia no están en el archivo. Serán
                                   # agregados al llamar a la función actualizar
        self.__separador = '#'     # Separa entre los campos del registro al escribir el archivo (valor por defecto)
        self.__modificado = False  # Indica si se ha realizado algún cambio que todavía no está actualizado

        self.__formato = "%d/%m/%Y-%H:%M:%S.%f"  # Formato de fecha y hora. Por defecto es " dd/mm/aaaa-HH:MM:SS.ssssss "
                                                 # Para generar formatos alternativos ver docstring en la propiedad formato

    @property
    def archivoBD(self):
        '''Nombre del archivo de registro que es la base de datos.'''
        return self.__archivoBD

    @property
    def formato(self):
        """Formato de fecha y hora. Por defecto es 'dd/mm/aaaa-HH:MM:SS.ssssss'
            Se puede generar formatos alternativos usando la siguiente tabla:

                              Símbolo          Significado                                                   Ejemplo
                                %a       Día de la semana abreviado                                           'Wed'
                                %A       Nombre completo del día de la semana                                 'Wednesday'
                                %w       Número del día de la semana – 0 (Domingo) al 6 (Sábado)              '3'
                                %d       Día del mes (rellenado con cero)                                     '13'
                                %b       Nombre del mes abreviado                                             'Jan'
                                %B       Nombre completo del mes                                              'January'
                                %m       Mes del año                                                          '01'
                                %y       Año sin siglo                                                        '16'
                                %Y       Año con siglo                                                        '2016'
                                %H       Hora del reloj de 24 horas                                           '17'
                                %I       Hora del reloj de 12 horas                                           '05'
                                %p       AM/PM                                                                'PM'
                                %M       Minutos                                                              '00'
                                %S       Segundos                                                             '00'
                                %f       Microsegundos                                                        '000000'
                                %z       Desplazamiento UTC para objetos con reconocimiento de zona horaria   '-0500'
                                %Z       Nombre de la zona horaria                                            'EST'
                                %j       Día del año                                                          '013'
                                %W       Semana del año                                                       '02'
                                %c       Representación de fecha y hora para el lugar presente                'Wed Jan 13 17:00:00 2016'
                                %x       Representación de fecha para el lugar presente                       '01/13/16'
                                %X       Representación de hora para el lugar presente                        '17:00:00'
                                %%       Un caractér % literal                                                '%'
        """
        return self.__formato

    @formato.setter
    def formato(self, val):
        self.__formato = val

    @property
    def separador(self):
        '''Caracter para separar entre los campos del registro al guardar el archivo'''
        return self.__separador

    @separador.setter
    def separador(self, val):
        self.__separador = val

    @property
    def modificado(self):
        '''Indica si se ha realizado algún cambio y que todavía no se haya actualizado el archivo'''
        return self.__modificado

    @property
    def registros(self):
        '''Lista con los registros de la base de datos'''

        # lista = self.__regs.copy()
        # nuevos = self.__regsNuevos.copy()
        # lista.extend(nuevos)

        lista = []
        lista.extend(self.__regs)
        lista.extend(self.__regsNuevos)
        return lista

    def cargarArchivo(self):
        '''Carga el archivo indicado en self.__archivo. El separador de los datos del registro y el formato de
        fecha utilizado será el indicado en self.separador y self.formato. Devuelve True si el archivo existe
        o False si no puede encontrar el archivo.'''

        try:
            f = None
            f = open(self.__archivo, 'r')

        except FileNotFoundError:
            return False

        else:
            # Limpio la lista, por las dudas
            self.__regs.clear()

            # Agrego a la lista cada linea del archivo
            for linea in f:
                fechahora, evento, argumentos, comentarios = linea.strip().split(self.separador)
                self.__regs.append(Registro(evento, argumentos, comentarios, fechahora, self.formato))

            # Modificado a False. Como recién cargo el archivo no está modificado
            self.__modificado = False

            return True

        finally:
            if f is not None:
                f.close()

    def buscarRegistros(self, campo, cadena):
        '''Buscar registros segun algun filtro indicado. Devuelve una lista con los resultados'''

        # Actualmente solo busca coincidencias. En vesiones futuras usar regex

        lista = self.registros  # Lista con todos los registros cargados (los del archivos y los que aún no fueron actualizados)
        resultados = []

        for r in lista:
            if campo == 'fechahora':  # Caso especial si el campo s 'fechahora'
                if cadena in getattr(r, 'strFechahora')(self.formato):
                    resultados.append(r)

            elif campo in ['evento', 'argumentos', 'comentarios']:  # Evito que se pueda buscar otra cosa. Solo estos campos estan disponibles para buscar
                if cadena in getattr(r, campo):
                    resultados.append(r)

        return resultados

    def agregarRegistro(self, registro, actualizar=True):
        '''Agrega un registro a la lista regs.
         Si actualizar es True (valor por defecto) se actualiza el archivo inmediatamente, si es False el archivo no se actualizará
         hasta que no se llame a la función actualizar'''

        self.__regsNuevos.append(registro)
        self.__modificado = True

        if actualizar:
            self.actualizar()

        return registro

    def actualizar(self):
        '''Actualiza el archivo del log con los registros agregados recientemente. Si tiene éxito devuelve True,
         si falla devuelve False'''

        if len(self.__regsNuevos) == 0:  # Si la lista de nuevos está vacía no hay nada para actualizar
            return True   # Salgo sin hacer nada y devolviendo True porque no es un error

        resultado = False
        self.aux = []

        try:
            self.aux = self.__regs.copy()  # Copia los registros en una lista auxiliar
            self.__regsNuevos.sort()            # ordenados por fecha y hora, por las dudas...
            self.__regs.extend(self.__regsNuevos)  # Pongo los nuevos en la lista principal

            f = open(self.__archivo, 'a')  # intento abrir el archivo para agregar lineas

        except FileNotFoundError:
            resultado = False     # si el archivo no existe devuelvo falso

        except:  # si es otra excepcion la lanzo
            raise

        else:    # si pude abrir el archivo guardo los registros nuevos
            for reg in self.__regsNuevos:
                f.write(reg.reg2str(self.formato, self.separador) + '\n')

            resultado = True

        finally:
            f.close()  # cierro el archivo

            if resultado:  # si pude guardar todos los registros
                self.__regsNuevos.clear()  # limpio la lista de nuevos
                self.__modificado = False  # reseteo la bandera de modificacion

            else:  # Si no se pudo actualizar
                self.__regs = self.aux  # vuelvo el estado de __regs al valor antes del __regs.extend()

            # devuelvo el resultado
            return resultado


class Registro(object):
    """Clase que representa un registro dentro de un archivo"""

    def __init__(self, evento, argumentos="", comentarios="", fechahora="", formatoFechahora='%d/%m/%Y-%H:%M:%S.%f'):

        if fechahora == "":
            self.__fechahora = datetime.datetime.now()  # Si no se especifica fecha y hora se debe aregar automáticamente, y es en el momento en que se crea el objeto
        else:
            self.__fechahora = datetime.datetime.strptime(fechahora, formatoFechahora)  # Parsea fecha y hora según el formato pasado

        self.__evento = evento
        self.__argumentos = argumentos
        self.__comentarios = comentarios

    def __lt__(self, reg):
        '''Compara reg con self y devuelve True si self.fechahora es menor que reg.fechahora, si no devuelve False'''

        if self.__fechahora < reg.fechahora:
            return True
        else:
            return False

    def __gt__(self, reg):
        '''Compara reg con self y devuelve True si self.fechahora es mayor que reg.fechahora, si no devuelve False'''

        if self.__fechahora > reg.fechahora:
            return True
        else:
            return False

    def __eq__(self, reg):
        '''Compara reg con self y devuelve True si self.fechahora es igual a reg.fechahora, si no devuelve False'''

        if self.__fechahora > reg.fechahora:
            return True
        else:
            return False

    def __str__(self):
        '''Devuelve el registro como string '''
        return self.reg2str()

    @property
    def fechahora(self):
        '''Devuelve la fecha y hora del registro como un objeto datetime del modulo datetime'''
        return self.__fechahora

    @property
    def evento(self):
        '''Devuelve el evento que ocasionó registro'''
        return self.__evento

    @property
    def argumentos(self):
        '''Devuelve los argumentos del evento que ocasionó el registro'''
        return self.__argumentos

    @property
    def comentarios(self):
        '''Devuelve comentarios asociados al registro'''
        return self.__comentarios

    def reg2str(self, formatoFechahora='%d/%m/%Y-%H:%M:%S.%f', separador='#'):
        '''Devuelve el registro como un string, muy útil para escribir en el archivo.
         Si no se especifica el formato de fecha se utiliza el formato por defecto ( %d/%m/%Y-%H:%M:%S.%f )
         Para separar entre los campos del registro se utiliza separador. Si no se especifica se usa el caracter #'''

        return self.strFechahora(formatoFechahora) + separador + self.evento + separador + self.argumentos + separador + self.comentarios

    def strFechahora(self, formatoFechahora='%d/%m/%Y-%H:%M:%S.%f'):
        '''Devuelve la fecha y hora como un string, con el formato pasado'''
        return self.__fechahora.strftime(formatoFechahora)
