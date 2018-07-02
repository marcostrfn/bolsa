#! /usr/bin/env/python
# -*- coding: utf-8 -*-


import funciones.graficos as fg
from clases.Configuracion import Configuracion, CsvData

if __name__ == '__main__':      
    ''' graficos de las mejores medias de trading.
    resultado en /graficos/medias
    lee los valores de fichero de configuracion con tag calculo'''
    
    obj_csv = CsvData()
    obj_config = Configuracion()
    
    procesar = obj_config.get_valores_calculo()
    for valor in procesar:
        fg.graficar_valor_medias(obj_config, valor,'D', media='mejor')

