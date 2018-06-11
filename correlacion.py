from __future__ import print_function
import os, csv, sys
from pylab import *
import matplotlib.pyplot as plt
import funciones.data as fd
import funciones.bolsa as fb
import itertools
import ConfigParser


# https://matplotlib.org/examples/index.html

# ===========================================================
# INICIO
# ===========================================================

PERIODO = 'D' # PERIODO DE TIEMPO A LEER 1,60,D,M
FILENAME = 'valores.csv'
TEMPORALIDAD = 500
CONFIGURACION = 'configuracion.cfg'

def correlacion(titulo,data,rsi,DIRECTORIO_BASE,tipo_valor,periodo=250):

	t = arange(0.0, len(data[-periodo:]), 1)

	plt.subplot(2, 1, 1)
	plt.plot(t, data[-periodo:])
	plt.title(titulo)
	plt.grid(True)
	
	plt.subplot(2, 1, 2)
	plt.plot(t, rsi[-periodo:])
	plt.title("RSI14")
	plt.grid(True)

	filename = os.path.join(DIRECTORIO_BASE, 'pares', "{}_{}.png".format(tipo_valor,titulo))	
	plt.savefig(filename)   # save the figure to file
	plt.close()    # close the figure


def graficar(VALORES_PROCESAR,directorio_base):	
	data = [None,None]
	fname = os.path.join(os.path.dirname(__file__),FILENAME)
	with open(fname, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';')
		tipo_valor_1 = None
		tipo_valor_2 = None
		for row in spamreader:
			valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
			if valor == VALORES_PROCESAR[0]: 
				datos = fd.cargar_valores(valor,PERIODO)
				data[0]=datos['close'][-TEMPORALIDAD:]
				tipo_valor_1 = tipo
			elif valor == VALORES_PROCESAR[1]: 
				datos = fd.cargar_valores(valor,PERIODO)
				data[1]=datos['close'][-TEMPORALIDAD:]
				tipo_valor_2 = tipo
				

	data_correlacion = []
	for x in range(0,len(data[0])):
		data_correlacion.append(data[0][x]/data[1][x])
	
	rsi14 = fb.calcular_rsi(14, data_correlacion)
	
	TITULO = "{}-{}".format(VALORES_PROCESAR[0],VALORES_PROCESAR[1])
	correlacion(TITULO,data_correlacion,rsi14,directorio_base,"{}-{}".format(tipo_valor_1,tipo_valor_2),TEMPORALIDAD)



def seleccionValor():
	data = []
	fname = os.path.join(os.path.dirname(__file__),FILENAME)
	with open(fname, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';')
		for row in spamreader:
			valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
			# if "USDIDX" in valor or "FX" in tipo:
			if "CMD" in tipo:
				data.append(valor)
	
	return data
				
				
if __name__ == '__main__':
	
	# LECTURA DE VALORES DE CONFIGURACION
	config = ConfigParser.ConfigParser()
	config.read(CONFIGURACION)
	DIRECTORIO_BASE = config.get('data', 'directorio_base')
	
	directorio_destino =  os.path.join(DIRECTORIO_BASE, 'pares')	
	if not os.path.exists(directorio_destino):
		os.makedirs(directorio_destino)
		print ("creando directorio.... {}".format(directorio_destino))
		
	VALORES=[]
	VALORES_1 = list(itertools.permutations(seleccionValor(), 2))
	for v in VALORES_1:
		'''if not v[0]=='USDIDX':
			continue'''
		VALORES.append(v)
		
	x=0
	for v in VALORES:
		x+=1
		d = []
		d.append(v[0])
		d.append(v[1])
		print ("graficando {} de {} ( {}-{} )".format(x, len(VALORES), v[0],v[1]))
		graficar(d,DIRECTORIO_BASE)


				
