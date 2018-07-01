#! /usr/bin/env/python
# -*- coding: utf-8 -*-


from __future__ import print_function
from datetime import datetime, timedelta
from time import mktime
import urllib, json, os
import ssl, csv
import ConfigParser
import sys
import pandas as pd 


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

def normalizar_lista(original_vals, rango=1):
    # get max absolute value
    try:
        original_max = max([abs(val) for val in original_vals])
        # normalize to desired range size
        new_range_val = rango
        normalized_vals = [float(val)/original_max * new_range_val for val in original_vals]
    
        final = [float_round(n, 2, round) for n in normalized_vals]
        return final
    except ZeroDivisionError:
        return original_vals
    

    


def tratar_velas(velas):
    
    velas_normalizadas = []
    
    
    for vela in velas:    
        open,close,high,low = vela
        
        diferencia = high - low
        cuerpo = close - open
        if cuerpo > 0: 
            superior = high - close
            inferior = open - low
            tipo = 1
        elif cuerpo < 0: 
            tipo = -1
            superior = high - open
            inferior = close - low
        else:
            superior = high - close
            inferior = high - close
            tipo = 0

        
        cuerpo = abs(cuerpo)

        if diferencia == 0:        
            tpc_superior = 0
            tpc_inferior = 0
            tpc_cuerpo = 0
        else:
            tpc_superior = float_round(superior * 100. / diferencia, 0, round)
            tpc_inferior = float_round(inferior * 100. / diferencia, 0, round)
            tpc_cuerpo = float_round(cuerpo * 100. / diferencia, 0, round)
        
        
        velas_normalizadas.append((tipo, tpc_superior,tpc_cuerpo,tpc_inferior))
    
    return velas_normalizadas



def get_tipo_vela(vela):
    t,s,c,i = vela # s=superior, c=centro, i=inferior
        
    k = -1
        
    if c >= 80:
        if s==0: k=1
        elif i==0: k=2
        else: k=0    
                    
    elif c >=70 and c <=80:
        if s==0: k=5
        elif i==0: k=3
        else: k=4
            
    elif c >= 40 and c <=70:
        if s==0: k=8
        elif i==0: k=6
        else: k=7
        
    elif c >=20 and c <=40:
        if s==0: k=11
        elif i==0: k=9
        else: k=10
     
    elif c >=0 and c <=20:
        if s==0: k=14
        elif i==0: k=12
        else: k=13
            
    
    return k,s,c,i
    
    
    
def calcular(valor,periodo):
    data = fd.cargar_datos_valor(valor, periodo)   
    
    open = data ['open']
    close = data ['close']
    high = data ['high']
    low = data ['low']
    fecha = [datetime.strptime(f, '%Y-%m-%d %H:%M') for f in data['fecha']]
    
    porcentaje = [((b-a)*100/a) for a,b in zip(close,close[1:])]
    porcentaje.insert(0,0)
    
    elementos = len(fecha)

    velas = []
    for a in range(0,elementos):
        velas.append([open[a],close[a],high[a],low[a]])
   
    velas_normalizadas = tratar_velas(velas)
    
    tipos = {'-1':[], '0':[],'1':[], '2':[], '3':[], '4':[],
             '5':[],'6':[], '7':[], '8':[], '9':[],
             '10':[],'11':[], '12':[], '13':[], '14':[]}
    
    for vela in velas_normalizadas:
        k,s,c,i = get_tipo_vela(vela)
        tipos[str(k)].append([s,c,i])
         

    return tipos
        


def calculo_mejor_valor():
    

    procesar = ['DE30','US500']
    resoluciones = ['60']
    tipos = ['IND']    
    
    df = pd.read_csv('valores.csv',  names=['valor','lotes','margen','spread','tp_spread','tipo','codigo','nombre','descripcion'], sep=';')
    # print (df.columns)    
    # print (df.head(3))
    # ELIMINAR COLUMNAS INNECESARIAS
    df = df.drop(['lotes','margen','spread','tp_spread','nombre','descripcion'], axis=1)    
    # ELIMINAR VALORES NULOS
    # a = df.dropna()
    # SELECCION DE TIPO
    df = df.loc[df['tipo'] == 'IND' ]
    valores = [a for a in df['valor'] if a in procesar]
    print (valores)


    for valor in valores:
        for periodo in resoluciones:         
            tipos = calcular(valor,periodo)
            print (valor)
            
            for k in tipos.keys():
                print (k, len(tipos[k]))
    
    sys.exit()

    
    elementos = len(L)
    ofile = open('velas_test.csv', 'wb')
    spamwriter = csv.writer(ofile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow([elementos,3,'uno','dos','tres'])   
    for dataset in L:                    
        spamwriter.writerow(dataset)    
    ofile.close()

                    
calculo_mejor_valor()       
    
