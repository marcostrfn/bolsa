#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os, csv, datetime
import ConfigParser
import funciones.bolsa as fb
import funciones.data as fd


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





# ===========================================================
# INICIO
# ===========================================================	
	
configuracion = 'configuracion.cfg'

if __name__ == '__main__':
	
	# LECTURA DE VALORES DE CONFIGURACION
	config = ConfigParser.ConfigParser()
	config.read(configuracion)
	PROCESAR, RESOLUCIONES, CSV_RESULTADOS, IMPRIMIR, CABECERA, TIPOS = fd.get_valores_proceso_hora(config)

	resultados = []	
	horas = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']

	# SELECCION DE VALORES
	valores = fd.cargar_valores_from_csv(TIPOS)	
	for row in valores:		
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		if valor in PROCESAR or PROCESAR[0] == "ALL":
			
			mi_valor = []
					
			for PERIODO in RESOLUCIONES:				
				# POR CADA VALOR Y PERIODO
				if True:
					VALOR_PROCESAR = valor							
					if CABECERA and IMPRIMIR: print_cabecera(VALOR_PROCESAR, PERIODO)
					
					# CARGA DE VALORES
					data = fd.cargar_datos_valor(VALOR_PROCESAR, PERIODO)
						
					# TRATMIENTO DE LOS VALORES RECIBIDOS
					resultado_valor = fb.procesar_valores_hora(VALOR_PROCESAR, PERIODO, tipo, fd.get_datos(data,500), config)					
					
					for hora in horas:
						total_diferencia = 0
						total_valores = 0
						
						for par in resultado_valor[hora]:
							diferencia = par[0] - par[1]								
							total_valores += 1
							total_diferencia += diferencia
						
						try:
							# print_resultado((valor, tipo, PERIODO, hora, total_diferencia, total_diferencia/total_valores))
							mi_valor.append([valor, tipo, PERIODO, hora, total_diferencia, total_diferencia/total_valores])
						except:
							# print_resultado((valor, tipo, PERIODO, hora, total_diferencia, 0))
							mi_valor.append([valor, tipo, PERIODO, hora, total_diferencia, 0])
							
			
					
					
			mi_valor.sort(key=lambda (a,b,c,d,e,f):(f), reverse=True)
			for m in mi_valor:
				(valor, tipo, PERIODO, hora, total_diferencia, media) = m
				print_resultado(m)
				
				
			# resultados.append(resultado_valor[0])
					
					# IMPRIMIMOS RESULTADOS
					# if IMPRIMIR: 
					#	for r in resultado_valor: print_resultado(r)
					
						

					
	
	
	# ESCRIBIR FICHERO CSV CON RESULTADOS
	# if CSV_RESULTADOS=='si': fd.escribir_csv_resultados(resultados)	

