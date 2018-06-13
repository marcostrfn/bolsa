"""
Show how to use plot_day_summary_oclh function
"""
import matplotlib.pyplot as plt
from pylab import *
import pandas as pd
from matplotlib.dates import (MONDAY, DateFormatter, MonthLocator,
                              WeekdayLocator, date2num)

from mpl_finance import plot_day_summary_oclh
import funciones.bolsa as fb


date1 = "2017-6-1"
date2 = "2017-12-31"

# every monday
mondays = WeekdayLocator(MONDAY)
daysFmt = DateFormatter("%d %b %y")


quotes = pd.read_csv('yahoofinance-GOOG-20040819-20180120.csv',
                     index_col=0,
                     parse_dates=True,
                     infer_datetime_format=True)

''' generamos la ema. recordar que los valores pueden
ser 0 y daria problemas en el grafico.
por eso la generamos aqui.'''
ema50 = fb.get_ema_periodo(50,quotes['Close'])

# select desired range of dates
quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]

''' ajustamos los valores de la media a los valores del cierre'''
l = len(quotes['Close'])
ema50=ema50[-l:]


fig, ax = plt.subplots(figsize=(24, 12))


plot_day_summary_oclh(ax, zip(date2num(quotes.index.to_pydatetime()),
                              quotes['Open'], quotes['Close'],
                              quotes['Low'], quotes['High']),
                      ticksize=3)


plt.plot( zip(date2num(quotes.index.to_pydatetime())), ema50)


ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_major_formatter(daysFmt)
ax.autoscale_view()
ax.xaxis.grid(True, 'major')
ax.grid(True)

fig.autofmt_xdate()

plt.show()
