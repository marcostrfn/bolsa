#! /usr/bin/env/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import funciones.data as fd
import funciones.graficos as fg
from funciones import reporting as fr
from clases.Configuracion import Configuracion, CsvData
import time


'''import optparse

if __name__=="__main__":
    parser = optparse.OptionParser("usage: %prog [options] arg1 arg2")
    parser.add_option("-H", "--host", dest="hostname",
                      default="127.0.0.1", type="string",
                      help="specify hostname to run on")
    parser.add_option("-p", "--port", dest="portnum", default=80,
                      type="int", help="port number to run on")

    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("incorrect number of arguments")
    hostname = options.hostname
    portnum = options.portnum
	

lista = ['limpiar_graficas','descargar_datos','preparar_datos_csv','calculo_mejor_valor',
         'calculo_mejor_hora','calculo_mejor_valor','calculo_soportes_resistencias',
         'graficar_valores','graficar_valores_pares','graficar_valor_medias',
         'graficar_maximos_minimos','diferencia_cierre_horas','crear_reporte']

'''


if __name__ == '__main__':
    
    obj_csv = CsvData()
    obj_config = Configuracion()

    tiempos = []

    start = time.time()
    fg.limpiar_graficas(obj_config)
    done = time.time()
    elapsed = done - start
    tiempos.append(('limpiar_graficas',elapsed))
 
 
    start = time.time()
    fd.descargar_datos(obj_config,obj_csv)
    done = time.time()
    elapsed = done - start
    tiempos.append(('descargar_datos',elapsed))
  
  
    start = time.time()
    fd.preparar_datos_csv(obj_config,obj_csv)
    done = time.time()
    elapsed = done - start
    tiempos.append(('preparar_datos_csv',elapsed))
      
      
    start = time.time()
    fd.calculo_mejor_valor(obj_config,obj_csv)
    done = time.time()
    elapsed = done - start
    tiempos.append(('calculo_mejor_valor', elapsed))
      
      
    start = time.time()
    fd.calculo_mejor_hora(obj_config,obj_csv,grafico=True)
    done = time.time()
    elapsed = done - start
    tiempos.append(('calculo_mejor_hora',elapsed))
  
  
    start = time.time()
    fd.calculo_soportes_resistencias(obj_config,obj_csv)
    done = time.time()
    elapsed = done - start
    tiempos.append(('calculo_soportes_resistencias',elapsed))
  
  
    start = time.time()
    fd.graficar_valores(obj_config)
    done = time.time()
    elapsed = done - start
    tiempos.append(('graficar_valores',elapsed))
     
     
    start = time.time()
    fd.graficar_valores_pares(obj_config)
    done = time.time()
    elapsed = done - start
    tiempos.append(('graficar_valores_pares',elapsed))
     
     
    start = time.time()
    procesar = obj_config.get_valores_calculo()
    for valor in procesar:
        fg.graficar_valor_medias(obj_config, valor,'D', media='mejor')
    done = time.time()
    elapsed = done - start
    tiempos.append(('graficar_valor_medias',elapsed))
     
     
    start = time.time()
    fd.graficar_maximos_minimos(obj_config,obj_csv)
    done = time.time()
    elapsed = done - start
    tiempos.append(('graficar_maximos_minimos',elapsed))
 
 
    start = time.time()
    fd.diferencia_cierre_horas(obj_config, obj_csv)
    done = time.time()
    elapsed = done - start
    tiempos.append(('diferencia_cierre_horas',elapsed))
     
 
    start = time.time()
    fr.crear_reporte(obj_config)
    done = time.time()
    elapsed = done - start
    tiempos.append(('crear_reporte',elapsed))
 
 
    for t in tiempos:   
        print (t)  