#! /usr/bin/env/python
# -*- coding: utf-8 -*-


import funciones.graficos as fg
import itertools
import ConfigParser
import sys

from clases.Configuracion import Configuracion, CsvData


if __name__ == '__main__':   
    ''' graficos de las valores y resultado en /graficos/valores
    lee los valores de fichero de configuracion con tag calculo
    combina pares de valores y deja el resultado en /csv/pares/
    graficos de correlacion en /graficos/pares
    lee los valores de configuracion tag calculo '''
    
    obj_csv = CsvData()
    obj_config = Configuracion()
    
    directorio_base = obj_config.get_directorio_base()
    procesar = obj_config.get_valores_calculo()
    
    for valor in procesar:
        fg.graficar_valor(obj_config, valor, 'D', media='mejor')
        fg.graficar_valor(obj_config, valor, '60', media='mejor')
        fg.graficar_valor(obj_config, valor, 'W', media='mejor')
            
    C = itertools.permutations(procesar, 2)
    tramitado = []
    for valores in C:
        if valores[1] in tramitado:
            print ("excluir combinacion {}".format(valores))
        else:
            print ("combinar {}".format(valores))
            fg.combinar_valores(obj_config, valores,'D',24)
        
        if not valores[0] in tramitado:
            tramitado.append(valores[0]) 
        
        
        