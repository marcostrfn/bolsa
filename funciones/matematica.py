#! /usr/bin/env/python
# -*- coding: utf-8 -*-

import math

def desviacion_estandar(datax):
	
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
	
def cov(datax,datay):
	return covarianza(datax,datay) / varianza(datay)
	
def rendimiento(datax,periodo=250):
	precio_inicial_accion = datax[-periodo]
	precio_final_accion = datax[-1]
	rendimiento_accion = (precio_final_accion - precio_inicial_accion ) / precio_inicial_accion
	
	return rendimiento_accion
	
def beta(datax,datay,rendimiento_bono,periodo=250):
	# https://www.datosmacro.com/bono/usa 
	rendimiento_accion = rendimiento(datax, periodo)
	rendimiento_indice = rendimiento(datay, periodo)

	ind_accion = rendimiento_accion - rendimiento_bono
	ind_indice = rendimiento_indice - rendimiento_bono

	beta = ind_accion / ind_indice
	return beta
 
 
 
 
 
