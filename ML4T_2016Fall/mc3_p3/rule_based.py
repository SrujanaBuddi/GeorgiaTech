import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import math as math
import csv
    
def build_orders (symbols, sd, ed, lookback):
  dates = pd.date_range(sd, ed)

  df_price = get_data(symbols, dates)

  symbols.append('SPY')
  sma = df_price.rolling(window=lookback,min_periods=lookback).mean()
  rolling_std = df_price.rolling(window=lookback,min_periods=lookback).std()
  cci = (df_price-sma)/(0.015*rolling_std)
  top_band = sma + (2 * rolling_std)
  bottom_band = sma - (2 * rolling_std)
  bbp = (df_price - bottom_band) / (top_band - bottom_band)
  sma = df_price / sma
  norm=df_price/df_price.ix[0,:]

  rs = df_price.copy()
  rsi = df_price.copy()
  daily_rets = df_price.copy()
  daily_rets.values[1:,:] = df_price.values[1:,:] - df_price.values[:-1,:]
  daily_rets.values[0,:] = np.nan

  up_rets = daily_rets[daily_rets >= 0].fillna(0).cumsum()
  down_rets = -1 * daily_rets[daily_rets < 0].fillna(0).cumsum()

  up_gain = df_price.copy()
  up_gain.ix[:,:] = 0
  up_gain.values[lookback:,:] = up_rets.values[lookback:,:] - up_rets.values[:-lookback,:]

  down_loss = df_price.copy()
  down_loss.ix[:,:] = 0
  down_loss.values[lookback:,:] = down_rets.values[lookback:,:] - down_rets.values[:-lookback,:]

  rs = (up_gain / lookback) / (down_loss / lookback)
  rsi = 100 - (100 / (1 + rs))
  rsi.ix[:lookback,:] = np.nan
  rsi[rsi == np.inf] = 100

  mom = (df_price/df_price.shift(10))-1
  mom5 = (df_price/df_price.shift(5))-1

  orders = df_price.copy()
  orders.ix[:,:] = np.NaN

  # Create a copy of RSI but with the SPY column copied to all columns.
  spy_rsi = rsi['SPY']
  #spy_rsi.values[:,:] = spy_rsi.ix[:,['SPY']]
  #print spy_rsi

  # Create a binary (0-1) array showing when price is above SMA-14.
  sma_cross = pd.DataFrame(0, index=sma.index, columns=sma.columns)
  sma_cross[sma >= 1] = 1

  sma_cross[1:] = sma_cross.diff()
  sma_cross.ix[0] = 0
  orders=[]
  holdings ={'IBM':0}
  d = 10
  while (d<df_price.shape[0]-1):
	count=False
	while(count==False):
		d=d+1
		if (d>=df_price.shape[0]-1):
			break
		if (sma.ix[d,'IBM']<1.04) or (bbp.ix[d,'IBM']<0) and (cci.ix[d,'IBM']<-50) and ((rsi.ix[d,'IBM']<30) and (spy_rsi.ix[d,'SPY']>30)) and (mom5.ix[d,'IBM'] - mom.ix[d,'IBM']< -0.1):#or(mom.ix[d,'IBM']>-1.0):
			if holdings['IBM']<500:
				holdings['IBM']=holdings['IBM']+500
          			orders.append([df_price.index[d].date(), 'IBM', 'BUY', 500, 'LONG'])
				count = True
		elif (sma.ix[d,'IBM']>1.05) or (bbp.ix[d,'IBM']>1) and (cci.ix[d,'IBM']>150) and ((rsi.ix[d,'IBM']>70) and (spy_rsi.ix[d,'SPY']<70)) and (mom5.ix[d,'IBM'] - mom.ix[d,'IBM'] > 0.07):#(mom.ix[d,'IBM']<-0.07):
			if holdings['IBM']>-500:
				holdings['IBM']=holdings['IBM']-500
          			orders.append([df_price.index[d].date(), 'IBM', 'SELL', 500, 'SHORT'])
				count = True
   	d = d + 10
    	if(d >= df_price.shape[0] - 1):
      		break
  
  	if(holdings['IBM'] > 0):
        	holdings['IBM'] = 0
      		orders.append([df_price.index[d].date(), 'IBM', 'SELL', 500, 'EXIT'])
    	else:
      		holdings['IBM'] = 0
      		orders.append([df_price.index[d].date(), 'IBM', 'BUY', 500, 'EXIT'])
	d=d-1

  with open("rule_based_output.csv", "wb") as f:
    writer = csv.writer(f)	
    writer.writerow(['Date','Symbol','Order','Shares','Type'])
    writer.writerows(orders)

if __name__ == "__main__":
  sd = dt.datetime(2006,01,01)
  ed = dt.datetime(2009,12,31)
  symbols = ['IBM']
  lookback = 10
  build_orders(symbols, sd, ed, lookback)

