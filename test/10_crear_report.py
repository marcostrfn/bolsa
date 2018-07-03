#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os

path_src = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(path_src)

from funciones import reporting as fr
from clases.Configuracion import Configuracion, CsvData

if __name__ == '__main__':
    ''' crea un reporte con los graficos de pares, valores
    pivot y mejores horas de trading.
    resultado en pdf en /graficos/valores/reporte'''
    
    obj_csv = CsvData()
    obj_config = Configuracion()
    
    fr.crear_reporte(obj_config)
