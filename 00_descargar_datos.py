#! /usr/bin/env/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import funciones.data as fd


if __name__ == '__main__':
	''' descarga datos en json desde investing.com. Resultado en data/XX/XX.json 
	Lee los valores a descargar desde fichero configuracion con etiqueta [descargar]'''
	fd.descargar_datos()
