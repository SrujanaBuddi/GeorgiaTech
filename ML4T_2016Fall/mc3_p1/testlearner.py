"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import LinRegLearner as lrl
import sys
import matplotlib as plt
import csv

if __name__=="__main__":
    if len(sys.argv) != 2:
        print "Usage: python -m mc3_p1.testlearner <filename>"
        sys.exit(1)
    inf = open(sys.argv[1])
    data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

    # compute how much of the data is training and testing
    train_rows = math.floor(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]

    print testX.shape
    print testY.shape

    # create a learner and train it
    learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner
    learner.addEvidence(trainX, trainY) # train it

    # evaluate in sample
    predY = learner.query(trainX) # get the predictions
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    print
    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0,1]

    # evaluate out of sample
    predY = learner.query(testX) # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0,1]


#RT learner
    import RTLearner as rt
    rmse_in=np.zeros(50)
    corr_in=np.zeros(50)
    rmse=np.zeros(50)
    corr=np.zeros(50)
    for i in range(0,50):
    	learner = rt.RTLearner(leaf_size = i, verbose = False) # constructor
    	learner.addEvidence(trainX, trainY) # training step
    	predY=learner.query(trainX)
    	rmse_in[i] = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    	#print
    	#print "In sample results for RT Learner"
    	#print "RMSE: ", rmse
    	c = np.corrcoef(predY, y=trainY)
	corr_in[i]=c[0,1]
    	#print "corr: ", c[0,1]

	predY = learner.query(testX) # query
    	rmse[i] = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    	#print "Out of sample results for RT Learner"
    	#print "RMSE: ", rmse
    	c = np.corrcoef(predY, y=testY)
	corr[i]=c[0,1]
    	#print "corr: ", c[0,1]
	#print rmse_in[i],rmse[i],corr_in[i],corr[i]
    #print "insample"
    #print rmse_in,corr_in
    #print "outsample"
    #print rmse,corr   

#bag learner for RT learner
    '''for i in range(1,50):
    	import BagLearner as bl
    	bllearner = bl.BagLearner(learner = rt.RTLearner, kwargs = {"leaf_size":i}, bags =20, boost = False, verbose = False)
    	bllearner.addEvidence(trainX, trainY)
    
    	predY=bllearner.query(trainX)
    	rmse_in[i] = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    	#print
    	#print "In sample results for bag Learner"
    	#print "RMSE: ", rmse
    	c = np.corrcoef(predY, y=trainY)
	corr_in[i]=c[0,1]
    	#print "corr: ", c[0,1]

    	predY = bllearner.query(testX)
    	rmse[i] = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    	#print
    	#print "Out of sample results for bag learner"
    	#print "RMSE: ", rmse
    	c = np.corrcoef(predY, y=testY)
	corr[i]=c[0,1]
	print rmse_in[i],rmse[i]
    	#print "corr: ", c[0,1]'''
#implementing boosting

    import BagLearner as bl
    bllearner1 = bl.BagLearner(learner = rt.RTLearner, kwargs = {"leaf_size":1}, bags =20, boost = False, verbose = False)
    bllearner1.addEvidence(trainX, trainY)
    predY1=bllearner1.query(trainX)
    rmse1 = math.sqrt(((trainY - predY1) ** 2).sum()/trainY.shape[0])
    c = np.corrcoef(predY1, y=trainY)
    corr1=c[0,1]
    bllearner2 = bl.BagLearner(learner = rt.RTLearner, kwargs = {"leaf_size":1}, bags =20, boost = True, verbose = False)
    bllearner2.addEvidence(trainX, trainY)
    predY2 = bllearner2.query(testX)
    rmse2 = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    c = np.corrcoef(predY, y=testY)
    corr2=c[0,1]
    #print rmse_in[i],rmse[i]
    print rmse1,rmse2,corr1,corr2
    #print rmse1,corr1

