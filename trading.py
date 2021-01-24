import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import quandl
import datetime

def stock(symbol, start, end):
    print("getting data")
    try:
        stock = quandl.get("WIKI/" + symbol, start_date=start + "-1-1", end_date=end +"-12-31")
        # stock = pd.read_csv("data/AAPL.csv", header=0, index_col="Date", parse_dates=True)
    except:
        print("Please enter a stock symbol, or check if a correct year was entered")

    # Incase data wants to be saved
    # stock.to_csv("data/"+symbol+".csv")
    # df = pd.read_csv("data/"+symbol+".csv", header=0, index_col="Date", parse_dates=True)

    # Difference will be important in teaching algorthim how to buy and sell
    stock['diff'] = stock.Open - stock.Close

    # Trading strategy
    # making a short and long moving average
    shortWindow = 40
    longWindow = 100

    signals = pd.DataFrame(index=stock.index)
    signals['signal'] = 0.0

    signals['short_mavg'] = stock['Close'].rolling(window=shortWindow, min_periods=1, center=False).mean()

    signals['long_mavg'] = stock['Close'].rolling(window=longWindow, min_periods=1, center=False).mean()

    signals['signal'][shortWindow:] = np.where(signals['short_mavg'][shortWindow:] > signals['long_mavg'][shortWindow:], 1.0, 0.0)

    signals['positions'] = signals['signal'].diff()

    fig = plt.figure()

    plt.title("Buy/Sell Strategy: " + symbol)

    axs = fig.add_subplot(111, ylabel='Price($)')

    stock['Close'].plot(ax=axs, color='r', lw=2.)

    signals[['short_mavg', 'long_mavg']].plot(ax=axs, lw=2.)

    # Plotting buy markers
    axs.plot(signals.loc[signals.positions == 1.0].index, signals.short_mavg[signals.positions == 1.0], '^', markersize=10, color='#87FF2A')

    # Plotting sell markers
    axs.plot(signals.loc[signals.positions == -1.0].index, signals.short_mavg[signals.positions == -1.0], 'v', markersize=10, color='#00CCCC')

    plt.show()


symbolInput = input("What stock symbol would you like to analyze?").upper()
start_date = input("What year would you like to start at?")
end_date = input("What year would you like to end?")

while(end_date < start_date):
    print("please make sure the end year is greater than or equal to the start year")
    end_date = input("What year would you like to end?")

stock(symbolInput, start_date, end_date)
