#! /usr/bin/env/python
# -*- coding: utf-8 -*-


import funciones.graficos as fg

from clases.Configuracion import Configuracion, CsvData

       
if __name__ == '__main__':
    ''' limpia graficos de la carpeta /graficos/ y deja backup en
    carpeta backup'''

    
    obj_csv = CsvData()
    obj_config = Configuracion()
    
    fg.limpiar_graficas(obj_config)

