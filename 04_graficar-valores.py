#! /usr/bin/env/python
# -*- coding: utf-8 -*-


import funciones.graficos as fg
import itertools
import ConfigParser
import sys

if __name__ == '__main__':   
    ''' graficos de las valores y resultado en /graficos/valores
    lee los valores de fichero de configuracion con tag calculo
    combina pares de valores y deja el resultado en /csv/pares/
    graficos de correlacion en /graficos/pares
    lee los valores de configuracion tag calculo '''
    
    configuracion = 'configuracion.cfg'
    
    # LECTURA DE valores DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    directorio_base = config.get('data', 'directorio_base')
    procesar = config.get('calculo', 'procesar').split(',')
    for valor in procesar:
        fg.graficar_valor(valor,'D', media='mejor')
        fg.graficar_valor(valor,'60', media='mejor')
        fg.graficar_valor(valor,'W', media='mejor')
            
    C = itertools.permutations(procesar, 2)
    tramitado = []
    for valores in C:
        if valores[1] in tramitado:
            print ("excluir combinacion {}".format(valores))
        else:
            print ("combinar {}".format(valores))
            fg.combinar_valores(valores,'D',24)
        
        if not valores[0] in tramitado:
            tramitado.append(valores[0]) 
        
        
        