#! /usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
import os

path_src = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(path_src)

import funciones.data as fd
from clases.Configuracion import Configuracion, CsvData


if __name__ == '__main__':   
    ''' graficos de las valores y resultado en /graficos/valores
    lee los valores de fichero de configuracion con tag calculo '''
    
    obj_csv = CsvData()
    obj_config = Configuracion()
    
    fd.graficar_valores(obj_config)
    
        