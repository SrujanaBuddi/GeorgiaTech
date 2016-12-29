"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""
"""
TODO: Add more indicators to learner's state
"""
import datetime as dt
import QLearner as ql
import pandas as pd
import numpy as np
import util as ut

#import sys
#sys.path.insert(0, '../mc3_p2')
#from estimator import orders_to_csv


#################
### Constants ###
#################

TIME_FRAME = 20 # 20 days
ALLOWED_LOT = 500 # number of stock per trade

# Buy, sell and nothing flags
BUY = 1
SELL = 2
NOTHING = 0


######################
### Analysis tools ###
######################

def normalise_data(df):
    """ Normalise stock prices using the first row of dataframe. """
    return df / df.ix[0, :]

def compute_rolling_mean(df):
    return df.rolling(window=TIME_FRAME).mean().dropna()

def compute_rolling_std(df):
    return df.rolling(window=TIME_FRAME).std().dropna()

def compute_bollinger(df, rm, rstd):
    """ Compute normalised bollinger value. """
    bb_feature = (df - rm) / (2 * rstd)
    return bb_feature.dropna()

def adjclose_sma(df_adjclose, df_sma):
    """ Compute adjusted close / SMA ratio. """
    ratio = np.divide(df_adjclose, df_sma)
    return ratio

def get_all_stats(df_prices):
    """
    normed - normalised adjusted closing price
    ac_sma - adjusted close / SMA
    b_band - bollinger value
    """
    normed = normalise_data(df_prices)

    sma = compute_rolling_mean(normed)
    rstd = compute_rolling_std(normed)
    ac_sma = adjclose_sma(normed[TIME_FRAME-1:], sma) # -1 because array is 0-based
    b_val = compute_bollinger(normed, sma, rstd)

    return normed[TIME_FRAME-1:], ac_sma, b_val


### Discretizing ###
def discretize_all(df_acsma, df_bval, steps, symbol):
    """ 
        Convert a real number to a discrete value.
        This method takes real values from the two dataframes, sorts them
        and assigns an integer value based on their position in the sorted df.
        Example:
        --------
        Dataframes with size 230 and steps=10:
        all elements with index [0, 23) = 0
        all elements with index [23, 46) = 1
        all elements with index [207, 230) = 9
    """
    if len(df_acsma) != len(df_bval):
        raise IndexError('Data frames should be of equal size.')

    sorted_acsma = df_acsma.sort_values(by=symbol)
    sorted_bval = df_bval.sort_values(by=symbol)
    step_size = len(sorted_bval) // steps

    for i in range(0, steps):
        sorted_acsma[i*step_size : (i+1) * step_size] = i
        sorted_bval[i*step_size : (i+1) * step_size] = i

    # Some of the last elements might have been skipped.
    sorted_acsma[-step_size:] = steps - 1
    sorted_bval[-step_size:] = steps - 1

    # Change the real values to corresponding integer values.
    for i in range(0, len(sorted_bval)):
        df_acsma.ix[i] = sorted_acsma.loc[df_acsma.ix[i].name]
        df_bval.ix[i] = sorted_bval.loc[df_bval.ix[i].name]

    result = pd.concat([df_acsma, df_bval], axis=1)
    return result.astype(int)


### Strategy learner ###
class StrategyLearner:

    def __init__(self, verbose = False):
        self.learner = None
        self.verbose = verbose


    def compute_rse(en_price, curr_price):
        """ Compute return since entry.
            en_price - the entry price
            curr_price - the current price
        """
        return (curr_price - en_price) / en_price

    def add_evidence(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):
        """ Add data, discretize and return. """ 

        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols

        normed, ac_sma, b_val = get_all_stats(prices)
        discretized = discretize_all(ac_sma, b_val, 10, symbol)
        prices = prices[TIME_FRAME-1:] # Clear the first N prices to align this df with discretized

        return discretized, normed, prices


    def train_learner(self, discretized, normed, prices, episodes=600, sv=10000):
        """ Train a learner for a number of episodes to update its policy. """

        self.learner = ql.QLearner(num_states=999, num_actions=3, alpha=0.2, rar=0.99, radr=0.99993)

        for i in range(0, episodes):

            holding = NOTHING # Hold nothing at start.
            state = int(str(discretized.ix[0].values[0]) + str(discretized.ix[0].values[1]) + str(holding))
            action = self.learner.querysetstate(state)
            portval = sv # used in verbose mode to print portfolio value after each episode

            for j in range(1, len(discretized)):
                """
                1) Compute the state:
                    - adj close / SMA (index 0 of discretized values)
                    - BB value (index 1 of discretized values)
                    - holding stock
                2) Compute reward for last action
                3) Query the learner with current state and reward to get an action
                """
                # Partial state as string, converted to int, once last action is known.
                state = str(discretized.ix[j].values[0]) + str(discretized.ix[j].values[1]) 

                # Check previous action to update state and holding
                if action == BUY and holding != ALLOWED_LOT:
                    state = int(state + str(BUY))
                    holding += ALLOWED_LOT
                    portval -= ALLOWED_LOT * prices.ix[j-1]

                elif action == SELL and holding != -ALLOWED_LOT:
                    state = int(state + str(SELL))
                    holding += -ALLOWED_LOT
                    portval += ALLOWED_LOT * prices.ix[j-1]

                else:
                    state = int(state + str(NOTHING))

                # Reward is the number of shares holding * daily return:
                r = holding * (normed.ix[j] / normed.ix[j-1] - 1)
                if action == NOTHING and holding == NOTHING:
                    r = -0.5 # Punish idleness!

                action = self.learner.query(state, r)

            if self.verbose:
                if holding == ALLOWED_LOT:
                    portval += ALLOWED_LOT * prices.ix[-1]
                elif holding == -ALLOWED_LOT:
                    portval -= ALLOWED_LOT * prices.ix[-1]
                print('episode: {0}, portval: {1}'.format(i, portval[0]))


    def test_policy(self, symbol = "IBM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,1,1), sv = 10000):
        """ Use existing policy to test against out of sample data. 
            Return generated orders as list of pairs (ORDER, date).
            Used later to generate a csv file and test it using marketsim from mc2_p1
        """

        if not self.learner:
            raise UnboundLocalError('Train learner before testing.')

        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        prices = prices_all[[symbol,]]  # only portfolio symbols

        normed, ac_sma, b_val = get_all_stats(prices)
        discretized = discretize_all(ac_sma, b_val, 10, symbol)

        # Clear the first N prices to align dates with discretized, and stringify dates.
        dates = prices[TIME_FRAME-1:].index.map(lambda x: x.strftime('%Y-%m-%d')) 
        orders = []

        state = int(str(discretized.ix[0].values[0]) + str(discretized.ix[0].values[1]) + str(0))
        action = self.learner.querysetstate(state)
        holding = NOTHING

        for i in range(1, len(discretized)):
            state = str(discretized.ix[i].values[0]) + str(discretized.ix[i].values[1]) #partial state

            if action == BUY and holding != ALLOWED_LOT:
                state = int(state + str(BUY))
                holding += ALLOWED_LOT
                orders.append(['BUY', dates[i-1]])

            elif action == SELL and holding != -ALLOWED_LOT:
                state = int(state + str(SELL))
                holding += -ALLOWED_LOT
                orders.append(['SELL', dates[i-1]])

            else:
                state = int(state + str(NOTHING))

            r = holding * (normed.ix[i] / normed.ix[i-1] - 1)
            if action == NOTHING and holding == NOTHING:
                r = -0.5 # Punish idleness!
            action = self.learner.query(state, r)

        return orders


if __name__ == "__main__":
    """ Test basic functionality. """
    sl = StrategyLearner(verbose=True)
    discretized, normed, prices = sl.add_evidence()
    sl.train_learner(discretized, normed, prices)

orders = sl.test_policy()

