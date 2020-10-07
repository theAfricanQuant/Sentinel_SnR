"""
Created on Tue Sep 29 21:01:11 2020

@author: Ricky Macharm

"""

import numpy as np
import pandas as pd

import yfinance

from mplfinance.original_flavor import candlestick_ohlc

import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)


inst = ['BTCUSD=X', 'EURUSD=X', 'JPY=X', 'GBPUSD=X', 
        'AUDUSD=X', 'NZDUSD=X', 'EURJPY=X', 'GBPJPY=X',
        'EURGBP=X', 'EURCAD=X', 'EURSEK=X', 'EURCHF=X',
        'EURJPY=X', '^GSPC', '^DJI', '^IXIC', '^RUT', 
        '^VIX', '^FTSE', 'GC=F']

def isSupport(df,i):
  support = df['Low'][i] <= df['Low'][i-1]  and df['Low'][i] <= df['Low'][i+1] and df['Low'][i] <= df['Low'][i+2] and df['Low'][i] <= df['Low'][i-2]
  return support
  
def isResistance(df,i):
  resistance = df['High'][i] >= df['High'][i-1]  and df['High'][i] >= df['High'][i+1] and df['High'][i] >= df['High'][i+2] and df['High'][i] >= df['High'][i-2]
  return resistance


def snr(inst,tf='1d'):
  '''plots structure levels on several pairs
  '''
  #locating the levels
  levels = []
  ticker = yfinance.Ticker(inst)
  df = ticker.history(interval=tf, period='4mo')

  df['Date'] = pd.to_datetime(df.index)
  df['Date'] = df['Date'].apply(mpl_dates.date2num)
  df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

  
  for i in range(59,df.shape[0]-2):
    if isSupport(df,i):
      levels.append((i,df['Low'][i]))
      if isResistance(df,i):
        levels.append((i,df['High'][i]))
    elif isResistance(df,i):
      levels.append((i,df['High'][i]))
      if isSupport(df,i):
        levels.append((i,df['Low'][i]))

  # plotting the chart
  fig, ax = plt.subplots()
  candlestick_ohlc(ax,df.values,width=0.6, \
                   colorup='green', colordown='red', alpha=0.8)
  date_format = mpl_dates.DateFormatter('%d %b %Y')
  ax.xaxis.set_major_formatter(date_format)
  fig.autofmt_xdate()
  fig.tight_layout()
  for level in levels:
    plt.hlines(level[1],xmin=df['Date'][level[0]],\
               xmax=max(df['Date']),colors='blue')
  plt.title(f"{inst}") 
  #fig.savefig(f'{inst}.png')
  #fig.show()
  return fig.show()


def structures(inst=inst,tf='1d'):
  print(f'Calculating Structure levels on {tf}...')
  for i in range(0, len(inst)):
    snr(inst[i], tf)
  return f'Check again next {tf} period'


    