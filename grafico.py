
from __future__ import print_function
import os, csv, sys
from pylab import *
import matplotlib.pyplot as plt
import funciones.data as fd

# https://matplotlib.org/examples/index.html

# ===========================================================
# INICIO
# ===========================================================

PROCESAR =	['GOLD', 'SILVER'] # VALOR A PROCESAR
PERIODO = 'D' # PERIODO DE TIEMPO A LEER 1,60,D,M
FILENAME = 'valores.csv'


def compara_dos_valores(d1,d2,periodo=250):

	titulo1, data1 = d1
	titulo2, data2 = d2
	
	t = arange(0.0, len(data1['close'][-periodo:]), 1)

	plt.subplot(2, 1, 1)
	plt.plot(t, data1['close'][-periodo:])
	plt.title(titulo1)
	plt.grid(True)
 
	plt.subplot(2, 1, 2)
	plt.plot(t, data2['close'][-periodo:])
	# plt.xlabel('Item (s)')
	# plt.ylabel(titulo2)
	plt.title(titulo2)
	plt.grid(True)


	plt.show()




def compara_dos_valores2(d1,d2,periodo=250):

	titulo1, data1 = d1
	titulo2, data2 = d2
	
	t = arange(0.0, len(data1['close'][-periodo:]), 1)

	
	plt.plot(t, data1['close'][-periodo:])
	plt.plot(t, data2['close'][-periodo:])
	plt.title(titulo1)
	plt.grid(True)
 


	plt.show()



if __name__ == '__main__':
	
	data = []
	fname = os.path.join(os.path.dirname(__file__),FILENAME)
	with open(fname, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';')
		for row in spamreader:
			valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
			if valor in PROCESAR or PROCESAR=='ALL': 
				data.append((valor, fd.cargar_valores(valor,PERIODO)))

	
	print (data[0])
	compara_dos_valores(data[0],data[1],100)
				
				
				
