import time
import numpy as np
import pandas as pd
import QLearner as ql
import datetime as dt
from util import get_data

class StrategyLearner(object):
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.ql = ql.QLearner(num_states=3000, num_actions=3, rar=0.5, radr=0.99,dyna=30)
        
    def addEvidence(self, \
                    symbol='IBM', \
                    sd=dt.datetime(2008,1,1), \
                    ed=dt.datetime(2009,1,1), \
                    sv=10000):
        self.symbol = symbol
        self.sd = sd
        self.ed = ed
        self.sv = sv
        #calculate features
        df_features = self.calc_features()
        if np.sum(df_features.values) == 0:
            print 'NO FEATURES!'
        else:
            #calculate discretize thresholds
            self.thresholds = self.disc_thresh(df_features)
            #train learner
            self.train_learner(df_features)

    def testPolicy(self, \
                   symbol='IBM', \
                   sd=dt.datetime(2008,1,1), \
                   ed=dt.datetime(2009,1,1), \
                   sv=10000):
        self.symbol = symbol
        self.sd = sd
        self.ed = ed
        #calculate the features
        df_features = self.calc_features()
        if np.sum(df_features.values) == 0:
            print 'NO FEATURES!'
            df_trades =  pd.DataFrame(index=df_features.index, columns=['Trades'])
            df_trades.ix[:] = 0
        else:
            #test learner
            df_trades = self.test_learner(df_features)
        return df_trades
        

    """
    Test Learner Functions
    """

    def test_learner(self, df_features):
        #Actions: 0 = BUY, 1 = SELL, 2 = NOTHING
        BUY = 0
        SELL = 1
        NOTHING = 2
        #positions: 0 = CASH, 1 = SHORT, 2 = LONG
        CASH = 0
        SHORT = 1
        LONG = 2
        #prime test
        df_trades = pd.DataFrame(index=df_features.index, columns=['Trades'])
        cur_pos = CASH
        holdings = 0
        for date in range(0, df_features.shape[0]):
            state = self.discretize(df_features.ix[date,'BB'], \
                                    df_features.ix[date,'MOM'], \
                                    df_features.ix[date,'VOL']) + cur_pos * 1000
            action = self.ql.querysetstate(state)
            if action == BUY and cur_pos != LONG:
                df_trades.ix[date, 'Trades'] = 100
                holdings += 100
            elif action == SELL and cur_pos != SHORT:
                df_trades.ix[date, 'Trades'] = -100
                holdings -= 100
            else:
                df_trades.ix[date, 'Trades'] = 0
            if holdings == 100:
                cur_pos = LONG
            elif holdings == -100:
                cur_pos = SHORT
            else:
                cur_pos = CASH
        return df_trades

    """
    Train Learner Functions
    """
    def train_learner(self, df_features):
        #build a df_holdings
        df_original_holdings = self.build_holdings(df_features)
        #Training loop
        for i in range(0, 200):
            #reset df_holdings
            df_holdings = df_original_holdings.copy()
            #calc start state
            date = 0
            cur_pos = 0
            state = self.discretize(df_features.ix[date,'BB'], \
                                    df_features.ix[date,'MOM'], \
                                    df_features.ix[date,'VOL']) + cur_pos * 1000
            action = self.ql.querysetstate(state)
            #loop through all the dates in df_features
            inner = time.time()
            for date in range(1, df_features.shape[0]):
                #apply action and update df_holdings and cur_pos
                df_holdings, cur_pos = self.apply_action(date, df_holdings, action)
                #calculate the reward - % change in port val from previous day
                daily_ret = (df_holdings.ix[date, 'Portfolio Value'] / \
                          df_holdings.ix[date - 1, 'Portfolio Value'] - 1)
                reward = daily_ret
                #update state by discretizing
                state = self.discretize(df_features.ix[date,'BB'], \
                                        df_features.ix[date,'MOM'], \
                                        df_features.ix[date,'VOL']) + cur_pos * 1000
                if state == 0:
                    print df_features.ix[date], self.symbol
                    continue
                #query learner and get new action
                #print state, reward, df_holdings.ix[date, 'Portfolio Value']
                action = self.ql.query(state, reward)
            print 'inner', time.time() - inner
            cum_ret = df_holdings.ix[-1, 'Portfolio Value'] / self.sv - 1
            print i, 'Cum Ret:', cum_ret
                

    """
    Discretize Functions
    """

    def discretize(self, bb, mom, vol):
        disc_val = 0
        for i in range(0, self.disc_steps):
            if bb <= self.thresholds[i,0]:
                disc_val += i
                break
        for i in range(0, self.disc_steps):
            if mom <= self.thresholds[i,1]:
                disc_val += i * 10
                break
        for i in range(0, self.disc_steps):
            if vol <= self.thresholds[i,2]:
                disc_val += i * 100
                break
        return disc_val

    def disc_thresh(self, df_features):
        thresholds = np.zeros((10,3))
        #data.sort()
        df_bb = df_features['BB'].copy()
        df_bb.sort()
        df_mom = df_features['MOM'].copy()
        df_mom.sort()
        df_vol = df_features['VOL'].copy()
        df_vol.sort()
        #define number of buckets
        self.disc_steps = steps = 10
        #stepsize = size(data)/steps
        stepsize = df_bb.size / steps 
        #for i in range(0, steps):
        #    threshold[i] = data[(i+1)*stepsize]
        if df_bb.size == 10:
            for i in range(0, steps):
                #bb threshold
                thresholds[i, 0] = df_bb[i]
                #mom threshold
                thresholds[i, 1] = df_bb[i]
                #vol threshold
                thresholds[i, 2] = df_bb[i]
        else:
            for i in range(0, steps):
                #bb threshold
                thresholds[i, 0] = df_bb[(i+1)*stepsize]
                #mom threshold
                thresholds[i, 1] = df_bb[(i+1)*stepsize]
                #vol threshold
                thresholds[i, 2] = df_bb[(i+1)*stepsize]
        return thresholds
        
    """
    build features dataframe
    """
    def calc_daily_rets(self, prices):
        normed = prices/prices.ix[0]
        daily_rets = (normed/normed.shift(1))-1
        daily_rets = daily_rets[1:]
        return daily_rets

    def calc_features(self):
        window = 20
        #get stock prices for symbol
        df_prices = get_data(symbols=[self.symbol],\
                                  dates=pd.date_range(self.sd, self.ed))
        if 'SPY' in df_prices.columns.values:
            del df_prices['SPY']
        #calculate dataframes for features
        df_daily_rets = self.calc_daily_rets(df_prices)
        df_sma = pd.rolling_mean(df_prices, window=window)
        df_std = pd.rolling_std(df_prices, window=window)
        df_daily_rets_std = pd.rolling_std(df_daily_rets, window=window)
        columns = ['BB', 'MOM', 'VOL', 'Price']
        index = df_sma.index
        df_features = pd.DataFrame(index=index, columns=columns)
        #calculate features for each day
        for t in range(window-1, df_prices.shape[0]-1):
            df_features.ix[t,'BB'] = (df_prices.ix[t,self.symbol] - df_sma.ix[t,self.symbol]) / \
                                     (2*df_std.ix[t,self.symbol])
            df_features.ix[t,'MOM'] = ((df_prices.ix[t,self.symbol] / \
                                        df_prices.ix[t-window, self.symbol]) - 1.0)
            df_features.ix[t,'VOL'] = df_daily_rets_std.ix[t, self.symbol]
            df_features.ix[t, 'Price'] = df_prices.ix[t, self.symbol]
        return df_features.fillna(0)

    """
    Utility Functions
    """
    def build_holdings(self, df_features):
        dates = pd.date_range(df_features.index[0], df_features.index[-1])
        columns = [self.symbol, 'Stock Price','Cash', 'Portfolio Value']
        df_holdings = pd.DataFrame(index=dates, columns=columns)
        df_holdings.ix[:, self.symbol] = 0
        df_holdings.ix[:, 'Stock Price'] = df_features.ix[:, 'Price']
        df_holdings.ix[:, 'Cash'] = self.sv
        df_holdings.ix[:, 'Portfolio Value'] = self.sv
        return df_holdings.dropna()

    def calc_cur_pos(self, df_holdings, date):
        #positions: 0 = CASH, 1 = SHORT, 2 = LONG
        if df_holdings.ix[date, self.symbol] == 0: #cash position
            cur_pos = 0
        elif df_holdings.ix[date, self.symbol] < 0: #short position
            cur_pos = 1
        else: #long position
            cur_pos = 2
        return cur_pos

    def apply_action(self, date, df_holdings, action):
        #Actions: 0 = BUY, 1 = SELL, 2 = NOTHING
        BUY = 0
        SELL = 1
        NOTHING = 2
        #positions: 0 = CASH, 1 = SHORT, 2 = LONG
        CASH = 0
        SHORT = 1
        LONG = 2
        #calculate current position
        cur_pos = self.calc_cur_pos(df_holdings, date)
        #apply action if able
        if action == BUY and cur_pos != LONG: 
            #add 100 shares and extend that holding into the future
            df_holdings.ix[date:, self.symbol] += 100
            #deduct purchase cost from cahs and extend into the future
            df_holdings.ix[date:, 'Cash'] = df_holdings.ix[date, 'Cash'] - \
                                            df_holdings.ix[date, 'Stock Price'] * 100
        elif action == SELL and cur_pos != SHORT:
            #subtract 100 shares and extend that holding into the future
            df_holdings.ix[date:, self.symbol] -= 100
            #deduct purchase cost from cahs and extend into the future
            df_holdings.ix[date:, 'Cash'] = df_holdings.ix[date, 'Cash'] + \
                                            df_holdings.ix[date, 'Stock Price'] * 100
        cur_pos = self.calc_cur_pos(df_holdings, date)
        #update portfolio value and extend into the future
        df_holdings.ix[date:, 'Portfolio Value'] = df_holdings.ix[date, 'Cash'] +\
                                                   df_holdings.ix[date, self.symbol] *\
                                                   df_holdings.ix[date, 'Stock Price']
        return df_holdings, cur_pos
