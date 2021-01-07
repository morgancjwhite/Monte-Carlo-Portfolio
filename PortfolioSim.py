"""

This module simulates differing weights for holding
in a portfolio

Try weights from 1-5 for all unfixed holders

"""
#==========================
# Imports
import yfinance as yf
import WeightGen
import numpy as np
import pickle
import pandas as pd


#==========================
"""
This function downloads financial market data in a given period using the
yfinance API
"""
def DownloadFinanceData(tickers, period, interval):
    data = yf.download(tickers=tickers, period=period, interval=interval)
    return data


#==========================
"""
Input: list/array of numbers with recent date at the bottom

Returns percentage difference of value between most recent and furthest dates
"""
def ret(priceArray):
    retVal = 100 * (priceArray[-1] - priceArray[0]) / priceArray[0]
    return retVal


#==========================
"""
This function is called at every generated weight profile.
It maps market data to weights to generate a simulated portfolio and calculates
risk and return for each configuration.

Using Sharpes ratio as a metric, it selects the optimal portfolio and returns
it, also saves all generated portfolios (and their risk/return)
"""
def CalculateOptimalPortConfig(weights, marketData, portPerfor, portReturn, count, bestSoFar, riskHist):
    # map security values to holding ratio
    values = marketData * weights
    
    # sums values horizontally (calculates total portfolio value each day)
    values['Total'] = values.sum(axis=1)
    totalArr = values['Total'].values
    
    # save portfolio performance
    portPerfor = np.vstack((portPerfor, totalArr))
    
    # define risk as std of performance, save as risk history
    portRisk = np.std(portPerfor[-1])
    riskHist = np.append(riskHist, portRisk / portPerfor[-1,-1])
    
    # calculate return over time period, save as port return
    currentRet = ret(totalArr)
    portReturn = np.append(portReturn, currentRet)
    
    # risk free return
    riskFree = 0.05
    
    # this is how we define a 'better' portfolio
    # for now use Sharpes ratio as a metric    
    if (currentRet - riskFree) / portRisk > bestSoFar[0]:
        bestWeight = weights.copy()
        bestSoFar = [currentRet, count, bestWeight]    
    
    return [portPerfor, portReturn, bestSoFar, riskHist]


#==========================
"""
Takes in the best portfolio ratio and converts it to holding percentages and
prints to console
"""
def returnPercentages(bestSoFar, tickers):
    sumOfWeights = sum(bestSoFar[2])
    piece = 100 / sumOfWeights
    perce = np.array(bestSoFar[2]) * piece
    optimal = np.vstack((tickers, perce))
    return optimal


#==========================
"""
Takes in best portfolio configuration and prints return, risk

Also compares to SPY (generalisation of general market) to calculate financial
values such as alpha/beta/etc
"""
def printPortfolio(optimal, bestSoFar, period, interval, portPerfor):
    spyData = yf.download('SPY', period=period, interval=interval)['Close']
    spyRet = ret(spyData.values)
    normSpy = spyData.values / np.mean(spyData)
    normPort = portPerfor[:, bestSoFar[1]] / np.mean(portPerfor[:, bestSoFar[1]])
    
    
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
    


#==========================
"""
Function that simulates specified tickers in a portfolio given market data
Option for new simulation or to use saved output (isGenData)
func in GenerateWeights specifies what operation to perform on each weightset

After simulation, puts return and risk for portfolios in dataframe that is 
saved as a csv. Saves other variables as pickle files

"""
def SimulatePortfolio(tickers, marketData, isGenData):
    
    if isGenData:
        print('Generating weights')
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
        print('Using saved output')
        bestSoFar = pickle.load(open("bestSoFar.p","rb"))
        portPerfor = pickle.load(open("portPerfor.p","rb"))

        portHistory = pd.read_csv("portHistory.csv")
        portReturn = portHistory['Return History'].values
        riskHist = portHistory['Risk History'].values
            
    return [portPerfor.T, portReturn, bestSoFar, riskHist]
    
            
        
    


