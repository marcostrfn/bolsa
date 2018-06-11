import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os, csv, sys
import funciones.data as fd

# ===========================================================
# INICIO
# ===========================================================

PROCESAR =	['GOLD'] # VALOR A PROCESAR
PERIODO = 'D' # PERIODO DE TIEMPO A LEER 1,60,D,M
FILENAME = 'valores.csv'



def get_data():
	fname = os.path.join(os.path.dirname(__file__),FILENAME)
	with open(fname, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';')
		for row in spamreader:
			valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
			if valor in PROCESAR or PROCESAR=='ALL': 
				data = (valor, fd.cargar_valores(valor,PERIODO))
	
	return data
	
valor, data = get_data()

				
# the random data
x = np.arange(1000)
y = np.array(data['cierre'][-1000:])

plt.scatter(x,y)


plt.draw()
plt.show()