import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
plt.style.use('seaborn-colorblind')  

def portfolio_annualized_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns*weights ) *252
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return std, returns

def generate_random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate):
    results = np.zeros((3,num_portfolios))
    weight_array = []
    for i in range(num_portfolios):
        weights = np.random.random(4)
        weights /= np.sum(weights)
        weight_array.append(weights)
        portfolio_std_dev, portfolio_return = portfolio_annualized_performance(weights, mean_returns, cov_matrix)
        results[0,i] = portfolio_std_dev
        results[1,i] = portfolio_return
        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return results, weight_array

def simulated_portfolios(mean_returns, cov_matrix, num_portfolios, risk_free_rate):
    results, weights = generate_random_portfolios(num_portfolios,mean_returns, cov_matrix, risk_free_rate)
    max_sharpe_idx = np.argmax(results[2])
    stdev_portfolio, returns_portfolio = results[0,max_sharpe_idx], results[1,max_sharpe_idx]
    max_sharpe_allocation = pd.DataFrame(weights[max_sharpe_idx],index=data.columns,columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i*100,2)for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T
    print("-"*100)
    print("PORTFOLIO OVERVIEW\n")
    print(f"Annualized Return: {(round(returns_portfolio,2)*100)}%")
    print(f"Annualized Volatility: {(round(stdev_portfolio,2)*100)}%")
    print(max_sharpe_allocation)
    print("-"*100)
    plt.figure(figsize=(16, 9))
    plt.scatter(results[0,:],results[1,:],c=results[2,:], cmap='winter', marker='o', s=10, alpha=0.3)
    plt.colorbar()
    plt.scatter(stdev_portfolio, returns_portfolio, marker='o',color='g',s=100, label='Optimal Sharpe ratio')
    plt.title(f'EFFICIENT FRONTIER SIMULATION')
    plt.xlabel('ANNUALIZED VOLATILITY')
    plt.ylabel('ANNUALIZED RETURNS')
    plt.legend(labelspacing=1.2)

    f = open("DATA/portfolio_data.txt", "a")
    f.write(f"PORTFOLIO OVERVIEW, {dt.date.today()}\n")
    f.write(f"Annualized Return: {(round(returns_portfolio,2)*100)}% \n")
    f.write(f"Annualized Volatility: {(round(stdev_portfolio,2)*100)}% \n")
    f.close()
    plt.savefig('DATA/efficient_frontier_simulation.png')
    plt.show()

def ticker_counter():
    tickers = []
    num_ticks = input('NUMBER OF ASSETS: ')
    for i in list(range(int(num_ticks))):
        ticker_ = ''
        ticker_= input(f'ASSET: {i+1}: ')
        tickers.append(ticker_)
    return tickers


if __name__ == '__main__':
    tickers = ticker_counter()
    data = pdr.get_data_yahoo(tickers, start="2018-01-01", end=dt.date.today())['Close']
    returns = data.pct_change()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    number_portfolios = 10000
    risk_free_r = 0.018
    simulated_portfolios(mean_returns, cov_matrix, number_portfolios, risk_free_r)



