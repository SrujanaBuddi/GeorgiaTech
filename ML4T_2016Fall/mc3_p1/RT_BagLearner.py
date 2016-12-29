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
	
	if self.boost==False:	
		def addEvidence(self,Xtrain,Ytrain):
			self.Xtrain=Xtrain
			self.Ytrain=Ytrain
			bag_size=self.Xtrain.shape[0]/self.bags
			xb_train=np.zeros((bag_size,self.Xtrain.shape[1]))
			yb_train=np.zeros((bag_size,1))
			learner=[]
			for i in range(0,bags):
				idx= rand.sample(range(0,self.Xtrain.shape[0]),bag_size)
				for j in (0,bag_size):
					k=idx[j]
					xb_train[j,:]=self.Xtrain[k,:]
					yb_train[j,:]=self.Ytrain[k,:]
			learner[i]=lr.LinRegLearner(verbose = True) 
			learner[i].addEvidence(xb_train,yb_train)
	
	if self.boost==True:	
		def addEvidence(self,Xtrain,Ytrain):
			self.Xtrain=Xtrain
			self.Ytrain=Ytrain
			bag_size=self.Xtrain.shape[0]/self.bags
			learner=[]
			err_pos=[]
			xb_train=np.zeros((bag_size,self.Xtrain.shape[1]))
			yb_train=np.zeros((bag_size,1))
			xbb_train=np.zeros((bag_size+len(err_pos),self.Xtrain.shape[1]))
			ybb_train=np.zeros((bag_size+len(err_pos),1))
			xbb_train=xb_train
			ybb_train=yb_train
			for i in range(0,bags):
				idx= rand.sample(range(0,self.Xtrain.shape[0]),bag_size)
				for j in (0,bag_size):
					k=idx[j]
					xb_train[j,:]=self.Xtrain[k,:]
					yb_train[j,:]=self.Ytrain[k,:]
				if len(err_pos)>0:
					for i in range (0,len(err_pos)):
						k=err_pos[i];
						xbb_train.append(self.Xtrain[k,:])
						ybb_train.append(self.Ytrain[k,:])	
				learner[i]=lr.LinRegLearner(verbose = True) 
				learner[i].addEvidence(xbb_train,ybb_train)
				predY=learner[i].query(self.Xtrain)
				#ids where error is very high
				error=np.zeros(predY.shape[0],1)
				error[:,]=self.Ytrain[:,]-predY[:,]
				mean_error=np.mean(error)
				for i in range(0,error.shape[0]):
					if error[i]>mean_error:
						err_pos.append(i)
				
	def query(self,Xtest):
		for i in range (0,bags):
        		fmodel_coefs=fmodel_coefs+learner[i].model_coefs
		fmodel_coefs=fmodel_coefs/self.bags
		return (self.fmodel_coefs[:-1] * Xtest).sum(axis = 1) + self.fmodel_coefs[-1]
			
