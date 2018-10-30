'''
The homie Brad Lucas HOOKED IT UP
I love this dude for writing this post up.
Helpful, informative, saved lots of time.
http://blog.bradlucas.com/posts/2017-06-03-yahoo-finance-quote-download-python/
https://github.com/bradlucas/get-yahoo-quotes-python

Main entry point to script is download_quotes
'''

import re
import time
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def split_crumb_store(v):
    if v is None:
        return
    return v.split(':')[2].strip('"')


def find_crumb_store(lines):
    for l in lines:
        if re.findall(r'CrumbStore', l):
            return l
    print("Did not find CrumbStore")


def get_cookie_value(r):
    if not r.cookies:
        return
    return {'B': r.cookies['B']}


def get_page_data(symbol):
    url = "https://finance.yahoo.com/quote/%s/?p=%s" % (symbol, symbol)
    r = requests.get(url)
    cookie = get_cookie_value(r)
    lines = r.content.decode('unicode-escape').strip(). replace('}', '\n')
    return cookie, lines.split('\n')


def get_cookie_crumb(symbol):
    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    return cookie, crumb


def get_data(symbol, start_date, end_date, cookie, crumb):
    filename = 'C:/Users/carme/Desktop/TheProverbialCode/StockMarket' \
               '/CSVFiles/' +'%s.csv' % (symbol)
    url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s" % (symbol, start_date, end_date, crumb)
    response = requests.get(url, cookies=cookie)
    with open(filename, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)


def get_now_epoch():
    return int(time.time())


def waitbar(all_iters, current_iter):
    percent_complete = 100*(current_iter/all_iters)
    here_sym = '>'
    complete_sym = '-'
    print(int(np.round((percent_complete/2)-1))*complete_sym + here_sym)


def download_quotes(symbols):
    num_symbols = len(symbols)
    if num_symbols > 1:
        for i in range(1, num_symbols):
            symbol = symbols[i][0]
            print("--------------------------------------------------")
            print("Downloading %s to %s.csv" % (symbol, symbol))
            waitbar(num_symbols, i)
            # print("--------------------------------------------------")
            start_date = 0
            end_date = get_now_epoch()
            cookie, crumb = get_cookie_crumb(symbol)
            get_data(symbol, start_date, end_date, cookie, crumb)
    else:
        symbol = symbols[0][0]
        print("--------------------------------------------------")
        print("Downloading %s to %s.csv" % (symbol, symbol))
        print("--------------------------------------------------")
        start_date = 0
        end_date = get_now_epoch()
        cookie, crumb = get_cookie_crumb(symbol)
        get_data(symbol, start_date, end_date, cookie, crumb)


class StockClass:
    def __init__(self, symbol, sector, filename):
        try:
            self.data = pd.read_csv(filename)
            self.data_mean = self.data.iloc[:, 1:5].mean(1)
            self.ticker = [symbol]
            self.sector = [sector]
            self.filter_out_nan()
            print('Adding Data For Stock %s' % symbol)
        except Exception:
            self.data = []
            self.ticker = ['No File']
            print('file: %s.csv' % symbol, 'does not exist')
    def filter_out_nan(self):
        if self.ticker[:][0] != 'No File':
            self.data.iloc[:, 1:] = self.data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
            self.data = self.data.iloc[:, :].fillna(method='ffill')
            return self


def parse_csv(symbols):
    stock = []
    print(len(symbols))
    for i in range(len(symbols)):
        try:
            filename = 'C:/Users/carme/Desktop/TheProverbialCode/StockMarket' \
                       '/CSVFiles/' + '%s.csv' % (symbols[i][0])
            stock.append(StockClass(symbols[i][0], symbols[i][1], filename))
        except Exception:
            print('file: %s.csv' % symbols[i][0], symbols[i][1], 'does not exist')
    return stock


def gather_tickers(ticker_list):
    tickers = open(ticker_list, 'r')
    tickers = tickers.read()
    tickers = tickers.split('\n')
    for i in range(len(tickers)):
        tickers[i] = tickers[i].split('\t')
    return tickers


def make_labels_percent_gain(stocks):
    for i in range(len(stocks)):
        if stocks[i].ticker[0][:] != 'No File':
            stocks[i].label_pg = np.zeros((len(stocks[i].data), 1))
            buy_label = 100*(stocks[i].data.iloc[:, 4]-stocks[i].data.iloc[:, 1])/stocks[i].data.iloc[:, 1]
            buy_label_idx = np.nonzero(buy_label >= 5)
            stocks[i].label_pg[buy_label_idx[0][:], :] = 1
    return stocks

ticker_list = 'SP500_Labels.txt'
tickers = gather_tickers(ticker_list)

# download_quotes(tickers)
stocks = parse_csv(tickers)
stocks = make_labels_percent_gain(stocks)

to_show = np.random.random_integers(0,len(tickers),1)
ax1= plt.subplot(2,1,1)
line1 = plt.plot(stocks[to_show[0]].data_mean)
plt.title(stocks[to_show[0]].ticker[0][:])
ax2 =plt.subplot(2,1,2, sharex=ax1)
line2 = plt.plot(stocks[to_show[0]].label_pg)
plt.show()
