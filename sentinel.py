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
  return (df['Low'][i] <= df['Low'][i - 1] and df['Low'][i] <= df['Low'][i + 1]
          and df['Low'][i] <= df['Low'][i + 2]
          and df['Low'][i] <= df['Low'][i - 2])
  
def isResistance(df,i):
  return (df['High'][i] >= df['High'][i - 1]
          and df['High'][i] >= df['High'][i + 1]
          and df['High'][i] >= df['High'][i + 2]
          and df['High'][i] >= df['High'][i - 2])


def plot_support_n_resistance(pair,tf):
  '''plots structure levels on several pairs
  '''
  #locating the levels
  levels = []
  ticker = yfinance.Ticker(pair)
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
  # plt.title(f"{pair}")
  # import os create the directory
  # check if the pair does not exist then create otherwise we may overwrite
  # if possible delete each image when a newone is created to save space
  # remember sessions
  path = f"static/images/{pair.split('=')[0]}.png"
  fig.savefig(path)
  return path

    