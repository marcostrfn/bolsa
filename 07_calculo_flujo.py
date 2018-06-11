#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os, csv, datetime
import ConfigParser
import funciones.bolsa as fb
import funciones.data as fd
import matplotlib.pyplot as plt
from pylab import *



# ===========================================================
# FUNCIONES
# ===========================================================

def print_resultado(registro):
	(valor, tipo, tiempo, hora, total_diferencia, media)= registro
	if tipo=="FX":
		s = "{:<10} {:>3}  {:>5} {:>5} {: >12.5f} {: >12.5f}"
	else:
		s = "{:<10} {:>3}  {:>5} {:>5} {: >12.2f} {: >12.2f}"
	
	print (s.format(valor, tipo, tiempo, hora, total_diferencia, media))

def print_cabecera(valor, PERIODO):
	print ('-'*79)
	print ("Calculo de {} en periodo de {}".format(valor, PERIODO))
	print ('-'*79)



def compara_dos_valores(d1,d2,periodo=250):

	titulo1 = 'NORMAL'
	titulo2 = 'SMART'  
	data1 = d1
	data2 = d2
	
	t = arange(0.0, len(data1[-periodo:]), 1)

	plt.subplot(2, 1, 1)
	plt.plot(t, data1[-periodo:])
	plt.title(titulo1)
	plt.grid(True)
 
	plt.subplot(2, 1, 2)
	plt.plot(t, data2[-periodo:])
	# plt.xlabel('Item (s)')
	# plt.ylabel(titulo2)
	plt.title(titulo2)
	plt.grid(True)


	plt.show()


def compara_dos_valores2(d1,d2,periodo=250):

	titulo1 = 'NORMAL VS SMART'
	data1 = d1
	data2 = d2
	
	t = arange(0.0, len(data1[-periodo:]), 1)

	
	plt.plot(t, data1[-periodo:])
	plt.plot(t, data2[-periodo:])
	plt.title(titulo1)
	plt.grid(True)

	plt.legend(['Normal', 'Smart'])



	plt.show()


# ===========================================================
# INICIO
# ===========================================================	
	
configuracion = 'configuracion.cfg'

if __name__ == '__main__':
	
	# LECTURA DE VALORES DE CONFIGURACION
	config = ConfigParser.ConfigParser()
	config.read(configuracion)
	PROCESAR, RESOLUCIONES, CSV_RESULTADOS, IMPRIMIR, CABECERA, TIPOS = fd.get_valores_proceso_flujo(config)

	resultados = []	
	horas = [
		'00:00',
		'00:30',
		'01:00',
		'01:30',
		'02:00',
		'02:30',
		'03:00',
		'03:30',
		'04:00',
		'04:30',
		'05:00',
		'05:30',
		'06:00',
		'06:30',
		'07:00',
		'07:30',
		'08:00',
		'08:30',
		'09:00',
		'09:30',
		'10:00',
		'10:30',
		'11:00',
		'11:30',
		'12:00',
		'12:30',
		'13:00',
		'13:30',
		'14:00',
		'14:30',
		'15:00',
		'15:30',
		'16:00',
		'16:30',
		'17:00',
		'17:30',
		'18:00',
		'18:30',
		'19:00',
		'19:30',
		'20:00',
		'20:30',
		'21:00',
		'21:30',
		'22:00',
		'22:30',		
		'23:00',
		'23:30'
	]
	
	horas_dax = [
		'08:00',
		'21:00',
		'21:30'
	]


	array1 = []
	array2 = []
	# SELECCION DE VALORES
	valores = fd.cargar_valores_from_csv(TIPOS)	
	for row in valores:		
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		if valor in PROCESAR or PROCESAR[0] == "ALL":
			
			puntos_apertura = []
			puntos_cierre = []
			puntos_cierre_1 = []
			puntos_cierre_2 = []



					
			for PERIODO in RESOLUCIONES:				
				# POR CADA VALOR Y PERIODO
				if True:
					VALOR_PROCESAR = valor							
					if CABECERA and IMPRIMIR: print_cabecera(VALOR_PROCESAR, PERIODO)
					
					# CARGA DE VALORES
					data = fd.cargar_datos_valor(VALOR_PROCESAR, PERIODO)
						
					# TRATMIENTO DE LOS VALORES RECIBIDOS
					resultado_valor = fb.procesar_valores_flujo(VALOR_PROCESAR, PERIODO, tipo, fd.get_datos(data,3000), config)					

					apertura = resultado_valor['08:00']
					cierre =  (resultado_valor['21:00'], resultado_valor['21:30'])
								
					for a in apertura:
						fecha = a[0]
						open = a[1]
						close = a[2]

						valor = close - open 
						
						puntos_apertura.append((a[0],a[1],valor))


					for a in cierre[0]:
						fecha = a[0]
						open = a[1]
						close = a[2]

						valor = close - open 
						
						puntos_cierre_1.append((a[0],a[1],valor))

					for a in cierre[1]:
						fecha = a[0]
						open = a[1]
						close = a[2]

						valor = close - open 
						
						puntos_cierre_2.append((a[0],a[1],valor))
 

					
					# print (len(puntos_apertura))
					# print (len(puntos_cierre_1))
					# print (len(puntos_cierre_2))
					
					for a in range(0,len(puntos_apertura)):
						fecha_1 = puntos_apertura[a][0].split(' ')
						fecha_2 = puntos_cierre_1[a][0].split(' ')
						fecha_3 = puntos_cierre_2[a][0].split(' ')
						# print (fecha_1,fecha_2,fecha_3)

					
					for a in range(0,len(puntos_apertura)):
						puntos_1 = puntos_cierre_1[a][2]
						puntos_2 = puntos_cierre_2[a][2]
						valor = puntos_1 + puntos_2
						puntos_cierre.append((puntos_cierre_1[a][0], valor))
						# print (puntos_apertura[a],puntos_cierre_1[a], puntos_cierre_2[a])

					smart_money = []
					
					
				
					for a in range(0,len(puntos_apertura)):
						fecha1 = puntos_apertura[a]
						fecha = fecha1[0].split(' ')
						puntos =  puntos_apertura[a][1]
						
						pt_apertura =  puntos_apertura[a][2]
						pt_cierre =  puntos_cierre[a][1]
						
						puntos_smart = puntos - pt_apertura + pt_cierre
						smart_money.append((fecha[0],puntos, puntos_smart))
					
					for a in range(1,len(smart_money)):
						fecha_a, puntos_a, puntos_smart_a = smart_money[a-1]
						fecha, puntos, puntos_smart = smart_money[a]

						if puntos_smart > puntos_smart_a:
							indicador_fin = '+'
						else:
							indicador_fin = '-'
							
						if puntos > puntos_a:
							indicador_ini = '+'
						else:
							indicador_ini = '-'
							
						print ("{:>8} {} {: >12.2f} {: >12.2f} {}".format(fecha, indicador_ini, puntos, puntos_smart, indicador_fin))
						
						array1.append(puntos)
						array2.append(puntos_smart)


			print (array1)
			print (array2)
			compara_dos_valores2(array1,array2,len(array1))
						
					
			#mi_valor.sort(key=lambda (a,b,c,d,e,f):(f), reverse=True)
			#for m in mi_valor:
			#	(valor, tipo, PERIODO, hora, total_diferencia, media) = m
			#	print_resultado(m)
				
				
			# resultados.append(resultado_valor[0])
					
					# IMPRIMIMOS RESULTADOS
					# if IMPRIMIR: 
					#	for r in resultado_valor: print_resultado(r)
					
						

					
	
	
	# ESCRIBIR FICHERO CSV CON RESULTADOS
	# if CSV_RESULTADOS=='si': fd.escribir_csv_resultados(resultados)	

