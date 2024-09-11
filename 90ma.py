# 90 day moving average strategy

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

def candle_chart(data):
    # visually show the candlestick chart
    N = 100000000
    mpf.plot(data, type='candle', style='yahoo', warn_too_much_data=N)

def get_index(buy_info):
    if buy_info[0]['in_buy'] == False:
        return 0
    elif buy_info[1]['in_buy'] == False:
        return 1
    else:
        return 2
def buy_info_init():
    buy_info = [{'og': 0, 'curr': 0, 'price': 0, 'first': False, 'in_buy': False, 'money': 3000}, {'og': 0, 'curr': 0, 'price': 0, 'first': False, 'in_buy': False, 'money': 3000}, {'og': 0, 'curr': 0, 'price': 0, 'first': False, 'in_buy': False, 'money': 3000}]
    return buy_info
def buy_info_initv2():
    buy_info = [{'og': 0, 'curr': 0, 'price': 0, 'sells': 0, 'in_buy': False, 'money': 3000}, {'og': 0, 'curr': 0, 'price': 0, 'sells': 0, 'in_buy': False, 'money': 3000}, {'og': 0, 'curr': 0, 'price': 0, 'sells': 0, 'in_buy': False, 'money': 3000}]
    return buy_info
def update_buy_lists(buy_list, index, close, count): 
    if index == count:
        buy_list.append(close)
    else:
        buy_list.append(np.nan)
    return (buy_list)
def update_buy_info(buy_info, index, close):
    buy_info[index]['price'] = close
    buy_info[index]['og'] = buy_info[index]['money']/close
    buy_info[index]['curr'] = buy_info[index]['money']/close
    buy_info[index]['money'] = buy_info[index]['money'] - (buy_info[index]['og'] * close)
    buy_info[index]['in_buy'] = True
    return buy_info
def reset_buy_info(buy_info, index, close):
    buy_info[index]['money'] = buy_info[index]['money'] + (buy_info[index]['curr'] * close)
    buy_info[index]['curr'] = 0
    buy_info[index]['og'] = 0
    buy_info[index]['first'] = False
    buy_info[index]['in_buy'] = False
    buy_info[index]['price'] = 0
    return buy_info

def update_df(data, strategy):
    # set the index to the date
    data = data.set_index(pd.DatetimeIndex(data['Date'].values))

    # ninety-day exponential moving average
    ninetyEMA = data.Close.ewm(span=90, adjust=False).mean()
    data['Ninety'] = ninetyEMA
    money = 0
    if strategy == '1':
        data['Buy0'], data['Buy1'], data['Buy2'], data['Sell0'], data['Sell1'], data['Sell2'], money = signal_funcv1(data)
        return (data, money, ninetyEMA)
    elif strategy == '2':
        data['Buy0'], data['Buy1'], data['Buy2'], data['Sell0'], data['Sell1'], data['Sell2'], money = signal_funcv2(data)
        return (data, money, ninetyEMA)
    

    return (data, money, ninetyEMA)
    


def make_plot(df, ninetyEMA, ticker):
    # visually show the stock buy and sell signals
    plt.figure(figsize=(12.2, 4.5))
    plt.title('Buy and Sell Plot ' + str({ticker}), fontsize = 18)
    plt.plot(df['Close'], label='Close Price', color='blue', alpha=0.4)
    plt.plot(ninetyEMA, label='ninetyEMA', color='green', alpha=0.35)
    plt.xlabel('Date', fontsize = 18)
    plt.ylabel('Close Price', fontsize = 18)
    plt.scatter(df.index, df['Buy0'], color='green', marker='^', alpha=1)
    plt.scatter(df.index, df['Sell0'], color='red', marker='v', alpha=1)
    plt.scatter(df.index, df['Buy1'], color='blue', marker='^', alpha=1)
    plt.scatter(df.index, df['Sell1'], color='orange', marker='v', alpha=1)
    plt.scatter(df.index, df['Buy2'], color='purple', marker='^', alpha=1)
    plt.scatter(df.index, df['Sell2'], color='yellow', marker='v', alpha=1)
    plt.show()

def engine():
    # set the start and end dates
    start = date_to_time_stamp(2022, 7, 10)
    end = int(time.mktime(dt.datetime.now().timetuple()))

    # get the ticker
    ticker = input('Input Ticker: ')

    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start}&period2={end}&interval=1d&events=history&includeAdjustedClose=true'

    strategy = input('Choose strategy [1/2]: ')
    # read in the data from yahoo finance
    df = pd.read_csv(query_string)
    df, money, ninetyEMA = update_df(df, strategy)
    answer = input('Would you like to print the available money [y/n]? ')
    if answer == 'y':
        print("\033[91m {}\033[00m" .format(money))
    
    make_plot(df, ninetyEMA, ticker)    

# this strategy executes max 3 buy at a time with a set amount of price, selling 1/4 at half peak delta and 3/4 at peak 
def signal_funcv1(data):
    buy_list0 = []
    sell_list0 = []
    buy_list1 = []
    sell_list1 = []
    buy_list2 = []
    sell_list2 = []
    buy_info = buy_info_init()
    num_buys = 0
    peak = 0
    
    
    for i in range(0, len(data)):
        if data['Close'][i] > peak:
            peak = data['Close'][i]
        # buy conditional
        if (data['Close'][i]) <= data['Ninety'][i] and num_buys < 3 and i > 260:
            index = get_index(buy_info)
            num_buys+=1
            buy_list0 = update_buy_lists(buy_list0, index, data['Close'][i], 0)
            buy_list1 = update_buy_lists(buy_list1, index, data['Close'][i], 1)
            buy_list2 = update_buy_lists(buy_list2, index, data['Close'][i], 2)
            buy_info = update_buy_info(buy_info, index, data['Close'][i])
        else:
            buy_list0.append(np.nan)
            buy_list1.append(np.nan)
            buy_list2.append(np.nan)
        # sell conditional
        for index in range(0, 3):
            if buy_info[index]['in_buy'] == True:
                if buy_info[index]['first'] == False:
                    if ((peak - buy_info[index]['price']) / 2) <= data['Close'][i] - buy_info[index]['price']:
                        if index == 0:
                            sell_list0.append(data['Close'][i])
                        elif index == 1:
                            sell_list1.append(data['Close'][i])
                        else:
                            sell_list2.append(data['Close'][i])
                        buy_info[index]['money'] = buy_info[index]['money'] + ((buy_info[index]['og'] / 4) * data['Close'][i])
                        buy_info[index]['curr'] = buy_info[index]['og'] - (buy_info[index]['og'] / 4)
                        buy_info[index]['first'] = True
                    else:
                        if index == 0:
                            sell_list0.append(np.nan)
                        elif index == 1:
                            sell_list1.append(np.nan)
                        else:
                            sell_list2.append(np.nan)
                elif buy_info[index]['first'] == True:
                    if data['Close'][i] >= peak:
                        if index == 0:
                            sell_list0.append(data['Close'][i])
                        elif index == 1:
                            sell_list1.append(data['Close'][i])
                        else:
                            sell_list2.append(data['Close'][i])
                        num_buys-=1
                        buy_info = reset_buy_info(buy_info, index, data['Close'][i])
                    else:
                        if index == 0:
                            sell_list0.append(np.nan)
                        elif index == 1:
                            sell_list1.append(np.nan)
                        else:
                            sell_list2.append(np.nan)
            else:
                if index == 0:
                    sell_list0.append(np.nan)
                elif index == 1:
                    sell_list1.append(np.nan)
                else:
                    sell_list2.append(np.nan)

    money = buy_info[0]['money'] + buy_info[1]['money'] + buy_info[2]['money']

    return (buy_list0, buy_list1, buy_list2, sell_list0, sell_list1, sell_list2, money)
def signal_funcv2(data):
    buy_list0 = []
    sell_list0 = []
    buy_list1 = []
    sell_list1 = []
    buy_list2 = []
    sell_list2 = []
    buy_info = buy_info_initv2()
    num_buys = 0
    peak = 0
    
    
    for i in range(0, len(data)):
        if data['Close'][i] > peak:
            peak = data['Close'][i]
        # buy conditional
        if (data['Close'][i]) <= data['Ninety'][i] and num_buys < 3 and i > 260:
            index = get_index(buy_info)
            num_buys+=1
            if index == 0:
                buy_list0.append(data['Close'][i])
                buy_list1.append(np.nan)
                buy_list2.append(np.nan)
            elif index == 1:
                buy_list1.append(data['Close'][i])
                buy_list0.append(np.nan)
                buy_list2.append(np.nan)
            elif index == 2:
                buy_list2.append(data['Close'][i])
                buy_list1.append(np.nan)
                buy_list0.append(np.nan)

            buy_info[index]['price'] = data['Close'][i]
            buy_info[index]['og'] = buy_info[index]['money']/data['Close'][i]
            buy_info[index]['curr'] = buy_info[index]['money']/data['Close'][i]
            buy_info[index]['money'] = buy_info[index]['money'] - (buy_info[index]['og'] * data['Close'][i])
            buy_info[index]['in_buy'] = True
        else:
            buy_list0.append(np.nan)
            buy_list1.append(np.nan)
            buy_list2.append(np.nan)
        # sell conditional
        for index in range(0, 3):
            if buy_info[index]['in_buy'] == True:
                if buy_info[index]['sells'] == 0:
                    if ((peak - buy_info[index]['price']) / 2) <= data['Close'][i] - buy_info[index]['price']:
                        if index == 0:
                            sell_list0.append(data['Close'][i])
                        elif index == 1:
                            sell_list1.append(data['Close'][i])
                        else:
                            sell_list2.append(data['Close'][i])
                        buy_info[index]['money'] = buy_info[index]['money'] + ((buy_info[index]['og'] / 4) * data['Close'][i])
                        buy_info[index]['curr'] = buy_info[index]['curr'] - (buy_info[index]['og'] / 4)
                        buy_info[index]['sells'] = 1
                    else:
                        if index == 0:
                            sell_list0.append(np.nan)
                        elif index == 1:
                            sell_list1.append(np.nan)
                        else:
                            sell_list2.append(np.nan)
                elif buy_info[index]['sells'] == 1:
                    if data['Close'][i] >= peak:
                        if index == 0:
                            sell_list0.append(data['Close'][i])
                        elif index == 1:
                            sell_list1.append(data['Close'][i])
                        else:
                            sell_list2.append(data['Close'][i])
                        buy_info[index]['money'] = buy_info[index]['money'] + (buy_info[index]['og'] / 4 * data['Close'][i])
                        buy_info[index]['curr'] = buy_info[index]['curr'] - (buy_info[index]['og'] / 4)
                        buy_info[index]['sells'] = 2
                    else:
                        if index == 0:
                            sell_list0.append(np.nan)
                        elif index == 1:
                            sell_list1.append(np.nan)
                        else:
                            sell_list2.append(np.nan)
                elif buy_info[index]['sells'] == 2:
                    if data['Close'][i] >= peak:
                        if index == 0:
                            sell_list0.append(data['Close'][i])
                        elif index == 1:
                            sell_list1.append(data['Close'][i])
                        else:
                            sell_list2.append(data['Close'][i])
                        buy_info[index]['money'] = buy_info[index]['money'] + (buy_info[index]['og'] / 4 * data['Close'][i])
                        buy_info[index]['curr'] = buy_info[index]['curr'] - (buy_info[index]['og'] / 4)
                        buy_info[index]['sells'] = 3
                    else:
                        if index == 0:
                            sell_list0.append(np.nan)
                        elif index == 1:
                            sell_list1.append(np.nan)
                        else:
                            sell_list2.append(np.nan)
                elif buy_info[index]['sells'] == 3:
                    if data['Close'][i] >= peak:
                        if index == 0:
                            sell_list0.append(data['Close'][i])
                        elif index == 1:
                            sell_list1.append(data['Close'][i])
                        else:
                            sell_list2.append(data['Close'][i])
                        num_buys-=1
                        buy_info[index]['money'] = buy_info[index]['money'] + (buy_info[index]['curr'] * data['Close'][i])
                        buy_info[index]['curr'] = 0
                        buy_info[index]['og'] = 0
                        buy_info[index]['sells'] = 0
                        buy_info[index]['price'] = 0
                        buy_info[index]['in_buy'] = False
                    else:
                        if index == 0:
                            sell_list0.append(np.nan)
                        elif index == 1:
                            sell_list1.append(np.nan)
                        else:
                            sell_list2.append(np.nan)
            else:
                if index == 0:
                    sell_list0.append(np.nan)
                elif index == 1:
                    sell_list1.append(np.nan)
                else:
                    sell_list2.append(np.nan)

    money = buy_info[0]['money'] + buy_info[1]['money'] + buy_info[2]['money']

    return (buy_list0, buy_list1, buy_list2, sell_list0, sell_list1, sell_list2, money)

# ---------------------------------------------------------------------------- #

# run the program
engine()
