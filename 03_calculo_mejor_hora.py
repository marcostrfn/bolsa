#! /usr/bin/env/python
# -*- coding: utf-8 -*-


from __future__ import print_function

import os, csv, datetime
import ConfigParser
import funciones.bolsa as fb
import funciones.data as fd


if __name__ == '__main__':
	''' calcula el mejor horario para el trading de un valor.
	deja el resultado en fichero result/horas.csv
	Lee los valores de fichero de configuración tag horas
	Graficos en graficos/horas'''
	
	fd.calculo_mejor_hora(grafico=True)
	
	
				