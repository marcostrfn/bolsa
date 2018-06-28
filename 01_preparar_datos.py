#! /usr/bin/env/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import os, csv, sys
from datetime import datetime
import funciones.data as fd
import ConfigParser

if __name__ == '__main__':
	''' lee un fichero json con valores y prepara un csv con datos para uso posterior
	(macd, rsi, estocastico, medias, etc. Deja el fichero en data/csv/xx/xx.csvç
	lee los valores desde fichero de configuracion, opcion descargar'''
	
	fd.prepararDatos()
	
	
