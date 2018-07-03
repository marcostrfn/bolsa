#! /usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
import os

path_src = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(path_src)

import funciones.data as fd
from clases.Configuracion import Configuracion, CsvData


if __name__ == '__main__':
	''' calcula el mejor horario para el trading de un valor.
	deja el resultado en fichero result/horas.csv
	Lee los valores de fichero de configuración tag horas
	Graficos en graficos/horas'''
	
	obj_csv = CsvData()
	obj_config = Configuracion()
	
	fd.calculo_mejor_hora(obj_config,obj_csv,grafico=True)
	
	
				