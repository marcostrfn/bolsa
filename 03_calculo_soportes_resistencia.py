#! /usr/bin/env/python
# -*- coding: utf-8 -*-


from __future__ import print_function

import os, csv, datetime
import ConfigParser
import funciones.bolsa as fb
import funciones.data as fd


from clases.Configuracion import Configuracion, CsvData


if __name__ == '__main__':
	''' calcula soportes y resistencias diarias de un valor.
	deja el resultado en fichero result/pivot.csv
	Lee los valores de fichero de configuración tag calculo'''

	obj_csv = CsvData()
	obj_config = Configuracion()
	
	fd.calculo_soportes_resistencias(obj_config,obj_csv)
	
	
				