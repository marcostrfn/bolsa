


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



def test_graph(archivo, valor, HORA_COMPARAR):
    
    
    df = pd.read_csv(archivo, header=None, names=['puntos_inicio', 'puntos_final'])
    
    colores=['green','blue', 'red', 'black']
    tamanios=[30,60]

    asignar=[]
    for index, row in df.iterrows():
#         if(row['puntos_final'] > 0):
#             asignar.append(colores[0])
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
            
        
    plt.scatter(df['puntos_inicio'], df['puntos_final'], c=asignar, s=tamanios[0])
    plt.title('Comparativa {} {}-22'.format(valor, HORA_COMPARAR))
    plt.xlabel('PUNTOS A LAS {}'.format(HORA_COMPARAR))
    plt.ylabel('PUNTOS A LAS 22')
    plt.grid()
    plt.show()


    
    

        
        
def procesa(HORA_COMPARAR, PROCESAR, filename):
    df = pd.read_csv(filename, sep=';')
    numero_elementos = df.shape[0]
    df['fecha'] = df['fecha'].apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M'))

    datetime_compara = [d for d in df['fecha'] if d.hour==HORA_COMPARAR]    
    datetime_22 = [d for d in  df['fecha'] if d.hour==22]

    dfCompara = df.loc[df['fecha'].isin(datetime_compara)]
    df22 = df.loc[df['fecha'].isin(datetime_22)]
    
    
    array_apertura = []
    array_cierre = []
    for d in dfCompara['fecha']:
        new_df=df.loc[df['fecha'] == d]
        array_apertura.append( ( d, new_df['apertura'].values[0], new_df['cierre'].values[0] ) )
        
    for d in df22['fecha']:
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
    
    test_graph(filename, PROCESAR, HORA_COMPARAR)


def main():
    
    PROCESAR = 'DE30'
    
    configuracion = 'configuracion.cfg'
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    DIR_BASE = config.get('data', 'directorio_base')

    filename = os.path.join(DIR_BASE,'csv','60','{}.csv'.format(PROCESAR))
    
    for HORA_COMPARA in range(8,21):
        procesa(HORA_COMPARA, PROCESAR, filename)
        
                          
if __name__ == '__main__':
    main()
