#! /usr/bin/env/python
# -*- coding: utf-8 -*-


import funciones.data as fd
import funciones.graficos as fg
from clases.Configuracion import Configuracion, CsvData


if __name__ == '__main__':  
    ''' grafica las horas donde se dan los maximos y minimos de un valor 
    resultado en graficos/max-min
    lee los valores a procesar de configuracion calculo '''
    
    obj_csv = CsvData()
    obj_config = Configuracion()
    
    fd.graficar_maximos_minimos(obj_config,obj_csv)
    

    