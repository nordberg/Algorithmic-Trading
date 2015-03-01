from yahoo_finance import Share
from datetime import date
import random
import Queue
import numpy as np

# Shares to try
stocks = ['GOOGL']
data = {}
fromYear = '2010'
fromMonth = '09'
fromDay = '25'
toYear = '2015'
toMonth = '03'
toDay = '01'
days = 0

# Get the historical data for every share. Save them in a dict structure.
for stock_name in stocks:
    print 'Getting stock information about ' + stock_name + ' ... '
    stock = Share(stock_name)
    symb = stock.get_info()['symbol']
    hist_data = stock.get_historical(fromYear + '-' + fromMonth + '-' + fromDay,
        toYear + '-' + toMonth + '-' + toDay)
    data[symb] = hist_data
    days = len(data[symb])

balance = 100000 # Starting money

# The time period in days
#days = (date(int(toYear),int(toMonth),int(toDay)) 
#    - date(int(fromYear),int(fromMonth),int(fromDay))).days

hist_val = {}

longTime = 200
shortTime = 20

longHist = np.zeros(longTime)
shortHist = np.zeros(shortTime)

for stock in stocks:
    hist_val[stock + 'long'] = np.zeros(longTime)
    hist_val[stock + 'short'] = np.zeros(shortTime)

longIdx = 0
shortIdx = 0
amountOfStocks = 0

print 'Running for ' + str(days) + ' days.'
for i in range(0, days - 1):
    print 'Day: ' + str(i) + ', Balance: $' + str(balance) + ', Stocks: ' + str(amountOfStocks)
    for stock in stocks:
        ## MOVING AVERAGE
        closePrice = float(data[stock][i]['Close'])
        longHist = hist_val[stock + 'long']
        shortHist = hist_val[stock + 'short']
        longHist[longIdx] = closePrice
        shortHist[shortIdx] = closePrice

        ## Print the long and short moving average
        if (longHist[longTime - 1]):
            longAvg = float(sum(longHist)/longTime)
            shortAvg = float(sum(shortHist)/shortTime)
            if shortAvg > longAvg:
                print 'BUY! (Long: ' + str(longAvg) + ', Short: ' + str(shortAvg) + ')'
                if balance > 0 and balance > closePrice:
                    if (balance - (closePrice * amountOfStocks)) > 0:
                        amountOfStocks += int(balance / closePrice)
                        balance -= closePrice * amountOfStocks
                        print 'Bought ' + str(amountOfStocks) + ' shares at a cost of $' + str(closePrice) + ' each'
            else:
                print 'SELL! (Long: ' + str(longAvg) + ', Short: ' + str(shortAvg) + ')'
                if amountOfStocks > 0:
                    print 'Sold ' + str(amountOfStocks) + ' shares at a cost of $' + str(closePrice) + ' each'
                    balance += amountOfStocks * closePrice
                    amountOfStocks = 0


        longIdx += 1
        shortIdx += 1

        if longIdx == longTime:
            longIdx = 0
        if shortIdx == shortTime:
            shortIdx = 0
        ## END MOVING AVERAGE

if amountOfStocks > 0:
    print 'Sold ' + str(amountOfStocks) + ' shares at a cost of $' + str(closePrice)
    balance += amountOfStocks * closePrice
    amountOfStocks = 0

print '________________________________'
print 'Balance: ' + str(balance)