# https://www.grenade.tw/blog/how-to-use-the-python-financial-analysis-visualization-module-mplfinance/

import time
import requests

import numpy as np
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

from talib import abstract
from datetime import datetime

# # DataFrame Setting
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 100)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# # Global Variables Setting
symbol = 'BTCUSDT'
url = 'https://api.binance.com/'

# # Get Market Data


def GetKline(url, symbol, interval, startTime=None, endTime=None):
    try:
        data = requests.get(url + 'api/v3/klines', params={
                            'symbol': symbol, 'interval': interval, 'startTime': startTime, 'limit': 1000}).json()
    except Exception as e:
        print('Error! problem is {}'.format(e.args[0]))
    tmp = []
    pair = []
    for base in data:
        tmp = []
        for i in range(0, 6):
            if i == 0:
                base[i] = datetime.fromtimestamp(base[i]/1000)
            tmp.append(base[i])
        pair.append(tmp)
    df = pd.DataFrame(
        pair, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df.date = pd.to_datetime(df.date)
    df.set_index("date", inplace=True)
    df = df.astype(float)
    return df


def GetHistoricalKline(url, symbol, interval, startTime):
    # init
    klines = GetKline(url, symbol, interval)
    tmptime = ToMs(klines.iloc[0].name)

    # Send request until tmptime > startTime
    while tmptime > startTime:
        # tmp minus period ms plus 1000 (1000 K)
        tmptime -= PeriodToMs(interval) * 1000
        if tmptime < startTime:
            tmptime = startTime
        tmpdata = GetKline(url, symbol, interval, tmptime)
        klines = pd.concat([tmpdata, klines])

    return klines.drop_duplicates(keep='first', inplace=False)

# Math Tools


def ToMs(date):
    # Binance timestamp format is 13 digits
    return int(time.mktime(time.strptime(str(date), "%Y-%m-%d %H:%M:%S")) * 1000)


def PeriodToMs(period):
    Ms = None
    ToSeconds = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }
    unit = period[-1]

    if unit in ToSeconds:
        try:
            Ms = int(period[:-1]) * ToSeconds[unit] * 1000
        except ValueError:
            pass
    return Ms


if __name__ == "__main__":
    # klines = GetHistoricalKline(url, symbol, '4h', ToMs('2019-05-01 12:00:00'))
    # print (klines)
    klines = GetKline(url, symbol, '1d', ToMs('2019-05-01 12:00:00'))
    mpf.plot(klines, type='candle', title=symbol, style='binance')  # 蠟燭圖
