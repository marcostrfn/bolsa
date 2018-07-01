#! /usr/bin/env/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import funciones.data as fd
import funciones.graficos as fg
import funciones.matematica as fm
import ConfigParser
import sys

def calcular_porcentajes():

    configuracion = 'configuracion.cfg'
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    PROCESAR = config.get('calculo', 'PROCESAR').split(',')  

    
    # SELECCION DE VALORES
    valores = fd.cargar_valores_from_csv(None)    
    for row in valores:     
        valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
        if valor in PROCESAR and valor=='DE30':   
            data = fd.cargar_datos_valor(valor, '60')
            print (data['close'])
             
            porcentaje = fm.calcularPorcentaje(data['close'])
            porcentaje.insert(0, 0)
            print (porcentaje)
            
            print (len(data['close']))
            print (len(porcentaje))
             
             
             
             
            for x in range(0,len(porcentaje)):
                print ("{:<20} {:<20}" .format(data['close'][x], porcentaje[x]))
                 
                 
            
            fg.graficoSimple(valor,valor,"porcentajes",porcentaje)
        
    
calcular_porcentajes() 
    