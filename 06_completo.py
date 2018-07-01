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
    procesar = config.get('calculo', 'procesar').split(',')
    
    
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
    fg.limpiar_graficas()
    done = time.time()
    elapsed = done - start
    print("tiempo fd.limpiar_graficas() {}".format(elapsed))
    tiempos.append(('limpiar_graficas',elapsed))



    start = time.time()
    fd.calculo_mejor_valor()
    done = time.time()
    elapsed = done - start
    print("tiempo fd.calculo_mejor_valor() {}".format(elapsed))
    tiempos.append(('calculo_mejor_valor',elapsed))
        
    start = time.time()    
    fd.calculo_mejor_hora(grafico=True)
    done = time.time()
    elapsed = done - start
    print("tiempo fd.calculo_mejor_hora() {}".format(elapsed))
    tiempos.append(('calculo_mejor_hora',elapsed))
        
    start = time.time()
    fd.calculo_soportes_resistencias()
    done = time.time()
    elapsed = done - start
    print("tiempo fd.calculo_soportes_resistencias() {}".format(elapsed))
    tiempos.append(('calculo_soportes_resistencias',elapsed))
        
    start = time.time()   
    for valor in procesar:
        fg.graficar_valor(valor,'D', media='mejor')
        fg.graficar_valor(valor,'60', media='mejor')
        fg.graficar_valor(valor,'W', media='mejor')

    done = time.time()
    elapsed = done - start
    print("tiempo fd.graficar_valor() {}".format(elapsed))
    tiempos.append(('graficar_valor',elapsed))
    
    start = time.time()        
    C = itertools.permutations(procesar, 2)
    tramitado = []
    for valores in C:
        if valores[1] in tramitado:
            print ("excluir combinacion {}".format(valores))
        else:
            print ("combinar {}".format(valores))
            fg.combinarValores(valores,'D',24)
        
        if not valores[0] in tramitado:
            tramitado.append(valores[0]) 
        
    done = time.time()
    elapsed = done - start
    print("tiempo fd.combinarValores() {}".format(elapsed))
    tiempos.append(('combinarValores',elapsed))
      
    start = time.time()
    fr.crear_reporte()
    done = time.time()
    elapsed = done - start
    print("tiempo fd.crear_reporte() {}".format(elapsed))
    tiempos.append(('crear_reporte',elapsed))
    
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
            
            

      