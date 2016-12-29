"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
import math
from util import get_data, plot_data

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000):
    # this is the function the autograder will call to test your code
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    #orders=pd.read_csv('./orders/orders.csv') #orders first step done
    orders=pd.read_csv(orders_file) #orders first step done
    portvals= portval_comp(orders,start_val)
    return portvals

def portval_comp(orders,start_val):
    mod=False
    orders=orders.sort_values(by='Date')
    spl_date='2011-06-15'
    if spl_date in orders['Date'] :
    	orders=orders.drop(orders['Date']==spl_date)
    order_date=list(orders['Date'])
    start_date = order_date[0]
    end_date = order_date[-1]
    sym=orders.Symbol.unique()
    i=np.where(sym=='SPY')
    sym=np.delete(sym,i,None)
    sym= list(sym)
    prices= get_data(sym, pd.date_range(start_date, end_date))
    prices['Cash']=1.0
    del prices['SPY']
    trades=prices.copy()
    l= len(trades)
    s=len(sym)
    trades.ix[:]=0
    for d in trades.index:
		d1= str(d.date())
		curr_order=orders[orders.Date==d1]
		for i,row in curr_order.iterrows():
					if (row.Order=='BUY'):
						flag=1;
					else:
						flag=-1;
					trades.ix[d][row['Symbol']]=trades.ix[d][row['Symbol']]+flag*(row.Shares)
					curr_price=prices.ix[d][row['Symbol']]
					trades.ix[d]['Cash']=trades.ix[d]['Cash']+(-1)*curr_price*flag*(row.Shares)
					#lev=sum(abs(trades.ix[d]*prices.ix[d]))
					#lev=lev/trades.ix[d]['Cash']
					#print lev
					#if lev>3.0:
						#trades.ix[d][row['Symbol']]=trades.ix[d][row['Symbol']]-flag*(row.Shares)
						#print trades.ix[d][row['Symbol']]
						#trades.ix[d]['Cash']=trades.ix[d]['Cash']+curr_price*flag*(row.Shares)
    holding=trades.copy()
    holding.ix[:]=0
    holding.ix[0]=trades.ix[0]    
    holding.ix[0]['Cash']= holding.ix[0]['Cash']+start_val
    for i in range(1,len(holding)):
	holding.ix[i]=holding.ix[i-1]+trades.ix[i]
    value=holding.copy()
    value.ix[:]=0
    for d in value.index:
	value.ix[d]=prices.ix[d]*holding.ix[d]				
    portvals = value.sum(axis=1)
    return portvals

#portfolio optimization calcs
def optimize_portfolio(portvals):
	cr=(portvals[-1]/portvals[0])-1
	dr=portvals.copy()
	dr=(portvals/portvals.shift(1))-1
	dr.ix[0]=0
	dr=dr[1:]
	adr=dr.mean()
	sddr=dr.std()
	tmp=dr.mean()
	sr=math.sqrt(252)*(tmp/sddr)		
	return cr, adr, sddr, sr

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    #if isinstance(portvals_SPY, pd.DataFrame):
     #   portvals_SPY = portvals_SPY[portvals_SPY.columns[0]] # just get the first column
    
    # Get portfolio stats
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]
    start_date= portvals.index.tolist()[0]
    end_date = portvals.index.tolist()[-1]
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = optimize_portfolio(portvals)

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
