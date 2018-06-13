from __future__ import print_function
import os, csv, sys

from pylab import *
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ohlc

import funciones.data as fd
import funciones.bolsa as fb
import itertools
import ConfigParser


# https://matplotlib.org/examples/index.html

# ===========================================================
# INICIO
# ===========================================================

PERIODO = '60' # PERIODO DE TIEMPO A LEER 1,60,D,M
VALORES_COMPARAR = [('NICKEL','SOYBEAN')]
FILENAME = 'valores.csv'
TEMPORALIDAD = 500
CONFIGURACION = 'configuracion.cfg'

def correlacion(titulo,data_fecha,data_correlacion,ema9,ema20,ema50,rsi,macd, macd_signal, macd_histograma, estocastico_sk_14,estocastico_sd_14, DIRECTORIO_BASE,tipo_valor,periodo=250):
	
	
	data_cierre = []
	data_open = []
	data_high = []
	data_low = []
	for v in data_correlacion:
		data_open.append(v[0])
		data_cierre.append(v[1])
		data_high.append(v[2])
		data_low.append(v[3])
		
	
	data = data_cierre
		
	desde = 150
	
	directorio_destino = os.path.join(DIRECTORIO_BASE, 'pares', PERIODO, tipo_valor)	
	# directorio_destino = os.path.join(DIRECTORIO_BASE, 'pares', PERIODO)	
	if not os.path.exists(directorio_destino):
		os.makedirs(directorio_destino)
		print ("creando directorio.... {}".format(directorio_destino))
		
	fig, ax = plt.subplots(figsize=(24, 12))

	
	x = arange(0.0, len(data[desde:]), 1)

	plt.subplot2grid((8,5), (0,0), colspan=5, rowspan=5)
	
	
	# candlestick2_ohlc(ax,data_open[desde:],data_high[desde:],data_low[desde:],data_cierre[desde:],width=0.6)
	plt.plot(x, data[desde:],'g',linewidth=3, label='DATA')
	plt.plot(x, ema9[desde:],'r', label='EMA12')
	plt.plot(x, ema20[desde:],'b', label='EMA50')
	plt.plot(x, ema50[desde:],'y', label='EMA100')
	plt.title("{} ( {} )".format(titulo,PERIODO),  fontsize=20)
	
	plt.legend(loc="upper left")
	plt.grid(True)
	plt.xticks(np.arange(min(x), max(x)+2, 20))
	v = (max(data[desde:]) - min(data[desde:])) / 20.
	plt.yticks(np.arange(min(data[desde:]), max(data[desde:])+v, v))
	
	
	
	
	x = np.arange(len(rsi[desde:]))
	plt.subplot2grid((8,5), (5, 0), colspan=5) # plt.subplot(5, 1, 1, rowspan=3)
	plt.plot(x, rsi[desde:],'g')
	# plt.title("RSI14")
	plt.grid(True)
	plt.xticks(np.arange(min(x), max(x)+2, 20))
	
	
	
	
	x = np.arange(len(macd_signal[desde:]))
	plt.subplot2grid((8,5), (6, 0), colspan=5) # plt.subplot(5, 1, 4)
	plt.plot(x, macd[desde:], 'r')
	plt.plot(x, macd_signal[desde:], 'g')
	# plt.bar(x, macd_histograma[50:])
	# plt.title("MACD")
	plt.grid(True)
	plt.xticks(np.arange(min(x), max(x)+2, 20))
	
	
	

	x = np.arange(len(estocastico_sk_14[desde:]))
	plt.subplot2grid((8,5), (7, 0), colspan=5) # plt.subplot(5, 1, 5)
	plt.plot(x, estocastico_sd_14[desde:], 'r')
	plt.plot(x, estocastico_sk_14[desde:], 'g')
	# plt.bar(x, macd_histograma[50:])
	# plt.title("STO")
	plt.grid(True)
	plt.xticks(np.arange(min(x), max(x)+2, 20))

	
	
	
	
	filename = os.path.join(directorio_destino, "{}.png".format(titulo))	
	print("generando.... {}".format(filename)) 
	plt.savefig(filename)   # save the figure to file
	plt.close()
	
	
def graficar(VALORES_PROCESAR,directorio_base):	
	data = [None,None,None,None,None,None,None,None,None]
	fname = os.path.join(os.path.dirname(__file__),FILENAME)
	with open(fname, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';')
		tipo_valor_1 = None
		tipo_valor_2 = None
		for row in spamreader:
			valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
			if valor == VALORES_PROCESAR[0]: 
				datos = fd.cargar_valores(valor,PERIODO)

				data[1]=datos['open'][-TEMPORALIDAD:]
				data[2]=datos['close'][-TEMPORALIDAD:]
				data[3]=datos['high'][-TEMPORALIDAD:]
				data[4]=datos['low'][-TEMPORALIDAD:]
				data[0]=datos['fecha'][-TEMPORALIDAD:]
				
				tipo_valor_1 = tipo
				
			elif valor == VALORES_PROCESAR[1]: 
				datos = fd.cargar_valores(valor,PERIODO)
				
				data[5]=datos['open'][-TEMPORALIDAD:]
				data[6]=datos['close'][-TEMPORALIDAD:]
				data[7]=datos['high'][-TEMPORALIDAD:]
				data[8]=datos['low'][-TEMPORALIDAD:]
				
				tipo_valor_2 = tipo
				

	data_correlacion = []
	data_fecha = []
	for x in range(0,len(data[0])):
		a = [data[1][x]/data[5][x], data[2][x]/data[6][x], data[3][x]/data[7][x], data[4][x]/data[8][x]]
		data_correlacion.append(a)
		data_fecha.append(data[0][x])

	
	data_cierre = []
	for v in data_correlacion:
		data_cierre.append(v[1])
	
	rsi14 = fb.calcular_rsi(14, data_cierre)
	macd, macd_signal, macd_histograma = fb.get_macd(data_cierre,12,26,9) 
	estocastico_sk_14, estocastico_sd_14 = fb.calcular_estocastico(data_cierre, data_cierre, data_cierre, 20, 3)
	
	ema9 = fb.get_ema_periodo(12,data_cierre)
	ema20 = fb.get_ema_periodo(50,data_cierre)
	ema50 = fb.get_ema_periodo(100,data_cierre)

	TITULO = "{}-{}".format(VALORES_PROCESAR[0],VALORES_PROCESAR[1])
	correlacion(TITULO,data_fecha,data_correlacion,ema9,ema20,ema50,rsi14,macd, macd_signal, macd_histograma,estocastico_sk_14,estocastico_sd_14,directorio_base,"{}-{}".format(tipo_valor_1,tipo_valor_2),TEMPORALIDAD)



			
if __name__ == '__main__':
	
	# LECTURA DE VALORES DE CONFIGURACION
	config = ConfigParser.ConfigParser()
	config.read(CONFIGURACION)
	DIRECTORIO_BASE = config.get('data', 'directorio_base')
	
	directorio_destino =  os.path.join(DIRECTORIO_BASE, 'pares')	
	if not os.path.exists(directorio_destino):
		os.makedirs(directorio_destino)
		print ("creando directorio.... {}".format(directorio_destino))
	

	directorio_destino =  os.path.join(DIRECTORIO_BASE, 'pares', PERIODO)	
	if not os.path.exists(directorio_destino):
		os.makedirs(directorio_destino)
		print ("creando directorio.... {}".format(directorio_destino))

	
	x = 0
	for v in VALORES_COMPARAR:
		# try:
			x += 1
			d = []
			d.append(v[0])
			d.append(v[1])
			print ("graficando {} de {} ( {}-{} )".format(x, len(VALORES_COMPARAR), v[0],v[1]))
			graficar(d,DIRECTORIO_BASE)
		# except Exception, e:
		#	print ("{} {}".format("Error en fichero",e))

				
