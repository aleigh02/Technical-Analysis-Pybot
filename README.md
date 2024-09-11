# Technical-Analysis-Pybot
Folder focused on Technical Analysis programs of stock prices using Yahoo Finance API

Files:

ema_analysis -> This file, takes start/end time, as well as stock ticker from the user and builds a pyplot based off the different
                relationships between the stocks 5, 21, and 63 day moving averages. It indicates buy and sell points within the plot.

oc_analysis -> This file takes a stock ticker as , and triggers buy/sell functions based off momentum moves of the stock over a period of
                a couple of days. All of this data is portrayed in a pyplot.

90ma_analysis -> This file takes a stock ticker as input and also prompts the user to identify what type of buy/sell strategy they would like
                  to use. The program, then triggers a specific signal function which will trigger buy functions when the stock price crosses
                  the 90 day moving average. The program then incremently sells back the stock based on it's price compared to the peak price of
                  the stock. Depending on the type of strategy the program will be more cautious or risky. 
