


from __future__ import print_function
import os, csv, sys

import pandas as pd
import datetime

import funciones.bolsa as fb

filename1 = 'DE30.csv'
filename2 = 'US500.csv'

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


'''date1 = "2018-5-3 01:00"
y = file_1[(file_1.index == date1)]'''


fecha = []
apertura = []
cierre = []
high = []
low = []

for f in file_1.index:
    
    y = file_2[(file_2.index == f)]
    if len(y)==0: continue
    
    fecha.append(f)
    apertura.append(file_1['apertura'][f] / file_2['apertura'][0])
    cierre.append(file_1['cierre'][f] / file_2['cierre'][0])
    high.append(file_1['high'][f] / file_2['high'][0])
    low.append(file_1['low'][f] / file_2['low'][0])
    
    # print (f, file_1['cierre'][f])
    # print(file_2['cierre'][0])
    
    print (file_1['cierre'][f] / file_2['cierre'][0])
    sys.exit()
    



macd, macd_signal, macd_histograma = fb.get_macd(cierre,12,26,9)
rsi14 = fb.calcular_rsi(14, cierre)
rsi50 = fb.calcular_rsi(50, cierre)
   
estocastico_sk_14, estocastico_sd_14 = fb.calcular_estocastico(cierre, high, low, 14, 3)
estocastico_sk_50, estocastico_sd_50 = fb.calcular_estocastico(cierre, high, low, 14, 3)    
        
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
file_path="resultado2.csv"
with open( file_path, 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    dataset = ['fecha','apertura','cierre','high','low','macd','macd_signal','macd_histograma','rsi14','rsi50','esk14','esd14','esk50', 'esd50','sma[5]','ema[5]','sma[20]','ema[20]','sma[50]','ema[50]','sma[100]','ema[100]','sma[200]','ema[200]','sma[400]','ema[400]']            
    spamwriter.writerow(dataset)
                
    for x in range(0,lecturas):
        dataset = [fecha[x],apertura[x],cierre[x],high[x],low[x],macd[x],macd_signal[x],macd_histograma[x],rsi14[x],rsi50[x],estocastico_sk_14[x],estocastico_sd_14[x],estocastico_sk_50[x], estocastico_sd_50[x], sma5[x], ema5[x], sma20[x], ema20[x], sma50[x], ema50[x], sma100[x], ema100[x], sma200[x], ema200[x], sma400[x], ema400[x]]            
        spamwriter.writerow(dataset)
                



print (macd)
print (cierre)