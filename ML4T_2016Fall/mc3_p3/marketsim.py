"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
import math
import matplotlib.pyplot as plt
from util import get_data, plot_data

def compute_portvals(orders_file = "ml_test_output.csv", start_val = 100000):
    orders=pd.read_csv(orders_file,index_col='Date') #orders first step done
    portvals= portval_comp(orders,start_val)
    return portvals

def portval_comp(orders,start_val):
    mod=False
    orders=orders.sort_index(axis=0)
    spl_date='2011-06-15'
    if spl_date in orders.index :
    	orders=orders.drop(orders.index==spl_date)
    order_date=list(orders.index)
    start_date = order_date[0]
    end_date = order_date[-1]
    sym=orders.Symbol.unique()
    i=np.where(sym=='SPY')
    sym=np.delete(sym,i,None)
    sym= list(sym)
    prices= get_data(sym, pd.date_range(start_date, end_date))
    norm_prices = prices/prices.ix[0]
    prices['Cash']=1.0
    del prices['SPY']
    trades=prices.copy()
    l= len(trades)
    s=len(sym)
    trades.ix[:]=0
    for d in trades.index:
		d1= str(d.date())
		curr_order=orders[orders.index==d1]
		for i,row in curr_order.iterrows():
					if (row.Order=='BUY'):
						flag=1;
					else:
						flag=-1;
					trades.ix[d][row['Symbol']]=trades.ix[d][row['Symbol']]+flag*(row.Shares)
					curr_price=prices.ix[d][row['Symbol']]
					trades.ix[d]['Cash']=trades.ix[d]['Cash']+(-1)*curr_price*flag*(row.Shares)
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

    '''orders1=pd.read_csv('rule_based_output.csv',index_col='Date')
    mod=False
    orders1=orders1.sort_index(axis=0)
    spl_date='2011-06-15'
    if spl_date in orders1.index :
    	orders1=orders1.drop(orders1.index==spl_date)
    order1_date=list(orders1.index)
    start1_date = order1_date[0]
    end1_date = order1_date[-1]
    sym1=orders1.Symbol.unique()
    i=np.where(sym1=='SPY')
    sym1=np.delete(sym1,i,None)
    sym1= list(sym1)
    prices1= get_data(sym1, pd.date_range(start1_date, end1_date))
    norm1_prices = prices1/prices1.ix[0]
    prices1['Cash']=1.0
    del prices1['SPY']
    trades1=prices1.copy()
    l1= len(trades1)
    s1=len(sym1)
    trades1.ix[:]=0
    for d in trades1.index:
		d1= str(d.date())
		curr_order=orders1[orders1.index==d1]
		for i,row in curr_order.iterrows():
					if (row.Order=='BUY'):
						flag=1;
					else:
						flag=-1;
					trades1.ix[d][row['Symbol']]=trades1.ix[d][row['Symbol']]+flag*(row.Shares)
					curr_price=prices1.ix[d][row['Symbol']]
					trades1.ix[d]['Cash']=trades1.ix[d]['Cash']+(-1)*curr_price*flag*(row.Shares)
    holding1=trades1.copy()
    holding1.ix[:]=0
    holding1.ix[0]=trades1.ix[0]    
    holding1.ix[0]['Cash']= holding1.ix[0]['Cash']+start_val
    for i in range(1,len(holding1)):
	holding1.ix[i]=holding1.ix[i-1]+trades1.ix[i]
    value1=holding1.copy()
    value1.ix[:]=0
    for d in value1.index:
	value1.ix[d]=prices1.ix[d]*holding1.ix[d]	

    portvals1 = value1.sum(axis=1)'''


    ex = orders[orders['Type'] == 'EXIT']
    lo = orders[orders['Type'] == 'LONG']
    sh = orders[orders['Type'] == 'SHORT']
    df_temp = pd.concat([norm_prices['IBM'], portvals/portvals[0],' portvals1/portvals1[0]],' keys=['Benchmark', 'ML Based Portfolio','Rule Based Portfolio'], axis=1)
    ax = df_temp.plot(color=['black', 'green','blue'])
    ax.vlines(x=lo.index, ymin=0.5, ymax=2, color='green', linestyle='dashed',linewidth=2)
    ax.vlines(x=sh.index, ymin=0.5, ymax=2, color='red', linestyle='dashed',linewidth=3)
    ax.vlines(x=ex.index, ymin=0.5, ymax=2, color='black', linestyle='solid')
    plt.savefig('Part3.png')
    plt.show()

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
    of = "ml_test_output.csv"
    sv = 100000

    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
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
