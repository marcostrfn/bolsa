

import os
import sys
import csv
import pandas as pd
import ConfigParser
import datetime


# Implementacion del metodo del gradiente con pandas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from array import array



def test_graph(data, valor, HORA_INICIO, HORA_FINAL, HORA_DESTINO):
    
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
            
    
    
    
    directorio_destino = os.path.join(DIR_BASE, 'graficos')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))
        
    directorio_destino = os.path.join(DIR_BASE, 'graficos', 'comparativaHoraria')    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
        print ("creando directorio.... {}".format(directorio_destino))
        
    
    filenameGrafico = os.path.join(DIR_BASE, 'graficos', 'comparativaHoraria', '{}-{}-{}-{}.png'.format(valor,HORA_INICIO, HORA_FINAL,HORA_DESTINO))       
                
    plt.scatter(df['puntos_inicio'], df['puntos_final'], c=asignar, s=tamanios[0])
    plt.title('Comparativa {} {}-{} a {}'.format(valor, HORA_INICIO, HORA_FINAL, HORA_DESTINO))
    plt.xlabel('PUNTOS A LAS {}-{} '.format(HORA_INICIO,HORA_FINAL))
    plt.ylabel('PUNTOS A LAS {}'.format(HORA_DESTINO))
    plt.grid()
    print("generando.... {}".format(filenameGrafico)) 
    plt.savefig(filenameGrafico)  # save the figure to file

    plt.close()

    
    

        
        
def procesa(DIR_BASE, HORA_INICIO, HORA_FINAL, HORA_DESTINO, PROCESAR, filename):
    
    array_result = []
    
    df = pd.read_csv(filename, sep=';')
    numero_elementos = df.shape[0]
    df['fecha'] = df['fecha'].apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M'))
    
    datetime_inicio = [d for d in df['fecha'] if d.hour==HORA_INICIO]
    
    for d in datetime_inicio:        
        df_hora_inicio = df.loc[df['fecha']==d]
        df_hora_comparar =  df.loc[df['fecha']==d.replace(hour=HORA_FINAL)]                
        df_hora_final = df.loc[df['fecha']==d.replace(hour=HORA_DESTINO)]
        
        if df_hora_inicio.empty or df_hora_comparar.empty or df_hora_final.empty:
            continue

        precioApertura = df_hora_inicio['apertura'].values[0]
        precioCierre = df_hora_final['cierre'].values[0]
        precioCierreComparar = df_hora_comparar['cierre'].values[0]
                            
        dif1 = precioCierreComparar - precioApertura
        dif2 = precioCierre - precioApertura
        array_result.append((dif1,dif2))
                    
    test_graph(array_result, PROCESAR, HORA_INICIO, HORA_FINAL, HORA_DESTINO)



configuracion = 'configuracion.cfg'
# LECTURA DE VALORES DE CONFIGURACION
config = ConfigParser.ConfigParser()
config.read(configuracion)
DIR_BASE = config.get('data', 'directorio_base')
    
def main():
    
    PROCESAR = 'DE30'        

    filename = os.path.join(DIR_BASE,'csv','60','{}.csv'.format(PROCESAR))
    
    HORAS = [(8,8,21),(8,9,21),(8,10,21),(8,12,21),
             (9,9,21),(9,10,21),(9,12,21),
             (8,8,16),(8,9,16),(8,10,16),(8,12,16),
             (9,9,16),(9,10,16),(9,12,16),
             (14,14,21),(14,15,21),(14,16,21),(14,17,21),
             (16,16,21),(16,17,21),
             (17,17,21)]
    
    for horas in HORAS:
        (hora_inicio,hora_final,hora_destino) = horas
    
#    for HORA_COMPARA in range(HORA_INICIO, HORA_DESTINO):        
        procesa(DIR_BASE, hora_inicio, hora_final, hora_destino, PROCESAR, filename)        
        
                          
if __name__ == '__main__':
    main()
