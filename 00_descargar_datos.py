#! /usr/bin/env/python
# -*- coding: utf-8 -*-


# https://tvc4.forexpros.com/68c02b45d81bc622207f060efd07ca9f/1523342501/4/4/58/history?symbol=1&resolution=D&from=1492238737&to=1523342797

from __future__ import print_function
import os, csv
import funciones.data as fd
import ConfigParser


# ===========================================================
# INICIO
# ===========================================================

FILENAME = 'valores.csv'
TIEMPO = 365 * 10
RESOLUCIONES = ['30', '60'] # ['1', '5', '15', '30', '60', 'D', 'W', 'M'] # ['1','60','D','M','W'] 
TIPOS = ['IND', 'FX', 'CMD']

configuracion = 'configuracion.cfg'


if __name__ == '__main__':

	# LECTURA DE VALORES DE CONFIGURACION
	config = ConfigParser.ConfigParser()
	config.read(configuracion)
	directorio_base = config.get('data', 'directorio_base')
	
	valores = fd.cargar_valores_from_csv(TIPOS)
	for row in valores:
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		if True: # valor=='BRENT':
			
			for resolucion in RESOLUCIONES:
				uri = fd.create_url(codigo,resolucion,TIEMPO)
				print ("descargando valor {: >10}({: >10}) Resolucion {: >5}".format(valor, codigo, resolucion))

				data = fd.get_json(uri)
				
				filename = valor + '.json'
				directorio_destino =  os.path.join(directorio_base,'data',resolucion)
				if not os.path.exists(directorio_destino):
					os.makedirs(directorio_destino)
					print ("creando directorio.... {}".format(directorio_destino))
				fname = os.path.join(directorio_destino,filename)
				
				print ("guardando archivo {}".format(fname))
				f = open(fname,'w')
				f.write(data)
				f.close()

