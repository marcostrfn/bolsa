#! /usr/bin/env/python
# -*- coding: utf-8 -*-


import funciones.data as fd
from clases.Configuracion import Configuracion, CsvData


if __name__ == '__main__':   
    ''' lee los valores de fichero de configuracion con tag calculo
    combina pares de valores y deja el resultado en /csv/pares/
    graficos de correlacion en /graficos/pares '''
    
    obj_csv = CsvData()
    obj_config = Configuracion()
    
    fd.graficar_valores_pares(obj_config)
    
        