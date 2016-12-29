"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""

import datetime as dt
import QLearner as ql
import pandas as pd
import util as ut
from util import get_data

class holdings:
	none = 4
	allowed = 500
	long_five_hundred = 5
	short_five_hundred = 6

class actions:
	nothing = 0
	sell = 2
	buy = 1

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False):
        self.verbose = verbose

    def calcindi(self,sd,ed,syms, window=10):
	dates = pd.date_range(sd,ed)
	df_prices = get_data(syms,dates)
	df_prices = df_prices[syms]
	df_norm = df_price/df_prices.ix[0,:]
	sma = df_price.rolling(window=window).mean().dropna()
	vol = df_price.rolling(window=window).std().dropna()
	bb = 
	df_indis = pdf.concat(df_norm[window-1:],sma,vol)
	df_indis.columns = ['NORM','SMA','volatility']
	return df_indis
	

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), sv = 10000): 

        self.learner = ql.QLearner( num_states=1000,num_actions = 3,alpha = 0.2, gamma = 0.9,rar = 0.5,radr = 0.99, dyna = 0, verbose = False)
        # add your code to do learning here

        df_indis = self.calcindi(sd, ed, [symbol])
	df_states = self.discretize(df_inidcators)
  	
	port_vals = []
	max_iters = 10000
	iter_con = 100
	
	for i in range(0,max_iters):
		curr_holdings = holdings.NONE
	        curr_val = sv
       		curr_state = 0
		first = True
        
	for day in df_states.index:
                curr_state = self.comp_currstate(df_states[day], curr_holdings)
                
                if first:
                    curr_action = self.learner.querysetstate(curr_state)
                    curr_holdings, curr_val = self.actions(day, curr_action, curr_holdings, curr_val, df_prices[symbol])
                    first = False
                    pass
                else :
                    #    Compute the current state (including holding)
                    r = self.calculate_portfolio_value(day, i_current_holdings, i_current_cash, df_prices[symbol])
                    if self.verbose:
                        print "Day:", day, " State:",i_current_state, "Last Action:", action, "R:", r
                    
                    #    Query the learner with the current state and reward to get an action
                    action = self.learner.query(i_current_state,r)
                    
                    #    Implement the action the learner returned (BUY, SELL, NOTHING), and update portfolio value
                    i_current_holdings, i_current_cash = self.perform_action(day, action, i_current_holdings, i_current_cash, df_prices[symbol])
                
                portfolio_value = self.calculate_portfolio_value(day, i_current_holdings, i_current_cash, df_prices[symbol])
                
            if self.verbose:
                print "iteration:", iteration, "portfolio_value:", portfolio_value
            portfolio_values.append(portfolio_value)
            
            if len(portfolio_values) >= convergent_iterations and (portfolio_value == portfolio_values[-convergent_iterations:]).all():
                if self.verbose:
                    print "Convergence found at iteration:", iteration
                break;
            #Repeat the above loop multiple times until cumulative return stops improving.
        
        
        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose: print prices
  
        # example use with new colname 
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        volume = volume_all[syms]  # only portfolio symbols
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later
if self.verbose: print volume

    def discretize(self,df_indis):
	ncols = df_indis.shape[1]
        for col in range(ncols):
            df_indis.iloc[:, col] = pd.cut(df_indis.iloc[:, col], 9, labels = range(1,10)).astype('float')
            df_indis.iloc[:, col] = df_indis.iloc[:, col].astype('float')
            if(col > 0):
                df_indis.iloc[:, col] = df_indis.iloc[:, col] * (col * 10)       
        df_indis = df_indis.fillna(0)
        df_indis = df_indis.astype(int)
        df_states = df_indis.sum(axis = 1)
	return df_states

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # here we build a fake set of trades
        # your code should return the same sort of data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        trades = prices_all[[symbol,]]  # only portfolio symbols
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later
        trades.values[:,:] = 0 # set them all to nothing
        trades.values[3,:] = 500 # add a BUY at the 4th date
        trades.values[5,:] = -500 # add a SELL at the 6th date 
        trades.values[6,:] = -500 # add a SELL at the 7th date 
        trades.values[8,:] = 1000 # add a BUY at the 9th date
        if self.verbose: print type(trades) # it better be a DataFrame!
        if self.verbose: print trades
        if self.verbose: print prices_all
        return trades

if __name__=="__main__":
    print "One does not simply think up a strategy"
