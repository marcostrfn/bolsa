#! /usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
import os

path_src = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(path_src)

import funciones.data as fd
from clases.Configuracion import Configuracion, CsvData


if __name__ == '__main__': 
	''' calcula la mejor media simple para el trading de un valor.
	deja el resultado en fichero result/medias.csv
	Lee los valores de fichero de configuración tag calculo'''
	
	obj_csv = CsvData()
	obj_config = Configuracion()
	
	
	fd.calculo_mejor_valor(obj_config,obj_csv)
	
