#! /usr/bin/env/python
# -*- coding: utf-8 -*-


import funciones.graficos as fg
import itertools
import ConfigParser
import sys

import funciones.data as fd
import funciones.bolsa as fb


def mediaDorada(cierre, sma50, sma200):
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
    PROCESAR = config.get('calculo', 'PROCESAR').split(',')
    
    PERIODO = 'D'
    
    for VALOR in PROCESAR:
        
        
        data = fd.cargar_datos_valor(VALOR, PERIODO)
        
        # print (data['close'])
        dorada = mediaDorada(data['close'],data['sma50'],data['sma200'])
        
        pivot_point = fb.calcular_pivot_fibo(data['close'], data['high'], data['low'])
        
         
        for d in range(0,len(data['close'])):
            # print (data['fecha'][d], data['close'][d],dorada[d], pivot_point[d])
            
            accion = None
            
            if dorada[d]>0:
                s3,s2,s1,pp,r1,r2,r3 = pivot_point[d]
                if data['close'][d] <= s3 and data['rsi14'][d]<=40:
                    accion = 'comprar ++'
                elif data['close'][d] <= s2 and data['close'][d] >= s3 and data['rsi14'][d]<=40:
                    accion = 'comprar +'
                


            if dorada[d]<0:
                s3,s2,s1,pp,r1,r2,r3 = pivot_point[d]
                if data['close'][d] >= r3 and data['rsi14'][d]>=60:
                    accion = 'vender ++'
                elif data['close'][d] >= r2 and data['close'][d] <= r3 and data['rsi14'][d]>=60:
                    accion = 'vender +'     


            if accion is not None:
                print (VALOR, data['fecha'][d], dorada[d], data['rsi14'][d], data['close'][d], accion)
                           
                    
        sys.exit()