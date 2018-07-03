#! /usr/bin/env/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import sys
import os

path_src = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(path_src)

import funciones.data as fd
from clases.Configuracion import Configuracion, CsvData


if __name__ == '__main__':
	''' descarga datos en json desde investing.com. Resultado en data/XX/XX.json 
	Lee los valores a descargar desde fichero configuracion con etiqueta [descargar]'''
	
	obj_csv = CsvData()
	obj_config = Configuracion()
	
	fd.descargar_datos(obj_config,obj_csv)
