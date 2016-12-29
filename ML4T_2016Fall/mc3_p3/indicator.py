"""Indicators"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import math as math
       

def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band=rm+2*rstd
    lower_band=rm-2*rstd
    return upper_band, lower_band

def get_RSI(df,window):
    ret= df.diff(periods=1)
    
    return df 

def test_run():
    insample_dates = pd.date_range('2006-01-01', '2009-12-31')
    symbols = ['IBM']
    df = get_data(symbols, insample_dates)
    #df_spy = df['SPY']
    del df['SPY']
    df_norm = df/df.ix[0,:]
    lookback = 10
    sma = df_norm.rolling(window=20,center=False).mean()
    sma_IBM = df.rolling(window=20,center=False).mean()
    indi1= df/sma_IBM#price/sma

    rstd_IBM = df.rolling(window=20,center=False).std()
    upper_band, lower_band = get_bollinger_bands(sma_IBM, rstd_IBM) #bollinger bands
    indi2 = (df - upper_band) / (upper_band - lower_band)#bbp
   
    indi3 = (df - sma_IBM)/(0.015*rstd_IBM) #CCI

    indi4 = (df/df.shift(10))-1 #momentum

    rs = df.copy()
    rsi = df.copy()
    daily_rets = df.copy()
    daily_rets.values[1:,:] = df.values[1:,:] - df.values[:-1,:]
    daily_rets.values[0,:] = np.nan
    up_rets = daily_rets[daily_rets >= 0].fillna(0).cumsum()
    down_rets = -1 * daily_rets[daily_rets < 0].fillna(0).cumsum()
    up_gain = df.copy()
    up_gain.ix[:,:] = 0
    up_gain.values[lookback:,:] = up_rets.values[lookback:,:] - up_rets.values[:-lookback,:]
    down_loss = df.copy()
    down_loss.ix[:,:] = 0
    down_loss.values[lookback:,:] = down_rets.values[lookback:,:] - down_rets.values[:-lookback,:]

    rs = (up_gain / lookback) / (down_loss / lookback)
    rsi = 100 - (100 / (1 + rs))
    rsi.ix[:lookback,:] = np.nan
    rsi[rsi == np.inf] = 100
    indi5 = rsi

    # Plot raw SPY values, rolling mean and Bollinger Bands
    df_temp = pd.concat([df_norm['IBM'], sma['IBM'], indi1['IBM']], keys=['Normalized IBM Price', 'SMA','Price/SMA'], axis=1)
    ax = df_temp.plot(title="Price/SMA")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.savefig('Price_SMA.png')

    df_temp = pd.concat([df['IBM'], sma_IBM['IBM'],upper_band['IBM'], lower_band['IBM'],indi2['IBM']], keys=['IBM Price','SMA', 'Upper Band','Lower Band','BBP'], axis=1)
    ax = df_temp.plot(title="Bollinger Bands - BBP")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.savefig('Bollinger Bands-BBP.png')

    df_temp = pd.concat([df['IBM'], sma_IBM['IBM'],rstd_IBM['IBM'],indi3['IBM']], keys=['IBM Price','SMA','Std Dev', 'CCI'], axis=1)
    ax = df_temp.plot(title="CCI- Commodity Channel Index")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.savefig('CCI.png')

    df_temp = pd.concat([df_norm['IBM'], indi4['IBM']], keys=['Normalized IBM Price','Momentum'], axis=1)
    ax = df_temp.plot(title="Momentum")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.savefig('Momentum.png')

    df_temp = pd.concat([df['IBM'],up_gain['IBM'],down_loss['IBM'], rsi['IBM']], keys=['IBM Price','Gain','Loss','RSI'], axis=1)
    ax = df_temp.plot(title="RSI-Relative Strength Index")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.savefig('RSI.png')
    return 0

if __name__ == "__main__":
    test_run()
