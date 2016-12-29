"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo
import numpy as np

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def sharpe_ratio(allocs,prices):
	tmp_prtval=((prices/prices.ix[0,:])*allocs).sum(axis=1)
	tmp_dr=(tmp_prtval/tmp_prtval.shift(1))-1
	tmp_dr=tmp_dr[1:]
	tmp_adr=tmp_dr.mean()
	sharpe=((tmp_adr)/tmp_dr.std())
	sharpe= (-1)*sharpe
	return sharpe
def some(allocs):
	return 1-np.sum(allocs)

def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):


    # Read in adjusted closing prices for given symbols, date range
	dates = pd.date_range(sd, ed)
	prices_all = get_data(syms, dates)  # automatically adds SPY
	prices = prices_all[syms]  # only portfolio symbols
	prices_SPY = prices_all['SPY']  # only SPY, for comparison later


    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
	#allocs = np.asarray([0.2, 0.2, 0.3, 0.3,0.0]) # add code here to find the allocations
	length=len(syms)
	l=float(length)
	#allocs=np.ones(length)*(1/l)
	allcs=[]
	for x in range(0,length):
		allcs.append(1/l)
	bnds = tuple((0,1) for x in allcs)
	#consts = ({ 'type': 'eq', 'fun': sone inputs: 1.0 - np.sum(allcs)})
	consts = ({ 'type': 'eq', 'fun': some })
	result=spo.minimize(sharpe_ratio,allcs,args=(prices,),method='SLSQP',bounds=bnds,constraints=consts,options={'disp':True})
	allocs=result.x

    # Get daily portfolio value
	port_val = prices_SPY # add code here to compute daily portfolio values
	pos_val= (prices/prices.ix[0,:])*allocs
	port_val=pos_val.sum(axis=1)
	
	cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
	cr=(port_val[-1]/port_val[0])-1
	dr=port_val.copy()
	dr=(port_val/port_val.shift(1))-1
	dr.ix[0]=0
	dr=dr[1:]
	adr=dr.mean()
	sddr=dr.std()
	tmp=dr.mean()
	sr=(tmp/sddr)
	
	
    # Compare daily portfolio value with SPY using a normalized plot
	if gen_plot:
        # add code to plot here
        	df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
		#ax=df_temp['Portfolio'].plot()
		#plot_data(df_temp['Portfolio'])
		#plot_data(df_temp['SPY'])
		df_temp=df_temp/df_temp.ix[0,:]
		ax=df_temp['Portfolio'].plot()
		ax=df_temp['SPY'].plot()
		ax.set_title("Daily portfolio value and SPY")
		ax.set_xlabel("Dates")
    		ax.set_ylabel("Normalized Prices")
		plt.legend(loc="upper right")
		plt.grid()
		plt.show()
        	pass
		
	return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

	start_date = dt.datetime(2009,1,1)
	end_date = dt.datetime(2010,1,1)
	symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']
	#start_date = dt.datetime(2008,1,1)
	#end_date = dt.datetime(2009,12,31)
	#symbols = ['IBM', 'X', 'HNZ', 'XOM', 'GLD']

    # Assess the portfolio
	allocations, cr, adr, sddr, sr =  optimize_portfolio(sd = start_date, ed = end_date,\
	syms = symbols, \
	gen_plot = True)

    # Print statistics
	print "Start Date:", start_date
	print "End Date:", end_date
	print "Symbols:", symbols
	print "Allocations:", allocations
	print "Sharpe Ratio:", sr
	print "Volatility (stdev of daily returns):", sddr
	print "Average Daily Return:", adr
	print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
	test_code()
