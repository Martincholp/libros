#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

'''Módulo para crear y manipular archivos de log'''

class ArchivoLog(object):
    """Clase que representa un archivo de registro"""
    def __init__(self, archivo):

        self.__archivo = archivo  # Ruta al archivo de texto que contiene el log
        self.__regs = []          # Lista con todos los registros del archivo. 
        self.__regsNuevos = []    # Lista con los registros creados recientemente y que todavia no están en el archivo. Serán 
                                  # agregados al llamar a la función actualizar
        self.__separador = '#'    # Separa entre los campos del registro al escribir el archivo (valor por defecto)
        self.__modificado = False # Indica si se ha realizado algún cambio que todavía no está actualizado
                                  
        self.__formato = "%d/%m/%Y-%H:%M:%S.%f"  # Formato de fecha y hora. Por defecto es " dd/mm/aaaa-HH:MM:SS.ssssss "
                                                 # Se puede generar formatos alternativos usando la siguiente tabla:

                        #  Símbolo          Significado                                                   Ejemplo
                        #    %a       Día de la semana abreviado                                           'Wed'
                        #    %A       Nombre completo del día de la semana                                 'Wednesday'
                        #    %w       Número del día de la semana – 0 (Domingo) al 6 (Sábado)              '3'
                        #    %d       Día del mes (rellenado con cero)                                     '13'
                        #    %b       Nombre del mes abreviado                                             'Jan'
                        #    %B       Nombre completo del mes                                              'January'
                        #    %m       Mes del año                                                          '01'
                        #    %y       Año sin siglo                                                        '16'
                        #    %Y       Año con siglo                                                        '2016'
                        #    %H       Hora del reloj de 24 horas                                           '17'
                        #    %I       Hora del reloj de 12 horas                                           '05'
                        #    %p       AM/PM                                                                'PM'
                        #    %M       Minutos                                                              '00'
                        #    %S       Segundos                                                             '00'
                        #    %f       Microsegundos                                                        '000000'
                        #    %z       Desplazamiento UTC para objetos con reconocimiento de zona horaria   '-0500'
                        #    %Z       Nombre de la zona horaria                                            'EST'
                        #    %j       Día del año                                                          '013'
                        #    %W       Semana del año                                                       '02'
                        #    %c       Representación de fecha y hora para el lugar presente                'Wed Jan 13 17:00:00 2016'
                        #    %x       Representación de fecha para el lugar presente                       '01/13/16'
                        #    %X       Representación de hora para el lugar presente                        '17:00:00'
                        #    %%       Un caractér % literal                                                '%'

    @property
    def formato(self):
        """ Formato de fecha y hora. Por defecto es 'dd/mm/aaaa-HH:MM:SS.ssssss'
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
        '''Lista de los registros de la base de datos'''

        lista = self.__regs.copy()
        nuevos = self.__regsNuevos.copy()
        lista.extend(nuevos)
        return lista
    


    def cargarArchivo():
        '''Carga el archivo indicado en self.__archivo'''
        pass
    
    
    def buscarRegistros():
        '''Buscar registros segun algun filtro indicado. Devuelve una lista con los resultados'''
        pass




    def agregarRegistro(self, registro, actualizar=True):
        '''Agrega un registro a la lista regs. 
        Si actualizar es True (valor por defecto) se actualiza el archivo inmediatamente, si es False el archivo no se actualizará 
        hasta que no se llame a la función actualizar'''

        self.__regsNuevos.append(registro)
        self.__modificado = True

        if actualizar:
            self.actualizar()
        


    def actualizar(self):
        '''Actualiza el archivo del log con los registros agregados recientemente. Si tiene éxito devuelve True, 
        si falla devuelve False'''

        if len(self.__regsNuevos) == 0: # Si la lista de nuevos está vacía no hay nada para actualizar
            return True   # Salgo sin hacer nada y devolviendo True porque no es un error 

        
        resultado = False
        self.aux = []

        try:
            print('try')
            self.aux = self.__regs.copy()  # Copia los registros en una lista auxiliar
            self.__regsNuevos.sort()            # ordenados por fecha y hora, por las dudas...
            self.__regs.extend(self.__regsNuevos)  # Pongo los nuevos en la lista principal

            f = open(self.__archivo, 'a')  # intento abrir el archivo para agregar lineas
            print('/try')

        except FileNotFoundError:
            print('except1')
            resultado = False     # si el archivo no existe devuelvo falso
            print('/except1')

        except:  # si es otra excepcion la lanzo 
            print('except2')
            raise
            print('/except2')

        else:    # si pude abrir el archivo guardo los registros nuevos
            print('else')

            for reg in self.__regsNuevos:
                f.write(reg.reg2str(self.formato, self.separador) + '\n')

            resultado = True

            print('/else')
        finally:
            print('finally')

            if resultado: # si pude guardar todos los registros 
                f.close()  #cierro el archivo
                self.__regsNuevos.clear()  # limpio la lista de nuevos
                self.__modificado = False  # reseteo la bandera de modificacion

            else:  # Si no se pudo actualizar
                self.__regs = self.aux  # vuelvo el estado de __regs al valor antes del __regs.extend()

            print('/finally')
            # devuelvo el resultado
            return resultado





class Registro(object):
    """Clase que representa un registro dentro de un archivo"""
    def __init__(self, evento, argumentos="", comentarios=""):

        self.__fechahora = datetime.datetime.now()  # La fecha y hora se debe aregar automáticamente, y es en el momento en que se crea el objeto
        self.__evento = evento
        self.__argumentos = argumentos
        self.__comentarios=comentarios
        

    def __lt__(self, reg):
        # Compara reg con self y devuelve True si self.fechahora es menor que reg.fechahora, si no devuelve False

        if self.__fechahora < reg.fechahora:
            return True
        else:
            return False

    def __gt__(self, reg):
        # Compara reg con self y devuelve True si self.fechahora es mayor que reg.fechahora, si no devuelve False

        if self.__fechahora > reg.fechahora:
            return True
        else:
            return False

    def __eq__(self, reg):
        # Compara reg con self y devuelve True si self.fechahora es igual a reg.fechahora, si no devuelve False

        if self.__fechahora > reg.fechahora:
            return True
        else:
            return False

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

    def reg2str(self, formato, separador=''):
        '''Devuelve el registro como un string, con la fecha en el formato pasado. Útil para escribir el archivo. 
        Para separar entre los campos del registro se utiliza separador. Si no se especifica se usa el caracter #'''

        if separador == '':
            separador = '#'

        return  self.strFechahora(formato) + separador + self.evento + separador + self.argumentos + separador + self.comentarios

    def strFechahora(self, formato = "%d/%m/%Y-%H:%M:%S.%f"):
        '''Devuelve la fecha y hora como un string, con el formato pasado'''
        return self.__fechahora.strftime(formato)

