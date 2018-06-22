#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import datetime, timedelta
from time import mktime
import urllib, json, os
import ssl, csv
import ConfigParser
import sys

import funciones.bolsa as fb
import funciones.data as fd
import funciones.estrategia as fe
from django.template.defaultfilters import lower


from math import ceil, floor
def float_round(num, places = 0, direction = floor):
    return direction(num * (10**places)) / float(10**places)


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

def normalizarLista(original_vals, rango=1):
    # get max absolute value
    original_max = max([abs(val) for val in original_vals])
    # normalize to desired range size
    new_range_val = rango
    normalized_vals = [float(val)/original_max * new_range_val for val in original_vals]
    
    final = [float_round(n, 4, round) for n in normalized_vals]
    return final

def componerVela(open,close,high,low):
    
    tipo = 'baja'
    
    if close > open: tipo = 'alza'
    elif close == open : tipo = 'plana'

    velaNormalizada = normalizarLista([open,close,high,low])
    
    
    print (tipo,open,close,high,low,velaNormalizada)
    
    sys.exit()
    



def porcentuarVela(velaNormalizada):
    for vela in velaNormalizada:
        
        tipo = 'doji'
        open,close,high,low = vela

        cuerpo = high - low

        if close > open:
            tipo = 'alza'
            mechaSuperior = high - close
            mechaInferior = open - low
            medio = close - open

        elif close < open:
            tipo = 'baja'
            mechaSuperior = high - open
            mechaInferior = close - low
            medio = open - close    

            
        numeroVela = -1
        
        if mechaSuperior==0 and close > open and mechaInferior==0: numeroVela = 1
        elif mechaSuperior<medio and close > open and mechaInferior==0: numeroVela = 2
        elif mechaSuperior>=medio and close > open and mechaInferior==0: numeroVela = 3
        elif mechaSuperior==mechaInferior and mechaSuperior>=medio and close > open: numeroVela = 4
        elif mechaSuperior==0 and close > open and mechaInferior<medio: numeroVela = 5
        elif mechaSuperior>medio and (close > open or close==open) and mechaInferior==0: numeroVela = 6
        elif mechaSuperior==mechaInferior and mechaSuperior < 2*medio and close > open: numeroVela = 7
        
        
        
            
        if tipo == 'alza' and numeroVela==-1:
            s = "{:<10} [ {: >1.4f} {: >1.4f} {: >1.4f} {: >1.4f} ] | {: >1.4f} | {: >1.4f}  {: >1.4f}  {: >1.4f} {}"
            print (s.format(tipo, open, close, high, low, cuerpo, mechaSuperior, medio, mechaInferior,numeroVela))
          
    
    
    
def normalizarVelas(open,close,high,low):
    velas = []
    for i in range(0,len(open)):
        velaNormalizada = normalizarLista([open[i],close[i],high[i],low[i]])
        velas.append(velaNormalizada)
    return velas
    

def calcular(VALOR,PERIODO):
    data = fd.cargar_datos_valor(VALOR, PERIODO)   
    
    open = data ['open']
    close = data ['close']
    high = data ['high']
    low = data ['low']
    fecha = [datetime.strptime(f, '%Y-%m-%d %H:%M') for f in data['fecha']]
    
    porcentaje = [((b-a)*100/a) for a,b in zip(close,close[1:])]
    porcentaje.insert(0,0)
    
    print (len(porcentaje), len(fecha))
    elementos = len(fecha)
    
    
    velaNormalizada = normalizarVelas(open,close,high,low)   
    porcentajesVela = porcentuarVela(velaNormalizada[0:50])


def calculoMejorValor():
    

    PROCESAR = ['DE30']
    RESOLUCIONES = ['30']
    TIPOS = ['IND']
    resultados = []    

    # SELECCION DE VALORES
    
    valores = fd.cargar_valores_from_csv(TIPOS)    
    for row in valores:
        VALOR,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
        if VALOR == 'DE30':       
            for PERIODO in RESOLUCIONES:                    
                calcular(VALOR,PERIODO)            
                    
                    
                    
calculoMejorValor()       
    