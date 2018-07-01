#! /usr/bin/env/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import pandas as pd
import ConfigParser
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from array import array

def test_graph(data, valor, hora_inicio, hora_final, hora_destino):
    
    df = pd.DataFrame(data)
    df.columns = ['puntos_inicio','puntos_final']
    
    colores=['green','blue', 'red', 'black']
    tamanios=[30,60]

    asignar=[]
    for index, row in df.iterrows():
        if (row['puntos_inicio'] > 0): 
            if row['puntos_final'] > row['puntos_inicio']:
                asignar.append(colores[0])
            else:
                asignar.append(colores[1])
        elif (row['puntos_inicio'] < 0): 
            if row['puntos_final'] < row['puntos_inicio']:
                asignar.append(colores[2])
            else:
                asignar.append(colores[1])
        else:
            asignar.append(colores[3])
            
    directorio_destino = os.path.join(dir_base, 'graficos')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))
        
    directorio_destino = os.path.join(dir_base, 'graficos', 'comparativaHoraria')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))
        
    
    filename_grafico = os.path.join(dir_base, 'graficos', 'comparativaHoraria', '{}-{}-{}-{}.png'.format(valor,hora_inicio, hora_final,hora_destino))       
                
    plt.scatter(df['puntos_inicio'], df['puntos_final'], c=asignar, s=tamanios[0])
    plt.title('Comparativa {} {}-{} a {}'.format(valor, hora_inicio, hora_final, hora_destino))
    plt.xlabel('PUNTOS A LAS {}-{} '.format(hora_inicio,hora_final))
    plt.ylabel('PUNTOS A LAS {}'.format(hora_destino))
    plt.grid()
    print("generando.... {}".format(filename_grafico)) 
    plt.savefig(filename_grafico)  # save the figure to file

    plt.close()

    
    

        
        
def procesa(dir_base, hora_inicio, hora_final, hora_destino, procesar, filename):
    
    array_result = []
    
    df = pd.read_csv(filename, sep=';')
    df['fecha'] = df['fecha'].apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M'))
    
    datetime_inicio = [d for d in df['fecha'] if d.hour==hora_inicio]
    
    for d in datetime_inicio:        
        df_hora_inicio = df.loc[df['fecha']==d]
        df_hora_comparar =  df.loc[df['fecha']==d.replace(hour=hora_final)]                
        df_hora_final = df.loc[df['fecha']==d.replace(hour=hora_destino)]
        
        if df_hora_inicio.empty or df_hora_comparar.empty or df_hora_final.empty:
            continue

        precio_apertura = df_hora_inicio['apertura'].values[0]
        precio_cierre = df_hora_final['cierre'].values[0]
        precio_cierre_comparar = df_hora_comparar['cierre'].values[0]
                            
        dif1 = precio_cierre_comparar - precio_apertura
        dif2 = precio_cierre - precio_apertura
        array_result.append((dif1,dif2))
                    
    test_graph(array_result, procesar, hora_inicio, hora_final, hora_destino)



configuracion = 'configuracion.cfg'
# LECTURA DE VALORES DE CONFIGURACION
config = ConfigParser.ConfigParser()
config.read(configuracion)
dir_base = config.get('data', 'directorio_base')
    
if __name__ == '__main__':
    ''' calcula la diferencia de precios de cierre de un valor
    en distintos horarios y deja el resultado en una grafica en
    graficos/comparativaHoraria'''
    
    procesar = 'DE30'        

    filename = os.path.join(dir_base,'csv','60','{}.csv'.format(procesar))
    
    horas = [(8,8,21),(8,9,21),(8,10,21),(8,12,21),(8,16,21),
             (9,9,21),(9,10,21),(9,12,21),
             (8,8,16),(8,9,16),(8,10,16),(8,12,16),
             (9,9,16),(9,10,16),(9,12,16),
             (14,14,21),(14,15,21),(14,16,21),(14,17,21),
             (16,16,21),(16,17,21),
             (17,17,21)]
    
    for horas in horas:
        (hora_inicio,hora_final,hora_destino) = horas     
        procesa(dir_base, hora_inicio, hora_final, hora_destino, procesar, filename)        
        
