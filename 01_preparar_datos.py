#! /usr/bin/env/python
# -*- coding: utf-8 -*-

import funciones.data as fd
from clases.Configuracion import Configuracion, CsvData


if __name__ == '__main__':
	''' lee un fichero json con valores y prepara un csv con datos para uso posterior
	(macd, rsi, estocastico, medias, etc. Deja el fichero en data/csv/xx/xx.csvç
	lee los valores desde fichero de configuracion, opcion descargar'''
		
	obj_csv = CsvData()
	obj_config = Configuracion()
	
	fd.preparar_datos_csv(obj_config,obj_csv)
	
