"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as spo 
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    sv = 1000000
    rfr=0.0
    sf=252.0

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    allocs = find_optimal_allocations(prices) # add code here to find the allocations

    # Get daily portfolio value
    port_val = get_portfolio_value(prices, allocs, sv)

    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr, adr, sddr, sr = get_portfolio_stats(port_val, rfr, sf)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_normalized_data(df_temp, "Daily portfolio value and SPY", "Date", "Normalized price")
        pass

    return allocs, cr, adr, sddr, sr

def find_optimal_allocations(prices):
    bnds = ((0.0, 1.0),(0.0, 1.0),(0.0, 1.0),(0.0, 1.0))    
    cons = ({'type': 'eq', 'fun': lambda x:  1 - sum(x)}) #one minus the sum of all variables must be zero
    Xguess = (0.2, 0.2, 0.3, 0.3)
    min_result = spo.minimize(f, Xguess, prices, method = 'SLSQP', bounds=bnds, constraints=cons)
    return min_result.x

# return negative sharpe ratio 
def f(X, prices): #pass allocs
    sv = 100000
    rfr=0.0
    sf=252.0
    port_val = get_portfolio_value(prices, X, sv)
    daily_rets = compute_daily_returns(port_val)
    daily_rets = daily_rets[1:]
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sr = 252**(1.0/2) * (adr - rfr) / sddr
    return -sr 

def get_portfolio_value(prices, allocs, start_val):
    # Plot adjusted closing prices for the 4 equities
    #plot_data(prices)
    # Normalize the prices according to the first day. The first row for each stock should have a value of 1.0 at this point
    normal_prices = normalize_data(prices)
    # Multiply each column by the allocation to the corresponding equity.
    normal_allocs_prices = normal_prices * allocs
    # Multiply these normalized allocations by starting value of overall portfolio, to get position values
    adj_position_prices = normal_allocs_prices * start_val
    #Sum each row (i.e. all position values for each day). That is your daily portfolio value.
    daily_port_value = adj_position_prices.sum(axis=1)
    return daily_port_value

def get_portfolio_stats(port_val, daily_rf, samples_per_year):
    daily_rets = compute_daily_returns(port_val)
    daily_rets = daily_rets[1:]
    cr = (port_val[-1] / port_val[0]) - 1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sr = 252**(1.0/2) * (adr - daily_rf) / sddr
    return cr, adr, sddr, sr

def plot_normalized_data(df, title, xlabel, ylabel):
    normalized_df = normalize_data(df);
    ax = normalized_df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    daily_returns = (df / df.shift(1)) -1
    daily_returns.ix[0] = 0  # Note: Returned DataFrame must have the same number of rows
    return daily_returns

def normalize_data(df):
    return df/ df.ix[0,:]

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date, syms = symbols, gen_plot = True)

    # Print statistics
    print ("Start Date:", start_date)
    print ("End Date:", end_date)
    print ("Symbols:", symbols)
    print ("Optimal allocations:", allocations)
    print ("Sharpe Ratio:", sr)
    print ("Volatility (stdev of daily returns):", sddr)
    print ("Average Daily Return:", adr)
    print ("Cumulative Return:", cr)

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
