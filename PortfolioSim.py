"""

This module simulates differing weights for holding
in a portfolio

Try weights from 1-5 for all unfixed holders

"""

import yfinance as yf
import WeightGen
import numpy as np
import pickle
import pandas as pd


def DownloadFinanceData(tickers, period, interval):
    data = yf.download(tickers=tickers, period=period, interval=interval)
    return data


def ret(priceArray):
    retVal = 100 * (priceArray[-1] - priceArray[0]) / priceArray[0]
    return retVal


def CalculateOptimalPortConfig(weights, marketData, portPerfor, portReturn, count, bestSoFar, riskHist):
    values = marketData * weights
    
    values['Total'] = values.sum(axis=1)
    totalArr = values['Total'].values
    
    portPerfor = np.vstack((portPerfor, totalArr))
    
    # define risk as std of performance
    portRisk = np.std(portPerfor[-1])
    riskHist = np.append(riskHist, portRisk / portPerfor[-1,-1])
    
    currentRet = ret(totalArr)
    portReturn = np.append(portReturn, currentRet)
    
   # if (currentRet)**(2) / portRisk > bestSoFar[0]:    
    if (currentRet - 0.05) / portRisk > bestSoFar[0]:
        bestWeight = weights.copy()
        bestSoFar = [currentRet, count, bestWeight]    
    
    return [portPerfor, portReturn, bestSoFar, riskHist]


def returnPercentages(bestSoFar, tickers):
    sumOfWeights = sum(bestSoFar[2])
    piece = 100 / sumOfWeights
    perce = np.array(bestSoFar[2]) * piece
    optimal = np.vstack((tickers, perce))
    
    return optimal


def printPortfolio(optimal, bestSoFar, period, interval, portPerfor):
    spyData = yf.download('SPY', period=period, interval=interval)['Close']
    spyRet = ret(spyData.values)
    normSpy = spyData.values / np.mean(spyData)
    normPort = portPerfor[:, bestSoFar[1]] / np.mean(portPerfor[:, bestSoFar[1]])
    
    #
    #beta = (np.cov(normPort, normSpy) / np.var(normSpy))[1, 0]
    beta = 1.7
    alpha = bestSoFar[0] - 0.05 - (beta * (spyRet - 0.05))
    
    print('===============')
    
    # Prints percentages against ticker
    for i in range(len(optimal[0])):
        print(optimal[0,i] + ':', str(round(float(optimal[1, i]), 2))+ '%')
    
    print('=============== Info ===============')
    print(f'Return = {str(round(bestSoFar[0], 2))}% ({period})')
    print(f'Alpha = {alpha}')
    print(f'Beta = {beta}')
    



def MonteCarlo(tickers, marketData, isGenData):
    
    if isGenData:
        
        [portPerfor, portReturn, bestSoFar, riskHist] = WeightGen.GenerateWeights(weightMax=4,
        weightLen=len(tickers), marketData=marketData, 
        func=CalculateOptimalPortConfig, method='iterate')
        
        
        portHistory = pd.DataFrame({
        'Return History': portReturn,
        'Risk History': riskHist
        })
        portHistory.to_csv("portHistory.csv")

        pickle.dump(portPerfor, open("portPerfor.p", "wb"))
        pickle.dump(bestSoFar, open("bestSoFar.p", "wb"))
        
        return [portPerfor.T, portReturn, bestSoFar, riskHist]
    
    
    else:
        bestSoFar = pickle.load(open("bestSoFar.p","rb"))
        portPerfor = pickle.load(open("portPerfor.p","rb"))

        portHistory = pd.read_csv("portHistory.csv")
        portReturn = portHistory['Return History'].values
        riskHist = portHistory['Risk History'].values
            
    return [portPerfor.T, portReturn, bestSoFar, riskHist]
    
    
#MonteCarlo([1, 2, 3, 4])


            
        
    


