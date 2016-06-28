# OptimizePortfolio

## Overview
Optimize a portfolio using maximum sharpe ratio in Python

------

## Usage
Input
* A date range to select the historical data to use (specified by a start and end date)
* Symbols for equities (e.g., GOOG, AAPL, GLD, XOM). Note: You should support any symbol in the data directory.

Example Output
    
    Start Date: 2010-01-01 00:00:00
    End Date: 2010-12-31 00:00:00
    Symbols: ['GOOG', 'AAPL', 'GLD', 'XOM']
    Optimal allocations: [  2.43467736e-16   3.96673885e-01   6.03326115e-01   0.00000000e+00]
    Sharpe Ratio: 2.004015013600846
    Volatility (stdev of daily returns): 0.01011645809885585
    Average Daily Return: 0.0012771125936759202
    Cumulative Return: 0.360093798618
