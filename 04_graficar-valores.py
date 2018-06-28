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
    ''' graficos de las valores y resultado en /graficos/valores
    lee los valores de fichero de configuracion con tag calculo
    combina pares de valores y deja el resultado en /csv/pares/
    graficos de correlacion en /graficos/pares
    lee los valores de configuracion tag calculo '''
    
    configuracion = 'configuracion.cfg'
    
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    directorio_base = config.get('data', 'directorio_base')
    PROCESAR = config.get('calculo', 'PROCESAR').split(',')
    for valor in PROCESAR:
        fg.graficarValor(valor,'D', media='mejor')
        fg.graficarValor(valor,'60', media='mejor')
        fg.graficarValor(valor,'W', media='mejor')
            
    C = itertools.permutations(PROCESAR, 2)
    tramitado = []
    for VALORES in C:
        if VALORES[1] in tramitado:
            print ("excluir combinacion {}".format(VALORES))
        else:
            print ("combinar {}".format(VALORES))
            fg.combinarValores(VALORES,'D',24)
        
        if not VALORES[0] in tramitado:
            tramitado.append(VALORES[0]) 
        
        
        