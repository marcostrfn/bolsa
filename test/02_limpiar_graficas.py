#! /usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
import os

path_src = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(path_src)

import funciones.graficos as fg
from clases.Configuracion import Configuracion, CsvData

       
if __name__ == '__main__':
    ''' limpia graficos de la carpeta /graficos/ y deja backup en
    carpeta backup'''
    
    obj_csv = CsvData()
    obj_config = Configuracion()
    
    fg.limpiar_graficas(obj_config)

