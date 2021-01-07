"""

This module has wieght generating functions

Recur provides a recurisve solution to produce all iterations of weights
i.e weightLength 2 with a weightMax of 2 has [1, 1], [2, 1], [1, 2], [2, 2]

Also want to try randomly generated weights, specifed with arguement  

"""

import numpy as np
#=======================

def Recur(weights, i, maximum):
    if weights[i] == maximum+1:
        i+=1
        weights[i]+=1
        Recur(weights, i, maximum)
        i-=1
        weights[i]=1



def GenerateWeights(weightMax, weightLen, marketData, func, method):
    # weightLen is len(tickers)
    # weightMax is highest number to simulate
    # marketData is df from yfinance
    # func is the function that you want to apply to each weight
    # method specifies form of weight generation
    
    
    if method == 'iterate':
        weights = [1] * weightLen
        i=0
        count = 0
        portPerfor = np.empty([marketData.shape[0], 0]).T
        portReturn = np.zeros(0)
        riskHist = np.zeros(0)
        bestSoFar = [0,0,0]
        while True:
            
            #### Do thing
            if count % 8000 == 0:
                print(str(round(count / (weightMax**(weightLen) - 1 )* 100, 2)) + '%')
            
            [portPerfor, portReturn, bestSoFar, riskHist] = func(weights, marketData, portPerfor, portReturn, count, bestSoFar, riskHist)
            ###
            if sum(weights) == len(weights) * weightMax:
                break
            weights[i] += 1
            Recur(weights, i, weightMax)
            count +=1
        print('Total number of iterations was', count)
        return [portPerfor, portReturn, bestSoFar, riskHist]
    
    elif method=='random':
        return None













