


from __future__ import print_function
import os, csv, sys

import matplotlib.pyplot as plt
from pylab import *
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.dates import (MONDAY, DateFormatter, MonthLocator,
                              WeekdayLocator, HourLocator, date2num)

import datetime
import ConfigParser

import funciones.bolsa as fb




def correlacion(VALORES, DIRECTORIO_BASE, TEMPORALIDAD, filename):
    
    
    titulo = "{} - {} ( {} )".format(VALORES[0],VALORES[1],TEMPORALIDAD)
    # every monday
    mondays = MonthLocator()
    daysFmt = DateFormatter("%d %b %y")


    quotes = pd.read_csv(filename,
                        index_col=0,
                        parse_dates=True,
                        infer_datetime_format=True,
                        sep=";")
    
    # eliminar valores nulos por macd, emas, etc
    
    date1 = "2016-6-12 00:00"
    date2 = "2018-6-12 23:00"

    quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]
    
    directorio_destino = os.path.join(DIRECTORIO_BASE, 'pares', TEMPORALIDAD)    
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
    plt.plot(x, quotes['ema[100]'],'y', label='EMA100')
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
    filenameResult = directorio_destino = os.path.join(DIRECTORIO_BASE, 'pares', "par-{}-{}.png".format(valor1,valor2))
      
    print("generando.... {}".format(filenameResult)) 
    plt.savefig(filenameResult)   # save the figure to file
    # plt.show()
    plt.close()
    
    
    
    
    
def combinarValores(DIRECTORIO_BASE,VALORES,TEMPORALIDAD):

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
        
        # print (f, file_1['cierre'][f])
        
        # print(a.values[0])
        # sys.exit()
        
        
        
   
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
    with open( filename3, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dataset = ['fecha','apertura','cierre','high','low','macd','macd_signal','macd_histograma','rsi14','rsi50','esk14','esd14','esk50', 'esd50','sma[5]','ema[5]','sma[20]','ema[20]','sma[50]','ema[50]','sma[100]','ema[100]','sma[200]','ema[200]','sma[400]','ema[400]']            
        spamwriter.writerow(dataset)
                    
        for x in range(0,lecturas):
            dataset = [fecha[x],apertura[x],cierre[x],high[x],low[x],macd[x],macd_signal[x],macd_histograma[x],rsi14[x],rsi50[x],estocastico_sk_14[x],estocastico_sd_14[x],estocastico_sk_50[x], estocastico_sd_50[x], sma5[x], ema5[x], sma20[x], ema20[x], sma50[x], ema50[x], sma100[x], ema100[x], sma200[x], ema200[x], sma400[x], ema400[x]]            
            spamwriter.writerow(dataset)
                


    correlacion(VALORES, DIRECTORIO_BASE, TEMPORALIDAD, filename3)


configuracion = 'configuracion.cfg'

def main():
        
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    DIRECTORIO_BASE = config.get('data', 'directorio_base')
    VALORES = ('DE30','IBEX35')
    TEMPORALIDAD = 'D'
    combinarValores(DIRECTORIO_BASE,VALORES,TEMPORALIDAD)
    


if __name__ == '__main__':
    main()
    
    
