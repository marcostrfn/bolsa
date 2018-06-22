
import funciones.data as fd
import funciones.graficos as fg
import ConfigParser
import sys

def calculoVelas():
    




    configuracion = 'configuracion.cfg'
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    PROCESAR = config.get('calculo', 'PROCESAR').split(',')

    resultados = []    

    
    # SELECCION DE VALORES
    valores = fd.cargar_valores_from_csv(None)    
    for row in valores:     
        valor,lotes,margen,spread,tp_spread,tipo,codigo,nombre,descripcion = row
        if valor in PROCESAR:   
            
            horasMaximo = [0] * 24
            horasMinimo = [0] * 24                     
            fechaDesde = 0
            fechaHasta = 0
            
            data = fd.cargar_datos_valor(valor, '60')
                       
                
            fecha = data['fecha'][0].split(' ')   
            diaOld = fecha[0]           
            fechaDesde = diaOld
            
            maximoHigh = 0
            maximoLow = 100000
            
            
            valoresDiarios = []
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
                    
                    if high > maximoHigh: maximoHigh = high
                    if low < maximoLow: maximoLow = low
                    
                    # print (dia, hora[0], maximoHigh, maximoLow, high, low)
                    valoresDiarios.append((dia, hora[0], maximoHigh, maximoLow))  

                else:
                    
                    # print ('a', diaOld, maximoHigh, maximoLow)
                    
                    maximoDia = 0
                    minimoDia = 100000
                    horaDiaMaximo = None
                    horaDiaMinimo = None                    
                    diaDiaMaximo = None
                    diaDiaMinimo = None
                    for a in valoresDiarios:
                        dDia, dHora, dMaximoHigh, dMaximoLow = a
                        if dMaximoHigh > maximoDia: 
                            maximoDia = dMaximoHigh
                            horaDiaMaximo = dHora
                            diaDiaMaximo = dDia
                        if dMaximoLow < minimoDia: 
                            minimoDia = dMaximoLow
                            horaDiaMinimo = dHora
                            diaDiaMinimo = dDia
                    
                    # print ('----------------------------------------------')
                    # print (diaDiaMaximo, horaDiaMaximo, dMaximoHigh )
                    # print (diaDiaMinimo, horaDiaMinimo, dMaximoLow )
                    # print ('----------------------------------------------')
                    try:
                        horasMaximo[int(horaDiaMaximo)] += 1
                        horasMinimo[int(horaDiaMinimo)] += 1
                    except Exception:
                        print (Exception)
                        
                    
                    
                    
                    
                        
                    valoresDiarios = []
                    
                    
                    maximoHigh = 0
                    maximoLow = 100000
                    diaOld = dia
                    
                    open = data['open'][i]
                    close = data['close'][i]
                    high = data['high'][i]
                    low = data['low'][i]
                    
                    if high > maximoHigh: maximoHigh = high
                    if low < maximoLow: maximoLow = low
                    
                    # print (dia, hora[0], maximoHigh, maximoLow, high, low)
                    valoresDiarios.append((dia, hora[0], maximoHigh, maximoLow)) 
                    fechaHasta = dia
                    
                        
    
            fechas = "de {} a {}".format(fechaDesde,fechaHasta)
            fg.graficarHorasMaxMin(valor, horasMaximo,'maximos',fechas)
            fg.graficarHorasMaxMin(valor ,horasMinimo,'minimos',fechas)
    
    
calculoVelas() 
    