from __future__ import print_function

#! /usr/bin/env/python
# -*- coding: utf-8 -*-

import numpy as np
from scipy import stats # importando scipy.stats

def desviacion_estandar(datax):
	import math
	return math.sqrt(varianza(datax))


def varianza(datax):
		
	col1 = list(map(lambda x: float(x), datax))
	media = reduce(lambda x,y: x+y, col1) / len(col1)
	
	col2 = list(map(lambda x: x - media, col1))
	col3 = list(map(lambda x: x*x, col2))
	suma_cuadrados = reduce(lambda x,y: x+y, col3) 
	
	return suma_cuadrados / (len(col1) - 1)
	
	
def covarianza(datax,datay):
	if not len(datax)==len(datay):
		return None
		
		
	col1 = [0]*len(datax)
	col2 = [0]*len(datay)
	col3 = [0]*len(datax)
	col4 = [0]*len(datay)
	col5 = [0]*len(datax)
	
	for x in range(0,len(col1)): 
		col1[x] = float(datax[x])
		col2[x] = float(datay[x])

	promedio_col1 = reduce(lambda x,y: x+y, col1) / len(col1)
	promedio_col2 = reduce(lambda x,y: x+y, col2) / len(col2)
	
	for x in range(0,len(col1)):
		col3[x] = col1[x] - promedio_col1
		col4[x] = col2[x] - promedio_col2
		col5[x] = col3[x] * col4[x]
	
	suma_productos = reduce(lambda x,y: x+y, col5)
	
	covarianza = suma_productos / (len(col1) - 1)
	
	return covarianza
	


x = [1,3,2,5,8,7,12,2,4,2]
y = [8,6,9,4,3,3,2,7,7,5]

z = [17,15,23,7,9,13]


print (covarianza(x,y))
print (np.cov(x,y)[0][1])


print (varianza(z))
print (np.var(z))


print (desviacion_estandar(z))


a = [3,7,10,15,19]
print( np.mean(a) ) # media aritmetica
print( np.median(a) ) # mediana
print( np.std(a) ) # desviacion tipica


print( np.corrcoef([1,2,3], [4,4,6])) # coeficiente de correlacion 
print( np.corrcoef(np.array([1,2,7,6,1])) )

a,b = stats.mode(y)  # moda
print (a,b)
