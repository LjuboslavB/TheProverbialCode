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
import pandas as pd


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


def download_quotes(symbols):
    if len(symbols) > 1:
        for i in range(1, len(symbols)):
            symbol = symbols[i][0]
            print("--------------------------------------------------")
            print("Downloading %s to %s.csv" % (symbol, symbol))
            print("--------------------------------------------------")
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
            self.ticker = [symbol]
            self.sector = [sector]
            print('adding data for stock %s' % symbol)
        except Exception:
            self.data = []
            self.ticker = 'No File'
            self.sector = 'No File'
            print('file: %s.csv' % symbols[i][0], 'does not exist')


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


tickers = open('SP500_Labels.txt', 'r')
tickers = tickers.read()
tickers = tickers.split('\n')
for i in range(len(tickers)):
    tickers[i] = tickers[i].split('\t')

# download_quotes(tickers)
# tickers = ['ZION']
stocks = parse_csv(tickers)
print(stocks[10].ticker)























# from command line, enter this stuff to get cookie, crumb
# link to instructions : http://blog.bradlucas.com/posts/2017-06-02-new-yahoo-finance-quote-download-url/
# step 1: curl https://finance.yahoo.com/quote/GOOG?p=GOOG > goog.html
# step 2: open the .html file to view raw code
# step 3: get cookie
#         curl -s --cookie-jar cookie.txt https://finance.yahoo.com/quote/GOOG?p=GOOG > goog.html
#           alternatively, echo it out
#         echo -en "$(curl -s --cookie-jar $cookieJar https://finance.yahoo.com/quote/GOOG/?p=GOOG)"
# CrumbStore":{"crumb":"DDuBQ4pnLZc"}
# Cookie B Value: 0f82loddq6241&b=3&s=jq


# crumble_link = 'https://finance.yahoo.com/quote/{0}/history?p={0}'
# crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'
# cookie_regex = r'Set-Cookie: (.*?); '
# quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&crumb={}'

#
# class StockClass:
#     def __init__(self, symbol, filename):
#         try:
#             self.data = pd.read_csv(filename)
#             self.name = [symbol]
#             print('adding data')
#         except Exception:
#             self.data=[]
#             self.name='No File'
#             print('file: %s.csv' % symbols[i], 'does not exist')
#
#
# def parse_csv(symbols):
#     for i in range(len(symbols)):
#         try:
#             filename = 'C:/Users/carme/Desktop/C_D/Projects/Python/Stock/TheProverbialCode/StockMarket' \
#                        '/CSVFiles/' + '%s.csv' % (symbols[i])
#         except Exception:
#             filename='Nothing'
#             print('file: %s.csv' % symbols[i], 'does not exist')
#         stock = StockClass(symbols[i], filename)
#     return stock

# class StockClass:
#
#     def __init__(self, symbols):
#         self.max = len(symbols)
#
#     def __iter__(self):
#         self.n = 0
#         return self
#
#     def __next__(self, symbols):
#         if self.n <= self.max:
#             try:
#                 filename = 'C:/Users/carme/Desktop/C_D/Projects/Python/Stock/TheProverbialCode' \
#                            '/StockMarket' \
#                            '/CSVFiles/' + '%s.csv' % (symbols[self.n])
#                 self.data[self.n] = pd.read_csv(filename)
#                 self.name[self.n] = [symbols[self.n]]
#                 print('adding data')
#             except Exception:
#                 self.data[self.n] = []
#                 self.name[self.n] = 'No File'
#                 print('file: %s.csv' % symbols[self.n], 'does not exist')
#             self.n += 1
#         else:
#             raise StopIteration
#         return self
#
#
# def parse_csv(symbols):
#     stock_data = StockClass(symbols)
#     return stock_data