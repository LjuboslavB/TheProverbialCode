import re
import time
import random
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2_ohlc

import keras
import tensorflow as tf
from keras.utils import to_categorical
from keras.layers import Input, Dense, Dropout
from keras.models import Model, Sequential

# s = 25
# random.seed(6+s)
# tf.set_random_seed(333+s*2)
# np.random.seed(856+s*3)


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
    lines = r.content.decode('latin-1').replace('\\', '')
    lines = lines.replace('}', '\n')
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
            # start_date = end_date-8640000
            # print('shit start date 94 ish')
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
            self.percent_change = 100*(self.data.iloc[:, 4]-self.data.iloc[:, 1])/self.data.iloc[:, 1]
            self.percent_change[0] = 0
            self.d1price = self.data_mean.shift(2)-4*self.data_mean.shift(1)+3*self.data_mean
            self.d2price = self.data_mean.shift(2)-2*self.data_mean.shift(1)+self.data_mean
            self.d3price = -self.data_mean.shift(3)+3*self.data_mean.shift(2)+-3*self.data_mean.shift(1)+self.data_mean
            self.d1volume = self.data.iloc[:, -1].shift(2)-4*self.data.iloc[:, -1].shift(1)+3*self.data.iloc[:, -1]
            self.d2volume = self.data.iloc[:, -1].shift(2)-2*self.data.iloc[:, -1].shift(1)+self.data.iloc[:, -1]
            self.d3volume = -self.data.iloc[:,-1].shift(3)+3*self.data.iloc[:,-1].shift(2)-3*self.data.iloc[:,-1].shift(1)+self.data.iloc[:,-1]
            self.d1price[0:3] = self.d1price[3]
            self.d2price[0:3] = self.d2price[3]
            self.d3price[0:3] = self.d3price[3]
            self.d1volume[0:3] = self.d1volume[3]
            self.d2volume[0:3] = self.d2volume[3]
            self.d3volume[0:3] = self.d3volume[3]
            self.ma5 = self.data_mean.rolling(5, min_periods=1).mean()
            self.ma10 = self.data_mean.rolling(10, min_periods=1).mean()
            self.ma15 = self.data_mean.rolling(15, min_periods=1).mean()
            self.ma20 = self.data_mean.rolling(20, min_periods=1).mean()
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
            buy_label_idx = np.nonzero(stocks[i].percent_change >=0.5)
            stocks[i].label_pg[buy_label_idx[0][:]-1, :] = 1
    return stocks


def normalize_data(data):
    try:
        for i in range(data.shape[1]):
            data[:, i] = data[:, i] / np.max(data[:, i])
    except IndexError:
        data[:] = data[:] / np.max(data[:])
    return data


ticker_list = 'SP500_Labels.txt'
# ticker_list = 'Penny.txt'
# ticker_list = 'Single.txt'
tickers = gather_tickers(ticker_list)

# download_quotes(tickers)

stocks = parse_csv(tickers)
stocks = make_labels_percent_gain(stocks)
to_show = np.random.random_integers(0, len(tickers)-1, 1)
print(stocks[to_show[0]].ticker[0])

# ANN Code: Binary Buy Signal
# first testing for just one symbol
split_percent = 0.75
split_idx = round(split_percent*len(stocks[to_show[0]].data))
###
train_percent_change = stocks[to_show[0]].percent_change.iloc[:split_idx]
train_price = stocks[to_show[0]].data_mean[:split_idx]
train_volume = stocks[to_show[0]].data.iloc[:split_idx, -1]
train_ma5 = stocks[to_show[0]].ma5.iloc[:split_idx]
train_ma10 = stocks[to_show[0]].ma10.iloc[:split_idx]
train_ma15 = stocks[to_show[0]].ma15.iloc[:split_idx]
train_ma20 = stocks[to_show[0]].ma20.iloc[:split_idx]
train_d1price = stocks[to_show[0]].d1price.iloc[:split_idx]
train_d2price = stocks[to_show[0]].d2price.iloc[:split_idx]
train_d3price = stocks[to_show[0]].d3price.iloc[:split_idx]
train_d1volume = stocks[to_show[0]].d1volume.iloc[:split_idx]
train_d2volume = stocks[to_show[0]].d2volume.iloc[:split_idx]
train_d3volume = stocks[to_show[0]].d3volume.iloc[:split_idx]
train_data = np.column_stack((train_percent_change, train_d1price, train_d2price, train_d3price, train_d1volume, train_d2volume, train_d3volume,
                              train_volume))


test_percent_change = stocks[to_show[0]].percent_change.iloc[split_idx:]
test_price = stocks[to_show[0]].data_mean[split_idx:]
test_volume = stocks[to_show[0]].data.iloc[split_idx:, -1]
test_ma5 = stocks[to_show[0]].ma5.iloc[split_idx:]
test_ma10 = stocks[to_show[0]].ma10.iloc[split_idx:]
test_ma15 = stocks[to_show[0]].ma15.iloc[split_idx:]
test_ma20 = stocks[to_show[0]].ma20.iloc[split_idx:]
test_d1price = stocks[to_show[0]].d1price.iloc[split_idx:]
test_d2price = stocks[to_show[0]].d2price.iloc[split_idx:]
test_d3price = stocks[to_show[0]].d3price.iloc[split_idx:]
test_d1volume = stocks[to_show[0]].d1volume.iloc[split_idx:]
test_d2volume = stocks[to_show[0]].d2volume.iloc[split_idx:]
test_d3volume = stocks[to_show[0]].d3volume.iloc[split_idx:]
test_data = np.column_stack((test_percent_change, test_d1price, test_d2price, test_d3price, test_d1volume, test_d2volume, test_d3volume, test_volume))
###
# train_labels = train_price.shift(-1)
# train_labels.iloc[-1] = train_labels.iloc[-2]
# test_labels = test_price.shift(-1)
# test_labels.iloc[-1] = test_labels.iloc[-2]
###
norm_to = 1
train_data[:, norm_to:] = normalize_data(train_data[:, norm_to:])
test_data[:, norm_to:] = normalize_data(test_data[:, norm_to:])


train_labels = stocks[to_show[0]].label_pg[:split_idx]
test_labels = stocks[to_show[0]].label_pg[split_idx:]
train_labels_a = train_labels
test_labels_a = test_labels
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)
###
###
print('Creating Model')
n_inputs = train_data.shape[1]
n_outputs = 2
model = Sequential()
model.add(Dense(n_inputs, input_dim=n_inputs, activation='relu'))
# model.add(Dropout(0.15))
model.add(Dense(n_inputs*2, activation='relu'))
# model.add(Dropout(0.15))
model.add(Dense(n_outputs))
omt = keras.optimizers.Adam(lr=0.0005)
loss = 'binary_crossentropy'
print('Compiling Model')
model.compile(loss=loss,
              optimizer=omt,
              metrics=['binary_accuracy'])
print('Fitting Model')
history = model.fit(train_data, train_labels,
          epochs=500,
          batch_size=int(np.round((len(test_labels) / 10))),
          verbose=True,
          shuffle=False,
          validation_data=(test_data, test_labels))
print('Scoring Model')
scoresTest = model.evaluate(test_data, test_labels, verbose=0)
prd = model.predict_classes(test_data)
print(np.column_stack((prd, test_labels)))
print(str(model.metrics_names[1])+' %.2f%%' % (scoresTest[1]*100) + ' accuracy on test data')

###
###
buy_price = np.array([])
sell_price = np.array([])
buy_day = np.array([])
sell_day = np.array([])
i = -1
f_day = len(stocks[to_show[0]].data_mean) - len(prd)
ts = stocks[to_show[0]]
pg = 2
while i < len(prd)-2:
    i += 1
    # print(i)
    if prd[i] == 1:
        i += 1
        buy_price = np.append(buy_price, ts.data.iloc[f_day + i, 1])
        buy_day = np.append(buy_day, f_day + i)
        pc = 100*(ts.data.iloc[f_day + i, 4] - buy_price[-1])/buy_price[-1]
        if pc > pg:
            sell_price = np.append(sell_price, ts.data.iloc[f_day + i, 4])
            sell_day =np.append(sell_day, f_day + i)
        elif pc < -pg:
            sell_price = np.append(sell_price, ts.data.iloc[f_day + i, 4])
            sell_day = np.append(sell_day, f_day + i)
        while abs(pc) < pg and i < len(prd)-1:
            i += 1
            # print(i)
            pc = 100 * (ts.data.iloc[f_day + i, 4] - buy_price[-1]) / buy_price[-1]
            if pc > pg:
                sell_price = np.append(sell_price, ts.data.iloc[f_day + i, 4])
                sell_day = np.append(sell_day, f_day + i)
            elif pc < -pg:
                sell_price = np.append(sell_price, ts.data.iloc[f_day + i, 4])
                sell_day = np.append(sell_day, f_day + i)
                break


if len(sell_price) != len(buy_price):
    a = (sell_price[:] - buy_price[:-1])/buy_price[:-1]
else:
    a = (sell_price[:] - buy_price[:]) / buy_price[:]

if len(a) != 0:
    print(5*'\n'+'Win Percent :' + str(np.round(100*len(np.nonzero(a > 0)[0])/len(a), 2)))

print('Average Percent Change :' + str(np.round((100*np.mean(a)), 2)) + 5*'\n')

##
###
plt.figure()
ax1 = plt.subplot(3, 1, 1)
test_ohlc = stocks[to_show[0]].data.iloc[split_idx:, :]
candlestick2_ohlc(ax1, test_ohlc['Open'], test_ohlc['High'], test_ohlc['Low'], test_ohlc['Close'], colorup="green", colordown="red", width=.4)
plt.plot(buy_day-f_day, ts.data_mean.iloc[buy_day], 'g.', markersize=10)
plt.plot(sell_day-f_day, ts.data.iloc[sell_day, 4], 'r.', markersize=10)
plt.title(stocks[to_show[0]].ticker[0][:])
ax2 = plt.subplot(3, 1, 2, sharex=ax1)
line2 = plt.plot(np.arange(len(test_labels)), test_labels[:, 1], 'k')
ax3 = plt.subplot(3, 1, 3, sharex=ax1)
line3 = plt.plot(np.arange(len(prd)), prd, 'k')

if len(a) != 0:
    print(5*'\n'+'Win Percent :' + str(np.round(100*len(np.nonzero(a > 0)[0])/len(a), 2)))

print('Average Percent Change :' + str(np.round((100*np.mean(a)), 2)) + 5*'\n')

plt.show()



