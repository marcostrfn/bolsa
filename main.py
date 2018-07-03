#! /usr/bin/env/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import funciones.data as fd
from clases.Configuracion import Configuracion, CsvData
import time

    

if __name__ == '__main__':
    
    obj_csv = CsvData()
    obj_config = Configuracion()

    tiempos = []

    start = time.time()
    fd.descargar_datos(obj_config,obj_csv)
    done = time.time()
    elapsed = done - start
    tiempos.append(('descargarDatos',elapsed))


    start = time.time()
    fd.preparar_datos_csv(obj_config,obj_csv)
    done = time.time()
    elapsed = done - start
    tiempos.append(('prepararDatos',elapsed))
    
    
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
    fd.graficar_maximos_minimos(obj_config)
    done = time.time()
    elapsed = done - start
    tiempos.append(('graficar_maximos_minimos',elapsed))


    start = time.time()
    fr.crear_reporte(obj_config)
    done = time.time()
    elapsed = done - start
    tiempos.append(('crear_reporte',elapsed))


    print (tiempos)
