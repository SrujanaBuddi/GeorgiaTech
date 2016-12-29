__author__='sbuddi3'

import numpy as np
import LinRegLearner as lr
import random as rand

class BagLearner(object):
	
	def __init__(self,learner,kwargs,bags,boost,verbose):
		self.learner=learner
		self.kwargs=kwargs
		self.bags=bags
		self.boost=boost
		self.verbose=verbose
	
	def addEvidence(self,Xtrain,Ytrain):
		bag_size=int(Xtrain.shape[0]*0.6)
		self.learners=[]
		for i in range(0,self.bags):
                        if self.boost==True and i>1:
                                predY=self.learners[i-1].query(Xtrain)
                                err=abs(Ytrain-predY)
                                sumerr=sum(err)
                                err=err/sumerr
                                idx=np.random.choice(Xtrain.shape[0],size=bag_size,p=err)
			else:
				idx= rand.sample(range(0,Xtrain.shape[0]),bag_size)		
			self.learners.append(self.learner(**self.kwargs))
			self.learners[i].addEvidence(Xtrain[idx,:],Ytrain[idx])
				
	def query(self,Xtest):
		res=np.zeros((Xtest.shape[0],self.bags))
		predY=np.zeros(Xtest.shape[0])
		for i in range (0,self.bags):
        		res[:,i]=self.learners[i].query(Xtest)
		#predY=np.mean(res,axis=1)
		#print predY.shape[0]
		return np.mean(res,axis=1)
			
