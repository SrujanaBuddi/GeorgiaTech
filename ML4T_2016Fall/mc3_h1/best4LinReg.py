import numpy as np
import random
import matplotlib.pyplot as plt

def polyFun(coefs = [1,2,3], x = 1):
    y = 0.0
    for i in range(0, len(coefs)):
        y += coefs[i] * (x**i)
    return y

def genLinData(elements = 1000):
    data = np.empty([elements,3])
    for x in range(0, elements):
        x1 = x2 = x * 100 
        y = polyFun([3,5],x1)  + random.randint(0,100) / 100.0
        data[x, :] = [x1, x2, y]

    np.random.shuffle(data)
    np.savetxt('./Data/best4linreg.csv', data, delimiter=',')

if __name__=='__main__':
genLinData()
