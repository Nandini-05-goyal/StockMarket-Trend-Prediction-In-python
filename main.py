import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#load the data
tcs = pd.read_csv('tcs.csv')
#print(tcs['Volume'])
#visualize the data
#plt.figure(figsize=(12.5,5.5))
#plt.plot(tcs['Close'], label='TCS Historical Price')
#plt.plot(tcs['Adj Close'], label='Volume of shares traded')
#plt.title('TCS Close Price Chart')
#plt.xlabel('12 Aug, 2002 - 5 May, 2021')
#plt.ylabel('Close price in rupees')
#plt.legend(loc='upper left')
#plt.show()

#create the simple moving average with a 30 days window
SMA30 = pd.DataFrame()
SMA30['Close'] = tcs['Close'].rolling(window=30).mean()
SMA100 = pd.DataFrame()
SMA100['Close'] = tcs['Close'].rolling(window=100).mean()

#visualize the SMA30, SMA100 and TCS close price
#plt.figure(figsize=(12.5,5.5))
#plt.plot(tcs['Close'], label='TCS Close Price')
#plt.plot(SMA30['Close'], label='SMA30')
#plt.plot(SMA100['Close'], label='SMA100')
#plt.title('Coparision of TCS SMA30, SMA100 and Close Price')
#plt.xlabel('12 Aug, 2002 - 5 May, 2021')
#plt.ylabel('Close Price')
#plt.legend(loc='upper left')
#plt.show()

#create a new data frame to store all the Data
data = pd.DataFrame()
data['TCS'] = tcs['Close']
data['SMA30'] = SMA30['Close']
data['SMA100'] = SMA100['Close']
#print(data)
#create a func to signal when to buy and sell the stock
def buy_sell(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

    for i in range(len(data)):
        if data['SMA30'][i] > data['SMA100'][i]:
            if flag != 1:
                sigPriceBuy.append(data['TCS'][i])
                sigPriceSell.append(np.nan)
                flag=1;
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif data['SMA30'][i] < data['SMA100'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['TCS'][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return  (sigPriceBuy, sigPriceSell)


#store the buy and sell data into a variable
buy_sell_data = buy_sell(data)
data['Buy_Signal_Price'] = buy_sell_data[0]
data['Sell_Signal_Price'] = buy_sell_data[1]
#print(data)

#visualize the data and market trend of buy and sell
plt.figure(figsize=(12.5,5.5))
plt.plot(data['TCS'], label='TCS Close Price', alpha=0.5)
plt.plot(data['SMA30'], label ='SMA30', alpha=0.5)
plt.plot(data['SMA100'], label ='SMA100', alpha=0.5)
plt.scatter(data.index, data['Buy_Signal_Price'], label = 'Buy', marker = '^', color='green')
plt.scatter(data.index, data['Sell_Signal_Price'], label = 'Sell', marker = 'v', color='red')
plt.title('TCS Close price history of buy and sell')
plt.xlabel('12 Aug, 2002 - 5 May, 2021')
plt.ylabel('Close Price')
plt.legend(loc='upper left')
plt.show()
