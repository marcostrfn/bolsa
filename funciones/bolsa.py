

from datetime import datetime, timedelta, date
import estrategia as fe



def procesar_valores_hora(valor, tiempo, tipo, data, config):
	

	resultados = {
		'00' : [],
		'01' : [],
		'02' : [],
		'03' : [],
		'04' : [],
		'05' : [],
		'06' : [],
		'07' : [],
		'08' : [],
		'09' : [],
		'10' : [],
		'11' : [],
		'12' : [],
		'13' : [],
		'14' : [],
		'15' : [],
		'16' : [],
		'17' : [],
		'18' : [],
		'19' : [],
		'20' : [],
		'21' : [],
		'22' : [],
		'23' : [],
		}
		
	for d in range(0,len(data['fecha'])):
		# print (data['fecha'][d], data['high'][d], data['low'][d])
		
		fecha = data['fecha'][d].split(' ')
		hora = fecha[1].split(':')		
		
		h = hora[0]
		resultados[h].append( (data['high'][d], data['low'][d]) )
		
	
		
	return resultados

def procesar_valores_flujo(valor, tiempo, tipo, data, config):
	

	resultados = {		
		'00:00': [],
		'00:30': [],
		'01:00': [],
		'01:30': [],
		'02:00': [],
		'02:30': [],
		'03:00': [],
		'03:30': [],
		'04:00': [],
		'04:30': [],
		'05:00': [],
		'05:30': [],
		'06:00': [],
		'06:30': [],
		'07:00': [],
		'07:30': [],
		'08:00': [],
		'08:30': [],
		'09:00': [],
		'09:30': [],
		'10:00': [],
		'10:30': [],
		'11:00': [],
		'11:30': [],
		'12:00': [],
		'12:30': [],
		'13:00': [],
		'13:30': [],
		'14:00': [],
		'14:30': [],
		'15:00': [],
		'15:30': [],
		'16:00': [],
		'16:30': [],
		'17:00': [],
		'17:30': [],
		'18:00': [],
		'18:30': [],
		'19:00': [],
		'19:30': [],
		'20:00': [],
		'20:30': [],
		'21:00': [],
		'21:30': [],
		'22:00': [],
		'22:30': [],
		'23:00': [],
		'23:30': [],
	}
		
	for d in range(0,len(data['fecha'])):
		# print (data['fecha'][d], data['high'][d], data['low'][d])
		
		fecha = data['fecha'][d].split(' ')
		hora = fecha[1]	
		
		h = hora		
		datetime_fecha = datetime.strptime(data['fecha'][d], '%Y-%m-%d %H:%M')
		
		if datetime_fecha.weekday() > 3:
			pass
		else:
			# print (data['fecha'][d], datetime_fecha.weekday() )
			resultados[h].append( (data['fecha'][d], data['open'][d], data['close'][d]) )
		

	return resultados


	
def procesar_valores(valor, tiempo, tipo, data, config):
	

	pivot = calcular_pivot_fibo(data['close'], data['high'], data['low'])
	parabolic_sar_bear, parabolic_sar_bull = psar(data['fecha'], data['close'], data['high'], data['low'], 0.02, 0.2)

	resultados = []
	
	# cortes del sar parabolico
	if config.get('operaciones', 'SAR_PARABOLICO') == 'si':
		r = fe.sar_parabolico(valor, tiempo, tipo, data, parabolic_sar_bull)
		resultados.append(r)
		
	# cortes del MACD
	if config.get('operaciones', 'MACD') == 'si':
		r = fe.macd(valor, tiempo, tipo, data)
		resultados.append(r)
	
	# cortes SMA con media simple de 400
	if config.get('operaciones', 'SMA_SMA400') == 'si':
		r = fe.sma_sma400(valor, tiempo, tipo, data)
		resultados.append(r)

	# cortes EMA con media simple de 400
	if config.get('operaciones', 'EMA_SMA400') == 'si':
		r = fe.ema_sma400(valor, tiempo, tipo, data)
		resultados.append(r)
		
	# cortes SMA con media simple de 100
	if config.get('operaciones', 'SMA_SMA100') == 'si':
		r = fe.sma_sma100(valor, tiempo, tipo, data)
		resultados.append(r)

	# cortes EMA con media simple de 100
	if config.get('operaciones', 'EMA_SMA400') == 'si':
		r = fe.ema_sma100(valor, tiempo, tipo, data)
		resultados.append(r)

	# cortes SMA con media simple de 50
	if config.get('operaciones', 'SMA_SMA50') == 'si':
		r = fe.sma_sma50(valor, tiempo, tipo, data)
		resultados.append(r)
	
	# cortes EMA con media simple de 50
	if config.get('operaciones', 'EMA_SMA50') == 'si':
		r = fe.ema_sma50(valor, tiempo, tipo, data)
		resultados.append(r)

	# cortes de una media simple
	if config.get('operaciones', 'SMA') == 'si':
		r = fe.media_simple(valor, tiempo, tipo, data)
		resultados.append(r)
	
	# cortes de una media exponencial
	if config.get('operaciones', 'EMA') == 'si':
		r = fe.media_exponencial(valor, tiempo, tipo, data)
		resultados.append(r)
	
	# cortes del MACD con media SIMPLE
	if config.get('operaciones', 'MACD_SMA') == 'si':
		r = fe.macd_sma(valor, tiempo, tipo, data)
		resultados.append(r)
	
	# print ()
	return resultados


def calcular_rsi(periodo, cierre):
	''' retorna el rsi en un array '''
	rsi = []
	for x in range(0, periodo):
		rsi.append(0)
	
	lecturas = len(cierre)	
	for x in range(periodo, lecturas):
		array_data = cierre[x-periodo:x]
		lista_subidas = []
		lista_bajadas = []
		for i in range(1,periodo):
			diferencia = float(array_data[i] - array_data[i-1])
			if diferencia > 0:
				lista_subidas.append(diferencia)
			else:
				lista_bajadas.append(diferencia * -1)

		suma_subidas = 0
		for l in lista_subidas:
			suma_subidas += l
			
		suma_bajadas = 0
		for l in lista_bajadas:
			suma_bajadas += l
			
		subidas = suma_subidas / periodo
		bajadas = suma_bajadas / periodo
		if bajadas > 0:
			rs = subidas / bajadas
		else:
			rs = 0
			
		r = 100 - (100/(1+(rs)))
		
		rsi.append(r)
		

	return rsi


def calcular_estocastico(cierre, high, low, periodo=14, smoothd=3):
	''' retorna el valor K y D del estocastico en un array '''
	# %K= (Cierre actual-Minimo mas bajo)/(Maximo mas alto-Minimo mas bajo) x 100
	# %D = Media movil simple de 3 periodos del %K.

	# vc = valor cierre de ultima sesion
    # maximo = valor maximo de sesion - numero_sesiones
	# minimo = valor minimo de sesion - numero_sesiones
	desde = periodo
	lecturas = len(cierre)	
	
	
	sk = []
	for x in range(0, periodo):
		sk.append(0)

	
	for x in range(desde, lecturas):
		inicio = x - periodo
		vc = cierre[x-1]
		maximos = high[inicio:x]
		minimos = low[inicio:x]
		
		maximos.sort(reverse=True)
		minimos.sort()
		
		try:
			calculo_estocastico = float(vc - minimos[0]) / float(maximos[0] - minimos[0]) 
			calculo_estocastico = calculo_estocastico * 100
		except:
			calculo_estocastico = 0
			
		if calculo_estocastico > 100: calculo_estocastico = 100	
		if calculo_estocastico < 0: calculo_estocastico = 0
		sk.append(calculo_estocastico)
	
	array_sd = ema_simple(sk,smoothd)
	sd = []		
	for c,v in array_sd.items():	
		if v > 100: v = 100	
		if v < 0: v = 0	
		sd.append(v)
	
	return (sk,sd)

	
def calcular_fecha(data, cierre):
	lecturas = len(data)
	fecha = {}
	for i in range(0,lecturas):
		if (float(cierre[i])==0): continue	
		tiempo = data[i]
		base_datetime = datetime( 1970, 1, 1 )
		delta = timedelta( 0, 0, 0, tiempo*1000 ) + timedelta(minutes=60)
		target_date = base_datetime + delta
		fecha[i] = target_date
	return fecha

	
def get_fechas(data, formato="%Y-%m-%d %H:%M"):
	''' retorna un array con la fecha en formtato string'''
	dataset = data['t']
	data_fecha = calcular_fecha(dataset, data['c'])
	fecha = []
	for d in data_fecha:
		fecha.append(data_fecha[d].strftime(formato))

	return fecha


def get_sma_periodo(periodo, cierre):
	''' retorna array con valor de media simple'''
	array_sma = ema_simple(cierre,periodo)
	array = []
	for clave,valor in array_sma.items():
		array.append(valor)
	
	return array

	
def get_ema_periodo(periodo, cierre):
	''' retorna array con valor de media exponencial'''	
	array_ema = ema_exponencial(cierre, get_sma_periodo(periodo,cierre), periodo)
	array = []
	for clave,valor in array_ema.items():
		array.append(valor)
		
	return  array

	
def get_macd(cierre,fast=12,slow=26,signal=9):
	''' retorna array con valores de macd, macd_signal, macd_histograma'''
	data = {}
	
	# CALCULO EMAS DE 12 Y 26, NECESARIAS PARA EMA EXPONENCIAL
	data['ema12'] = ema_simple(cierre,fast)
	data['ema26'] = ema_simple(cierre,slow)

		
	# CALUCULO EMA EXP DE 12 Y 26
	data['exp12'] = ema_exponencial(cierre, data['ema12'],fast)
	data['exp26'] = ema_exponencial(cierre, data['ema26'],slow)
		
	# CALCULO DE MACD
	data['macd'] = calcular_macd(data['exp12'],data['exp26'])
	data['macd_signal'] = ema_simple(data['macd'],signal)
	data['macd_histograma'] = calcular_macd_histograma(data['macd'],data['macd_signal'])

	
	array_macd = []		
	for c,v in data['macd'].items():
		array_macd.append(v)
		
	macd = array_macd

	
	array_macd = []		
	for c,v in data['macd_signal'].items():
		array_macd.append(v)
		
	macd_signal = array_macd
	
	array_macd = []		
	for c,v in data['macd_histograma'].items():
		array_macd.append(v)
		
	macd_histograma = array_macd
	
	return (macd, macd_signal, macd_histograma)


def calcular_ema_simple(data,f,valor):
	cierre = 0
	for i in range(f-valor,f):	
		close = round(data[i],6)
		cierre = cierre + close
		
	ema = cierre / valor
	return ema
	
	
def ema_simple(data, dias_ema = None):
	lecturas = len(data)
	emas = {}
	for i in range(0,lecturas):
		emas[i] = 0
	
	for i in range(dias_ema,lecturas):
		ema = calcular_ema_simple(data, i, dias_ema)
		emas[i] = ema
		
	return emas
	
	
def ema_exponencial(data, data_ema_simple, periodo):
	lecturas = len(data)
	emas = {}
	for i in range(0,lecturas):
		emas[i] = 0

	for i in range(periodo+1,lecturas):
		K = 2 / (float(periodo) + 1)
		if i == periodo+1:
			EMA_ANTERIOR = data_ema_simple[i]
		else:
			EMA_ANTERIOR = emas[i-1]
		
		ema = EMA_ANTERIOR + K * ( data[i] - EMA_ANTERIOR)
		emas[i] = ema
	
	return emas

	
def calcular_macd(ema1,ema2):
	lecturas = len(ema1)
	macd_line = {}
	for i in range(0,lecturas):
		macd_line[i] = 0
		
	for i in range(0,lecturas):
		macd_line[i] = ema1[i] - ema2[i]
	
	return macd_line

	
def ema_simple_macd(data, dias_ema = None):
	lecturas = len(data)
	emas = {}
	for i in range(0,lecturas):
		emas[i] = 0
		
	for i in range(dias_ema,lecturas):
		ema = calcular_ema_simple_macd(data, i, dias_ema)
		emas[i] = ema
		
	return emas

	
def calcular_macd_histograma(macd,macd_signal):
	lecturas = len(macd)
	histograma = {}
	for i in range(0,lecturas):
		histograma[i] = 0
	
	
	for i in range(0,lecturas):
		if macd[i] > macd_signal[i]:
			histograma[i] = macd[i] - macd_signal[i]
		else:
			histograma[i] = macd_signal[i] - macd[i]
		
		if histograma[i] < 0: histograma[i]	 = histograma[i]  * -1
		
		if macd[i] < macd_signal[i]: histograma[i]	= histograma[i]	 * -1
	
	return histograma
	
	
def psar(dates, close, high, low, iaf = 0.02, maxaf = 0.2):
	length = len(dates)
	psar = close[0:len(close)]
	psarbull = [0] * length
	psarbear = [0] * length
	bull = True
	af = iaf
	ep = low[0]
	hp = high[0]
	lp = low[0]
	
	
	for i in range(1,length):
		if bull:
			psar[i] = psar[i - 1] + af * (hp - psar[i - 1])
		else:
			psar[i] = psar[i - 1] + af * (lp - psar[i - 1])
		
		reverse = False
		
		if bull:
			if low[i] < psar[i]:
				bull = False
				reverse = True
				psar[i] = hp
				lp = low[i]
				af = iaf
		else:
			if high[i] > psar[i]:
				bull = True
				reverse = True
				psar[i] = lp
				hp = high[i]
				af = iaf
	
		if not reverse:
			if bull:
				if high[i] > hp:
					hp = high[i]
					af = min(af + iaf, maxaf)
				if low[i - 1] < psar[i]:
					psar[i] = low[i - 1]
				if low[i - 2] < psar[i]:
					psar[i] = low[i - 2]
			else:
				if low[i] < lp:
					lp = low[i]
					af = min(af + iaf, maxaf)
				if high[i - 1] > psar[i]:
					psar[i] = high[i - 1]
				if high[i - 2] > psar[i]:
					psar[i] = high[i - 2]
					
		if bull:
			psarbull[i] = psar[i]
		else:
			psarbear[i] = psar[i]

	
	# return {"dates":dates, "high":high, "low":low, "close":close, "psar":psar, "psarbear":psarbear, "psarbull":psarbull}
	return (psarbear, psarbull)
	

def get_pivot_fibo(c,h,l):

	PP = (h+l+c)/3.0
			   
	R1 = PP+0.382*(h-l)
	R2 = PP+0.618*(h-l)
	R3 = PP+1.000*(h-l)
				
	S1 = PP-0.382*(h-l)
	S2 = PP-0.618*(h-l)
	S3 = PP-1.000*(h-l)
	
	return (S3,S2,S1,PP,R1,R2,R3)
	
	
def calcular_pivot_fibo(c,h,l):
	pivot = [0]*len(c)
	for x in range(1, len(c)):
		pivot[x]=get_pivot_fibo(c[x-1],h[x-1],l[x-1]) # (S3,S2,S1,PP,R1,R2,R3)
	
	return pivot
			
			
def get_pares_corte(cruces):
	''' devuelve una tupla con pares de posiciones de inicio fin del corte 
		de un array de cruces
		una un array para posiciones largas y otro para cortas (12, 16)'''
	registros = len(cruces)
	# tratar largos
	l = []
	ini = 0
	for x in range(0,registros):
		if cruces[x]=="LARGO" and ini==0: 
			ini = x
		if not cruces[x]=="LARGO" and not ini==0: 
			l.append((ini,x-1))
			ini = 0
	
	if not ini == 0: l.append((ini,registros-1))
	
	# tratar cortos
	c = []
	ini = 0
	for x in range(0,registros):
		if cruces[x]=="CORTO" and ini==0: 
			ini = x
		if not cruces[x]=="CORTO" and not ini==0: 
			c.append((ini,x-1))
			ini = 0
	
	if not ini == 0: c.append((ini,registros-1))
			
	return (l,c)

	
def get_simulacion_importes(data,largos,cortos):
	''' devuelve un array con fecha inicio, fin, e importe 
		de las operaciones ('2018-02-14', '2018-02-27', 99.0),'''
		
	importe_largos = 0

	array_largos = []
	for valor in largos:
		inicio,final = valor
		precio_abrir = data['close'][inicio]
		final += 1
		if final >= data['registros']: 
			final =  data['registros'] - 1 
		precio_cerrar = data['close'][final]	
		importe_operacion = precio_cerrar - precio_abrir
		array_largos.append((data['fecha'][inicio], data['fecha'][final],importe_operacion))
		
		
		
		
	array_cortos = []
	for valor in cortos:
		inicio,final = valor
		precio_abrir = data['close'][inicio]
		final += 1
		if final >= data['registros']: 
			final =  data['registros'] - 1 
		precio_cerrar = data['close'][final]	
		importe_operacion = precio_abrir - precio_cerrar
		array_cortos.append((data['fecha'][inicio], data['fecha'][final],importe_operacion))
		
	
	return array_largos,array_cortos

	
def sumar_importes(data):
	''' suma los importes de un array devuelto por get_simulacion_importes'''
	importe = 0
	for valor in data:
		fecha_inicio, fecha_final, importe_operacion = valor
		importe += importe_operacion
	
	return importe
	

def cruce_precio_sma(array_sma, array_fecha, array_apertura, array_cierre):
	
	cortes = []
	lecturas = len(array_fecha)
	
	for x in range(1,lecturas):
		fecha, open, close, sma = array_fecha[x],array_apertura[x],array_cierre[x],array_sma[x]
		fecha_a, open_a, close_a, sma_a = array_fecha[x-1],array_apertura[x-1],array_cierre[x-1],array_sma[x-1]
		
		
		gap = True
		if open > sma and sma > close:
			# print (fecha,'CB', open, sma, close)
			gap = False
			cortes.append([fecha,'CB', open, sma, close])
			
		if open < sma and sma < close:
			# print (fecha,'CA', open, sma, close)
			gap = False
			cortes.append([fecha,'CA', open, sma, close])
			
		if close > sma and sma_a > close_a and gap:
			# print (fecha,'GA', open, sma, close_a)
			cortes.append([fecha,'GA', open, sma, close])
		
		if close < sma and sma_a < close_a and gap:
			# print (fecha,'GB', open, sma, close_a)
			cortes.append([fecha,'GB', open, sma, close])

	
	try:	
		while True:
			if cortes[0][1][:-1] == 'G':
				cortes.pop(0)
			else:
				break
				
		cortes_final = []	
		cortes_final.append(cortes[0])
		
		for x in range(1,len(cortes)):
			anterior = x - 1
			if cortes[x][1][-1:]==cortes[anterior][1][-1:]:
				pass
			else:
				cortes_final.append(cortes[x])
			
		if len(cortes_final)>1:
			return cortes_final
		else:
			return None
		

	except:
		return None

		
def get_operaciones_sma_exp200(periodo_desde, periodo_hasta, fecha, apertura, cierre, ema200):
	operaciones = []
	#calcula cruce de medias simple de periodo_desde hasta periodo_hasta y exponencial de 200
	for periodo in range(periodo_desde,periodo_hasta):
		print (periodo)
		# ema[periodo] = get_ema_periodo(periodo,cierre)
		array_sma = get_sma_periodo(periodo,cierre)
		cortes = cruce_precio_sma(array_sma, fecha, apertura, cierre)
		for corte in cortes:
			for x in range(0,len(fecha)):
				if corte[0]==fecha[x]:						
					if corte[1][-1:]=='A': 
						if apertura[x]>ema200[x]:
							operaciones.append(('LARGO', corte))	
					if corte[1][-1:]=='B': 
						if cierre[x]<ema200[x]:
							operaciones.append(('CORTO', corte))
	
	return operaciones

		
def get_operaciones_sma(periodo_desde, periodo_hasta, fecha, apertura, cierre):
	operaciones = []
	#calcula cruce de medias simple de periodo_desde hasta periodo_hasta y exponencial de 200
	for periodo in range(periodo_desde,periodo_hasta):
		print (periodo)
		# ema[periodo] = get_ema_periodo(periodo,cierre)
		array_sma = get_sma_periodo(periodo,cierre)
		cortes = cruce_precio_sma(array_sma, fecha, apertura, cierre)
		for corte in cortes:
			for x in range(0,len(fecha)):
				if corte[0]==fecha[x]:						
					if corte[1][-1:]=='A': 
						operaciones.append(('LARGO', corte))	
					if corte[1][-1:]=='B': 
						operaciones.append(('CORTO', corte))
	
	return operaciones

	
def get_operaciones_psar(psarbear, psarbull, fecha, apertura, cierre):
	operaciones=[]
	for x in range(1,len(fecha)):
		if psarbear[x]>0:						
			operaciones.append(('CORTO', fecha[x]))	
		else:
			operaciones.append(('LARGO', fecha[x]))
	x = 0
	while True:
		b1,c1 = operaciones[x]
		b2,c2 = operaciones[x+1]
		if b1 == b2: del operaciones[x+1]
		else: x += 1
		if x == len(operaciones) - 1: break
	
	return operaciones

	
def get_cruce_medias(array_1, array_2, valor):
	
	resultado = []
	for x in range(0,len(array_1)):
		if array_1[x]==valor and array_1[x]==array_2[x]:
			resultado.append(x)
			
	x = 0
	posicion_corte = 0
	cortes = [None]*len(array_1)
	while True:
		
		b1 = resultado[x]
		b2 = resultado[x+1]
		# print (x, b1,b2) 
		
		if b2 > b1+1:
			cortes[resultado[posicion_corte]]=valor
			# print ('----', fecha[resultado[posicion_corte]], posicion_corte, resultado[posicion_corte])
			posicion_corte = x+1

		x += 1
		if x == len(resultado) - 1: 
			cortes[resultado[posicion_corte]]=valor
			# print ('----', fecha[resultado[posicion_corte]], posicion_corte, resultado[posicion_corte])
			break
	
	# sys.exit()
	
	return cortes
	
	
def get_cruce_simple(array_1):
	
	resultado = array_1
	
	x = 0
	posicion_corte = 0
	cortes = [None]*len(array_1)
	array_cortes = []
	while True:
		
		b1 = resultado[x]
		b2 = resultado[x+1]
		
		if not b2 == b1:
			array_cortes.append((posicion_corte, resultado[posicion_corte]))
			# print ('----', posicion_corte, resultado[posicion_corte])
			posicion_corte = x+1

		x += 1
		if x == len(resultado) - 1: 
			array_cortes.append((posicion_corte, resultado[posicion_corte]))
			break
	
	for a in array_cortes:
		p,v = a
		cortes[p] = v

	return cortes

	
def combinar_entradas(array_entrada_1, array_entrada_2):
	result = [None]*len(array_entrada_1)
	for x in range(0,len(array_entrada_1)):
		if array_entrada_1[x] is not None:
			result[x] = array_entrada_1[x]
		else:
			if array_entrada_2[x] is not None:
				result[x] = array_entrada_2[x]
	
	return result


def get_cortes_sar(data, cierre):
	resultado = [0]*len(cierre)
	for x in range(0,len(cierre)):
		if cierre[x] > data[x] and data[x] > 0:
			resultado[x] = 'LARGO'
		else:
			resultado[x] = 'CORTO'

	return resultado

	
def get_cortes_macd(data):
	resultado = [0]*len(data)
	for x in range(0,len(data)):
		if data[x] > 0:
			resultado[x] = 'LARGO'
		else:
			resultado[x] = 'CORTO'

	return resultado

	
def get_cortes_cruce(cruce1,cruce2):
	result=[None]*len(cruce1)
	for x in range(0,len(cruce1)):
		if cruce1[x]==cruce2[x]:
			result[x] = cruce1[x]
		else:
			result[x] = None
	return result

	
def get_cortes(data, cierre):
	''' devuelve un array con resultado LARGO o CORTO por elemento si 
		cierre es mayor o menor que la media'''
	resultado = [0]*len(cierre)
	for x in range(0,len(cierre)):
		if cierre[x] > data[x]:
			resultado[x] = 'LARGO'
		else:
			resultado[x] = 'CORTO'

	return resultado
	
	
def corte_macd_media_simple(periodo,data,cruce_macd):
	array_data = get_sma_periodo(periodo, data['close'])
	cortes_media = get_cortes(array_data, data['close'])
	cruces = get_cortes_cruce(cruce_macd,cortes_media)		
	largos,cortos = get_pares_corte(cruces)	
	numero_operaciones = len(largos)+len(cortos)	
	l,c = get_simulacion_importes(data,largos,cortos)	
	imp_l = sumar_importes(l)
	imp_c = sumar_importes(c)
	return (periodo, numero_operaciones, imp_l + imp_c, imp_l, imp_c)
		
	
	