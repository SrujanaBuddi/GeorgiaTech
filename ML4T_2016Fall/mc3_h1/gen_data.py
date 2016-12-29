"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regresstion than random trees

def best4LinReg():
    X = np.random.normal(size = (100, 4))
    Y = 1 * X[:,0] + 2 * X[:,1] + 3 * X[:,2]+ 4*X[:,3]
    return X, Y

def best4RT():
   # X =np.random.normal(size=(100, 3))
    X=np.zeros(shape=(1000,2))
    X[:,0]=np.linspace(-math.pi,math.pi,1000)
    X[:,1]=np.linspace(-math.pi,math.pi,1000)
    Y=np.cos(X[:,0])+np.sin(X[:,1])
    #Y =X[:,0]*(1- X[:,1]**2)#+(5-X[:,0])**3#+2.0 *X[:,2]+X[:,3]
    return X, Y

if __name__=="__main__":
    print "they call me Tim."
