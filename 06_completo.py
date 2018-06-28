#! /usr/bin/env/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import funciones.data as fd
import funciones.graficos as fg
from funciones import reporting as fr

import sys, os, csv
import datetime
import itertools
import ConfigParser
import time
    
    
if __name__ == '__main__':
    
    configuracion = 'configuracion.cfg'
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    directorio_base = config.get('data', 'directorio_base')
    PROCESAR = config.get('calculo', 'PROCESAR').split(',')
    
    
    tiempos = []
    start1 = time.time()

#     start = time.time()
#     fd.descargarDatos()
#     done = time.time()
#     elapsed = done - start
#     print("tiempo fd.descargarDatos() {}".format(elapsed))
#     tiempos.append(('descargarDatos',elapsed))
# 
#     start = time.time()
#     fd.prepararDatos()
#     done = time.time()
#     elapsed = done - start
#     print("tiempo fd.prepararDatos() {}".format(elapsed))
#     tiempos.append(('prepararDatos',elapsed))


    start = time.time()
    fg.limpiarGraficas()
    done = time.time()
    elapsed = done - start
    print("tiempo fd.limpiarGraficas() {}".format(elapsed))
    tiempos.append(('limpiarGraficas',elapsed))



    start = time.time()
    fd.calculoMejorValor()
    done = time.time()
    elapsed = done - start
    print("tiempo fd.calculoMejorValor() {}".format(elapsed))
    tiempos.append(('calculoMejorValor',elapsed))
        
    start = time.time()    
    fd.calculoMejorHora(grafico=True)
    done = time.time()
    elapsed = done - start
    print("tiempo fd.calculoMejorHora() {}".format(elapsed))
    tiempos.append(('calculoMejorHora',elapsed))
        
    start = time.time()
    fd.calculoSoportesResistencias()
    done = time.time()
    elapsed = done - start
    print("tiempo fd.calculoSoportesResistencias() {}".format(elapsed))
    tiempos.append(('calculoSoportesResistencias',elapsed))
        
    start = time.time()   
    for valor in PROCESAR:
        fg.graficarValor(valor,'D', media='mejor')
        fg.graficarValor(valor,'60', media='mejor')
        fg.graficarValor(valor,'W', media='mejor')

    done = time.time()
    elapsed = done - start
    print("tiempo fd.graficarValor() {}".format(elapsed))
    tiempos.append(('graficarValor',elapsed))
    
    start = time.time()        
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
        
    done = time.time()
    elapsed = done - start
    print("tiempo fd.combinarValores() {}".format(elapsed))
    tiempos.append(('combinarValores',elapsed))
      
    start = time.time()
    fr.crearReporte()
    done = time.time()
    elapsed = done - start
    print("tiempo fd.crearReporte() {}".format(elapsed))
    tiempos.append(('crearReporte',elapsed))
    
    elapsed = done - start1
    print("tiempo total {}".format(elapsed)) 
    tiempos.append(('total',elapsed))

    
    filename = os.path.join(directorio_base, 'result', 'tiempos.csv')
    with open(filename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dataset = ['funcion', 'tiempo']            
        spamwriter.writerow(dataset)
        for t in tiempos:
            spamwriter.writerow(t)
            
            

      