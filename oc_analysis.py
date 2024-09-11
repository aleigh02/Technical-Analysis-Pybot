# open close analysis

import time
import pandas as pd
import datetime as dt
import mplfinance as mpf
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def date_to_time_stamp(year, month, day):
    # convert the date to a time stamp
    return int(time.mktime(dt.datetime(year, month, day, 0, 0).timetuple()))

def signal_func(data):
    num_buys = 0
    fall_count = 0
    rise_count = 0
    buy_list = []
    sell_list = []

    for i in range(0, len(data)):
        # condition for reading candles
        if data['Open'][i] > data['Close'][i]:
            fall_count += 1
            rise_count = 0
        elif data['Open'][i] < data['Close'][i]:
            fall_count = 0
            rise_count +=1
        

        # condition for buy/sell signal
        if fall_count >= 3 and num_buys < 2:
            # buy signal
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            fall_count = 0
            num_buys +=1
        elif rise_count >= 3 and num_buys > 0:
            # sell signal
            buy_list.append(np.nan)
            sell_list.append(data['Close'][i])
            rise_count = 0
            num_buys = 0
        else:
            # no signal for this day
            buy_list.append(np.nan)
            sell_list.append(np.nan)


    return (buy_list, sell_list)
    

start = date_to_time_stamp(2022, 1, 1)

end = int(time.mktime(dt.datetime.now().timetuple()))

ticker = input('\nInput ticker for data retrieval: ')

query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start}&period2={end}&interval=1d&events=history&includeAdjustedClose=true'

# read in the data from yahoo finance
df = pd.read_csv(query_string)
# set the index to the date
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
df['Buy'] = signal_func(df)[0]
df['Sell'] = signal_func(df)[1]
# print(df)

# visually show the candlestick chart
N = 100000000
mpf.plot(df, type='candle', style='yahoo', warn_too_much_data=N)

# visually show the stock buy signals
plt.figure(figsize=(12.2, 4.5))
plt.title('Buy and Sell Plot ' + str({ticker}), fontsize = 18)
plt.plot(df['Close'], label='Close Price', color='blue', alpha=0.4)
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Close Price', fontsize = 18)
plt.scatter(df.index, df['Buy'], color='green', marker='^', alpha=1)
plt.scatter(df.index, df['Sell'], color='red', marker='v', alpha=1)
plt.show()
