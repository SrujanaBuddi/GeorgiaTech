"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch
"""
import numpy as np

class RTLearner(object):

    def build_tree(self, dataX, dataY, node):
        if dataX.shape[0] == 0:
            return []
        elif dataX.shape[0] <= self.leaf_size:
	    if dataY.mean() <= -0.078:
		y=-1
	    elif dataY.mean() >= -0.088:
		y = 1
	    else:
		y=0	
            return [[node, -1, y, -1, -1]]
        elif np.std(dataY) == 0: 
            return [[node, -1, dataY[0], -1, -1]]
        else:
            while (True):
                feature = np.random.choice(dataX.shape[1])
                rand = np.random.choice(dataX[:, feature], size = 2, replace = False)
                if (rand[0] != rand[1]): 
                    break
            split_val = rand.mean()
            left_div = dataX[:,feature]<=split_val
            right_div = dataX[:,feature]>split_val
            if(np.any(left_div) and np.any(right_div)):
                left_tree = self.build_tree(dataX[left_div], dataY[left_div], node + 1) 
                right_tree = self.build_tree(dataX[right_div], dataY[right_div], node + len(left_tree) + 1) 
                root = [[node, feature, split_val, 1, len(left_tree) + 1]]
            else:
                root = [[node, -1, dataY.mean(), -1, -1]]
                left_tree = right_tree = []
            return root + left_tree + right_tree

    def __init__(self, leaf_size = 5, verbose = False):
        self.leaf_size = leaf_size # move along, these aren't the drones you're looking for
        self.verbose = verbose
        
    def addEvidence(self,dataX,dataY):
        # build and save the model
        self.tree = self.build_tree(dataX, dataY, 0)
        
    def query(self,points):
        output = np.zeros(points.shape[0])
        for idx,row in enumerate(points):
            curr = self.tree[0]
            while(curr[1] != -1):
                if(row[curr[1]] <= curr[2]):
                    curr = self.tree[curr[3]+curr[0]]
                else:
                    curr = self.tree[curr[4]+curr[0]]
            output[idx] = curr[2]
        return output

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
