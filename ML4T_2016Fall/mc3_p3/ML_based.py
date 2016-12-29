import time
import numpy as np
import pandas as pd
import RTLearner as rt
import datetime as dt
from util import get_data
import csv

def ml_model (symbols, sd, ed, test_sd, test_ed):
  dates = pd.date_range(sd, ed)

  df_price = get_data(symbols, dates)
  del df_price['SPY']
  
  features = ['SMA','MOM','VOL','BB']
  index = df_price.index

  df_features = pd.DataFrame(index=index,columns=features)
  df_norm = df_price/df_price.ix[0]
  df_daily_rets = (df_norm/df_norm.shift(1))-1
  df_daily_rets = df_daily_rets[1:] 
  sma = df_price.rolling(window=10,min_periods=10).mean()
  std = df_price.rolling(window=10,min_periods=10).std()
  df_features['SMA'] = df_price/sma
  df_features['VOL'] = df_daily_rets.rolling(window=10,min_periods=10).std()
  df_features['MOM'] = (df_price/df_price.shift(10))-1
  df_features['BB'] = (df_price-sma)/(2*std)
  df_features = df_features.fillna(0)

  df_features_m = df_features.as_matrix()
  df_output = df_features['MOM'].copy()

  for i in df_output.index:
	val = df_output.ix[i]
	if val < -0.078:
		df_output.ix[i] = -1
	elif val > -0.088:
		df_output.ix[i] = 1
	else:
		df_output.ix[i] = 0

  df_output_m = df_output.as_matrix()
  learner = rt.RTLearner(leaf_size = 5, verbose = False) # constructor
  learner.addEvidence(df_features_m, df_output_m)

  orders = []
  d = 9
  holdings ={'IBM':0}
  while (d < df_features_m.shape[0]-1):
	count= False
	while(count==False):
		d=d+1
		if (d > df_features_m.shape[0]-1):
			break
		if (df_output_m[d]==1):
			if holdings['IBM'] < 500:
        			holdings['IBM'] = holdings['IBM'] + 500
              			orders.append([df_price.index[d].date(), 'IBM', 'BUY', 500, 'LONG'])
              			count = True
		elif (df_output_m[d]==-1):
			if holdings['IBM'] > -500:
        			holdings['IBM'] = holdings['IBM'] - 500
        	      		orders.append([df_price.index[d].date(), 'IBM', 'SELL', 500, 'SHORT'])
        	      		count = True
	d = d+10
	if (d > df_features_m.shape[0]-1):
			break
	if(holdings['IBM']>0):
		holdings['IBM'] = 0
		orders.append([df_price.index[d].date(), 'IBM', 'SELL', 500, 'EXIT'])	
	else:
		holdings['IBM'] = 0
		orders.append([df_price.index[d].date(), 'IBM', 'BUY', 500, 'EXIT'])
	d = d - 1

  #print orders
  with open("ml_output.csv", "wb") as f:
    writer = csv.writer(f)	
    writer.writerow(['Date','Symbol','Order','Shares','Type'])
    writer.writerows(orders)
  f.close()

  test_dates = pd.date_range(test_sd, test_ed)
  df_test_price = get_data(symbols, test_dates)
  del df_test_price['SPY']
  test_features = ['SMA','MOM','VOL','BB']
  test_index = df_test_price.index

  df_test_features = pd.DataFrame(index=test_index,columns=test_features)
  df_test_norm = df_test_price/df_test_price.ix[0]
  df_test_daily_rets = (df_test_norm/df_test_norm.shift(1))-1
  df_test_daily_rets = df_test_daily_rets[1:] 
  test_sma = df_test_price.rolling(window=10,min_periods=10).mean()
  test_std = df_test_price.rolling(window=10,min_periods=10).std()
  df_test_features['SMA'] = df_test_price/test_sma
  df_test_features['VOL'] = df_test_daily_rets.rolling(window=10,min_periods=10).std()
  df_test_features['MOM'] = (df_test_price/df_test_price.shift(10))-1
  df_test_features['BB'] = (df_test_price-test_sma)/(2*test_std)
  df_test_features = df_test_features.fillna(0)
  df_test_features_m = df_test_features.as_matrix()
  df_test_output=learner.query(df_test_features_m)

  test_orders = []
  d = 9
  test_holdings ={'IBM':0}
  while (d < df_test_features_m.shape[0]-1):
	test_count= False
	while(test_count==False):
		d=d+1
		if (d > df_test_features_m.shape[0]-1):
			break
		if (df_test_output[d]==1):
			if test_holdings['IBM'] < 500:
        			test_holdings['IBM'] = test_holdings['IBM'] + 500
              			test_orders.append([df_test_price.index[d].date(), 'IBM', 'BUY', 500, 'LONG'])
              			test_count = True
		elif (df_test_output[d]==-1):
			if test_holdings['IBM'] > -500:
        			test_holdings['IBM'] = test_holdings['IBM'] - 500
        	      		test_orders.append([df_test_price.index[d].date(), 'IBM', 'SELL', 500, 'SHORT'])
        	      		test_count = True
	d = d+10
	if (d > df_test_features_m.shape[0]-1):
			break
	if(test_holdings['IBM']>0):
		test_holdings['IBM'] = 0
		test_orders.append([df_test_price.index[d].date(), 'IBM', 'SELL', 500, 'EXIT'])	
	else:
		test_holdings['IBM'] = 0
		test_orders.append([df_test_price.index[d].date(), 'IBM', 'BUY', 500, 'EXIT'])
	d = d - 1
  
  

  with open("ml_output.csv", "wb") as f:
    writer = csv.writer(f)	
    writer.writerow(['Date','Symbol','Order','Shares','Type'])
    writer.writerows(test_orders)
  f.close()

if __name__ == "__main__":
  sd = dt.datetime(2006,01,01)
  ed = dt.datetime(2009,12,31)
  test_sd = dt.datetime(2006,01,01)
  test_ed = dt.datetime(2009,12,31)
  symbols = ['IBM']
  ml_model(symbols, sd, ed, test_sd, test_ed)
