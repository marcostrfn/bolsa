#! /usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
import os

path_src = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(path_src)

import funciones.data as fd
from clases.Configuracion import Configuracion, CsvData



if __name__ == '__main__':
    ''' calcula la diferencia de precios de cierre de un valor
    en distintos horarios y deja el resultado en una grafica en
    graficos/comparativaHoraria'''

    obj_csv = CsvData()
    obj_config = Configuracion()
    
    fd.diferencia_cierre_horas(obj_config, obj_csv)