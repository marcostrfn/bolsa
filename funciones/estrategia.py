

import bolsa as fb
import data as fd
import matematica as fm


def sar_parabolico(valor, tiempo, tipo, data, parabolic_sar_bull):
	# cortes del sar parabolico
	titulo = "SAR PARABOLICO"
	cruces = fb.get_cortes_sar(parabolic_sar_bull,data['close'])
	
	largos,cortos = fb.get_pares_corte(cruces)
	numero_operaciones = len(largos)+len(cortos)
	l,c = fb.get_simulacion_importes(data,largos,cortos)	
	imp_l = fb.sumar_importes(l)
	imp_c = fb.sumar_importes(c)

	return (valor, tiempo, tipo, titulo, 0, numero_operaciones, imp_l + imp_c, imp_l, imp_c)




def macd(valor, tiempo, tipo, data):
	# cortes del MACD
	titulo = "MACD"
	cruces = fb.get_cortes_macd(data['macd_histograma'])
	
	largos,cortos = fb.get_pares_corte(cruces)
	numero_operaciones = len(largos)+len(cortos)
	l,c = fb.get_simulacion_importes(data,largos,cortos)	
	imp_l = fb.sumar_importes(l)
	imp_c = fb.sumar_importes(c)
	
	return (valor, tiempo, tipo, titulo, 0, numero_operaciones, imp_l + imp_c, imp_l, imp_c)

	

def sma_sma400(valor, tiempo, tipo, data):

	titulo = "SMA SMA400"
	importes_operaciones = []
	cortes_media_400 = fb.get_cortes(data['sma400'], data['close'])
	for periodo in range(5,100):
		array_data = fb.get_sma_periodo(periodo, data['close'])
		cortes_media = fb.get_cortes(array_data, data['close'])
		cruces = fb.get_cortes_cruce(cortes_media,cortes_media_400)		
		largos,cortos = fb.get_pares_corte(cruces)			
		numero_operaciones = len(largos)+len(cortos)
		l,c = fb.get_simulacion_importes(data,largos,cortos)	
		imp_l = fb.sumar_importes(l)
		imp_c = fb.sumar_importes(c)
		importes_operaciones.append((periodo, numero_operaciones, imp_l + imp_c, imp_l, imp_c))
		
	importes_operaciones.sort(key=lambda (a,b,c,d,e):c, reverse=True)
	(periodo, numero_operaciones, total, largos, cortos) = importes_operaciones[0]
	return (valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos)
	
	
def ema_sma400(valor, tiempo, tipo, data):

	titulo = "EMA SMA400"
	importes_operaciones = []
	cortes_media_400 = fb.get_cortes(data['sma400'], data['close'])
	for periodo in range(5,100):
		array_data = fb.get_ema_periodo(periodo, data['close'])
		cortes_media = fb.get_cortes(array_data, data['close'])
		cruces = fb.get_cortes_cruce(cortes_media,cortes_media_400)		
		largos,cortos = fb.get_pares_corte(cruces)			
		numero_operaciones = len(largos)+len(cortos)
		l,c = fb.get_simulacion_importes(data,largos,cortos)	
		imp_l = fb.sumar_importes(l)
		imp_c = fb.sumar_importes(c)
		importes_operaciones.append((periodo, numero_operaciones, imp_l + imp_c, imp_l, imp_c))
	
	importes_operaciones.sort(key=lambda (a,b,c,d,e):c, reverse=True)
	(periodo, numero_operaciones, total, largos, cortos) = importes_operaciones[0]
	return (valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos)


def sma_sma100(valor, tiempo, tipo, data):
	titulo = "SMA SMA100"
	importes_operaciones = []
	cortes_media_50 = fb.get_cortes(data['sma100'], data['close'])
	for periodo in range(5,100):
		array_data = fb.get_sma_periodo(periodo, data['close'])
		cortes_media = fb.get_cortes(array_data, data['close'])
		cruces = fb.get_cortes_cruce(cortes_media,cortes_media_50)		
		largos,cortos = fb.get_pares_corte(cruces)			
		numero_operaciones = len(largos)+len(cortos)
		l,c = fb.get_simulacion_importes(data,largos,cortos)	
		imp_l = fb.sumar_importes(l)
		imp_c = fb.sumar_importes(c)
		importes_operaciones.append((periodo, numero_operaciones, imp_l + imp_c, imp_l, imp_c))
	
	importes_operaciones.sort(key=lambda (a,b,c,d,e):c, reverse=True)
	(periodo, numero_operaciones, total, largos, cortos) = importes_operaciones[0]
	return (valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos)
	

	
def ema_sma100(valor, tiempo, tipo, data):	
	titulo = "EMA SMA100"
	importes_operaciones = []
	cortes_media_50 = fb.get_cortes(data['sma100'], data['close'])
	for periodo in range(5,100):
		array_data = fb.get_ema_periodo(periodo, data['close'])
		cortes_media = fb.get_cortes(array_data, data['close'])
		cruces = fb.get_cortes_cruce(cortes_media,cortes_media_50)		
		largos,cortos = fb.get_pares_corte(cruces)			
		numero_operaciones = len(largos)+len(cortos)
		l,c = fb.get_simulacion_importes(data,largos,cortos)	
		imp_l = fb.sumar_importes(l)
		imp_c = fb.sumar_importes(c)
		importes_operaciones.append((periodo, numero_operaciones, imp_l + imp_c, imp_l, imp_c))
	
	importes_operaciones.sort(key=lambda (a,b,c,d,e):c, reverse=True)
	(periodo, numero_operaciones, total, largos, cortos) = importes_operaciones[0]
	return (valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos)

	
def sma_sma50(valor, tiempo, tipo, data):	
	titulo = "SMA SMA50"
	importes_operaciones = []
	cortes_media_50 = fb.get_cortes(data['sma50'], data['close'])
	for periodo in range(5,50):
		array_data = fb.get_sma_periodo(periodo, data['close'])
		cortes_media = fb.get_cortes(array_data, data['close'])
		cruces = fb.get_cortes_cruce(cortes_media,cortes_media_50)		
		largos,cortos = fb.get_pares_corte(cruces)			
		numero_operaciones = len(largos)+len(cortos)
		l,c = fb.get_simulacion_importes(data,largos,cortos)	
		imp_l = fb.sumar_importes(l)
		imp_c = fb.sumar_importes(c)
		importes_operaciones.append((periodo, numero_operaciones, imp_l + imp_c, imp_l, imp_c))
	
	importes_operaciones.sort(key=lambda (a,b,c,d,e):c, reverse=True)
	(periodo, numero_operaciones, total, largos, cortos) = importes_operaciones[0]
	return (valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos)


def ema_sma50(valor, tiempo, tipo, data):	
	titulo = "SMA SMA50"
	importes_operaciones = []
	cortes_media_50 = fb.get_cortes(data['sma50'], data['close'])
	for periodo in range(5,50):
		array_data = fb.get_ema_periodo(periodo, data['close'])
		cortes_media = fb.get_cortes(array_data, data['close'])
		cruces = fb.get_cortes_cruce(cortes_media,cortes_media_50)		
		largos,cortos = fb.get_pares_corte(cruces)			
		numero_operaciones = len(largos)+len(cortos)
		l,c = fb.get_simulacion_importes(data,largos,cortos)	
		imp_l = fb.sumar_importes(l)
		imp_c = fb.sumar_importes(c)
		importes_operaciones.append((periodo, numero_operaciones, imp_l + imp_c, imp_l, imp_c))
	
	importes_operaciones.sort(key=lambda (a,b,c,d,e):c, reverse=True)
	(periodo, numero_operaciones, total, largos, cortos) = importes_operaciones[0]
	return (valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos)



def media_simple(valor, tiempo, tipo, data):
	# cortes de una media simple
	titulo = "SMA"
	importes_operaciones = []
	for periodo in range(5,200):
		# print ("Calculando media {}".format(periodo)),
		# calculo la sma de un periodo con datos de cierre
		array_data = fb.get_sma_periodo(periodo, data['close'])
	
		# devuelve array LARGO, CORTO por cada elemento del array
		cruces = fb.get_cortes(array_data, data['close'])
		
		# devuelve un array con pares de posiciones de inicio fin del corte 
		# de un array de cruces
		# un array para posiciones largas y otro para cortas (12, 16)
		largos,cortos = fb.get_pares_corte(cruces)
		numero_operaciones = len(largos)+len(cortos)
		# devuelve un array con fecha inicio, fin, e importe 
		# de las operaciones ('2018-02-14', '2018-02-27', 99.0),
		l,c = fb.get_simulacion_importes(data,largos,cortos)	
		
		
		# suma los importes de un array devuelto por get_simulacion_importes
		imp_l = fb.sumar_importes(l)
		imp_c = fb.sumar_importes(c)
		
		# anado elemento al array
		importes_operaciones.append((periodo, numero_operaciones, imp_l + imp_c, imp_l, imp_c))
	
	importes_operaciones.sort(key=lambda (a,b,c,d,e):c, reverse=True)
	(periodo, numero_operaciones, total, largos, cortos) = importes_operaciones[0]
	return (valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos)


def media_exponencial(valor, tiempo, tipo, data):
	titulo = "EMA"
	importes_operaciones = []
	for periodo in range(5,200):
		array_data = fb.get_ema_periodo(periodo, data['close'])
		cruces = fb.get_cortes(array_data, data['close'])
		
		largos,cortos = fb.get_pares_corte(cruces)
		numero_operaciones = len(largos)+len(cortos)
		l,c = fb.get_simulacion_importes(data,largos,cortos)	
		imp_l = fb.sumar_importes(l)
		imp_c = fb.sumar_importes(c)
		importes_operaciones.append((periodo, numero_operaciones, imp_l + imp_c, imp_l, imp_c))
			
	importes_operaciones.sort(key=lambda (a,b,c,d,e):c, reverse=True)
	(periodo, numero_operaciones, total, largos, cortos) = importes_operaciones[0]
	return (valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos)

	
	
def macd_sma(valor, tiempo, tipo, data):
	titulo = "MACD SMA"
	importes_operaciones = []
	cruce_macd = fb.get_cortes_macd(data['macd_histograma'])
	for periodo in range(5,200):
		importes_operaciones.append(fb.corte_macd_media_simple(periodo,data,cruce_macd))
		
	importes_operaciones.sort(key=lambda (a,b,c,d,e):c, reverse=True)
	(periodo, numero_operaciones, total, largos, cortos) = importes_operaciones[0]
	return (valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos)
	
	
	