

#! /usr/bin/env/python
# -*- coding: utf-8 -*-



# https://tvc4.forexpros.com/68c02b45d81bc622207f060efd07ca9f/1523342501/4/4/58/history?symbol=1&resolution=D&from=1492238737&to=1523342797

from __future__ import print_function
import os
import funciones.data as fd
import shutil
# ===========================================================
# INICIO
# ===========================================================

FILENAME = 'valores.csv'
TIEMPO = 365 * 10
RESOLUCIONES = ['1', '5', '15', '30', '60', 'D', 'W', 'M'] # ['1','60','D','M','W'] 
TIPOS = None # ['IND'] # IND, FX, CMD, EQT


if __name__ == '__main__':

	valores = fd.cargar_valores_from_csv(TIPOS)
	for row in valores:
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		for resolucion in RESOLUCIONES:
		
			nombre = valor + '_' + resolucion + '.json'
			nuevo_nombre = valor + '.json'
			
			origen = os.path.join(os.path.dirname(__file__),'data',nombre)
			destino = os.path.join(os.path.dirname(__file__),'data',resolucion,nuevo_nombre)
			
			shutil.copyfile(origen, destino)
			
	for row in valores:
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		for resolucion in RESOLUCIONES:
		
			nombre = valor + '_' + resolucion + '.csv'
			nuevo_nombre = valor + '.csv'
			
			origen = os.path.join(os.path.dirname(__file__),'csv',nombre)
			destino = os.path.join(os.path.dirname(__file__),'csv',resolucion,nuevo_nombre)
			try:
				shutil.copyfile(origen, destino)
			except Exception as e:
				print (origen, e)
			