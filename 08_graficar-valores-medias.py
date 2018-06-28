#! /usr/bin/env/python
# -*- coding: utf-8 -*-


import funciones.graficos as fg
import itertools
import ConfigParser
import sys




# 02_calculo_mejor_valor
# 03_calculo_Soportes_Resistencias
# 04_graficar-valores-medias
# 04_graficar-valores
# 07_graficar_maximos_minimos
# 08_graficar-valores-medias
# [calculo]

if __name__ == '__main__':   
    
    configuracion = 'configuracion.cfg'
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    directorio_base = config.get('data', 'directorio_base')
    PROCESAR = config.get('calculo', 'PROCESAR').split(',')
    for valor in PROCESAR:
        fg.graficarValorMedias(valor,'D', media='mejor')

