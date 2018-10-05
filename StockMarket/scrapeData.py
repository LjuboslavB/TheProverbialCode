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


def split_crumb_store(v):
    if v is None:
        return
    return v.split(':')[2].strip('"')


def find_crumb_store(lines):
    # Looking for
    # ,"CrumbStore":{"crumb":"9q.A4D1c.b9
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

    # Code to replace possible \u002F value
    # ,"CrumbStore":{"crumb":"FWP\u002F5EFll3U"
    # FWP\u002F5EFll3U
    lines = r.content.decode('unicode-escape').strip(). replace('}', '\n')
    return cookie, lines.split('\n')


def get_cookie_crumb(symbol):
    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    return cookie, crumb


def get_data(symbol, start_date, end_date, cookie, crumb):
    filename = 'C:/Users/carme/Desktop/C_D/Projects/Python/Stock/TheProverbialCode/StockMarket' \
               '/CSVFiles/' +'%s.csv' % (symbol)
    url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s" % (symbol, start_date, end_date, crumb)
    response = requests.get(url, cookies=cookie)
    with open(filename, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)


def get_now_epoch():
    # @see https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/#post5244109
    return int(time.time())


def download_quotes(symbols):

    if len(symbols) > 1:
        for i in range(1, len(symbols)):
            symbol = symbols[i]
            print("--------------------------------------------------")
            print("Downloading %s to %s.csv" % (symbol, symbol))
            # download_quotes(symbol)
            print("--------------------------------------------------")
            start_date = 0
            end_date = get_now_epoch()
            cookie, crumb = get_cookie_crumb(symbol)
            get_data(symbol, start_date, end_date, cookie, crumb)
    else:
        symbol = symbols
        print("--------------------------------------------------")
        print("Downloading %s to %s.csv" % (symbol, symbol))
        # download_quotes(symbol)
        print("--------------------------------------------------")
        start_date = 0
        end_date = get_now_epoch()
        cookie, crumb = get_cookie_crumb(symbol)
        get_data(symbol, start_date, end_date, cookie, crumb)


tickers = open('SP500.txt', 'r')
tickers = tickers.read()
tickers = tickers.split('\n')
# tickers = ['APD']
download_quotes(tickers)


























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
