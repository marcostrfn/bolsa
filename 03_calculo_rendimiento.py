#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os, csv, sys, datetime
import funciones.bolsa as fb
import funciones.data as fd
import funciones.matematica as fm

# ===========================================================
# FUNCIONES
# ===========================================================
def print_resultado(tipo, valor, r500,r200,r100,r50,r20,r5):	
	s = "{0:<6} {1:<10} {2: >8.2f} {3: >8.2f} {4: >8.2f} {5: >8.2f} {6: >8.2f} {7: >8.2f}"
	print (s.format(tipo, valor, r500,r200,r100,r50,r20,r5))



	
# ===========================================================
# INICIO
# ===========================================================	
	
PROCESAR =	['ALL'] # VALOR A PROCESAR
PERIODO = 'D' # PERIODO DE TIEMPO A LEER 1,60,D,M
TIPOS = ['CMD', 'IND', 'FX']		

	
if __name__ == '__main__':

	resultados = []
	
	# todos los valores
	valores = fd.cargar_valores_from_csv(TIPOS)		
			
	for row in valores:
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		if valor in PROCESAR or PROCESAR[0] == "ALL":			
			rendimientos = []
			for x in [500,200,100,50,20,5]:
				data = fd.cargar_datos_valor(valor, PERIODO)				
				data = fd.get_datos(data)
				
				r = fm.rendimiento(data['close'], x)
				rendimientos.append(r)
					
			
			resultados.append([tipo, valor, rendimientos[0], rendimientos[1], rendimientos[2], rendimientos[3], rendimientos[4], rendimientos[5]])
			print_resultado(tipo, valor, rendimientos[0], rendimientos[1], rendimientos[2], rendimientos[3], rendimientos[4], rendimientos[5])

	resultados.sort(key=lambda (a,b,c,d,e,f,g,h):(c,d,e,f,g,h), reverse=True)

	ahora = datetime.datetime.now().strftime("%Y_%m_%d_%H%M")	
	filename = os.path.join(os.path.dirname(__file__), 'result', 'RENDIMIENTO_' + ahora + '.csv')
	with open( filename, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		dataset = ['tipo','valor','500','200','100','50','20','5']			
		spamwriter.writerow(dataset)
				
		for r in resultados:
			dataset = r
			spamwriter.writerow(dataset)
						



	
	
	
	


	
	
	
				
