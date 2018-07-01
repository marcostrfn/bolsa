#! /usr/bin/env/python
# -*- coding: utf-8 -*-


import itertools
import ConfigParser
import sys

import funciones.data as fd
import funciones.bolsa as fb
import funciones.graficos as fg

import matplotlib.pyplot as plt
from pylab import *
import pandas as pd
import datetime as dt
import matplotlib.dates as mdates
 

def graficar_resistencias(valor,fechas,cierres,soportes,resistencias):
    
    titulo = "Soportes/Resistencias {}".format(valor)
    fig, ax = plt.subplots(figsize=(24, 12))

    print (fechas)
    x = arange(0,len(fechas),1) 
    x = [dt.datetime.strptime(d,'%Y-%m-%d %H:%M') for d in fechas]

    print (x)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d %b %y %H:%M"))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(byhour=range(0,24,4)))


    plt.plot(x, cierres, 'b', label='PRECIO', linewidth=1)
    plt.plot(x, soportes, 'r', label='soportes', linewidth=1, linestyle='dashed')
    plt.plot(x, resistencias, 'g', label='resistencias', linewidth=1, linestyle='dashed')
    plt.legend(loc="upper left")

    plt.title("{}".format(titulo),  fontsize=20)
    plt.grid(True)
    plt.gcf().autofmt_xdate()

    fig.autofmt_xdate()
    plt.show()
    plt.close()


def media_dorada(cierre, sma50, sma200):
    media_50 = []
    media_200 = []
    media = []
    for x in range(0,len(cierre)):
        dif_50 = cierre[x] - sma50[x]
        dif_200 = cierre[x] - sma200[x]
                      
        media_50.append(dif_50)
        media_200.append(dif_200)

        media.append(dif_200 - dif_50) 
    
    return (media) 



if __name__ == '__main__':   
    
    configuracion = 'configuracion.cfg'
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    directorio_base = config.get('data', 'directorio_base')
    procesar = config.get('calculo', 'procesar').split(',')
    
    periodo = '60'
    
    for valor in procesar:
        
        
        data = fd.cargar_datos_valor(valor, periodo)
        mejor_media = fd.getMejorMedia(valor, '60')
        sma_mejor = fb.get_sma_periodo(int(mejor_media),data['close'])

        pivot_point = fb.calcular_pivot_fibo(data['close'], data['high'], data['low'])
        
        fechas = []
        cierres = []
        soportes = []
        resistencias = []

        for d in range(0,len(data['close'])):
            if sma_mejor[d] == 0: continue
            
            s3,s2,s1,pp,r1,r2,r3 = pivot_point[d]
            
            fechas.append(data['fecha'][d])
            cierres.append(data['close'][d])
            soportes.append(s3)
            resistencias.append(r3)
       
        sesiones  = 100
        graficar_resistencias(valor,fechas[-sesiones:],cierres[-sesiones:],soportes[-sesiones:],resistencias[-sesiones:])
        sys.exit()
             
        for d in range(1,len(data['close'])):
            if sma_mejor[d] == 0: continue
           
            accion = None
            
            if data['close'] > sma_mejor[d]:
                s3,s2,s1,pp,r1,r2,r3 = pivot_point[d]
                if data['close'][d] <= s3 and data['rsi14'][d]<=40:
                    accion = 'comprar ++'
                elif data['close'][d] <= s2 and data['close'][d] >= s3 and data['rsi14'][d]<=40:
                    accion = 'comprar +'

            if data['close'] < sma_mejor[d]:
                s3,s2,s1,pp,r1,r2,r3 = pivot_point[d]
                if data['close'][d] >= r3 and data['rsi14'][d]>=60:
                    accion = 'vender ++'
                elif data['close'][d] >= r2 and data['close'][d] <= r3 and data['rsi14'][d]>=60:
                    accion = 'vender +'

            if accion is not None:
                print (valor, data['fecha'][d], sma_mejor[d], data['rsi14'][d], data['close'][d], accion)
                           
                    
        sys.exit()