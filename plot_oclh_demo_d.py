"""
Show how to use plot_day_summary_oclh function
"""
import matplotlib.pyplot as plt
from pylab import *
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.dates import (MONDAY, DateFormatter, MonthLocator,
                              WeekdayLocator, HourLocator, date2num)

from mpl_finance import plot_day_summary_oclh
from mpl_finance import candlestick_ohlc
import funciones.bolsa as fb

date1 = "2018-1-12 00:00"
date2 = "2018-6-12 23:00"

# every monday
mondays = WeekdayLocator(MONDAY)
horas = HourLocator(byhour=range(0,24,4)) # cada 4 horas
# daysFmt = DateFormatter("%d %b %y %H:%M")
daysFmt = DateFormatter("%d %b %y")


quotes = pd.read_csv('AUDNZD.csv',
                     index_col=0,
                     parse_dates=True,
                     infer_datetime_format=True,
                     sep=";")

# select desired range of dates
quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]

fig, ax = plt.subplots(figsize=(20, 10))


plot_day_summary_oclh(ax, zip(date2num(quotes.index.to_pydatetime()),
                              quotes['apertura'], quotes['cierre'],
                              quotes['low'], quotes['high']),
                      ticksize=3)
            
                    

                      

plt.plot( zip(date2num(quotes.index.to_pydatetime())), quotes['ema[5]'])
plt.plot( zip(date2num(quotes.index.to_pydatetime())), quotes['ema[50]'])

# ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_major_formatter(daysFmt)
ax.autoscale_view()
ax.xaxis.grid(True, 'major')
ax.grid(True)

fig.autofmt_xdate()

plt.show()
