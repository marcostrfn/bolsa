#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import datetime, timedelta
import urllib
import json
import os
import ssl
import csv
import ConfigParser
import itertools
import bolsa as fb
import graficos as fg


def crear_directorio(directorio):
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))  
        
# graficar maximo minimos
def graficar_maximos_minimos(obj_config, obj_csv):
	
	valores_a_procesar = obj_config.get_valores_calculo()
	valores = obj_csv.get_valores_by_valor(valores_a_procesar)	
	for row_valor in valores:
		valor = row_valor[0]	 
		horas_maximo = [0] * 24
		horas_minimo = [0] * 24					 
		fecha_desde = 0
		fecha_hasta = 0
			
		data = cargar_valores(obj_config, valor, '60')
					  
		fecha = data['fecha'][0].split(' ')   
		dia_old = fecha[0]		   
		fecha_desde = dia_old
			
		maximo_high = 0
		maximo_low = 100000
		valores_diarios = []
		for i in range (1,len(data['fecha'])):
				
			fecha = data['fecha'][i].split(' ')
			dia = fecha[0]
			hora = fecha[1].split(':')
			  
			if hora[0] in ['23','00','01','02','03','04','05','06','07']: continue
				
			if dia == dia_old:
				open = data['open'][i]
				close = data['close'][i]
				high = data['high'][i]
				low = data['low'][i]
					
				if high > maximo_high: maximo_high = high
				if low < maximo_low: maximo_low = low
				valores_diarios.append((dia, hora[0], maximo_high, maximo_low))  

			else:
					
				maximo_dia = 0
				minimo_dia = 100000
				hora_dia_maximo = None
				hora_dia_minimo = None					
				
				for a in valores_diarios:
					d_dia, d_hora, d_maximo_high, d_maximo_low = a
					if d_maximo_high > maximo_dia: 
						maximo_dia = d_maximo_high
						hora_dia_maximo = d_hora
						dia_dia_maximo = d_dia
					if d_maximo_low < minimo_dia: 
						minimo_dia = d_maximo_low
						hora_dia_minimo = d_hora
						dia_dia_minimo = d_dia

				try:
					horas_maximo[int(hora_dia_maximo)] += 1
					horas_minimo[int(hora_dia_minimo)] += 1
				except Exception:
					print (Exception)
						
				valores_diarios = []
						   
				maximo_high = 0
				maximo_low = 100000
				dia_old = dia
					
				open = data['open'][i]
				close = data['close'][i]
				high = data['high'][i]
				low = data['low'][i]
					
				if high > maximo_high: maximo_high = high
				if low < maximo_low: maximo_low = low
					
				valores_diarios.append((dia, hora[0], maximo_high, maximo_low)) 
				fecha_hasta = dia
					
		fechas = "de {} a {}".format(fecha_desde,fecha_hasta)
		fg.graficar_horas_max_min(obj_config, valor, horas_maximo,'maximos',fechas)
		fg.graficar_horas_max_min(obj_config, valor,horas_minimo,'minimos',fechas)	

# graficar valores
def graficar_valores(obj_config):
	procesar = obj_config.get_valores_calculo()
	
	for valor in procesar:
		fg.graficar_valor(obj_config, valor, 'D', media='mejor')
		fg.graficar_valor(obj_config, valor, '60', media='mejor')
		fg.graficar_valor(obj_config, valor, 'W', media='mejor')
		
		
		
def graficar_valores_pares(obj_config):
	procesar = obj_config.get_valores_calculo()

	C = itertools.permutations(procesar, 2)
	tramitado = []
	for valores in C:
		if valores[1] in tramitado:
			print ("excluir combinacion {}".format(valores))
		else:
			print ("combinar {}".format(valores))
			fg.combinar_valores(obj_config, valores,'D',24)
		
		if not valores[0] in tramitado:
			tramitado.append(valores[0]) 
		


# descarga_datos

def get_json(url):
	''' lee un json desde una url '''
	context = ssl._create_unverified_context()
	response = urllib.urlopen(url, context=context)
	data = response.read()
	return data

def create_url(valor, tiempo_grafico, tiempo):
	''' crea url para descarga de datos desde investing.com '''
	dt = datetime.now()
	if tiempo_grafico == '1':
		dt2 = dt - timedelta(minutes=tiempo)
	elif tiempo_grafico == '60' or tiempo_grafico == '5' or tiempo_grafico == '15' or tiempo_grafico == '30':
		dt2 = dt - timedelta(hours=tiempo)
	else:
		dt2 = dt - timedelta(days=tiempo)

	sec_since_epoch = mktime(dt.timetuple()) + dt.microsecond / 1000000.0
	millis_since_epoch = round(sec_since_epoch)

	sec_since_epoch2 = mktime(dt2.timetuple()) + dt2.microsecond / 1000000.0
	millis_since_epoch2 = round(sec_since_epoch2)

	url = "https://tvc4.forexpros.com/0d941e0ab58b4e0421ca50db636091fd/1508161952/4/4/58/history?symbol={}&resolution={}&from={:0.0f}&to={:0.0f}".format(valor, str(tiempo_grafico), millis_since_epoch2, millis_since_epoch)

	return url



def descargar_datos(obj_config,obj_csv):
	''' descarga datos en json desde investing.com. Resultado en data/XX/XX.json '''
	tiempo = 365 * 10	
	directorio_base = obj_config.get_directorio_base()
	valores_a_procesar,resoluciones = obj_config.get_valores_descarga()
	valores = obj_csv.get_valores_by_valor(valores_a_procesar)	
	for row in valores:
		valor, lotes, margen, spread, tp_spread, tipo, codigo, nombre, descripcion = row
		for resolucion in resoluciones:
			uri = create_url(codigo, resolucion, tiempo)
			print ("descargando valor {: >10}({: >10}) Resolucion {: >5}".format(valor, codigo, resolucion))

			data = get_json(uri)
				
			filename = valor + '.json'
			directorio_destino = os.path.join(directorio_base, 'data', resolucion)
			crear_directorio(directorio_destino)
				
			filename = os.path.join(directorio_destino, filename)
			print ("guardando archivo {}".format(filename))
			f = open(filename, 'w')
			f.write(data)
			f.close()
	
# preparar_datos

def preparar_datos_csv(obj_config,obj_csv):
	''' lee un fichero json con valores y prepara un csv con datos para uso posterior
	(macd, rsi, estocastico, medias, etc. Deja el fichero en data/csv/xx/xx.csvç
	lee los valores desde fichero de configuracion, opcion descargar'''
	
	valores_a_procesar,resoluciones = obj_config.get_valores_descarga()
	valores = obj_csv.get_valores_by_valor(valores_a_procesar)	
	for row in valores:
		valor, lotes, margen, spread, tp_spread, tipo, codigo, nombre, descripcion = row
		for resolucion in resoluciones:
			try:
				procesar_valor(obj_config, valor, codigo, resolucion)
			except:
				print ("error al procesar {}".format(valor))
					



def preparar_datos(spamreader):
	''' carga los valores de un fichero csv en un array '''
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
		vfecha, vapertura, vcierre, vhigh, vlow, vmacd, vmacd_signal, vmacd_histograma, \
			vrsi14, vrsi50, vesk14, vesd14, vesk50, vesd50, vsma5, vema5, vsma20, vema20, vsma50, vema50, vsma100, vema100, vsma200, vema400, vsma400, vema200 = row
		if vapertura == "apertura": continue
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


def cargar_valores(obj_config, valor, periodo):
	''' carga los valores de un fichero csv en un array '''
	directorio_base = obj_config.get_directorio_base()
	fname = valor
	filename = os.path.join(directorio_base, 'csv', periodo, fname)
	with open(os.path.join(filename + '.csv'), 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)		
		data = preparar_datos(spamreader)
		
	return data

	
def get_json_file(obj_config, valor, resolucion):
	''' carga un json desde fichero '''
	filename = valor + '.json'
	directorio_base = obj_config.get_directorio_base()
	fname = os.path.join(directorio_base, 'data', resolucion, filename)
	with open(fname, "r") as f:
		d = f.read()
	
	data = json.loads(d)
	return data

		
def procesar_valor(obj_config, valor, codigo, resolucion):
	''' lee un fichero json con valores y prepara un csv con datos para uso posterior
	(macd, rsi, estocastico, medias, etc. Deja el fichero en data/csv/xx/xx.csvç
	lee los valores desde fichero de configuracion, opcion descargar'''
	
	directorio_base = obj_config.get_directorio_base()
	
	fname = valor 
	print ("procesando valor {:<10} Resolucion {:>3}".format(fname, resolucion))
	
	data = get_json_file(obj_config, fname, resolucion)
	
	cierre, apertura, high, low = set_arrays_from_json_data(data)
	if cierre == None: 
		print ("error al procesar ", fname)
		return 
	
	lecturas = len(cierre)	
	fecha = fb.get_fechas(data)

	file_path = os.path.join(directorio_base, 'csv', resolucion, fname + '.csv')	
	
	if os.path.exists(file_path):
		print ('existe {}'.format(file_path))
		data = cargar_valores(obj_config, valor, resolucion)
		datetime_json = datetime.strptime(fecha[-1], "%Y-%m-%d %H:%M")
		datetime_file = datetime.strptime(data['fecha'][-1], "%Y-%m-%d %H:%M")
		# nada que hacer, las fechas no son superiores
		if datetime_json <= datetime_file:
			cierre_json = cierre[-1]
			cierre_file = data['close'][-1]	
			if cierre_json == cierre_file:
				print ('saliendo sin cambios, nada que anexar')
				return
	
	
	macd, macd_signal, macd_histograma = fb.get_macd(cierre, 12, 26, 9)
	
	rsi14 = fb.calcular_rsi(14, cierre)
	rsi50 = fb.calcular_rsi(50, cierre)
	
	estocastico_sk_14, estocastico_sd_14 = fb.calcular_estocastico(cierre, high, low, 14, 3)
	estocastico_sk_50, estocastico_sd_50 = fb.calcular_estocastico(cierre, high, low, 14, 3)	
		
	sma5 = fb.get_sma_periodo(5, cierre)
	ema5 = fb.get_ema_periodo(5, cierre)

	sma20 = fb.get_sma_periodo(20, cierre)
	ema20 = fb.get_ema_periodo(20, cierre)
	
	sma200 = fb.get_sma_periodo(200, cierre)
	ema200 = fb.get_ema_periodo(200, cierre)

	sma100 = fb.get_sma_periodo(100, cierre)
	ema100 = fb.get_ema_periodo(100, cierre)

	sma50 = fb.get_sma_periodo(50, cierre)
	ema50 = fb.get_ema_periodo(50, cierre)
	
	sma400 = fb.get_sma_periodo(400, cierre)
	ema400 = fb.get_ema_periodo(400, cierre)
	
	directorio_destino = os.path.join(directorio_base, 'csv', resolucion)	
	crear_directorio(directorio_destino)
	

	file_path = os.path.join(directorio_base, 'csv', resolucion, fname + '.csv')	
	if os.path.exists(file_path):		
		data = cargar_valores(obj_config, valor, resolucion)
		
		datetime_json = datetime.strptime(fecha[-1], "%Y-%m-%d %H:%M")
		datetime_file = datetime.strptime(data['fecha'][-1], "%Y-%m-%d %H:%M")
			
		print ("anexando desde {}".format(data['fecha'][-1]))
			
		with open(file_path, 'ab') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				
			for x in range(0, len(fecha)):
				datetime_json = datetime.strptime(fecha[x], "%Y-%m-%d %H:%M")
				if datetime_json > datetime_file:  # if datetime_json >= datetime_file: anade fila nueva	repitiendo		
					dataset = [fecha[x], apertura[x], cierre[x], high[x], low[x], macd[x], macd_signal[x], macd_histograma[x], rsi14[x], rsi50[x], estocastico_sk_14[x], estocastico_sd_14[x], estocastico_sk_50[x], estocastico_sd_50[x], sma5[x], ema5[x], sma20[x], ema20[x], sma50[x], ema50[x], sma100[x], ema100[x], sma200[x], ema200[x], sma400[x], ema400[x]]			
					spamwriter.writerow(dataset)
			
	else:
		print ('nuevo {}'.format(file_path))
		with open(file_path, 'wb') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			dataset = ['fecha', 'apertura', 'cierre', 'high', 'low', 'macd', 'macd_signal', 'macd_histograma', 'rsi14', 'rsi50', 'esk14', 'esd14', 'esk50', 'esd50', 'sma[5]', 'ema[5]', 'sma[20]', 'ema[20]', 'sma[50]', 'ema[50]', 'sma[100]', 'ema[100]', 'sma[200]', 'ema[200]', 'sma[400]', 'ema[400]']			
			spamwriter.writerow(dataset)
				
			for x in range(0, lecturas):
				dataset = [fecha[x], apertura[x], cierre[x], high[x], low[x], macd[x], macd_signal[x], macd_histograma[x], rsi14[x], rsi50[x], estocastico_sk_14[x], estocastico_sd_14[x], estocastico_sk_50[x], estocastico_sd_50[x], sma5[x], ema5[x], sma20[x], ema20[x], sma50[x], ema50[x], sma100[x], ema100[x], sma200[x], ema200[x], sma400[x], ema400[x]]			
				spamwriter.writerow(dataset)



# calculo_mejor_valor


def get_valores_proceso(obj_config):
	
	imprimir = False
	cabecera = False
	
	procesar = obj_config.get_valores_calculo()
	resoluciones = obj_config.get_resoluciones_calculo()
	csv_resultados = obj_config.get('calculo', 'csv_resultados')
	
	cabecera = obj_config.get('resultados', 'cabecera')
	imprimir = obj_config.get('resultados', 'imprimir')
	
	cabecera = True if cabecera == "si" else False
	imprimir = True if imprimir == "si" else False
	
	tipos = obj_config.get('calculo', 'tipos')
	tipos = None if tipos == "None" else tipos.split(',')
	
	return procesar, resoluciones, csv_resultados, imprimir, cabecera, tipos

def print_resultado(registro,imprimir=False):
	if imprimir:
		valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos = registro
		s = "{:<10} {:>3}  {:<15} {:>2} {:>4} {: >4} {: >12.2f} {: >12.2f} {: >12.2f}"
		print (s.format(valor, tipo, titulo, tiempo, periodo, numero_operaciones, total, largos, cortos))

def print_cabecera(valor, periodo,cabecera=False,imprimir=False):
	if cabecera and imprimir:
		print ('-' * 79)
		print ("calculo de {} en periodo de {}".format(valor, periodo))
		print ('-' * 79)


def escribir_csv_resultados(obj_config, resultados, escribir=False):
	
	if not escribir=="si": return
	
	directorio_base = obj_config.get_directorio_base()
	
	directorio_destino = os.path.join(directorio_base, 'result')
	crear_directorio(directorio_destino)
	
	filename = os.path.join(directorio_base, 'result', 'medias.csv')
	with open(filename, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		dataset = ['valor', 'tiempo', 'funcion', 'periodo', 'numero_operaciones', 'total', 'largos', 'cortos']			
		spamwriter.writerow(dataset)
						
		for r in resultados:
			valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos = r
			dataset = [valor, tiempo, titulo, periodo, numero_operaciones, total, largos, cortos]
			spamwriter.writerow(dataset)
	


def calculo_mejor_valor(obj_config,obj_csv):
	''' calcula la mejor media simple para el trading de un valor.
	deja el resultado en fichero result/medias.csv
	Lee los valores de fichero de configuración tag calculo'''
	resultados = []
	
	valores_a_procesar, resoluciones, csv_resultados, imprimir, cabecera, tipos = get_valores_proceso(obj_config)
	for valor_procesar in valores_a_procesar:
		for periodo in resoluciones:
			try:						
				print_cabecera(valor_procesar, periodo,cabecera,imprimir)
				data = cargar_valores(obj_config, valor_procesar, periodo)
				resultado_valor = fb.procesar_valores(valor_procesar, periodo, get_datos(data, 500), obj_config)					
				resultado_valor.sort(key=lambda (a, b, c, d, e, f, g, h, i):(g, h), reverse=True)
				resultados.append(resultado_valor[0])
				for r in resultado_valor: print_resultado(r,imprimir)
					
			except Exception as e:
				print ("Error {} {} {}".format(valor_procesar, periodo, e))
					
	escribir_csv_resultados(obj_config, resultados, csv_resultados)	



# calculo_mejor_hora





def get_valores_proceso_hora(obj_config):
	
	imprimir = False
	cabecera = False
	
	procesar = obj_config.get('hora', 'procesar').split(',')
	resoluciones = obj_config.get('hora', 'resoluciones').split(',')	
	csv_resultados = obj_config.get('hora', 'csv_resultados')
	cabecera = obj_config.get('resultados', 'cabecera')
	imprimir = obj_config.get('resultados', 'imprimir')
	
	cabecera = True if cabecera == 'si' else False
	imprimir = True if imprimir == 'si' else False
	
	tipos = obj_config.get('hora', 'tipos')
	tipos = None if tipos == 'None' else tipos.split(',')
	
	return procesar, resoluciones, csv_resultados, imprimir, cabecera, tipos


def print_resultado_mejor_hora(registro):
	(valor, tiempo, hora, total_diferencia, media) = registro
	s = "{:<10} {:>5} {:>5} {: >12.2f} {: >12.2f}"
	print (s.format(valor, tiempo, hora, total_diferencia, media))


def escribir_csv_resultados_hora(obj_config, resultados):
	
	directorio_base = obj_config.get_directorio_base()

	directorio_destino = os.path.join(directorio_base, 'result')
	crear_directorio(directorio_destino)
	
	filename = os.path.join(directorio_base, 'result', 'horas.csv')
	with open(filename, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		dataset = ['valor', 'periodo', 'hora', 'pip', 'media']			
		spamwriter.writerow(dataset)
						
		for v in resultados:
			for r in v:
				valor, periodo, hora, pip, media = r
				dataset = [valor, periodo, hora, pip, media]
				spamwriter.writerow(dataset)




def calculo_mejor_hora(obj_config,obj_csv,grafico=None):
	''' calcula el mejor horario para el trading de un valor.
	deja el resultado en fichero result/horas.csv
	Lee los valores de fichero de configuración tag horas
	Graficos en graficos/horas'''
	
	resultados = []	
	horas = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
	
	procesar, resoluciones, csv_resultados, imprimir, cabecera, tipos = get_valores_proceso_hora(obj_config)
	
	for valor in procesar:
		mi_valor = []	
		for periodo in resoluciones:				
			valor_procesar = valor							
			if cabecera and imprimir: print_cabecera_mejor_hora(valor_procesar, periodo)
			data = cargar_valores(obj_config, valor_procesar, periodo)
			resultado_valor = fb.procesar_valores_hora(valor_procesar, periodo, get_datos(data, 500), obj_config)					
			for hora in horas:
				total_diferencia = 0
				total_valores = 0
					
				for par in resultado_valor[hora]:
					diferencia = par[0] - par[1]								
					total_valores += 1
					total_diferencia += diferencia
					
				try:
					mi_valor.append([valor, periodo, hora, total_diferencia, total_diferencia / total_valores])
				except:
					mi_valor.append([valor, periodo, hora, total_diferencia, 0])

		fg.graficar_mejor_hora(obj_config, grafico, mi_valor)

		mi_valor.sort(key=lambda (a, b, c, d, e):(e), reverse=True)
		for m in mi_valor:
			(valor, periodo, hora, total_diferencia, media) = m
			print_resultado_mejor_hora(m)
	
		resultados.append(mi_valor)

	if csv_resultados == 'si': escribir_csv_resultados_hora(obj_config, resultados)





		
# calculo_soportes_resistencias


def escribir_csv_resultados_pivot(obj_config, resultados):

	directorio_base = obj_config.get_directorio_base()

	directorio_destino = os.path.join(directorio_base, 'result')
	crear_directorio(directorio_destino)
	
	filename = os.path.join(directorio_base, 'result', 'pivot.csv')
	print ("creando fichero.... {}".format(filename))
	with open(filename, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		dataset = ['valor', 's3', 's2', 's1', 'pp', 'r1', 'r2', 'r3']			
		spamwriter.writerow(dataset)
						
		for v in resultados:
			valor, datos = v
			s3, s2, s1, pp, r1, r2, r3 = datos
			dataset = [valor, s3, s2, s1, pp, r1, r2, r3]
			spamwriter.writerow(dataset)
				
				

def calculo_soportes_resistencias(obj_config,obj_csv,grafico=None):
	''' calcula soportes y resistencias diarias de un valor.
	deja el resultado en fichero result/pivot.csv
	Lee los valores de fichero de configuración tag calculo'''
	
	resultados = []	
		
	procesar = obj_config.get_valores_calculo()
	for valor in procesar:
		data = cargar_valores(obj_config, valor, 'D')
		pivot = fb.calcular_pivot_fibo(data['close'], data['high'], data['low'])
		resultados.append((valor, pivot[-1]))

	escribir_csv_resultados_pivot(obj_config, resultados)
	
#----------------------------------------------------------------------------------------	




#----------------------------------------------------------------------------------------	
#----------------------------------------------------------------------------------------	
#----------------------------------------------------------------------------------------	
#----------------------------------------------------------------------------------------	
def get_mejor_media(directorio_base, _valor, _periodo):
    filename = os.path.join(directorio_base, 'result', 'medias.csv')
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
        	valor, tiempo, funcion, periodo, numero_operaciones, total, largos, cortos = row
        	if valor == _valor and tiempo == _periodo:
        		return periodo
        	
   				
#----------------------------------------------------------------------------------------			            
             
             

               
               
              



def print_cabecera_mejor_hora(valor, periodo):
	print ('-' * 79)
	print ("calculo de {} en periodo de {}".format(valor, periodo))
	print ('-' * 79)





	


				
				
				


	
	
	






				
				
				
				
				

				


			






def get_valores_proceso_flujo(config):
	
	imprimir = False
	cabecera = False
	
	
	procesar = config.get('flujo', 'procesar').split(',')
	resoluciones = config.get('flujo', 'resoluciones').split(',')	
	csv_resultados = config.get('flujo', 'csv_resultados')
	cabecera = config.get('resultados', 'cabecera')
	imprimir = config.get('resultados', 'imprimir')
	
	if cabecera == 'si': 
		cabecera = True
	else:
		cabecera = False
		
	if imprimir == 'si': 
		imprimir = True
	else:
		imprimir = False
	
	
	tipos = config.get('flujo', 'tipos')
	if tipos == 'None':
		tipos = None
	else:
		tipos = tipos.split(',')
	
	
	return procesar, resoluciones, csv_resultados, imprimir, cabecera, tipos




def cargar_valores_from_csv(tipos=None):
	''' carga de valores desde fichero valores.csv '''
	
	data = []
	fname = os.path.join(os.path.dirname(__file__), '..', 'valores.csv')
	with open(fname, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';')
		for row in spamreader:
			valor, lotes, margen, spread, tp_spread, tipo, codigo, nombre, descripcion = row
			if tipos is None or tipo in tipos:
				data.append(row)

	return data





	
def get_datos(data, numero=500):

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
	


	
	
	
	

	
def set_arrays_from_json_data(data):
	cierre = []
	apertura = []
	high = []
	low = []
	try:
		lecturas = len(data['c'])
		for x in range(0, lecturas):
			if (float(data['c'][x]) == 0): continue	
			cierre.append(data['c'][x])
			apertura.append(data['o'][x])
			high.append(data['h'][x])
			low.append(data['l'][x])
		
		return cierre, apertura, high, low
	except:
		return None, None, None, None
		




