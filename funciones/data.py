from __future__ import print_function
from datetime import datetime, timedelta
from time import mktime
import urllib, json, os
import ssl, csv
import ConfigParser



def escribir_csv_resultados(resultados):
	
	config = ConfigParser.ConfigParser()
	config.read('configuracion.cfg')
	directorio_base = config.get('data', 'directorio_base')

	ahora = datetime.now().strftime("%Y_%m_%d_%H_%M")
	
	
	directorio_destino =  os.path.join(directorio_base,'result')
	if not os.path.exists(directorio_destino):
		os.makedirs(directorio_destino)
		print ("creando directorio.... {}".format(directorio_destino))
	
	
	filename = os.path.join(directorio_base, 'result', ahora + '.csv')
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