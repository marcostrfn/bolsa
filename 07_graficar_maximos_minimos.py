#! /usr/bin/env/python
# -*- coding: utf-8 -*-


import funciones.data as fd
import funciones.graficos as fg
import ConfigParser
import sys


if __name__ == '__main__':  
    ''' grafica las horas donde se dan los maximos y minimos de un valor 
    resultado en graficos/max-min
    lee los valores a procesar de configuracion calculo '''
    
    configuracion = 'configuracion.cfg'
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    procesar = config.get('calculo', 'procesar').split(',')

    resultados = []    

    valores = fd.cargar_valores_from_csv(None)    
    for row in valores:     
        valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
        if valor in procesar:   
            
            horas_maximo = [0] * 24
            horas_minimo = [0] * 24                     
            fechaDesde = 0
            fechaHasta = 0
            
            data = fd.cargar_datos_valor(valor, '60')
                       
                
            fecha = data['fecha'][0].split(' ')   
            diaOld = fecha[0]           
            fechaDesde = diaOld
            
            maximo_high = 0
            maximo_low = 100000
            valores_diarios = []
            for i in range (1,len(data['fecha'])):
                
                fecha = data['fecha'][i].split(' ')
                dia = fecha[0]
                hora = fecha[1].split(':')
                
                if hora[0] in ['23','00','01','02','03','04','05','06','07']: continue
                
                if dia == diaOld:
                    open = data['open'][i]
                    close = data['close'][i]
                    high = data['high'][i]
                    low = data['low'][i]
                    
                    if high > maximo_high: maximo_high = high
                    if low < maximo_low: maximo_low = low
                    valores_diarios.append((dia, hora[0], maximo_high, maximo_low))  

                else:
                    
                    maximo_dia = 0
                    minimo_dia = 100000
                    hora_dia_maximo = None
                    hora_dia_minimo = None                    
                    dia_dia_maximo = None
                    dia_dia_minimo = None
                    for a in valores_diarios:
                        dDia, dHora, d_maximo_high, d_maximo_low = a
                        if d_maximo_high > maximo_dia: 
                            maximo_dia = d_maximo_high
                            hora_dia_maximo = dHora
                            dia_dia_maximo = dDia
                        if d_maximo_low < minimo_dia: 
                            minimo_dia = d_maximo_low
                            hora_dia_minimo = dHora
                            dia_dia_minimo = dDia

                    try:
                        horas_maximo[int(hora_dia_maximo)] += 1
                        horas_minimo[int(hora_dia_minimo)] += 1
                    except Exception:
                        print (Exception)
                        
                    valores_diarios = []
                             
                    maximo_high = 0
                    maximo_low = 100000
                    diaOld = dia
                    
                    open = data['open'][i]
                    close = data['close'][i]
                    high = data['high'][i]
                    low = data['low'][i]
                    
                    if high > maximo_high: maximo_high = high
                    if low < maximo_low: maximo_low = low
                    
                    valores_diarios.append((dia, hora[0], maximo_high, maximo_low)) 
                    fechaHasta = dia
                    
            fechas = "de {} a {}".format(fechaDesde,fechaHasta)
            fg.graficar_horas_max_min(valor, horas_maximo,'maximos',fechas)
            fg.graficar_horas_max_min(valor ,horas_minimo,'minimos',fechas)
    