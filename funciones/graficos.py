#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import csv
import sys
import os
import shutil
import ConfigParser

import matplotlib.pyplot as plt
from pylab import *
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.dates import (MONDAY, DateFormatter, MonthLocator,
                              WeekdayLocator, HourLocator, date2num, num2date)

from mpl_finance import plot_day_summary_oclh


import dateutil.relativedelta
from datetime import datetime, timedelta


import bolsa as fb
import data as fd
from matplotlib import _mathtext_data





def limpiarGraficas():
    
    carpeta_backup = 'graficos'
    exclude_carpeta = ['reporte']
    
    config = ConfigParser.ConfigParser()
    config.read('configuracion.cfg')
    directorio_base = config.get('data', 'directorio_base')
    
    directorio_destino = os.path.join(directorio_base, 'backup')
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))
        
    directorio_destino = os.path.join(directorio_base, 'backup', carpeta_backup)
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))
    
    now = datetime.now()
    ahora = now.strftime("%Y%m%d_%H%M")

    base_path = os.path.join(directorio_base, carpeta_backup)
    for (path, directorios, archivos) in os.walk(base_path):   
            for excluir in exclude_carpeta:
                if excluir in path: continue
                 
            if not len(archivos) > 0: continue            
            
            for archivo in archivos:
                # directorio_destino =  os.path.join(directorio_base,'backup',carpeta_backup)
                
                directorios = path.split(base_path)
                directorios = directorios[1].split(os.sep)
                
                directorio_raiz = os.path.join(directorio_base, 'backup', carpeta_backup)
                for directorio in directorios:
                    directorio_destino = os.path.join(directorio_raiz, directorio)
                    if not os.path.exists(directorio_destino):
                        os.makedirs(directorio_destino)
                        print ("creando directorio.... {}".format(directorio_destino))                    
                    directorio_raiz = os.path.join(directorio_raiz, directorio)
                
                file_source = os.path.join(path, archivo)
                
                directorio_destino = os.path.join(directorio_raiz, ahora)
                if not os.path.exists(directorio_destino):
                    os.makedirs(directorio_destino)
                    print ("creando directorio.... {}".format(directorio_destino))
                
                file_dest = os.path.join(directorio_raiz, ahora, archivo)
                shutil.move(file_source, file_dest)

def graficarValorMedias(VALOR, TEMPORALIDAD='D', meses=24, media=None):

    configuracion = 'configuracion.cfg'
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    DIRECTORIO_BASE = config.get('data', 'directorio_base')
    
    
    filename = os.path.join(DIRECTORIO_BASE,'csv',TEMPORALIDAD,"{}.csv".format(VALOR))
    
    # every monday
    mondays = MonthLocator()
    daysFmt = DateFormatter("%d %b %y %H:%M")

    quotes = pd.read_csv(filename,
                        index_col=0,
                        parse_dates=True,
                        infer_datetime_format=True,
                        sep=";")
    
    if media is not None:
        mejor_media = fd.getMejorMedia(VALOR, 'D')
        sma_mejor = fb.get_sma_periodo(int(mejor_media),quotes['cierre'])
        
    quotes['sma_mejor'] = sma_mejor
    
    
    date2 = datetime.now()
    date1 = date2 - dateutil.relativedelta.relativedelta(months=meses)
    
    date1 = date1.strftime("%Y-%m-%d %H:%M")
    date2 = date2.strftime("%Y-%m-%d %H:%M")
    
    titulo = "{} ( {} ) De {} a {}".format(VALOR,TEMPORALIDAD,date1,date2)

    quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]
        
    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))

    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'medias')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))        
    
    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'medias', TEMPORALIDAD)    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))
    
    
    cierre = []
    for d in quotes['cierre']:
        cierre.append(d)
    
    sma50 = []
    for d in quotes['sma[50]']:
        sma50.append(d)

    sma200 = []
    for d in quotes['sma[200]']:
        sma200.append(d)
    
    media_50 = []
    media_200 = []
    media = []
    for x in range(0,len(cierre)):
        dif_50 = cierre[x] - sma50[x]
        dif_200 = cierre[x] - sma200[x]
                      
        media_50.append(dif_50)
        media_200.append(dif_200)

        media.append(dif_200 - dif_50)  
    
    quotes['dif_media'] = media
    quotes['dif_media_50'] = media_50
    quotes['dif_media_200'] = media_200


        
    if media is not None:
        sma_mejor = []
        for d in quotes['sma_mejor']:
            sma_mejor.append(d)
        
        media_mejor = []
        for x in range(0,len(cierre)):
            # dif_50 = abs(cierre[x] - sma50[x])
            #dif_200 = abs(cierre[x] - sma200[x])
 
            dif_mejor = cierre[x] - sma_mejor[x]
            media_mejor.append(dif_mejor)    
    
            
      
        quotes['media_sma_mejor'] = media_mejor
        
    
    
    
    fig, ax = plt.subplots(figsize=(24, 12))

    
    x = zip(date2num(quotes.index.to_pydatetime()))  
    
    ax1 = plt.subplot2grid((9,1), (0,0), rowspan=3)
    plt.bar(arange(0,len(quotes['media_sma_mejor']),1), quotes['media_sma_mejor'], label='mejor')
    plt.legend(loc="upper left")

    plt.title("{}".format(titulo),  fontsize=20)
    plt.grid(True)

    
    ax2 = plt.subplot2grid((9,1), (3, 0), rowspan=3) 
    plt.bar(arange(0,len(quotes['dif_media']),1), quotes['dif_media'], label='dorado')
    plt.legend(loc="upper left")
    plt.grid(True)
    
    ax3 = plt.subplot2grid((9,1), (6, 0), rowspan=3) 
    plt.plot(x, quotes['cierre'],'b', label='PRECIO', linewidth=2)
    plt.plot(x, quotes['sma[50]'], 'r', label='50', linewidth=1)
    plt.plot(x, quotes['sma[200]'], 'g', label='200', linewidth=1)
    plt.plot(x, quotes['sma_mejor'], 'k', label='mejor {}'.format(mejor_media), linewidth=1)
    
    plt.legend(loc="upper left")
    
    ax1.xaxis.set_major_locator(mondays)
    ax1.xaxis.set_major_formatter(daysFmt)    
    ax1.autoscale_view()
    ax1.xaxis.grid(True, 'major')
    ax1.grid(True)    

    ax2.xaxis.set_major_locator(mondays)
    ax2.xaxis.set_major_formatter(daysFmt)    
    ax2.autoscale_view()
    ax2.xaxis.grid(True, 'major')
    ax2.grid(True)
       
    ax3.xaxis.set_major_locator(mondays)
    ax3.xaxis.set_major_formatter(daysFmt)    
    ax3.autoscale_view()
    ax3.xaxis.grid(True, 'major')
    ax3.grid(True)   


    fig.autofmt_xdate()


    filenameResult = directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'medias', TEMPORALIDAD, "{}.png".format(VALOR))
      
    print("generando.... {}".format(filenameResult)) 
    plt.savefig(filenameResult)   # save the figure to file
    # plt.show()
    plt.close()



def graficoSimple(valor,tituloX,tituloY,data,tipo="linea"):

    
    
    x = np.arange(0,len(data))
    plt.axes()  # Definimos la posicion de los ejes
    if tipo=='linea':
        plt.plot(x,data)  # Dibujamos el grafico de barras
    elif tipo=='barra':
        plt.bar(x,data)
    
    plt.title(tituloX, fontsize=10)
    # plt.xticks(horas, rotation = 45)  # Colocamos las etiquetas del eje x, en este caso, las fechas
    plt.ylabel(tituloY)
    plt.show()
    plt.close()
    
    
    
def graficarHorasMaxMin(valor,data,titulo,fechas):
    
    horas = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
    configuracion = 'configuracion.cfg'
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    DIRECTORIO_BASE = config.get('data', 'directorio_base')
            

    plt.axes()  # Definimos la posicion de los ejes
    plt.bar(horas, data)  # Dibujamos el grafico de barras
    plt.title("{}\n{}".format(valor,fechas), fontsize=10)
    plt.xticks(horas, rotation = 45)  # Colocamos las etiquetas del eje x, en este caso, las fechas
    plt.ylabel(titulo)

    
    
    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'max_min')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))
        
    filenameResult =os.path.join(DIRECTORIO_BASE, 'graficos', 'max_min', "{}_{}.png".format(valor,titulo))
    print("generando grafico horas... {}".format(filenameResult)) 
    plt.savefig(filenameResult)   # save the figure to file    
    # plt.show()
    plt.close()

    
    
    

def graficarMejorHora(data):
    
    
    configuracion = 'configuracion.cfg'
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    DIRECTORIO_BASE = config.get('data', 'directorio_base')
    
    pips = []
    horas = []
    titulo = data[0][0]
    for d in data:
        valor,tipo,periodo,hora,pip,media = d
        horas.append(hora)
        pips.append(pip)
    
    title_string = titulo
    subtitle_string = "mejores horas trading"

    plt.axes()  # Definimos la posicion de los ejes
    plt.bar(horas, pips)  # Dibujamos el grafico de barras
    plt.title("{}\n{}".format(title_string,subtitle_string), fontsize=10)
    plt.xticks(horas, rotation = 45)  # Colocamos las etiquetas del eje x, en este caso, las fechas
    plt.ylabel('variacion de pips')

    
    filenameResult =os.path.join(DIRECTORIO_BASE, 'graficos', 'horas', "{}.png".format(data[0][0]))
    print("generando grafico horas... {}".format(filenameResult)) 
    plt.savefig(filenameResult)   # save the figure to file
    plt.close()

    
    
def graficarValor(VALOR, TEMPORALIDAD, tiempo = None, media = None):
    if TEMPORALIDAD=='D':
        if tiempo is None:
            tiempo = 10 
        if media=='mejor':
            media = fd.getMejorMedia(VALOR, 'D')
       
        graficarValorDiario(VALOR, tiempo, media)
            
    
    elif TEMPORALIDAD=='60': 
        if media=='mejor':
            media = fd.getMejorMedia(VALOR, '60')
        
        graficarValorHorario(VALOR, tiempo, media)
        
        
        
    elif TEMPORALIDAD=='W': 
        if media=='mejor':
            media = fd.getMejorMedia(VALOR, 'W')
        if tiempo is not None:
            graficarValorSemanal(VALOR, tiempo, media)
        else:
            graficarValorSemanal(VALOR, 3, media)



def graficarValorHorario(VALOR, dias = None, media = None):

    TEMPORALIDAD = '60'
    configuracion = 'configuracion.cfg'
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    DIRECTORIO_BASE = config.get('data', 'directorio_base')
    
    filename = os.path.join(DIRECTORIO_BASE,'csv',TEMPORALIDAD,"{}.csv".format(VALOR))
    
    
    # every monday
    horas = HourLocator(byhour=range(0,24,4)) # cada 4 horas
    daysFmt = DateFormatter("%d %b %y %H:%M")


    quotes = pd.read_csv(filename,
                        index_col=0,
                        parse_dates=True,
                        infer_datetime_format=True,
                        sep=";")
    
    if dias is None:
        today = datetime.now()
        idx = (today.weekday() + 1) % 7 # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
    else:
        idx = dias
    
    if idx==0:
         idx=7
    
    date2 = datetime.now()
    date1 = date2 - timedelta(days=idx)
    
    date1 = date1.strftime("%Y-%m-%d %H:%M")
    date2 = date2.strftime("%Y-%m-%d %H:%M")
    
    titulo = "{} ( {} ) De {} a {}".format(VALOR,TEMPORALIDAD,date1,date2)

    
    if media is not None:
        sma = fb.get_sma_periodo(int(media),quotes['cierre'])
        quotes['sma'] = sma

    quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]

    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))

    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'valores')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))        
    
    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'valores', TEMPORALIDAD)    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))
        
    fig, ax = plt.subplots(figsize=(24, 12))

    
    x = zip(date2num(quotes.index.to_pydatetime()))  
    ax1 = plt.subplot2grid((8,5), (0,0), colspan=5, rowspan=5)
    
    
    # candlestick2_ohlc(ax,data_open[desde:],data_high[desde:],data_low[desde:],data_cierre[desde:],width=0.6)
    plot_day_summary_oclh(ax1, zip(date2num(quotes.index.to_pydatetime()),
                              quotes['apertura'], quotes['cierre'],
                              quotes['low'], quotes['high']), ticksize=5)
    
   
    
    if media is not None:
        plt.plot(x, quotes['sma'],'k', label='MEJOR SMA {}'.format(media), linewidth=3)
    
    plt.plot(x, quotes['ema[50]'],'b', label='EMA 50', linewidth=2)
        
    plt.title("{}".format(titulo),  fontsize=20)
    
    plt.legend(loc="upper left")
    plt.grid(True)
    
    

    
    
    
       
    ax2 = plt.subplot2grid((8,5), (5, 0), colspan=5) # plt.subplot(5, 1, 1, rowspan=3)
    
    plt.plot(x, quotes['rsi14'],'g')
    plt.grid(True)
   

    ax3 = plt.subplot2grid((8,5), (6, 0), colspan=5) # plt.subplot(5, 1, 4)
    
    plt.plot(x,quotes['esk50'], 'r')
    plt.plot(x, quotes['esd50'], 'g')
    plt.grid(True)

    
    ax4 = plt.subplot2grid((8,5), (7, 0), colspan=5) # plt.subplot(5, 1, 5)
    
    plt.plot(x, quotes['macd'], 'r')
    plt.plot(x, quotes['macd_signal'], 'g')

    plt.grid(True)


    
    ax1.xaxis.set_major_locator(horas)
    ax1.xaxis.set_major_formatter(daysFmt)    
    ax1.autoscale_view()
    ax1.xaxis.grid(True, 'major')
    ax1.grid(True)    

    ax2.xaxis.set_major_locator(horas)
    ax2.xaxis.set_major_formatter(daysFmt)    
    ax2.autoscale_view()
    ax2.xaxis.grid(True, 'major')
    ax2.grid(True)
       
    ax3.xaxis.set_major_locator(horas)
    ax3.xaxis.set_major_formatter(daysFmt)    
    ax3.autoscale_view()
    ax3.xaxis.grid(True, 'major')
    ax3.grid(True)   

    ax4.xaxis.set_major_locator(horas)
    ax4.xaxis.set_major_formatter(daysFmt)    
    ax4.autoscale_view()
    ax4.xaxis.grid(True, 'major')
    ax4.grid(True)


    fig.autofmt_xdate()


    filenameResult = directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'valores', TEMPORALIDAD, "{}.png".format(VALOR))
      
    print("generando.... {}".format(filenameResult)) 
    plt.savefig(filenameResult)   # save the figure to file
    # plt.show()
    plt.close()


def graficarValorSemanal(VALOR, annos = 3,  media = None):

    TEMPORALIDAD = 'W'
    configuracion = 'configuracion.cfg'
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    DIRECTORIO_BASE = config.get('data', 'directorio_base')
    
    filename = os.path.join(DIRECTORIO_BASE,'csv',TEMPORALIDAD,"{}.csv".format(VALOR))
    
    
    # every monday
    mondays = MonthLocator()
    daysFmt = DateFormatter("%d %b %y")


    quotes = pd.read_csv(filename,
                        index_col=0,
                        parse_dates=True,
                        infer_datetime_format=True,
                        sep=";")
    
    if media is not None:
        sma = fb.get_sma_periodo(int(media),quotes['cierre'])
        quotes['sma'] = sma
        
    date2 = datetime.now()
    date1 = date2 - dateutil.relativedelta.relativedelta(years=annos)
    
    date1 = date1.strftime("%Y-%m-%d %H:%M")
    date2 = date2.strftime("%Y-%m-%d %H:%M")

    quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]

    nueva_fecha = None
    for f in quotes.index:  
        a = quotes['sma[200]'][(quotes.index == f)]     
        if a.values[0]>0: 
            nueva_fecha = f
            break
    
    if nueva_fecha is not None:
        quotes = quotes[(quotes.index > f) & (quotes.index <= date2)]
        date1 = f.strftime("%Y-%m-%d %H:%M")
    
    titulo = "{} ( {} ) De {} a {}".format(VALOR,TEMPORALIDAD,date1,date2)
    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))

    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'valores')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))        
    
    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'valores', TEMPORALIDAD)    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))
        
    fig, ax = plt.subplots(figsize=(24, 12))

    
    x = zip(date2num(quotes.index.to_pydatetime()))

    ax1 = plt.subplot2grid((8,5), (0,0), colspan=5, rowspan=5)
    
    
    # candlestick2_ohlc(ax,data_open[desde:],data_high[desde:],data_low[desde:],data_cierre[desde:],width=0.6)
    plot_day_summary_oclh(ax1, zip(date2num(quotes.index.to_pydatetime()),
                              quotes['apertura'], quotes['cierre'],
                              quotes['low'], quotes['high']), ticksize=5)
    
   
    
    if media is not None:
        plt.plot(x, quotes['sma'],'k', label='MEJOR SMA {}'.format(media), linewidth=2)
        
    plt.plot(x, quotes['ema[50]'],'b', label='EMA50')
    plt.plot(x, quotes['ema[200]'],'y', label='EMA200')
    plt.title("{}".format(titulo),  fontsize=20)
    
    plt.legend(loc="upper left")
    plt.grid(True)
    
    

    
    
    
       
    ax2 = plt.subplot2grid((8,5), (5, 0), colspan=5) # plt.subplot(5, 1, 1, rowspan=3)
    
    plt.plot(x, quotes['rsi14'],'g')
    plt.grid(True)
   

    ax3 = plt.subplot2grid((8,5), (6, 0), colspan=5) # plt.subplot(5, 1, 4)
    
    plt.plot(x,quotes['esk50'], 'r')
    plt.plot(x, quotes['esd50'], 'g')
    plt.grid(True)

    
    ax4 = plt.subplot2grid((8,5), (7, 0), colspan=5) # plt.subplot(5, 1, 5)
    
    plt.plot(x, quotes['macd'], 'r')
    plt.plot(x, quotes['macd_signal'], 'g')

    plt.grid(True)


    
    ax1.xaxis.set_major_locator(mondays)
    ax1.xaxis.set_major_formatter(daysFmt)    
    ax1.autoscale_view()
    ax1.xaxis.grid(True, 'major')
    ax1.grid(True)    

    ax2.xaxis.set_major_locator(mondays)
    ax2.xaxis.set_major_formatter(daysFmt)    
    ax2.autoscale_view()
    ax2.xaxis.grid(True, 'major')
    ax2.grid(True)
       
    ax3.xaxis.set_major_locator(mondays)
    ax3.xaxis.set_major_formatter(daysFmt)    
    ax3.autoscale_view()
    ax3.xaxis.grid(True, 'major')
    ax3.grid(True)   

    ax4.xaxis.set_major_locator(mondays)
    ax4.xaxis.set_major_formatter(daysFmt)    
    ax4.autoscale_view()
    ax4.xaxis.grid(True, 'major')
    ax4.grid(True)


    fig.autofmt_xdate()


    filenameResult = directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'valores', TEMPORALIDAD, "{}.png".format(VALOR))
      
    print("generando.... {}".format(filenameResult)) 
    plt.savefig(filenameResult)   # save the figure to file
    # plt.show()
    plt.close()
    
    

def graficarValorDiario(VALOR, meses = 12,  media = None):

    TEMPORALIDAD = 'D'
    configuracion = 'configuracion.cfg'
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    DIRECTORIO_BASE = config.get('data', 'directorio_base')
    
    filename = os.path.join(DIRECTORIO_BASE,'csv',TEMPORALIDAD,"{}.csv".format(VALOR))
    
    
    # every monday
    mondays = WeekdayLocator(MONDAY)
    daysFmt = DateFormatter("%d %b %y")


    quotes = pd.read_csv(filename,
                        index_col=0,
                        parse_dates=True,
                        infer_datetime_format=True,
                        sep=";")
    
    if media is not None:
        sma = fb.get_sma_periodo(int(media),quotes['cierre'])
        quotes['sma'] = sma
        
     
    date2 = datetime.now()
    date1 = date2 - dateutil.relativedelta.relativedelta(months=meses)
    
    date1 = date1.strftime("%Y-%m-%d %H:%M")
    date2 = date2.strftime("%Y-%m-%d %H:%M")
    
    titulo = "{} ( {} ) De {} a {}".format(VALOR,TEMPORALIDAD,date1,date2)
    

    quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]




    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))

    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'valores')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))        
    
    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'valores', TEMPORALIDAD)    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))
        
    fig, ax = plt.subplots(figsize=(24, 12))

    
    x = zip(date2num(quotes.index.to_pydatetime()))

    ax1 = plt.subplot2grid((8,5), (0,0), colspan=5, rowspan=5)
    
    
    # candlestick2_ohlc(ax,data_open[desde:],data_high[desde:],data_low[desde:],data_cierre[desde:],width=0.6)
    plot_day_summary_oclh(ax1, zip(date2num(quotes.index.to_pydatetime()),
                              quotes['apertura'], quotes['cierre'],
                              quotes['low'], quotes['high']), ticksize=5)
    
   
    
    if media is not None:
        plt.plot(x, quotes['sma'],'k', label='MEJOR SMA {}'.format(media), linewidth=2)
        
    plt.plot(x, quotes['ema[50]'],'b', label='EMA50')
    plt.plot(x, quotes['ema[200]'],'y', label='EMA200')
    plt.title("{}".format(titulo),  fontsize=20)
    
    plt.legend(loc="upper left")
    plt.grid(True)
    
    

    
    
    
       
    ax2 = plt.subplot2grid((8,5), (5, 0), colspan=5) # plt.subplot(5, 1, 1, rowspan=3)
    
    plt.plot(x, quotes['rsi14'],'g')
    plt.grid(True)
   

    ax3 = plt.subplot2grid((8,5), (6, 0), colspan=5) # plt.subplot(5, 1, 4)
    
    plt.plot(x,quotes['esk50'], 'r')
    plt.plot(x, quotes['esd50'], 'g')
    plt.grid(True)

    
    ax4 = plt.subplot2grid((8,5), (7, 0), colspan=5) # plt.subplot(5, 1, 5)
    
    plt.plot(x, quotes['macd'], 'r')
    plt.plot(x, quotes['macd_signal'], 'g')

    plt.grid(True)


    
    ax1.xaxis.set_major_locator(mondays)
    ax1.xaxis.set_major_formatter(daysFmt)    
    ax1.autoscale_view()
    ax1.xaxis.grid(True, 'major')
    ax1.grid(True)    

    ax2.xaxis.set_major_locator(mondays)
    ax2.xaxis.set_major_formatter(daysFmt)    
    ax2.autoscale_view()
    ax2.xaxis.grid(True, 'major')
    ax2.grid(True)
       
    ax3.xaxis.set_major_locator(mondays)
    ax3.xaxis.set_major_formatter(daysFmt)    
    ax3.autoscale_view()
    ax3.xaxis.grid(True, 'major')
    ax3.grid(True)   

    ax4.xaxis.set_major_locator(mondays)
    ax4.xaxis.set_major_formatter(daysFmt)    
    ax4.autoscale_view()
    ax4.xaxis.grid(True, 'major')
    ax4.grid(True)


    fig.autofmt_xdate()


    filenameResult = directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'valores', TEMPORALIDAD, "{}.png".format(VALOR))
      
    print("generando.... {}".format(filenameResult)) 
    plt.savefig(filenameResult)   # save the figure to file
    # plt.show()
    plt.close()


def graficoCorrelacion(VALORES, DIRECTORIO_BASE, TEMPORALIDAD, filename, meses = 12):
    
    # every monday
    mondays = MonthLocator()
    daysFmt = DateFormatter("%d %b %y")


    quotes = pd.read_csv(filename,
                        index_col=0,
                        parse_dates=True,
                        infer_datetime_format=True,
                        sep=";")
    
    # eliminar valores nulos por macd, emas, etc

    date2 = datetime.now()
    date1 = date2 - dateutil.relativedelta.relativedelta(months=meses)
    
    date1 = date1.strftime("%Y-%m-%d %H:%M")
    date2 = date2.strftime("%Y-%m-%d %H:%M")
    
    titulo = "{} - {} ( {} ) De {} a {}".format(VALORES[0],VALORES[1],TEMPORALIDAD,date1,date2)
    
    quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]

    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))

    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'pares')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))        
    
    directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'pares', TEMPORALIDAD)    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))
        
    fig, ax = plt.subplots(figsize=(24, 12))

    
    x = zip(date2num(quotes.index.to_pydatetime()))

    ax1 = plt.subplot2grid((8,5), (0,0), colspan=5, rowspan=5)
    
    
    # candlestick2_ohlc(ax,data_open[desde:],data_high[desde:],data_low[desde:],data_cierre[desde:],width=0.6)
    plt.plot(x, quotes['cierre'],'g',linewidth=3, label='DATA')
    plt.plot(x, quotes['ema[20]'],'r', label='EMA20')
    plt.plot(x, quotes['ema[50]'],'b', label='EMA50')
    plt.plot(x, quotes['ema[200]'],'y', label='EMA200')
    
    plt.title("{}".format(titulo),  fontsize=20)
    
    plt.legend(loc="upper left")
    plt.grid(True)
    
    

    
    
    
       
    ax2 = plt.subplot2grid((8,5), (5, 0), colspan=5) # plt.subplot(5, 1, 1, rowspan=3)
    
    plt.plot(x, quotes['rsi14'],'g')
    plt.grid(True)
   

    ax3 = plt.subplot2grid((8,5), (6, 0), colspan=5) # plt.subplot(5, 1, 4)
    
    plt.plot(x,quotes['esk50'], 'r')
    plt.plot(x, quotes['esd50'], 'g')
    plt.grid(True)

    
    ax4 = plt.subplot2grid((8,5), (7, 0), colspan=5) # plt.subplot(5, 1, 5)
    
    plt.plot(x, quotes['macd'], 'r')
    plt.plot(x, quotes['macd_signal'], 'g')

    plt.grid(True)


    
    ax1.xaxis.set_major_locator(mondays)
    ax1.xaxis.set_major_formatter(daysFmt)    
    ax1.autoscale_view()
    ax1.xaxis.grid(True, 'major')
    ax1.grid(True)    

    ax2.xaxis.set_major_locator(mondays)
    ax2.xaxis.set_major_formatter(daysFmt)    
    ax2.autoscale_view()
    ax2.xaxis.grid(True, 'major')
    ax2.grid(True)
       
    ax3.xaxis.set_major_locator(mondays)
    ax3.xaxis.set_major_formatter(daysFmt)    
    ax3.autoscale_view()
    ax3.xaxis.grid(True, 'major')
    ax3.grid(True)   

    ax4.xaxis.set_major_locator(mondays)
    ax4.xaxis.set_major_formatter(daysFmt)    
    ax4.autoscale_view()
    ax4.xaxis.grid(True, 'major')
    ax4.grid(True)


    fig.autofmt_xdate()


    
    
    valor1,valor2 = VALORES
    filenameResult = directorio_destino = os.path.join(DIRECTORIO_BASE, 'graficos', 'pares', TEMPORALIDAD, "{}-{}.png".format(valor1,valor2))
      
    print("generando.... {}".format(filenameResult)) 
    plt.savefig(filenameResult)   # save the figure to file
    # plt.show()
    plt.close()
    
    
    
    
    
def combinarValores(VALORES,TEMPORALIDAD, MESES=12):

    configuracion = 'configuracion.cfg'
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    DIRECTORIO_BASE = config.get('data', 'directorio_base')
    
    
    fname1,fname2 = VALORES
    filename1 = os.path.join(DIRECTORIO_BASE, 'csv', TEMPORALIDAD, fname1 + '.csv')
    filename2 = os.path.join(DIRECTORIO_BASE, 'csv', TEMPORALIDAD, fname2 + '.csv')        
    
    dirFilenameResult = os.path.join(DIRECTORIO_BASE, 'csv', 'pares')
    if not os.path.exists(dirFilenameResult):
        os.makedirs(dirFilenameResult)
        print ("creando directorio.... {}".format(dirFilenameResult))
        
    dirFilenameResult = os.path.join(DIRECTORIO_BASE, 'csv', 'pares', TEMPORALIDAD)
    if not os.path.exists(dirFilenameResult):
        os.makedirs(dirFilenameResult)
        print ("creando directorio.... {}".format(dirFilenameResult))
    
    dirFilenameResult = os.path.join(DIRECTORIO_BASE, 'csv', 'pares', TEMPORALIDAD)
    if not os.path.exists(dirFilenameResult):
        os.makedirs(dirFilenameResult)
        print ("creando directorio.... {}".format(dirFilenameResult))
        
    filename3 = os.path.join(DIRECTORIO_BASE, 'csv', 'pares', TEMPORALIDAD, "{}-{}.csv".format(fname1,fname2))   

    file_1 = pd.read_csv(filename1,
                        index_col=0,
                        parse_dates=True,
                        infer_datetime_format=True,
                        sep=";")
      
    file_2 = pd.read_csv(filename2,
                        index_col=0,
                        parse_dates=True,
                        infer_datetime_format=True,
                        sep=";")
    
        
    fecha = []
    apertura = []
    cierre = []
    high = []
    low = []
    
    for f in file_1.index:
        
        y = file_2[(file_2.index == f)]
        if len(y)==0: continue
        
        a = file_2['apertura'][(file_2.index == f)]
        b = file_2['cierre'][(file_2.index == f)]
        c = file_2['high'][(file_2.index == f)]
        d = file_2['low'][(file_2.index == f)]
        
        fecha.append(f)
        apertura.append(file_1['apertura'][f] / a.values[0])
        cierre.append(file_1['cierre'][f] / b.values[0])
        high.append(file_1['high'][f] / c.values[0])
        low.append(file_1['low'][f] / d.values[0])
        
    macd, macd_signal, macd_histograma = fb.get_macd(cierre,12,26,9)
    rsi14 = fb.calcular_rsi(14, cierre)
    rsi50 = fb.calcular_rsi(50, cierre)
       
    estocastico_sk_14, estocastico_sd_14 = fb.calcular_estocastico(cierre, high, low, 14, 3)
    estocastico_sk_50, estocastico_sd_50 = fb.calcular_estocastico(cierre, high, low, 20, 3)    
            
    #calcula emas de 5 a 200
    sma5 = fb.get_sma_periodo(5,cierre)
    ema5 = fb.get_ema_periodo(5,cierre)
    
    sma20 = fb.get_sma_periodo(20,cierre)
    ema20 = fb.get_ema_periodo(20,cierre)
        
    sma200 = fb.get_sma_periodo(200,cierre)
    ema200 = fb.get_ema_periodo(200,cierre)
    
    sma100 = fb.get_sma_periodo(100,cierre)
    ema100 = fb.get_ema_periodo(100,cierre)
    
    sma50 = fb.get_sma_periodo(50,cierre)
    ema50 = fb.get_ema_periodo(50,cierre)
        
    sma400 = fb.get_sma_periodo(400,cierre)
    ema400 = fb.get_ema_periodo(400,cierre)
        
    lecturas = len(cierre)    
    print ("creando fichero.... {}".format(filename3))
    with open( filename3, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dataset = ['fecha','apertura','cierre','high','low','macd','macd_signal','macd_histograma','rsi14','rsi50','esk14','esd14','esk50', 'esd50','sma[5]','ema[5]','sma[20]','ema[20]','sma[50]','ema[50]','sma[100]','ema[100]','sma[200]','ema[200]','sma[400]','ema[400]']            
        spamwriter.writerow(dataset)
                    
        for x in range(0,lecturas):
            dataset = [fecha[x],apertura[x],cierre[x],high[x],low[x],macd[x],macd_signal[x],macd_histograma[x],rsi14[x],rsi50[x],estocastico_sk_14[x],estocastico_sd_14[x],estocastico_sk_50[x], estocastico_sd_50[x], sma5[x], ema5[x], sma20[x], ema20[x], sma50[x], ema50[x], sma100[x], ema100[x], sma200[x], ema200[x], sma400[x], ema400[x]]            
            spamwriter.writerow(dataset)
                


    graficoCorrelacion(VALORES, DIRECTORIO_BASE, TEMPORALIDAD, filename3, MESES)