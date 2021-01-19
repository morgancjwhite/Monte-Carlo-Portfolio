"""

This module has wieght generating functions

Recur provides a recurisve solution to produce all iterations of weights
i.e weightLength 2 with a weightMax of 2 has [1, 1], [2, 1], [1, 2], [2, 2]

Also want to try randomly generated weights, specifed with arguement  

"""


#==========================
# Imports
import numpy as np


#=======================
"""
This recursive solution to the iterative weight generation checks to see if
the current element in the weight list has reached the given max, and increments
the element counter if so, and decrements after adding 1 to the next element.

Repeat ad infinitum
"""
def Recur(weights, i, maximum):
    if weights[i] == maximum+1:
        i+=1
        weights[i]+=1
        Recur(weights, i, maximum)
        i-=1
        weights[i]=1


#==========================
"""
Generate weights for portfolio (ratio)

if method == iterate, go through every single weight in a binary fashion as in
module header

weightLen is len(tickers)
weightMax is highest number to simulate
marketData is df from yfinance
func is the function that you want to apply to each weight
method specifies form of weight generation
"""
def GenerateWeights(weightMax, weightLen, marketData, func, method):
    
    if method == 'iterate':
        weights = [1] * weightLen
        i=0
        count = 0
        portPerfor = np.empty([marketData.shape[0], 0]).T
        portReturn = np.zeros(0)
        riskHist = np.zeros(0)
        bestSoFar = [0,0,0]
        while True:
            
            # Progress counter
            if count % 8000 == 0:
                print(str(round(count / (weightMax**(weightLen) - 1 )* 100, 2)) + '%')
            
            # Do thing
            [portPerfor, portReturn, bestSoFar, riskHist] = func(weights, marketData, portPerfor, portReturn, count, bestSoFar, riskHist)
            #
            
            # After all weights have been generated (3, 3, 3, 3) eg
            if sum(weights) == len(weights) * weightMax:
                break
            
            # i is counter from left side, so increment 1st element, then
            # check to see if it has reached weightMax using recursive function
            weights[i] += 1
            Recur(weights, i, weightMax)
            count +=1
        print('Total number of iterations was', count)
        return [portPerfor, portReturn, bestSoFar, riskHist]
    
    # To be added
    elif method=='monte carlo':
        return None













