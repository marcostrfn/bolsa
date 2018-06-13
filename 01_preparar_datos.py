#! /usr/bin/env/python
# -*- coding: utf-8 -*-



from __future__ import print_function
import os, csv, sys
from datetime import datetime
import funciones.data as fd
import funciones.bolsa as fb
import ConfigParser


def procesar_valor(VALOR,CODIGO,RESOLUCION,DIRECTORIO_BASE):
	
	fname = VALOR 
	print ("procesando valor {:<10} Resolución {:>3}".format(fname, RESOLUCION))
	
	data = fd.get_json_file(fname, RESOLUCION)
	
	cierre,apertura,high,low = fd.set_arrays_from_json_data(data)
	if cierre == None: 
		print ("Error al procesar ", fname)
		return 
	
	lecturas = len(cierre)	
	fecha = fb.get_fechas(data)
	
	
	
	file_path = os.path.join(DIRECTORIO_BASE, 'csv', RESOLUCION, fname + '.csv')	
	
	if os.path.exists(file_path):
		print ('\t\t Existe {}'.format(file_path))
		data = fd.cargar_valores(VALOR,RESOLUCION)
		datetime_json = datetime.strptime(fecha[-1], "%Y-%m-%d %H:%M")
		datetime_file = datetime.strptime(data['fecha'][-1], "%Y-%m-%d %H:%M")
		# nada que hacer, las fechas no son superiores
		if datetime_json <= datetime_file:
			cierre_json = cierre[-1]
			cierre_file = data['close'][-1]	
			if cierre_json == cierre_file:
				print ('\t\t Saliendo sin cambios, nada que anexar')
				# print ('\t\t', cierre_file, cierre_json)
				return
	
	# print (len(fecha), len(cierre),len(apertura),len(high),len(low))
	
	
	macd, macd_signal, macd_histograma = fb.get_macd(cierre,12,26,9)
	
	rsi14 = fb.calcular_rsi(14, cierre)
	rsi50 = fb.calcular_rsi(50, cierre)
	
	estocastico_sk_14, estocastico_sd_14 = fb.calcular_estocastico(cierre, high, low, 14, 3)
	estocastico_sk_50, estocastico_sd_50 = fb.calcular_estocastico(cierre, high, low, 14, 3)	
		
	# sma = [0]*201
	# ema = [0]*201
	
	#calcula emas de 5 a 200
	sma5 = fb.get_sma_periodo(5,cierre)
	ema5 = fb.get_ema_periodo(5,cierre)

	sma20 = fb.get_sma_periodo(20,cierre)
	ema20 = fb.get_ema_periodo(20,cierre)
	
	sma200 = fb.get_sma_periodo(200,cierre)
	ema200 = fb.get_ema_periodo(200,cierre)

	sma100 = fb.get_sma_periodo(100,cierre)
	ema100 = fb.get_ema_periodo(100,cierre)

	sma50 = fb.get_sma_periodo(50,cierre)
	ema50 = fb.get_ema_periodo(50,cierre)
	
	sma400 = fb.get_sma_periodo(400,cierre)
	ema400 = fb.get_ema_periodo(400,cierre)
	
	
	
	# print ('desde {} hasta {}'.format(fecha[0], fecha[-1]))
	
	directorio_destino =  os.path.join(DIRECTORIO_BASE, 'csv', RESOLUCION)	
	if not os.path.exists(directorio_destino):
		os.makedirs(directorio_destino)
		print ("creando directorio.... {}".format(directorio_destino))
	
	
	
	file_path = os.path.join(DIRECTORIO_BASE, 'csv', RESOLUCION, fname + '.csv')	
	if os.path.exists(file_path):		
		data = fd.cargar_valores(VALOR,RESOLUCION)
		
		datetime_json = datetime.strptime(fecha[-1], "%Y-%m-%d %H:%M")
		datetime_file = datetime.strptime(data['fecha'][-1], "%Y-%m-%d %H:%M")
			
		print ("\t\t anexando desde {}".format(data['fecha'][-1]))
		# print ('append fechas nuevas desde {} hasta {}'.format(data['fecha'][-1], fecha[-1] ))
	
		# aqui tenemos que modificar el ultimo valor en caso de que haya variacion
		# puedo cargar los valores a cargar en dataset y luego añadirlos al fichero csv
		# y luego recorrer el fichero y eliminar el penultimo valor
		
		with open( file_path, 'ab') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			# dataset = ['fecha','apertura','cierre','high','low','macd','macd_signal','macd_histograma','rsi14','rsi50','esk14','esd14','esk50', 'esd50','sma[5]','ema[5]','sma[20]','ema[20]','sma[50]','ema[50]','sma[100]','ema[100]','sma[200]','ema[200]','sma[400]','ema[400]']			
			# spamwriter.writerow(dataset)
				
			for x in range(0, len(fecha)):
				datetime_json = datetime.strptime(fecha[x], "%Y-%m-%d %H:%M")
				if datetime_json > datetime_file: # if datetime_json >= datetime_file: anade fila nueva	repitiendo		
					dataset = [fecha[x],apertura[x],cierre[x],high[x],low[x],macd[x],macd_signal[x],macd_histograma[x],rsi14[x],rsi50[x],estocastico_sk_14[x],estocastico_sd_14[x],estocastico_sk_50[x], estocastico_sd_50[x], sma5[x], ema5[x], sma20[x], ema20[x], sma50[x], ema50[x], sma100[x], ema100[x], sma200[x], ema200[x], sma400[x], ema400[x]]			
					spamwriter.writerow(dataset)
					# print ("\t\t Anadiendo {}".format(datetime_json))
				# else:
					# print ("\t\t Saliendo en {}".format(datetime_file))
		
	else:
		print ('\t\t nuevo {}'.format(file_path))
		with open( file_path, 'wb') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			dataset = ['fecha','apertura','cierre','high','low','macd','macd_signal','macd_histograma','rsi14','rsi50','esk14','esd14','esk50', 'esd50','sma[5]','ema[5]','sma[20]','ema[20]','sma[50]','ema[50]','sma[100]','ema[100]','sma[200]','ema[200]','sma[400]','ema[400]']			
			spamwriter.writerow(dataset)
				
			for x in range(0,lecturas):
				dataset = [fecha[x],apertura[x],cierre[x],high[x],low[x],macd[x],macd_signal[x],macd_histograma[x],rsi14[x],rsi50[x],estocastico_sk_14[x],estocastico_sd_14[x],estocastico_sk_50[x], estocastico_sd_50[x], sma5[x], ema5[x], sma20[x], ema20[x], sma50[x], ema50[x], sma100[x], ema100[x], sma200[x], ema200[x], sma400[x], ema400[x]]			
				spamwriter.writerow(dataset)
		
	
		
	
# ===========================================================
# INICIO
# ===========================================================

PROCESAR =  'ALL' # ['DE30', 'EURUSD'] # VALOR A PROCESAR
RESOLUCIONES = ['30', '60']
TIPOS = ['IND','FX','CMD'] # IND, FX, CMD, EQT NONE TODOS
configuracion = 'configuracion.cfg'


def main():
	
	# LECTURA DE VALORES DE CONFIGURACION
	config = ConfigParser.ConfigParser()
	config.read(configuracion)
	directorio_base = config.get('data', 'directorio_base')
	
	valores = fd.cargar_valores_from_csv(None)
	for row in valores:
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		if valor in PROCESAR or PROCESAR=='ALL': 
			for RESOLUCION in RESOLUCIONES:
				try:
					procesar_valor(valor,codigo,RESOLUCION,directorio_base)
				except:
					print ("error al procesar {}".format(valor))

if __name__ == '__main__':
	main()
	
	
