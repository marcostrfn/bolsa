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
	valor, tiempo, tipo, titulo,  periodo, numero_operaciones, total, largos, cortos = registro
	s = "{:<10} {:>3}  {:<15} {:>2} {:>4} {: >4} {: >12.2f} {: >12.2f} {: >12.2f}"
	print (s.format(valor, tipo, titulo, tiempo, periodo, numero_operaciones, total, largos, cortos))

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
	PROCESAR, RESOLUCIONES, CSV_RESULTADOS, IMPRIMIR, CABECERA, TIPOS = fd.get_valores_proceso(config)

	resultados = []	

	# SELECCION DE VALORES
	
	valores = fd.cargar_valores_from_csv(TIPOS)	
	for row in valores:
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		if valor in PROCESAR or PROCESAR[0] == "ALL":		
			for PERIODO in RESOLUCIONES:
				
				# POR CADA VALOR Y PERIODO
				try:
					VALOR_PROCESAR = valor							
					if CABECERA and IMPRIMIR: print_cabecera(VALOR_PROCESAR, PERIODO)
					
					# CARGA DE VALORES
					data = fd.cargar_datos_valor(VALOR_PROCESAR, PERIODO)
						
					# TRATMIENTO DE LOS VALORES RECIBIDOS
					resultado_valor = fb.procesar_valores(VALOR_PROCESAR, PERIODO, tipo, fd.get_datos(data,500), config)					
					resultado_valor.sort(key=lambda (a,b,c,d,e,f,g,h,i):(g,h), reverse=True)
					resultados.append(resultado_valor[0])
					
					# IMPRIMIMOS RESULTADOS
					if IMPRIMIR: 
						for r in resultado_valor: print_resultado(r)
					
						
				except Exception as e:
					print ("Error {} {} {}".format(VALOR_PROCESAR, PERIODO, e))
					
	
	
	# ESCRIBIR FICHERO CSV CON RESULTADOS
	if CSV_RESULTADOS=='si': fd.escribir_csv_resultados(resultados)	

