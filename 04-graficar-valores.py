

import funciones.graficos as fg
import itertools
import ConfigParser
import sys





if __name__ == '__main__':   
    
    configuracion = 'configuracion.cfg'
    
    # LECTURA DE VALORES DE CONFIGURACION
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    directorio_base = config.get('data', 'directorio_base')
    PROCESAR = config.get('calculo', 'PROCESAR').split(',')
    for valor in PROCESAR:
        fg.graficarValor(valor,'D', media='mejor')
        fg.graficarValor(valor,'60', media='mejor')
        fg.graficarValor(valor,'W', media='mejor')
            
    C = itertools.permutations(PROCESAR, 2)
    
                
        
    tramitado = []
    for VALORES in C:
        
        if VALORES[1] in tramitado:
            print ("excluir combinacion {}".format(VALORES))
        else:
            print ("combinar {}".format(VALORES))
            fg.combinarValores(VALORES,'D',24)
        
        if not VALORES[0] in tramitado:
            tramitado.append(VALORES[0]) 
        
        
        