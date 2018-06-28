#! /usr/bin/env/python
# -*- coding: utf-8 -*-


import funciones.graficos as fg
import itertools
import ConfigParser
import sys

if __name__ == '__main__':      
    ''' graficos de las mejores medias de trading.
    resultado en /graficos/medias
    lee los valores de fichero de configuracion con tag calculo'''
     
    configuracion = 'configuracion.cfg'
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    directorio_base = config.get('data', 'directorio_base')
    PROCESAR = config.get('calculo', 'PROCESAR').split(',')
    for valor in PROCESAR:
        fg.graficarValorMedias(valor,'D', media='mejor')

