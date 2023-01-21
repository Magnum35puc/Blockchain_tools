import requests
import pandas as pd
import datetime as dt
import json
import time

class Binance_API_data:
    def __init__(self, year_a:int, year_b:int):
        print(f"Loading {year_a}")
        self.full_data = get_binance_data(year_a)
        self.start = year_a
        self.end = year_b
        for i in list(range(year_a+1, year_b+1)):
            print(f"Loading {i}")
            self.full_data = pd.concat([self.full_data,get_binance_data(i)])
            time.sleep(0.5)



def get_binance_data(year):
    url = 'https://api.binance.com/api/v3/klines'
    symbol = 'BTCUSDT'
    interval = '1d'
    start = str(int(dt.datetime(year,1,1).timestamp()*1000))
    end = str(int(dt.datetime(year,12,31).timestamp()*1000))
    par = {'symbol': symbol, 'interval': interval, 'startTime': start, 'endTime': end}
    data = pd.DataFrame(json.loads(requests.get(url, params= par).text))
    #format columns name
    data.columns = ['datetime', 'Open', 'High', 'Low', 'Close', 'Volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
    data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.datetime]
    data=data.astype(float)
    return data[['Open', 'High', 'Low', 'Close', 'Volume']]

