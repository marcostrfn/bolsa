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



def test_graph(dir_base, archivo, valor, hora_comparar, hora_destino):
    
    
    df = pd.read_csv(archivo, header=None, names=['puntos_inicio', 'puntos_final'])
    
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
        
    
    filename_grafico = os.path.join(dir_base, 'graficos', 'comparativaHoraria', '{}-{}-{}.png'.format(valor,hora_comparar,hora_destino))       
                
    plt.scatter(df['puntos_inicio'], df['puntos_final'], c=asignar, s=tamanios[0])
    plt.title('Comparativa {} {}-{}'.format(valor, hora_comparar, hora_destino))
    plt.xlabel('PUNTOS A LAS {}'.format(hora_comparar))
    plt.ylabel('PUNTOS A LAS {}'.format(hora_destino))
    plt.grid()
    print("generando.... {}".format(filename_grafico)) 
    plt.savefig(filename_grafico)  # save the figure to file

    plt.close()

    
    

        
        
def procesa(dir_base, hora_comparar, hora_destino, procesar, filename):
    df = pd.read_csv(filename, sep=';')
    df['fecha'] = df['fecha'].apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M'))

    datetime_compara = [d for d in df['fecha'] if d.hour==hora_comparar]    
    datetime_destino = [d for d in  df['fecha'] if d.hour==hora_destino]

    df_compara = df.loc[df['fecha'].isin(datetime_compara)]
    df_destino = df.loc[df['fecha'].isin(datetime_destino)]
    
    
    array_apertura = []
    array_cierre = []
    for d in df_compara['fecha']:
        new_df=df.loc[df['fecha'] == d]
        array_apertura.append( ( d, new_df['apertura'].values[0], new_df['cierre'].values[0] ) )
        
    for d in df_destino['fecha']:
        new_df=df.loc[df['fecha'] == d]
        array_cierre.append( ( d, new_df['cierre'].values[0] ) )


    
    array_result = []
    for x in range(0,len(array_cierre)):
        for i in range(0,len(array_apertura)):
            if array_apertura[i][0].day==array_cierre[x][0].day and array_apertura[i][0].month==array_cierre[x][0].month and array_apertura[i][0].year==array_cierre[x][0].year:
               
                fecha_apertura,apertura_inicial,cierre_inicial = array_apertura[i]
                fecha_cierre,cierre_final = array_cierre[x]
                
                dif1 = cierre_inicial - apertura_inicial
                dif2 = cierre_final - apertura_inicial
                 
                array_result.append((dif1,dif2))
                       

                       
    filename = 'regresion.csv'     
    ofile = open(filename, 'wb')
    spamwriter = csv.writer(ofile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)    
    for dataset in array_result:                    
        spamwriter.writerow(dataset)    
    ofile.close()
    
    
    
    test_graph(dir_base, filename, procesar, hora_comparar, hora_destino)


if __name__ == '__main__':
        
    procesar = 'DE30'
    hora_inicio = 8
    hora_destino = 17
    
    configuracion = 'configuracion.cfg'
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    dir_base = config.get('data', 'directorio_base')

    filename = os.path.join(dir_base,'csv','60','{}.csv'.format(procesar))
    
    for hora_compara in range(hora_inicio, hora_destino):
        procesa(dir_base, hora_compara, hora_destino, procesar, filename)
        
                          