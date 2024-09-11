# exponential moving average analysis

# Import the libraries
import time
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def date_to_time_stamp(year, month, day):
    # convert the date to a time stamp
    return int(time.mktime(datetime.datetime(year, month, day, 0, 0).timetuple()))

ticker = input('\nInput ticker for data retrieval: ')
beg_year = int(input('Input start year: '))
beg_month = int(input('Input start month: '))
beg_day = int(input('Input start day: '))
period1 = date_to_time_stamp(beg_year, beg_month, beg_day)

print('\nStarting query for end-time!')
end_year = int(input('Input end year: '))
end_month = int(input('Input end month: '))
end_day = int(input('Input end day: '))
period2 = date_to_time_stamp(end_year, end_month, end_day)

query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true'
df = pd.read_csv(query_string)

# set the index to the date
df = df.set_index(pd.DatetimeIndex(df['Date'].values))

# calculate the moving averages

# short/fast exponential moving average
shortEMA = df.Close.ewm(span=5, adjust=False).mean()
# middle/medium exponential moving average
middleEMA = df.Close.ewm(span=21, adjust=False).mean()
# long/slow exponential moving average
longEMA = df.Close.ewm(span=63, adjust=False).mean()


# Add the exponential moving averages to the chart
df['Short'] = shortEMA
df['Middle'] = middleEMA
df['Long'] = longEMA

# create the function to buy and sell the stock
def buy_sell_func(data):
    buy_list = []
    sell_list = []
    flag_long = False
    flag_short = False

    for i in range(0, len(data)):
        if data['Middle'][i] < data['Long'][i] and data['Short'][i] < data['Middle'][i] and flag_short == False and flag_long == False:
            # signals a sell
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_short = True
        elif flag_short == True and data['Short'][i] > data['Middle'][i]:
            # signals a sell
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_short = False

        elif data['Middle'][i] > data['Long'][i] and data['Short'][i] > data['Middle'][i] and flag_short == False and flag_long == False:
            # signals a sell
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_long = True
        elif flag_long == True and data['Short'][i] < data['Middle'][i]:
            # signals a sell
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_long = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)
        
    return (buy_list, sell_list)

# Add the buy and sell signals to the data set
df['Buy'] = buy_sell_func(df)[0]
df['Sell'] = buy_sell_func(df)[1]

# visually show the stock buy and sell signals
plt.figure(figsize=(12.2, 4.5))
plt.title('Buy and Sell Plot ' + str({ticker}), fontsize = 18)
plt.plot(df['Close'], label='Close Price', color='blue', alpha=0.4)
plt.plot(shortEMA, label='SHort/Fast EMA', color='red', alpha=0.35)
plt.plot(middleEMA, label='Middle/Medium EMA', color='orange', alpha=0.35)
plt.plot(longEMA, label='Long/Slow EMA', color='green', alpha=0.35)
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Close Price', fontsize = 18)
plt.scatter(df.index, df['Buy'], color='green', marker='^', alpha=1)
plt.scatter(df.index, df['Sell'], color='red', marker='v', alpha=1)
plt.show()
