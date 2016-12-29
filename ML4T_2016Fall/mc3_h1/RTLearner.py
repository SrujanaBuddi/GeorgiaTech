"""
A FAKE Random Tree Learner.  (c) 2016 Tucker Balch
This is just a linear regression learner implemented named RTLearner so
it is used as a template or placeholder for use by testbest4.  You should
replace this code with your own RTLearner.
"""

import numpy as np

class RTLearner(object):

    def __init__(self, verbose = False, leaf_size = 1):
        pass # move along, these aren't the drones you're looking for

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        # slap on 1s column so linear regression finds a constant term
        newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])
        newdataX[:,0:dataX.shape[1]]=dataX

        # build and save the model
        self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)
        
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        # get the linear result
        ret_val = (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]
        # add some random noise
	ret_val = ret_val + 0.09 * np.random.normal(size = ret_val.shape[0])
	return ret_val

if __name__=="__main__":
    print "get me a shrubbery"
