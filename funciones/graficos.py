#! /usr/bin/env/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import csv
import sys
import os
import shutil
# import ConfigParser

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



def crear_directorio(directorio_destino):
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))    
    

def limpiar_graficas(obj_config):
    ''' limpia graficos de la carpeta /graficos/ y deja backup en
    carpeta backup'''
    
    carpeta_backup = 'graficos'
    exclude_carpeta = ['reporte']
    
    directorio_base = obj_config.get('data', 'directorio_base')
    
    directorio_destino = os.path.join(directorio_base, 'backup')
    crear_directorio(directorio_destino)

        
    directorio_destino = os.path.join(directorio_base, 'backup', carpeta_backup)
    crear_directorio(directorio_destino)
    
    now = datetime.now()
    ahora = now.strftime("%Y%m%d_%H%M")

    base_path = os.path.join(directorio_base, carpeta_backup)
    for (path, directorios, archivos) in os.walk(base_path):   
            for excluir in exclude_carpeta:
                if excluir in path: continue
                 
            if not len(archivos) > 0: continue            
            
            for archivo in archivos:
                directorios = path.split(base_path)
                directorios = directorios[1].split(os.sep)
                
                directorio_raiz = os.path.join(directorio_base, 'backup', carpeta_backup)
                for directorio in directorios:
                    directorio_destino = os.path.join(directorio_raiz, directorio)
                    crear_directorio(directorio_destino)                 
                    directorio_raiz = os.path.join(directorio_raiz, directorio)
                
                file_source = os.path.join(path, archivo)
                
                directorio_destino = os.path.join(directorio_raiz, ahora)
                crear_directorio(directorio_destino)
                
                file_dest = os.path.join(directorio_raiz, ahora, archivo)
                shutil.move(file_source, file_dest)




def graficar_valor_medias(obj_config, valor, temporalidad='D', meses=24, media=None):
    ''' graficos de las mejores medias de trading.
    resultado en /graficos/medias
    lee los valores de fichero de configuracion con tag calculo'''
    
    directorio_base = obj_config.get_directorio_base()
    filename = os.path.join(directorio_base,'csv',temporalidad,"{}.csv".format(valor))
    
    mondays = MonthLocator()
    days_fmt = DateFormatter("%d %b %y %H:%M")

    quotes = pd.read_csv(filename,
                        index_col=0,
                        parse_dates=True,
                        infer_datetime_format=True,
                        sep=";")
    
    if media is not None:
        mejor_media = fd.get_mejor_media(directorio_base,valor, 'D')
        sma_mejor = fb.get_sma_periodo(int(mejor_media),quotes['cierre'])
        
    quotes['sma_mejor'] = sma_mejor
    
    date2 = datetime.now()
    date1 = date2 - dateutil.relativedelta.relativedelta(months=meses)
    
    date1 = date1.strftime("%Y-%m-%d %H:%M")
    date2 = date2.strftime("%Y-%m-%d %H:%M")
    
    titulo = "{} ( {} ) De {} a {}".format(valor,temporalidad,date1,date2)

    quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]
        
    directorio_destino = os.path.join(directorio_base, 'graficos')    
    crear_directorio(directorio_destino)

    directorio_destino = os.path.join(directorio_base, 'graficos', 'medias')    
    crear_directorio(directorio_destino)    
    
    directorio_destino = os.path.join(directorio_base, 'graficos', 'medias', temporalidad)    
    crear_directorio(directorio_destino)
    
    cierre = [d for d in quotes['cierre']]
    sma50 = [d for d in quotes['sma[50]']]
    sma200 = [d for d in quotes['sma[200]']]
    
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
        sma_mejor = [d for d in quotes['sma_mejor']]        
        media_mejor = []
        for x in range(0,len(cierre)):
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
    ax1.xaxis.set_major_formatter(days_fmt)    
    ax1.autoscale_view()
    ax1.xaxis.grid(True, 'major')
    ax1.grid(True)    

    ax2.xaxis.set_major_locator(mondays)
    ax2.xaxis.set_major_formatter(days_fmt)    
    ax2.autoscale_view()
    ax2.xaxis.grid(True, 'major')
    ax2.grid(True)
       
    ax3.xaxis.set_major_locator(mondays)
    ax3.xaxis.set_major_formatter(days_fmt)    
    ax3.autoscale_view()
    ax3.xaxis.grid(True, 'major')
    ax3.grid(True)   
    
    fig.autofmt_xdate()

    filename_result = directorio_destino = os.path.join(directorio_base, 'graficos', 'medias', temporalidad, "{}.png".format(valor))
      
    print("generando.... {}".format(filename_result)) 
    plt.savefig(filename_result) 
    plt.close()



def grafico_simple(valor,titulo_x,titulo_y,data,tipo="linea"):
    
    x = np.arange(0,len(data))
    plt.axes()  # Definimos la posicion de los ejes
    if tipo=='linea':
        plt.plot(x,data)  # Dibujamos el grafico de barras
    elif tipo=='barra':
        plt.bar(x,data)
    
    plt.title(titulo_x, fontsize=10)
    # plt.xticks(horas, rotation = 45)  # Colocamos las etiquetas del eje x, en este caso, las fechas
    plt.ylabel(titulo_y)
    plt.show()
    plt.close()
    
    
    
def graficar_horas_max_min(config, valor,data,titulo,fechas):
    ''' grafica las horas donde se dan los maximos y minimos de un valor 
    resultado en graficos/max-min '''
    
    horas = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
    directorio_base = config.get('data', 'directorio_base')  

    plt.axes()  # Definimos la posicion de los ejes
    plt.bar(horas, data)  # Dibujamos el grafico de barras
    plt.title("{}\n{}".format(valor,fechas), fontsize=10)
    plt.xticks(horas, rotation = 45)  # Colocamos las etiquetas del eje x, en este caso, las fechas
    plt.ylabel(titulo)


    directorio_destino = os.path.join(directorio_base, 'graficos', 'max_min')    
    crear_directorio(directorio_destino)
        
    filename_result =os.path.join(directorio_base, 'graficos', 'max_min', "{}_{}.png".format(valor,titulo))
    print("generando grafico horas... {}".format(filename_result)) 
    plt.savefig(filename_result)
    plt.close()

    
    
    

def graficar_mejor_hora(obj_config, grafico, data):
    
    if not grafico: return
    directorio_base = obj_config.get_directorio_base()
    
    pips = []
    horas = []
    titulo = data[0][0]
    for d in data:
        valor,periodo,hora,pip,media = d
        horas.append(hora)
        pips.append(pip)
    
    title_string = titulo
    subtitle_string = "mejores horas trading"

    plt.axes()  # Definimos la posicion de los ejes
    plt.bar(horas, pips)  # Dibujamos el grafico de barras
    plt.title("{}\n{}".format(title_string,subtitle_string), fontsize=10)
    plt.xticks(horas, rotation = 45)  # Colocamos las etiquetas del eje x, en este caso, las fechas
    plt.ylabel('variacion de pips')

    directorio_destino = os.path.join(directorio_base, 'graficos', 'horas')    
    crear_directorio(directorio_destino)
    
    filename_result = os.path.join(directorio_base, 'graficos', 'horas', "{}.png".format(data[0][0]))
    print("generando grafico horas... {}".format(filename_result)) 
    plt.savefig(filename_result)   # save the figure to file
    plt.close()

    
    
def graficar_valor(obj_config, valor, temporalidad, tiempo = None, media = None):
    ''' graficos de las valores
    resultado en /graficos/valores'''
    directorio_base = obj_config.get_directorio_base()
    
    if media=='mejor':
        media = fd.get_mejor_media(directorio_base, valor, temporalidad)
            
    if temporalidad=='D':
        if tiempo is None: tiempo = 10 
        graficar_valor_diario(obj_config, valor, tiempo, media)
            
    elif temporalidad=='60':  
        graficar_valor_horario(obj_config, valor, tiempo, media)
        
    elif temporalidad=='W': 
        if tiempo is None: tiempo = 3
        graficar_valor_semanal(obj_config, valor, tiempo, media)



def graficar_valor_horario(config, valor, dias = None, media = None):

    temporalidad = '60'
    directorio_base = config.get('data', 'directorio_base')
    
    filename = os.path.join(directorio_base,'csv',temporalidad,"{}.csv".format(valor))

    horas = HourLocator(byhour=range(0,24,4)) # cada 4 horas
    days_fmt = DateFormatter("%d %b %y %H:%M")

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
    
    titulo = "{} ( {} ) De {} a {}".format(valor,temporalidad,date1,date2)

    
    if media is not None:
        sma = fb.get_sma_periodo(int(media),quotes['cierre'])
        quotes['sma'] = sma

    quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]

    directorio_destino = os.path.join(directorio_base, 'graficos')    
    crear_directorio(directorio_destino)

    directorio_destino = os.path.join(directorio_base, 'graficos', 'valores')    
    crear_directorio(directorio_destino)      
    
    directorio_destino = os.path.join(directorio_base, 'graficos', 'valores', temporalidad)    
    crear_directorio(directorio_destino)
        
    fig, ax = plt.subplots(figsize=(24, 12))

    
    x = zip(date2num(quotes.index.to_pydatetime()))  
    ax1 = plt.subplot2grid((8,5), (0,0), colspan=5, rowspan=5)

    plot_day_summary_oclh(ax1, zip(date2num(quotes.index.to_pydatetime()),
                              quotes['apertura'], quotes['cierre'],
                              quotes['low'], quotes['high']), ticksize=5)
    
   
    
    if media is not None:
        plt.plot(x, quotes['sma'],'k', label='MEJOR SMA {}'.format(media), linewidth=3)
    
    plt.plot(x, quotes['ema[50]'],'b', label='EMA 50', linewidth=2)
        
    plt.title("{}".format(titulo),  fontsize=20)
    
    plt.legend(loc="upper left")
    plt.grid(True)
 
       
    ax2 = plt.subplot2grid((8,5), (5, 0), colspan=5)
    
    plt.plot(x, quotes['rsi14'],'g')
    plt.grid(True)
   

    ax3 = plt.subplot2grid((8,5), (6, 0), colspan=5)
    
    plt.plot(x,quotes['esk50'], 'r')
    plt.plot(x, quotes['esd50'], 'g')
    plt.grid(True)

    
    ax4 = plt.subplot2grid((8,5), (7, 0), colspan=5)
    
    plt.plot(x, quotes['macd'], 'r')
    plt.plot(x, quotes['macd_signal'], 'g')

    plt.grid(True)
    
    ax1.xaxis.set_major_locator(horas)
    ax1.xaxis.set_major_formatter(days_fmt)    
    ax1.autoscale_view()
    ax1.xaxis.grid(True, 'major')
    ax1.grid(True)    

    ax2.xaxis.set_major_locator(horas)
    ax2.xaxis.set_major_formatter(days_fmt)    
    ax2.autoscale_view()
    ax2.xaxis.grid(True, 'major')
    ax2.grid(True)
       
    ax3.xaxis.set_major_locator(horas)
    ax3.xaxis.set_major_formatter(days_fmt)    
    ax3.autoscale_view()
    ax3.xaxis.grid(True, 'major')
    ax3.grid(True)   

    ax4.xaxis.set_major_locator(horas)
    ax4.xaxis.set_major_formatter(days_fmt)    
    ax4.autoscale_view()
    ax4.xaxis.grid(True, 'major')
    ax4.grid(True)


    fig.autofmt_xdate()

    filename_result = os.path.join(directorio_base, 'graficos', 'valores', temporalidad, "{}.png".format(valor))
      
    print("generando.... {}".format(filename_result)) 
    plt.savefig(filename_result)
    plt.close()




def graficar_valor_semanal(config, valor, annos = 3,  media = None):

    temporalidad = 'W'
    directorio_base = config.get('data', 'directorio_base')
    
    filename = os.path.join(directorio_base,'csv',temporalidad,"{}.csv".format(valor))

    # every monday
    mondays = MonthLocator()
    days_fmt = DateFormatter("%d %b %y")


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
    
    titulo = "{} ( {} ) De {} a {}".format(valor,temporalidad,date1,date2)
    directorio_destino = os.path.join(directorio_base, 'graficos')    
    crear_directorio(directorio_destino)

    directorio_destino = os.path.join(directorio_base, 'graficos', 'valores')    
    crear_directorio(directorio_destino)       
    
    directorio_destino = os.path.join(directorio_base, 'graficos', 'valores', temporalidad)    
    crear_directorio(directorio_destino)
        
    fig, ax = plt.subplots(figsize=(24, 12))

    
    x = zip(date2num(quotes.index.to_pydatetime()))

    ax1 = plt.subplot2grid((8,5), (0,0), colspan=5, rowspan=5)

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

       
    ax2 = plt.subplot2grid((8,5), (5, 0), colspan=5) 
    
    plt.plot(x, quotes['rsi14'],'g')
    plt.grid(True)
   

    ax3 = plt.subplot2grid((8,5), (6, 0), colspan=5)
    
    plt.plot(x,quotes['esk50'], 'r')
    plt.plot(x, quotes['esd50'], 'g')
    plt.grid(True)

    
    ax4 = plt.subplot2grid((8,5), (7, 0), colspan=5) 
    
    plt.plot(x, quotes['macd'], 'r')
    plt.plot(x, quotes['macd_signal'], 'g')

    plt.grid(True)
    
    ax1.xaxis.set_major_locator(mondays)
    ax1.xaxis.set_major_formatter(days_fmt)    
    ax1.autoscale_view()
    ax1.xaxis.grid(True, 'major')
    ax1.grid(True)    

    ax2.xaxis.set_major_locator(mondays)
    ax2.xaxis.set_major_formatter(days_fmt)    
    ax2.autoscale_view()
    ax2.xaxis.grid(True, 'major')
    ax2.grid(True)
       
    ax3.xaxis.set_major_locator(mondays)
    ax3.xaxis.set_major_formatter(days_fmt)    
    ax3.autoscale_view()
    ax3.xaxis.grid(True, 'major')
    ax3.grid(True)   

    ax4.xaxis.set_major_locator(mondays)
    ax4.xaxis.set_major_formatter(days_fmt)    
    ax4.autoscale_view()
    ax4.xaxis.grid(True, 'major')
    ax4.grid(True)

    fig.autofmt_xdate()

    filename_result = os.path.join(directorio_base, 'graficos', 'valores', temporalidad, "{}.png".format(valor))
      
    print("generando.... {}".format(filename_result)) 
    plt.savefig(filename_result)
    plt.close()
    
    

def graficar_valor_diario(config, valor, meses = 12,  media = None):

    temporalidad = 'D'
    directorio_base = config.get_directorio_base()
    
    filename = os.path.join(directorio_base,'csv',temporalidad,"{}.csv".format(valor))

    mondays = WeekdayLocator(MONDAY)
    days_fmt = DateFormatter("%d %b %y")

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
    
    titulo = "{} ( {} ) De {} a {}".format(valor,temporalidad,date1,date2)
    
    quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]

    directorio_destino = os.path.join(directorio_base, 'graficos')    
    crear_directorio(directorio_destino)

    directorio_destino = os.path.join(directorio_base, 'graficos', 'valores')    
    crear_directorio(directorio_destino)       
    
    directorio_destino = os.path.join(directorio_base, 'graficos', 'valores', temporalidad)    
    crear_directorio(directorio_destino)
        
    fig, ax = plt.subplots(figsize=(24, 12))
    
    x = zip(date2num(quotes.index.to_pydatetime()))

    ax1 = plt.subplot2grid((8,5), (0,0), colspan=5, rowspan=5)
    
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
    ax1.xaxis.set_major_formatter(days_fmt)    
    ax1.autoscale_view()
    ax1.xaxis.grid(True, 'major')
    ax1.grid(True)    

    ax2.xaxis.set_major_locator(mondays)
    ax2.xaxis.set_major_formatter(days_fmt)    
    ax2.autoscale_view()
    ax2.xaxis.grid(True, 'major')
    ax2.grid(True)
       
    ax3.xaxis.set_major_locator(mondays)
    ax3.xaxis.set_major_formatter(days_fmt)    
    ax3.autoscale_view()
    ax3.xaxis.grid(True, 'major')
    ax3.grid(True)   

    ax4.xaxis.set_major_locator(mondays)
    ax4.xaxis.set_major_formatter(days_fmt)    
    ax4.autoscale_view()
    ax4.xaxis.grid(True, 'major')
    ax4.grid(True)
    
    fig.autofmt_xdate()

    filename_result = os.path.join(directorio_base, 'graficos', 'valores', temporalidad, "{}.png".format(valor))
      
    print("generando.... {}".format(filename_result)) 
    plt.savefig(filename_result)
    plt.close()


def grafico_correlacion(valores, directorio_base, temporalidad, filename, meses = 12):

    mondays = MonthLocator()
    days_fmt = DateFormatter("%d %b %y")


    quotes = pd.read_csv(filename,
                        index_col=0,
                        parse_dates=True,
                        infer_datetime_format=True,
                        sep=";")

    date2 = datetime.now()
    date1 = date2 - dateutil.relativedelta.relativedelta(months=meses)
    
    date1 = date1.strftime("%Y-%m-%d %H:%M")
    date2 = date2.strftime("%Y-%m-%d %H:%M")
    
    titulo = "{} - {} ( {} ) De {} a {}".format(valores[0],valores[1],temporalidad,date1,date2)
    
    quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]

    directorio_destino = os.path.join(directorio_base, 'graficos')    
    crear_directorio(directorio_destino)

    directorio_destino = os.path.join(directorio_base, 'graficos', 'pares')    
    crear_directorio(directorio_destino)
    
    directorio_destino = os.path.join(directorio_base, 'graficos', 'pares', temporalidad)    
    crear_directorio(directorio_destino)
        
    fig, ax = plt.subplots(figsize=(24, 12))

    x = zip(date2num(quotes.index.to_pydatetime()))

    ax1 = plt.subplot2grid((8,5), (0,0), colspan=5, rowspan=5)
    
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
    ax1.xaxis.set_major_formatter(days_fmt)    
    ax1.autoscale_view()
    ax1.xaxis.grid(True, 'major')
    ax1.grid(True)    

    ax2.xaxis.set_major_locator(mondays)
    ax2.xaxis.set_major_formatter(days_fmt)    
    ax2.autoscale_view()
    ax2.xaxis.grid(True, 'major')
    ax2.grid(True)
       
    ax3.xaxis.set_major_locator(mondays)
    ax3.xaxis.set_major_formatter(days_fmt)    
    ax3.autoscale_view()
    ax3.xaxis.grid(True, 'major')
    ax3.grid(True)   

    ax4.xaxis.set_major_locator(mondays)
    ax4.xaxis.set_major_formatter(days_fmt)    
    ax4.autoscale_view()
    ax4.xaxis.grid(True, 'major')
    ax4.grid(True)

    fig.autofmt_xdate()
  
    valor1,valor2 = valores
    filename_result = os.path.join(directorio_base, 'graficos', 'pares', temporalidad, "{}-{}.png".format(valor1,valor2))
      
    print("generando.... {}".format(filename_result)) 
    plt.savefig(filename_result)
    plt.close()
    
    
    
    
    
def combinar_valores(config, valores,temporalidad, meses=12):
    ''' combina pares de valores y deja el resultado en /csv/pares/
    graficos de correlacion en /graficos/pares '''

    directorio_base = config.get_directorio_base()
    
    fname1,fname2 = valores
    filename1 = os.path.join(directorio_base, 'csv', temporalidad, fname1 + '.csv')
    filename2 = os.path.join(directorio_base, 'csv', temporalidad, fname2 + '.csv')        
    
    dir_filename_result = os.path.join(directorio_base, 'csv', 'pares')
    crear_directorio(dir_filename_result)
        
    dir_filename_result = os.path.join(directorio_base, 'csv', 'pares', temporalidad)
    crear_directorio(dir_filename_result)
    
    dir_filename_result = os.path.join(directorio_base, 'csv', 'pares', temporalidad)
    crear_directorio(dir_filename_result)

    filename3 = os.path.join(directorio_base, 'csv', 'pares', temporalidad, "{}-{}.csv".format(fname1,fname2))   

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
                


    grafico_correlacion(valores, directorio_base, temporalidad, filename3, meses)