#! /usr/bin/env/python
# -*- coding: utf-8 -*-


from __future__ import print_function
from datetime import datetime, timedelta
from time import mktime
import urllib, json, os
import ssl, csv
import ConfigParser

import funciones.bolsa as fb
import funciones.data as fd
import funciones.estrategia as fe

def print_resultado(registro):
    valor, tiempo, tipo, titulo,  periodo, numero_operaciones, total, largos, cortos = registro
    s = "{:<10} {:>3}  {:<15} {:>2} {:>4} {: >4} {: >12.2f} {: >12.2f} {: >12.2f}"
    print (s.format(valor, tipo, titulo, tiempo, periodo, numero_operaciones, total, largos, cortos))



def media_simple(valor, tiempo, tipo, data):
    # cortes de una media simple
    titulo = "SMA"
    importes_operaciones = []
    for periodo in range(5,200):
        # calculo la sma de un periodo con datos de cierre
        array_data = fb.get_sma_periodo(periodo, data['close'])
    
        # devuelve array LARGO, CORTO por cada elemento del array
        cruces = fb.get_cortes(array_data, data['close'])
        
        # devuelve un array con pares de posiciones de inicio fin del corte 
        # de un array de cruces
        # un array para posiciones largas y otro para cortas (12, 16)
        largos,cortos = fb.get_pares_corte(cruces)
        numero_operaciones = len(largos)+len(cortos)
        # devuelve un array con fecha inicio, fin, e importe 
        # de las operaciones ('2018-02-14', '2018-02-27', 99.0),
        l,c = fb.get_simulacion_importes(data,largos,cortos)    
        
        
        # suma los importes de un array devuelto por get_simulacion_importes
        imp_l = fb.sumar_importes(l)
        imp_c = fb.sumar_importes(c)
        
        # anado elemento al array
        importes_operaciones.append((periodo, numero_operaciones, imp_l + imp_c, imp_l, imp_c))
    
    importes_operaciones.sort(key=lambda (a,b,c,d,e):c, reverse=True)
    (periodo, numero_operaciones, total, largos, cortos) = importes_operaciones[0]
    return (valor, tiempo, tipo, titulo, periodo, numero_operaciones, total, largos, cortos)




def procesar_valores(valor, tiempo, tipo, data, config):
    

    pivot = fb.calcular_pivot_fibo(data['close'], data['high'], data['low'])
    parabolic_sar_bear, parabolic_sar_bull = fb.psar(data['fecha'], data['close'], data['high'], data['low'], 0.02, 0.2)

    resultados = []
    
    # cortes del sar parabolico
    if config.get('operaciones', 'SAR_PARABOLICO') == 'si':
        r = fe.sar_parabolico(valor, tiempo, tipo, data, parabolic_sar_bull)
        resultados.append(r)
        
   
    # cortes de una media simple
    if config.get('operaciones', 'SMA') == 'si':
        r = media_simple(valor, tiempo, tipo, data)
        resultados.append(r)
        
    
    # print ()
    return resultados



def calculoMejorValor():
    
    configuracion = 'configuracion.cfg'
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    PROCESAR, RESOLUCIONES, CSV_RESULTADOS, IMPRIMIR, CABECERA, TIPOS = fd.get_valores_proceso(config)

    resultados = []    

    # SELECCION DE VALORES
    
    valores = fd.cargar_valores_from_csv(TIPOS)    
    for row in valores:
        valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
        if valor == 'DE30':       
            for PERIODO in RESOLUCIONES:
                
                # POR CADA VALOR Y PERIODO
                try:
                    VALOR_PROCESAR = valor                            
                    if CABECERA and IMPRIMIR: print_cabecera(VALOR_PROCESAR, PERIODO)
                    
                    # CARGA DE VALORES
                    data = fd.cargar_datos_valor(VALOR_PROCESAR, PERIODO)
                        
                    # TRATMIENTO DE LOS VALORES RECIBIDOS
                    resultado_valor = procesar_valores(VALOR_PROCESAR, PERIODO, tipo, fd.get_datos(data,500), config)                    
                    resultado_valor.sort(key=lambda (a,b,c,d,e,f,g,h,i):(g,h), reverse=True)
                    resultados.append(resultado_valor[0])
                    
                    for r in resultado_valor: print_resultado(r)
                    



     
                except Exception as e:
                    print ("Error {} {} {}".format(VALOR_PROCESAR, PERIODO, e))
                    
                    
                    
calculoMejorValor()       
    