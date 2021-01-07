# Main

"""

The aim of this project is to compare holding ratios for a potential portfolio

Want to specify a group of tickers, and Monte Carlo different weights in
portfolio and compare strategies

Option to fix weighting of portfolio

"""




# Imports
import pandas as pd
import PortfolioSim as ps
import matplotlib.pyplot as plt
import numpy as np

tickers = ['ENPH', 'PLUG', 'FSLR', 'SEDG',
           'AFC', 'RUN', 'TANH', 'HASI']

# Also look at INRG (ICLN), PLL


# Enter tickers required here and 
tickerData = pd.DataFrame({
    'Ticker':tickers,
    'Weight':[1] * len(tickers),
    'Vary':[True] * len(tickers)
    })

##############
[period, interval] = ['1mo','1d']
marketData = ps.DownloadFinanceData(tickers, 
                                    period=period, interval=interval)['Close']




[portPerfor, portReturn, bestSoFar, riskHist] = ps.MonteCarlo(tickers, marketData, True)


portHistory = pd.DataFrame({
    'Return History': portReturn,
    'Risk History': riskHist
    })

portHistory.to_csv("portHistory.csv")

optimalPortfolio = ps.returnPercentages(bestSoFar, tickers)
ps.printPortfolio(optimalPortfolio, bestSoFar, period, interval, portPerfor)

plt.scatter(riskHist, portReturn, color = 'b', marker='x')
plt.plot(riskHist[bestSoFar[1]], bestSoFar[0], 'ro') 

    

#ps.MonteCarlo([1, 2, 3])














