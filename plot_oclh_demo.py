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
import funciones.bolsa as fb


class Jackarow(mdates.DateFormatter):
    def __init__(self, fmt):
        mdates.DateFormatter.__init__(self, fmt)
    def __call__(self, x, pos=0):
        # This gets called even when out of bounds, so IndexError must be prevented.
        if x < 0:
            x = 0
        elif x >= len(date):
            x = -1
        return mdates.DateFormatter.__call__(self, date[int(x)], pos)
    
    

date1 = "2018-6-01 02:00"
date2 = "2018-6-12 22:00"

# every monday
mondays = WeekdayLocator(MONDAY)
horas = HourLocator(byhour=range(0,24,4)) # cada 4 horas
daysFmt = DateFormatter("%d %b %y %H:%M")


quotes = pd.read_csv('ALUMINIO_60.csv',
                     index_col=0,
                     parse_dates=True,
                     infer_datetime_format=True,
                     sep=";")

'''quotes = pd.read_csv('yahoofinance-GOOG-20040819-20180120.csv',
                     index_col=0,
                     parse_dates=True,
                     infer_datetime_format=True)'''

# select desired range of dates
quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]

fig, ax = plt.subplots(figsize=(10, 5))


'''plot_day_summary_oclh(ax, zip(date2num(quotes.index.to_pydatetime()),
                              quotes['Open'], quotes['Close'],
                              quotes['Low'], quotes['High']),
                      ticksize=3)'''

plot_day_summary_oclh(ax, zip(date2num(quotes.index.to_pydatetime()),
                              quotes['apertura'], quotes['cierre'],
                              quotes['low'], quotes['high']),
                      ticksize=3)

                      

plt.plot( zip(date2num(quotes.index.to_pydatetime())), quotes['ema[5]'])


# ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_major_locator(horas)
ax.xaxis.set_major_formatter(daysFmt)
ax.autoscale_view()
ax.xaxis.grid(True, 'major')
ax.grid(True)

fig.autofmt_xdate()

plt.show()
