

'''
lotes = 0.02
pip = 1
spread = 0.04 
valor_pip = 8.07
'''


def de30():
	precio_entrada = 12600
	pip_a_conseguir = 100
	
	valor_pip_minimo = 0.25
	spread = 0.9

	lotes = 0.01

	valor_pip = lotes * valor_pip_minimo * 100
	importe_spread = spread * valor_pip 




	precio_salida = precio_entrada + pip_a_conseguir 
	importe_salida = (precio_salida - precio_entrada) * valor_pip 
	print precio_salida, importe_salida

	
	
def oil():
	precio_entrada = 67.70
	pip_a_conseguir = 0.10
	
	valor_pip_minimo = 8.07
	spread = 0.32

	lotes = 0.01

	valor_pip = lotes * valor_pip_minimo * 100
	importe_spread = spread * valor_pip 


	precio_salida = precio_entrada + pip_a_conseguir 
	importe_salida = (precio_salida - precio_entrada) * valor_pip 
	print precio_salida, importe_salida


def lotes_oil():
	precio_entrada = 68.10
	precio_salida = 68.30
	importe_a_conseguir = 100
	
	valor_pip_minimo = 8.07
	spread = 0.32
	
	pip_a_conseguir = precio_salida - precio_entrada
	x = 0.
	while True:		
		x+=0.01
		valor_pip = x * valor_pip_minimo * 100
		importe_spread = spread * valor_pip 
		
		importe_salida = (precio_salida - precio_entrada) * valor_pip 
		if importe_salida > importe_a_conseguir:
			print x, importe_salida, valor_pip
			break
	

	
	
lotes_oil()
