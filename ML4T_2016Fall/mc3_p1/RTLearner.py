__author__="sbuddi3"

import numpy as np
import random
from random import shuffle
import pdb

class RTLearner(object):
		
	def __init__(self,leaf_size,verbose=False):
		self.leaf_size=leaf_size
		self.verbose=verbose
		pass

	def build_tree(self,dataX,dataY,node):
		count=0
		if dataX.shape[0]==0:
			return []
		elif dataX.shape[0]<=self.leaf_size:
			return [[node,-1,dataY.mean(),'NA','NA']]
		for i in range (0,dataY.shape[0]):
			if dataY[0]==dataY[i]:
				count+=1
		if count==dataY.shape[0]:
			return[[node,-1,dataY.mean(),'NA','NA']]
		else:
			no_fun=dataX.shape[1]#no of functions
			#x=[[i] for i in range(no_fun)]
			#shuffle(x)
			s_rand1=0
			s_rand2=0
			while s_rand1==s_rand2:
				split_function=random.randint(0,no_fun-1)
				rand_val1=random.randint(0,dataX.shape[0]-1)
				rand_val2=random.randint(0,dataX.shape[0]-1)
				s_rand1=dataX[rand_val1,split_function]
				s_rand2=dataX[rand_val2,split_function]
			split_value=(s_rand1+s_rand2)/2.0
			Xleft=dataX[dataX[:,split_function]<split_value]
			Yleft=dataY[dataX[:,split_function]<split_value]
			Xright=dataX[dataX[:,split_function]>=split_value]
			Yright=dataY[dataX[:,split_function]>=split_value]
			lefttree= self.build_tree(Xleft,Yleft,node+1)
			righttree=self.build_tree(Xright,Yright,node+len(lefttree)+1)
			root=[[node,split_function,split_value,1,len(lefttree)+1]]
			return (root+lefttree+righttree)


	def addEvidence(self,Xtrain,Ytrain):
		self.Xtrain=Xtrain
		self.Ytrain=Ytrain
		init_node=0
		self.tree=self.build_tree(Xtrain,Ytrain,init_node)
		#print tree[0]
					
	def query(self,datatest):
		predY=np.zeros(datatest.shape[0])
		for i in range(0,datatest.shape[0]):
			level= self.tree[0]
			while level[1]!=-1:
				#pdb.set_trace()
				if (datatest[i,level[1]]<=level[2]):
					level=self.tree[level[0]+level[3]]
				else:
					level=self.tree[level[0]+level[4]]
				#print level[1]
				#print i,level,values[level[1]],level[2]
			#print i,level
			predY[i]=level[2]
		return predY
			

