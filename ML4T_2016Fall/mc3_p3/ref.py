import numpy as np
import pandas as pd
import datetime as dt
import math
import time
import util
import sys


def build_orders (symbols, start_date, end_date, lookback):

  print "Constructing SMA, BB%, RSI from " + str(start_date.date()) + \
        " to " + str(end_date.date())

  # Construct an appropriate DatetimeIndex object.
  dates = pd.date_range(start_date, end_date)

  # Read all the relevant price data (plus SPY) into a DataFrame.
  price = util.get_data(symbols, dates)

  # Add SPY to the symbol list for convenience.
  symbols.append('SPY')


  ### Calculate SMA-14 over the entire period in a single step.
  sma = price.rolling(window=lookback,min_periods=lookback).mean()


  ### Calculate Bollinger Bands (14 day) over the entire period.
  rolling_std = price.rolling(window=lookback,min_periods=lookback).std()
  top_band = sma + (2 * rolling_std)
  bottom_band = sma - (2 * rolling_std)

  bbp = (price - bottom_band) / (top_band - bottom_band)


  ### Now we can turn the SMA into an SMA ratio, which is more useful.
  sma = price / sma


  ### Calculate Relative Strength Index (14 day) for the entire date range for all symbols.
  rs = price.copy()
  rsi = price.copy()

  # Calculate daily_rets for the entire period (and all symbols).
  daily_rets = price.copy()
  daily_rets.values[1:,:] = price.values[1:,:] - price.values[:-1,:]
  daily_rets.values[0,:] = np.nan

  # Split daily_rets into a same-indexed DataFrame of only up days and only down days,
  # and accumulate the total-up-days-return and total-down-days-return for every day.
  up_rets = daily_rets[daily_rets >= 0].fillna(0).cumsum()
  down_rets = -1 * daily_rets[daily_rets < 0].fillna(0).cumsum()

  # Apply the sliding lookback window to produce for each day, the cumulative return
  # of all up days within the window, and separately for all down days within the window.
  up_gain = price.copy()
  up_gain.ix[:,:] = 0
  up_gain.values[lookback:,:] = up_rets.values[lookback:,:] - up_rets.values[:-lookback,:]

  down_loss = price.copy()
  down_loss.ix[:,:] = 0
  down_loss.values[lookback:,:] = down_rets.values[lookback:,:] - down_rets.values[:-lookback,:]

  # Now we can calculate the RS and RSI all at once.
  rs = (up_gain / lookback) / (down_loss / lookback)
  rsi = 100 - (100 / (1 + rs))
  rsi.ix[:lookback,:] = np.nan

  # An infinite value here indicates the down_loss for a period was zero (no down days), in which
  # case the RSI should be 100 (its maximum value).
  rsi[rsi == np.inf] = 100



  ### Use the three indicators to make some kind of trading decision for each day.

  # Orders starts as a NaN array of the same shape/index as price.
  orders = price.copy()
  orders.ix[:,:] = np.NaN

  # Create a copy of RSI but with the SPY column copied to all columns.
  spy_rsi = rsi.copy()
  spy_rsi.values[:,:] = spy_rsi.ix[:,['SPY']]

  # Create a binary (0-1) array showing when price is above SMA-14.
  sma_cross = pd.DataFrame(0, index=sma.index, columns=sma.columns)
  sma_cross[sma >= 1] = 1

  # Turn that array into one that only shows the crossings (-1 == cross down, +1 == cross up).
  sma_cross[1:] = sma_cross.diff()
  sma_cross.ix[0] = 0

  # Apply our entry order conditions all at once.  This represents our TARGET SHARES
  # at this moment in time, not an actual order.
  orders[(sma < 0.95) & (bbp < 0) & (rsi < 30) & (spy_rsi > 30)] = 100
  orders[(sma > 1.05) & (bbp > 1) & (rsi > 70) & (spy_rsi < 70)] = -100

  # Apply our exit order conditions all at once.  Again, this represents TARGET SHARES.
  orders[(sma_cross != 0)] = 0

  # We now have -100, 0, or +100 TARGET SHARES on all days that "we care about".  (i.e. those
  # days when our strategy tells us something)  All other days are NaN, meaning "hold whatever
  # you have".

  # Forward fill NaNs with previous values, then fill remaining NaNs with 0.
  orders.ffill(inplace=True)
  orders.fillna(0, inplace=True)

  # We now have a dataframe with our TARGET SHARES on every day, including holding periods.

  # Now take the diff, which will give us an order to place only when the target shares changed.
  orders[1:] = orders.diff()
  orders.ix[0] = 0

  # And now we have our orders array, just as we wanted it, with no iteration.



  # It would be hard to vectorize our weird formatting output, which triggers on individual
  # elements and needs the index values (row and column).

  # But we can at least drop the SPY column.
  del orders['SPY']
  symbols.remove('SPY')

  # And more importantly, drop all rows with no non-zero values (i.e. no orders).
  orders = orders.loc[(orders != 0).any(axis=1)]

  # Now we have only the days that have orders.  That's better, at least!
  order_list = []

  for day in orders.index:
    for sym in symbols:
      if orders.ix[day,sym] > 0:
        order_list.append([day.date(), sym, 'BUY', 100])
      elif orders.ix[day,sym] < 0:
        order_list.append([day.date(), sym, 'SELL', 100])

  # Dump the orders to stdout.  (Redirect to a file if you wish.)
  for order in order_list:
    print "	".join(str(x) for x in order)

### Main function.  Not called if imported elsewhere as a module.
if __name__ == "__main__":
  start_date = dt.datetime(2005,01,01)
  end_date = dt.datetime(2011,12,31)
  symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'HD', 'VZ', 'KO']
  lookback = 14

  build_orders(symbols, start_date, end_date, lookback)

