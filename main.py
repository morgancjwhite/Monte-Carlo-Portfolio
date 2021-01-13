# Main
"""

The aim of this project is to compare holding ratios for a potential portfolio

Want to specify a group of tickers, and Monte Carlo different weights in
portfolio and compare strategies

Option to fix weighting of portfolio

"""

#==========================
# Imports
import PortfolioSim as ps
import matplotlib.pyplot as plt


#==========================
# What tickers do we want to look at

tickers = ['TSLA', 'UBER', 'APPL']



#==========================
"""
What timescale and granularity do we want to look over
 Download market data for defined tickers within this period
"""
[period, interval] = ['1mo','1d']

marketData = ps.DownloadFinanceData(tickers, 
                                    period=period, interval=interval)['Close']


#==========================
"""
This calls the simulation function that measures the best portfolio possible
using a given metric (Sharpes for now)

Takes a list of tickers, df of market data and an isGenData bool as arguments.
If isGenData True, goes through the whole simulation again and saves output,
if False, loads previous simulation to save computation time
"""
[portPerfor, portReturn, bestSoFar, riskHist] = ps.SimulatePortfolio(tickers, 
                                                              marketData, True)


#==========================
"""
Extract percentage breakdown of potfoilio using calcualted optimal ratio

Print financial properties of portfolio, alpha, beta, etc
"""
optimalPortfolio = ps.returnPercentages(bestSoFar, tickers)
ps.printPortfolio(optimalPortfolio, bestSoFar, period, interval, portPerfor)


# Quick and easy plot of return against risk
plt.scatter(riskHist, portReturn, color = 'b', marker='x')
plt.plot(riskHist[bestSoFar[1]], bestSoFar[0], 'ro') 

    














