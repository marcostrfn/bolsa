
import funciones.graficos as fg
import itertools
import ConfigParser
import sys





if __name__ == '__main__':   
    
    configuracion = 'configuracion.cfg'
    config = ConfigParser.ConfigParser()
    config.read(configuracion)
    directorio_base = config.get('data', 'directorio_base')
    PROCESAR = config.get('calculo', 'PROCESAR').split(',')
    for valor in PROCESAR:
        fg.graficarValorMedias(valor,'D', media='mejor')

