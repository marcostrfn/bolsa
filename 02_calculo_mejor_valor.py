#! /usr/bin/env/python
# -*- coding: utf-8 -*-


from __future__ import print_function

import os, csv, datetime
import ConfigParser
import funciones.data as fd

if __name__ == '__main__': 
	''' calcula la mejor media simple para el trading de un valor.
	deja el resultado en fichero result/medias.csv
	Lee los valores de fichero de configuración tag calculo'''
	
	fd.calculoMejorValor()
	
