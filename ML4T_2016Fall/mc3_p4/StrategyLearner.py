import datetime as dt
import QLearner as ql
import pandas as pd
import numpy as np
import util as ut

WINDOW = 15 
BUY = 1
SELL = 2
NOTHING = 0
MAX_SHARES = 500

#calculate indicators for the price dataframe
def calindis(df):
    df_norm = df / df.ix[0, :]
    sma = pd.rolling_mean(df_norm,window=WINDOW).dropna()
    #sma = df_norm.rolling(window=WINDOW).mean().dropna()
    rstd = pd.rolling_std(df_norm,window=WINDOW).dropna()
    #rstd = df_norm.rolling(window=WINDOW).std().dropna()
    bb_index = (df_norm - sma) / (2 * rstd)
    bb_index = bb_index.dropna()
    macd =  pd.rolling_mean(df_norm, window=10).dropna()-pd.rolling_mean(df_norm, window=15).dropna()
    #macd =  df_norm.rolling(window=10).mean().dropna()-df_norm.rolling(window=15).mean().dropna()
    macd = macd.dropna()
    return macd,bb_index


#discretize all the indicators
def indis_discretize(macd, bb_index, symbol):
    if len(macd) != len(bb_index):
        raise IndexError('Data frames should be of equal size.')
    #sort all the indicators
    sorted_macd = macd.sort_values(by=symbol)
    sorted_bbands = bb_index.sort_values(by=symbol)
    #define number of steps
    steps = 10
    #calculate step size
    step_size = int(len(sorted_macd)/steps)

    for i in range(0, steps):
        sorted_macd[i*step_size : (i+1) * step_size] = i	
        sorted_bbands[i*step_size : (i+1) * step_size] = i
    sorted_macd[-step_size:] = steps - 1
    sorted_bbands[-step_size:] = steps - 1
    for i in range(0, len(sorted_macd)):
        macd.ix[i] = sorted_macd.loc[macd.ix[i].name]
        bb_index.ix[i] = sorted_bbands.loc[bb_index.ix[i].name]
    indis = pd.concat([macd,bb_index], axis=1)   
    return indis.astype(int)



#Strategy Learner definition
class StrategyLearner:

    def __init__(self, verbose = True):
        self.learner = None
        self.verbose = verbose

    def addEvidence(self, symbol = "IBM", sd=dt.datetime(2006,1,1), ed=dt.datetime(2009,12,31), sv = 10000):
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # remove SPY details and retain only portfolio symbols

        macd,bb_index = calindis(prices)
        discrete_states = indis_discretize(macd,bb_index, symbol)
        prices = prices[WINDOW-1:] # to align with states

	#define max number of iterations for convergence
        max_iters = 20
        
	#define Q learner
        self.learner = ql.QLearner(num_states=999, num_actions=3, alpha=0.2, rar=0.99, radr=0.99993)

        for i in range(0, max_iters):

            holding = NOTHING
            curr_state = (discrete_states.ix[0].values[0]*10 + discrete_states.ix[0].values[1])*10 + holding
            curr_action = self.learner.querysetstate(curr_state)

            for j in range(1, len(discrete_states)):
		
                curr_state = discrete_states.ix[j].values[0]*10 + discrete_states.ix[j].values[1]
                
                if curr_action == BUY and holding != MAX_SHARES:
                    curr_state = curr_state*10 + BUY
                    holding += MAX_SHARES
                elif curr_action == SELL and holding != -MAX_SHARES:
                    curr_state = curr_state*10 + SELL
                    holding += -MAX_SHARES
                else:
                    curr_state = curr_state*10 + NOTHING
                if curr_action == NOTHING and holding == 0:
                    r = 0 
                else: r = holding * (prices.ix[j] / prices.ix[j-1] - 1)
                curr_action = self.learner.query(curr_state, r)


    def testPolicy(self, symbol = "IBM", sd=dt.datetime(2009,1,1), ed=dt.datetime(2010,1,1), sv = 10000):
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        prices = prices_all[[symbol,]]  # only portfolio symbols

        macd,bb_index = calindis(prices)#calculate indices
        discrete_states = indis_discretize(macd,bb_index, symbol)#discretize all the indicators

	#create a trades dataframe
	trades = pd.DataFrame(0, index=discrete_states.index, columns=[symbol])
	#update current state as explained in video. if inicators are 5,4,3 current state is updated as 5*100+4*10+3
        curr_state = discrete_states.ix[0].values[0]*10 + discrete_states.ix[0].values[1]
	#update current action for current state using Q learner
        curr_action = self.learner.querysetstate(curr_state)
        holding = NOTHING

        for i in range(1, len(discrete_states)):
	    #update current state
            curr_state = discrete_states.ix[i].values[0]*10 + discrete_states.ix[i].values[1]
	    #if action is buy and maximum shares are not exceeded then buy
            if curr_action == BUY and holding != MAX_SHARES:
                curr_state = curr_state*10 + BUY
                holding += MAX_SHARES
                trades.iloc[i-1][symbol] = MAX_SHARES
	    #if action is sell and maximum shares are not exceeded then sell
            elif curr_action == SELL and holding != -MAX_SHARES:
                curr_state = curr_state*10 + SELL                
                holding += -MAX_SHARES
                trades.iloc[i-1][symbol] = -MAX_SHARES
            else:
                curr_state = curr_state*10 + NOTHING

            if curr_action == NOTHING and holding == 0:
                    r = 0 
            else: r = holding * (prices.ix[i] / prices.ix[i-1] - 1)
            curr_action = self.learner.query(curr_state, r)
        return trades

if __name__ == "__main__":
    print "One does not simply think up a strategy"
