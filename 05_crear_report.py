#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from funciones import reporting as fr



# medias = leer_mejores_medias()
# horas = leer_mejores_horas()
# pivot = leer_pivot_point()
    
# path1 = r"C:\tmp\bolsa\graficos\reporte"
# path2 = r"C:\tmp\bolsa\graficos\pares\D"
# path3 = r"C:\tmp\bolsa\graficos\valores"
# path4 = r"C:\tmp\bolsa\graficos\horas"
    
if __name__ == '__main__':
    ''' crea un reporte con los graficos de pares, valores
    pivot y mejores horas de trading.
    resultado en pdf en /graficos/valores/reporte'''
    
    fr.crearReporte()
