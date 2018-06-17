#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import datetime, timedelta
from time import mktime
import urllib, json, os
import ssl, csv
import ConfigParser

import bolsa as fb
import graficos as fg


def escribir_csv_resultados_pivot(resultados):
	
	config = ConfigParser.ConfigParser()
	config.read('configuracion.cfg')
	directorio_base = config.get('data', 'directorio_base')

	directorio_destino =  os.path.join(directorio_base,'result')
	if not os.path.exists(directorio_destino):
		os.makedirs(directorio_destino)
		print ("creando directorio.... {}".format(directorio_destino))
	
	
	filename = os.path.join(directorio_base, 'result', 'pivot.csv')
	with open( filename, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		dataset = ['valor', 's3', 's2', 's1', 'pp', 'r1', 'r2', 'r3']			
		spamwriter.writerow(dataset)
						
		for v in resultados:
			valor,datos = v
			s3, s2, s1, pp, r1, r2, r3 = datos
			dataset = [valor, s3, s2, s1, pp, r1, r2, r3]
			spamwriter.writerow(dataset)
				



def calculoSoportesResistencias(grafico=None):
	
	configuracion = 'configuracion.cfg'
	# LECTURA DE VALORES DE CONFIGURACION
	config = ConfigParser.ConfigParser()
	config.read(configuracion)
	PROCESAR = config.get('calculo', 'PROCESAR').split(',')

	resultados = []	
	
	# SELECCION DE VALORES
	valores = cargar_valores_from_csv(None)	
	for row in valores:		
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		if valor in PROCESAR:

			
			data = cargar_datos_valor(valor, 'D')
			
			pivot = fb.calcular_pivot_fibo(data['close'], data['high'], data['low'])
			
			resultados.append((valor,pivot[-1]))
			
	# ESCRIBIR FICHERO CSV CON RESULTADOS
	escribir_csv_resultados_pivot(resultados)

	



def getMejorMedia(VALOR, PERIODO):
	
    config = ConfigParser.ConfigParser()
    config.read('configuracion.cfg')
    directorio_base = config.get('data', 'directorio_base')
	
    filename = os.path.join(directorio_base, 'result', 'medias.csv')
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
        	valor,tiempo,funcion,periodo,numero_operaciones,total,largos,cortos = row
        	if valor==VALOR and tiempo==PERIODO:
        		return periodo
               
               
               

def print_resultado_mejor_hora(registro):
	(valor, tipo, tiempo, hora, total_diferencia, media)= registro
	if tipo=="FX":
		s = "{:<10} {:>3}  {:>5} {:>5} {: >12.5f} {: >12.5f}"
	else:
		s = "{:<10} {:>3}  {:>5} {:>5} {: >12.2f} {: >12.2f}"
	
	print (s.format(valor, tipo, tiempo, hora, total_diferencia, media))

def print_cabecera_mejor_hora(valor, PERIODO):
	print ('-'*79)
	print ("calculo de {} en periodo de {}".format(valor, PERIODO))
	print ('-'*79)


	
def calculoMejorHora(grafico=None):
	
	configuracion = 'configuracion.cfg'
	# LECTURA DE VALORES DE CONFIGURACION
	config = ConfigParser.ConfigParser()
	config.read(configuracion)
	PROCESAR, RESOLUCIONES, CSV_RESULTADOS, IMPRIMIR, CABECERA, TIPOS = get_valores_proceso_hora(config)

	resultados = []	
	horas = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']

	# SELECCION DE VALORES
	valores = cargar_valores_from_csv(TIPOS)	
	for row in valores:		
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		if valor in PROCESAR:
			
			mi_valor = []
					
			for PERIODO in RESOLUCIONES:				
				# POR CADA VALOR Y PERIODO
				if True:
					VALOR_PROCESAR = valor							
					if CABECERA and IMPRIMIR: print_cabecera_mejor_hora(VALOR_PROCESAR, PERIODO)
					
					# CARGA DE VALORES
					data = cargar_datos_valor(VALOR_PROCESAR, PERIODO)
						
					# TRATMIENTO DE LOS VALORES RECIBIDOS
					resultado_valor = fb.procesar_valores_hora(VALOR_PROCESAR, PERIODO, tipo, get_datos(data,500), config)					
					
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

			if grafico:
				fg.graficarMejorHora(mi_valor)

			mi_valor.sort(key=lambda (a,b,c,d,e,f):(f), reverse=True)
			for m in mi_valor:
				(valor, tipo, PERIODO, hora, total_diferencia, media) = m
				print_resultado_mejor_hora(m)
		
			resultados.append(mi_valor)
			
		# ESCRIBIR FICHERO CSV CON RESULTADOS
	if CSV_RESULTADOS=='si': escribir_csv_resultados_hora(resultados)
	


def escribir_csv_resultados_hora(resultados):
	
	config = ConfigParser.ConfigParser()
	config.read('configuracion.cfg')
	directorio_base = config.get('data', 'directorio_base')

	directorio_destino =  os.path.join(directorio_base,'result')
	if not os.path.exists(directorio_destino):
		os.makedirs(directorio_destino)
		print ("creando directorio.... {}".format(directorio_destino))
	
	
	filename = os.path.join(directorio_base, 'result', 'horas.csv')
	with open( filename, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		dataset = ['valor', 'tipo', 'periodo', 'hora', 'pip', 'media']			
		spamwriter.writerow(dataset)
						
		for v in resultados:
			for r in v:
				valor, tipo, periodo, hora, pip, media = r
				dataset = [valor, tipo, periodo, hora, pip, media]
				spamwriter.writerow(dataset)
				
				
				
def print_resultado(registro):
	valor, tiempo, tipo, titulo,  periodo, numero_operaciones, total, largos, cortos = registro
	s = "{:<10} {:>3}  {:<15} {:>2} {:>4} {: >4} {: >12.2f} {: >12.2f} {: >12.2f}"
	print (s.format(valor, tipo, titulo, tiempo, periodo, numero_operaciones, total, largos, cortos))

def print_cabecera(valor, PERIODO):
	print ('-'*79)
	print ("calculo de {} en periodo de {}".format(valor, PERIODO))
	print ('-'*79)


def calculoMejorValor():
	
	configuracion = 'configuracion.cfg'
	# LECTURA DE VALORES DE CONFIGURACION
	config = ConfigParser.ConfigParser()
	config.read(configuracion)
	PROCESAR, RESOLUCIONES, CSV_RESULTADOS, IMPRIMIR, CABECERA, TIPOS = get_valores_proceso(config)

	resultados = []	

	# SELECCION DE VALORES
	
	valores = cargar_valores_from_csv(TIPOS)	
	for row in valores:
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		if valor in PROCESAR or PROCESAR[0] == "ALL":		
			for PERIODO in RESOLUCIONES:
				
				# POR CADA VALOR Y PERIODO
				try:
					VALOR_PROCESAR = valor							
					if CABECERA and IMPRIMIR: print_cabecera(VALOR_PROCESAR, PERIODO)
					
					# CARGA DE VALORES
					data = cargar_datos_valor(VALOR_PROCESAR, PERIODO)
						
					# TRATMIENTO DE LOS VALORES RECIBIDOS
					resultado_valor = fb.procesar_valores(VALOR_PROCESAR, PERIODO, tipo, get_datos(data,500), config)					
					resultado_valor.sort(key=lambda (a,b,c,d,e,f,g,h,i):(g,h), reverse=True)
					resultados.append(resultado_valor[0])
					
					# IMPRIMIMOS RESULTADOS
					if IMPRIMIR: 
						for r in resultado_valor: print_resultado(r)
					
						
				except Exception as e:
					print ("Error {} {} {}".format(VALOR_PROCESAR, PERIODO, e))
					
	
	
	# ESCRIBIR FICHERO CSV CON RESULTADOS
	if CSV_RESULTADOS=='si': escribir_csv_resultados(resultados)	
	
	
	
def procesar_valor(VALOR,CODIGO,RESOLUCION,DIRECTORIO_BASE):
	
	fname = VALOR 
	print ("procesando valor {:<10} Resolucion {:>3}".format(fname, RESOLUCION))
	
	data = get_json_file(fname, RESOLUCION)
	
	cierre,apertura,high,low = set_arrays_from_json_data(data)
	if cierre == None: 
		print ("error al procesar ", fname)
		return 
	
	lecturas = len(cierre)	
	fecha = fb.get_fechas(data)
	
	
	
	file_path = os.path.join(DIRECTORIO_BASE, 'csv', RESOLUCION, fname + '.csv')	
	
	if os.path.exists(file_path):
		print ('existe {}'.format(file_path))
		data = cargar_valores(VALOR,RESOLUCION)
		datetime_json = datetime.strptime(fecha[-1], "%Y-%m-%d %H:%M")
		datetime_file = datetime.strptime(data['fecha'][-1], "%Y-%m-%d %H:%M")
		# nada que hacer, las fechas no son superiores
		if datetime_json <= datetime_file:
			cierre_json = cierre[-1]
			cierre_file = data['close'][-1]	
			if cierre_json == cierre_file:
				print ('saliendo sin cambios, nada que anexar')
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
		data = cargar_valores(VALOR,RESOLUCION)
		
		datetime_json = datetime.strptime(fecha[-1], "%Y-%m-%d %H:%M")
		datetime_file = datetime.strptime(data['fecha'][-1], "%Y-%m-%d %H:%M")
			
		print ("anexando desde {}".format(data['fecha'][-1]))
		# print ('append fechas nuevas desde {} hasta {}'.format(data['fecha'][-1], fecha[-1] ))
	
		# aqui tenemos que modificar el ultimo valor en caso de que haya variacion
		# puedo cargar los valores a cargar en dataset y luego a�adirlos al fichero csv
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
		print ('nuevo {}'.format(file_path))
		with open( file_path, 'wb') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			dataset = ['fecha','apertura','cierre','high','low','macd','macd_signal','macd_histograma','rsi14','rsi50','esk14','esd14','esk50', 'esd50','sma[5]','ema[5]','sma[20]','ema[20]','sma[50]','ema[50]','sma[100]','ema[100]','sma[200]','ema[200]','sma[400]','ema[400]']			
			spamwriter.writerow(dataset)
				
			for x in range(0,lecturas):
				dataset = [fecha[x],apertura[x],cierre[x],high[x],low[x],macd[x],macd_signal[x],macd_histograma[x],rsi14[x],rsi50[x],estocastico_sk_14[x],estocastico_sd_14[x],estocastico_sk_50[x], estocastico_sd_50[x], sma5[x], ema5[x], sma20[x], ema20[x], sma50[x], ema50[x], sma100[x], ema100[x], sma200[x], ema200[x], sma400[x], ema400[x]]			
				spamwriter.writerow(dataset)




def prepararDatos():
	configuracion = 'configuracion.cfg'
	# LECTURA DE VALORES DE CONFIGURACION
	config = ConfigParser.ConfigParser()
	config.read(configuracion)
	directorio_base = config.get('data', 'directorio_base')
	TIPOS = config.get('descargar', 'TIPOS').split(',')
	RESOLUCIONES = config.get('descargar', 'RESOLUCIONES').split(',')
	PROCESAR = config.get('descargar', 'PROCESAR').split(',')
	
	
	valores = cargar_valores_from_csv(None)
	for row in valores:
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		if valor in PROCESAR: 
			for RESOLUCION in RESOLUCIONES:
				try:
					procesar_valor(valor,codigo,RESOLUCION,directorio_base)
				except:
					print ("error al procesar {}".format(valor))
					
def descargarDatos():

	TIEMPO = 365 * 10
	FILENAME = 'valores.csv'
	configuracion = 'configuracion.cfg'
	
	# LECTURA DE VALORES DE CONFIGURACION
	config = ConfigParser.ConfigParser()
	config.read(configuracion)
	directorio_base = config.get('data', 'directorio_base')
	TIPOS = config.get('descargar', 'TIPOS').split(',')
	RESOLUCIONES = config.get('descargar', 'RESOLUCIONES').split(',')
	PROCESAR = config.get('descargar', 'PROCESAR').split(',')
	
	valores = cargar_valores_from_csv(TIPOS)
	for row in valores:
		valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
		if valor in PROCESAR:
			for resolucion in RESOLUCIONES:
				uri = create_url(codigo,resolucion,TIEMPO)
				print ("descargando valor {: >10}({: >10}) Resolucion {: >5}".format(valor, codigo, resolucion))

				data = get_json(uri)
				
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
				

def escribir_csv_resultados(resultados):
	
	config = ConfigParser.ConfigParser()
	config.read('configuracion.cfg')
	directorio_base = config.get('data', 'directorio_base')

	ahora = datetime.now().strftime("%Y_%m_%d_%H_%M")
	
	
	directorio_destino =  os.path.join(directorio_base,'result')
	if not os.path.exists(directorio_destino):
		os.makedirs(directorio_destino)
		print ("creando directorio.... {}".format(directorio_destino))
	
	
	filename = os.path.join(directorio_base, 'result', 'medias.csv')
	with open( filename, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		dataset = ['valor', 'tiempo', 'funcion', 'periodo', 'numero_operaciones', 'total', 'largos', 'cortos']			
		spamwriter.writerow(dataset)
						
		for r in resultados:
			valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos = r
			dataset = [valor, tiempo, titulo, periodo, numero_operaciones, total, largos, cortos]
			spamwriter.writerow(dataset)
			

def get_valores_proceso(config):
	
	IMPRIMIR = False
	CABECERA = False
	
	
	PROCESAR = config.get('calculo', 'PROCESAR').split(',')
	RESOLUCIONES = config.get('calculo', 'RESOLUCIONES').split(',')
	CSV_RESULTADOS = config.get('calculo', 'CSV_RESULTADOS')
	CABECERA = config.get('resultados', 'CABECERA')
	IMPRIMIR = config.get('resultados', 'IMPRIMIR')
	
	if CABECERA=='si': 
		CABECERA = True
	else:
		CABECERA = False
		
	if IMPRIMIR=='si': 
		IMPRIMIR = True
	else:
		IMPRIMIR = False
	
	
	TIPOS = config.get('calculo', 'TIPOS')
	if TIPOS=='None':
		TIPOS=None
	else:
		TIPOS = TIPOS.split(',')
	
	
	return PROCESAR, RESOLUCIONES, CSV_RESULTADOS, IMPRIMIR, CABECERA, TIPOS



def get_valores_proceso_hora(config):
	
	IMPRIMIR = False
	CABECERA = False
	
	
	PROCESAR = config.get('hora', 'PROCESAR').split(',')
	RESOLUCIONES = config.get('hora', 'RESOLUCIONES').split(',')	
	CSV_RESULTADOS = config.get('hora', 'CSV_RESULTADOS')
	CABECERA = config.get('resultados', 'CABECERA')
	IMPRIMIR = config.get('resultados', 'IMPRIMIR')
	
	if CABECERA=='si': 
		CABECERA = True
	else:
		CABECERA = False
		
	if IMPRIMIR=='si': 
		IMPRIMIR = True
	else:
		IMPRIMIR = False
	
	
	TIPOS = config.get('hora', 'TIPOS')
	if TIPOS=='None':
		TIPOS=None
	else:
		TIPOS = TIPOS.split(',')
	
	
	return PROCESAR, RESOLUCIONES, CSV_RESULTADOS, IMPRIMIR, CABECERA, TIPOS



def get_valores_proceso_flujo(config):
	
	IMPRIMIR = False
	CABECERA = False
	
	
	PROCESAR = config.get('flujo', 'PROCESAR').split(',')
	RESOLUCIONES = config.get('flujo', 'RESOLUCIONES').split(',')	
	CSV_RESULTADOS = config.get('flujo', 'CSV_RESULTADOS')
	CABECERA = config.get('resultados', 'CABECERA')
	IMPRIMIR = config.get('resultados', 'IMPRIMIR')
	
	if CABECERA=='si': 
		CABECERA = True
	else:
		CABECERA = False
		
	if IMPRIMIR=='si': 
		IMPRIMIR = True
	else:
		IMPRIMIR = False
	
	
	TIPOS = config.get('flujo', 'TIPOS')
	if TIPOS=='None':
		TIPOS=None
	else:
		TIPOS = TIPOS.split(',')
	
	
	return PROCESAR, RESOLUCIONES, CSV_RESULTADOS, IMPRIMIR, CABECERA, TIPOS



def cargar_valores_from_csv(tipos=None):
	data = []
	fname = os.path.join(os.path.dirname(__file__),'..','valores.csv')
	with open(fname, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';')
		for row in spamreader:
			valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
			if tipos is None:
				data.append(row)
			elif tipo in tipos:
					data.append(row)

	return data
	
def cargar_datos_valor(valor, periodo='D'):
	data = []
	fname = os.path.join(os.path.dirname(__file__),'..','valores.csv')
	with open(fname, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';')
		for row in spamreader:
			v,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
			if v == valor:
				data = cargar_valores(valor,periodo)

	return data

	
def get_datos(data,numero=500):

	data['fecha'] = data['fecha'][-numero:]
	data['open'] = data['open'][-numero:]
	data['close'] = data['close'][-numero:]
	data['high'] = data['high'][-numero:]
	data['low'] = data['low'][-numero:]
	data['macd'] = data['macd'][-numero:]
	data['macd_signal'] = data['macd_signal'][-numero:]
	data['macd_histograma'] = data['macd_histograma'][-numero:]
	data['rsi14'] = data['rsi14'][-numero:]
	data['rsi50'] = data['rsi50'][-numero:]
	data['esk14'] = data['esk14'][-numero:]
	data['esd14'] = data['esd14'][-numero:]
	data['esk50'] = data['esk50'][-numero:]
	data['esd50'] = data['esd50'][-numero:]
	data['sma5'] = data['sma5'][-numero:]
	data['ema5'] = data['ema5'][-numero:]
	data['sma20'] = data['sma20'][-numero:]
	data['ema20'] = data['ema20'][-numero:]
	data['sma50'] = data['sma50'][-numero:]
	data['ema50'] = data['ema50'][-numero:]
	data['sma100'] = data['sma100'][-numero:]
	data['ema100'] = data['ema100'][-numero:]
	data['sma200'] = data['sma200'][-numero:]
	data['ema200'] = data['ema200'][-numero:]
	data['sma400'] = data['sma400'][-numero:]
	data['ema400'] = data['ema400'][-numero:]
	data['registros'] = len(data['fecha'])
	
	return data
	

def preparar_datos(spamreader):
		
	fecha = []
	apertura = []
	cierre = []
	high = []
	low = []
	macd = []
	macd_signal = []
	macd_histograma = []
	rsi14 = []
	rsi50 = []
	esk14 = []
	esd14 = []
	esk50 = []
	esd50 = []
	sma5 = []
	ema5 = []
	sma20 = []
	ema20 = []
	sma50 = []
	ema50 = []
	sma100 = []
	ema100 = []
	sma200 = []
	ema200 = []
	sma400 = []
	ema400 = []
		
	for row in spamreader:
		vfecha,vapertura,vcierre,vhigh,vlow,vmacd,vmacd_signal,vmacd_histograma, \
			vrsi14,vrsi50,vesk14,vesd14,vesk50,vesd50,vsma5,vema5,vsma20,vema20,vsma50,vema50,vsma100,vema100,vsma200,vema400,vsma400,vema200 = row
		if vapertura=="apertura": continue
		fecha.append(vfecha)
		apertura.append(float(vapertura))
		cierre.append(float(vcierre))
		high.append(float(vhigh))
		low.append(float(vlow))
		macd.append(float(vmacd))
		macd_signal.append(float(vmacd_signal))
		macd_histograma.append(float(vmacd_histograma))
		rsi14.append(float(vrsi14))
		rsi50.append(float(vrsi50))
		esk14.append(float(vesk14))
		esd14.append(float(vesd14))
		esk50.append(float(vesk50))
		esd50.append(float(vesd50))
		sma5.append(float(vsma5))
		ema5.append(float(vema5))
		sma20.append(float(vsma20))
		ema20.append(float(vema20))
		sma50.append(float(vsma50))
		ema50.append(float(vema50))
		sma100.append(float(vsma100))
		ema100.append(float(vema100))
		sma200.append(float(vsma200))
		ema200.append(float(vema200))
		sma400.append(float(vsma400))
		ema400.append(float(vema400))			
			
	data = {}
	data['registros'] = len(fecha)
	data['fecha'] = fecha
	data['open'] = apertura
	data['close'] = cierre
	data['high'] = high
	data['low'] = low
	data['macd'] = macd
	data['macd_signal'] = macd_signal
	data['macd_histograma'] = macd_histograma
	data['rsi14'] = rsi14
	data['rsi50'] = rsi50
	data['esk14'] = esk14
	data['esd14'] = esd14
	data['esk50'] = esk50
	data['esd50'] = esd50
	data['sma5'] = sma5
	data['ema5'] = ema5
	data['sma20'] = sma20
	data['ema20'] = ema20
	data['sma50'] = sma50
	data['ema50'] = ema50
	data['sma100'] = sma100
	data['ema100'] = ema100
	data['sma200'] = sma200
	data['ema200'] = ema200
	data['sma400'] = sma400
	data['ema400'] = ema400
	
	
	
	return data
	
def cargar_valores(VALOR,PERIODO):


	config = ConfigParser.ConfigParser()
	config.read('configuracion.cfg')
	directorio_base = config.get('data', 'directorio_base')
	
	fname = VALOR
	filename = os.path.join(directorio_base, 'csv', PERIODO, fname)
	with open(os.path.join(filename + '.csv'), 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)		
		data = preparar_datos(spamreader)
		
	return data
	
def set_arrays_from_json_data(data):
	cierre = []
	apertura = []
	high = []
	low = []
	try:
		lecturas = len(data['c'])
		for x in range(0, lecturas):
			if (float(data['c'][x])==0): continue	
			cierre.append(data['c'][x])
			apertura.append(data['o'][x])
			high.append(data['h'][x])
			low.append(data['l'][x])
		
		return cierre, apertura, high, low
	except:
		return None,None,None,None
		
def get_json(url):
	context = ssl._create_unverified_context()
	response = urllib.urlopen(url, context=context)
	data = response.read()
	return data

def get_json_file(VALOR, RESOLUCION):
	filename = VALOR + '.json'
	config = ConfigParser.ConfigParser()
	config.read('configuracion.cfg')
	directorio_base = config.get('data', 'directorio_base')
	fname = os.path.join(directorio_base,'data',RESOLUCION,filename)
	with open(fname, "r") as f:
		d = f.read()
	
	data = json.loads(d)
	return data

def create_url(VALOR,TIEMPO_GRAFICO,TIEMPO):
	dt = datetime.now()
	if TIEMPO_GRAFICO == '1':
		dt2 = dt - timedelta(minutes=TIEMPO)
	elif TIEMPO_GRAFICO == '60' or TIEMPO_GRAFICO == '5' or TIEMPO_GRAFICO == '15' or TIEMPO_GRAFICO == '30':
		dt2 = dt - timedelta(hours=TIEMPO)
	else:
		dt2 = dt - timedelta(days=TIEMPO)
	
	# dt3 = dt - timedelta(minutes=10)

	sec_since_epoch = mktime(dt.timetuple()) + dt.microsecond / 1000000.0
	millis_since_epoch = round(sec_since_epoch)

	sec_since_epoch2 = mktime(dt2.timetuple()) + dt2.microsecond / 1000000.0
	millis_since_epoch2 = round(sec_since_epoch2)

	url = "https://tvc4.forexpros.com/0d941e0ab58b4e0421ca50db636091fd/1508161952/4/4/58/history?symbol={}&resolution={}&from={:0.0f}&to={:0.0f}".format(VALOR,str(TIEMPO_GRAFICO),millis_since_epoch2,millis_since_epoch)

	return url