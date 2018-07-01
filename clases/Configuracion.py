#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import ConfigParser
import os
import csv
    

class CsvData():
    __csv = os.path.join(os.path.dirname(os.path.abspath(__file__)),'valores.csv')
    __data = []
    __config = None

    def __init__(self):        
        self.__config = Configuracion()        
        with open(self.__csv, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                self.__data.append(row)

        
    def get_valores_by_tipo(self,tipos=None):        
        '''valor, lotes, margen, spread, tp_spread, tipo, codigo, nombre, descripcion = row'''
        if tipos is None: return self.__data 
        return [row for row in self.__data if row[5] in tipos]
        

    def get_valores_by_valor(self,valores=None):        
        '''valor, lotes, margen, spread, tp_spread, tipo, codigo, nombre, descripcion = row'''
        if valores is None: return self.__data         
        return [row for row in self.__data if row[0] in valores]





class Configuracion():
    
    __configuracion = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.cfg')

    def __init__(self):
        self.__config = ConfigParser.ConfigParser()
        self.__config.read(self.__configuracion)
        
        
    def get_valores_calculo(self):
        return self.__config.get('calculo', 'procesar').split(',')


    def get_directorio_base(self):
        return self.__config.get('data', 'directorio_base')
    
    
    def get_valores_proceso_hora(self):
    
        procesar = self.__config.get('hora', 'procesar').split(',')
        resoluciones = self.__config.get('hora', 'resoluciones').split(',')    
        csv_resultados = self.__config.get('hora', 'csv_resultados')
        cabecera = self.__config.get('resultados', 'cabecera')
        imprimir = self.__config.get('resultados', 'imprimir')
        
        cabecera = True if cabecera == "si" else False
        imprimir = True if imprimir == "si" else False
        
        
        tipos = self.__config.get('hora', 'tipos')
        tipos = None if tipos == 'None' else tipos.split(',')
        
        return procesar, resoluciones, csv_resultados, imprimir, cabecera, tipos


    def get_valores_descarga(self):
        resoluciones = self.__config.get('descargar', 'resoluciones').split(',')
        procesar = self.__config.get('descargar', 'procesar').split(',')
        return procesar,resoluciones


       
