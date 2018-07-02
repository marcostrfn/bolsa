#! /usr/bin/env/python
# -*- coding: utf-8 -*-


import funciones.data as fd
from clases.Configuracion import Configuracion, CsvData


if __name__ == '__main__':   
    ''' graficos de las valores y resultado en /graficos/valores
    lee los valores de fichero de configuracion con tag calculo '''
    
    obj_csv = CsvData()
    obj_config = Configuracion()
    
    fd.graficar_valores(obj_config)
    
        