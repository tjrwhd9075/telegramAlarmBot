
from logging import NullHandler
import sys
import datetime as dt
from ccxt.binance import binance
import pandas as pd
import pprint
from asyncio.windows_events import NULL
from os import name
from threading import Thread
from FinanceDataReader import data
import matplotlib as mpl
import pyupbit
import numpy as np
import requests
import time
from requests.models import DEFAULT_REDIRECT_LIMIT
import schedule
from fbprophet import Prophet
from bs4 import BeautifulSoup #웹 크롤링을 위한 라이브러리
import FinanceDataReader as fdr
from scipy.integrate._ivp.radau import P #종목 주가 정보 가져오기
import talib.abstract as ta #기술적 분석을 위한 지표
import datetime as dt
import matplotlib.pyplot as plt
# import yfinance
import mplfinance
import ccxt
import telegram as tel
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

myApikey = "hOpHmrM35aqoqakISj0m7PAy42bDLXBmhXIrOsvadPBU6bW8Gtin0ggp7UnzFg9f"
mySecretkey = "rJp7j47DyzzvqRhaa9ExusnxrcPSF2I6Aa1B6bNvjlzxv3VP7fs3sl3cMNvSbEdU"


# # 파일로부터 apiKey, Secret 읽기 
# with open("api.txt") as f:
#     lines = f.readlines()
#     api_key = lines[0].strip() 
#     secret = lines[1].strip() 

# 바이낸스 정보 , 선물 설정
def bnc():
    binance = ccxt.binance({
        'apiKey': myApikey,
        'secret': mySecretkey,
        'enableRateLimit': True,
        # 'dualSidePosition' : True,
        'options': { 
        'defaultType': 'future'                # 선물거래
        }
    })
    return binance   

# 바이낸스 딕셔너리 데이터를 데이터 프레임으로 변환
def dic2df(dic):
    df = pd.DataFrame(dic, columns = ['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    return df

# 과거 데이터 호출
def fetch_ohlcvs(coin, timeframe='1d', limit=30):
    binance = bnc()
    now = dt.datetime.utcnow()   # 현재 시간을 millsecond로 변환
    ohlcv = binance.fetch_ohlcv(symbol=coin, timeframe=timeframe, limit=limit)   #데이터 불러오기  
                                        # 시간간격 :'1m','3m','5m','15m','30m','1h','2h','4h','6h','8h','12h','1d','3d','1w','1M'
    return dic2df(ohlcv)   # 딕셔너리를 데이터프레임으로 변환

# 현재가 조회
def fetch_ticker(coin, ohlcvabl):
    '''
    ohlcvabl : "open" "high" "close" "volume" "ask"(매도1호가) "bid"(매수1호가) "last"(최근거래가격)
    '''
    binance = bnc()
    ticker = binance.fetch_ticker(coin)
    # ticker['open'], ticker['high'], ticker['low'], ticker['close'], ticker['ask'] 매도1호가, tichek['bid']매수1호가,tichek['last']최근가
    return ticker[ohlcvabl]

# 잔고조회
def fetch_balance(coin):
    '''
    coin : "BTC", "USDT" 
    fut : "free" 사용가능 "used" 주문넣은것 "total" 총합
    '''
    binance = bnc()
    return binance.fetch_balance(params={"type": "future"})[coin]     #선물 잔고 조회
    # print(balance.keys())  
    # print(balance['BTC']['free'], balance['BTC']['used'], balance['BTC']['total'])
    # free	거래에 사용하고 있지 않은 코인양
    # used	거래에 사용하고 있는 코인양
    # total	free + used
def fetch_balances():
            '''
            coin : "BTC", "USDT" 
            fut : "free" 사용가능 "used" 주문넣은것 "total" 총합
            '''
            binance = bnc()
            return binance.fetch_balance(params={"type": "future"})     #선물 잔고 조회 

# 지정가 매매: binance.create_limit_buy_order (티커, 주문 수량, 주문 가격), binance.create_limit_sell_order()      
# 시장가 매매: binance.create_market_buy_order(티커, 주문 수량), binance.create_market_sell_order()
# 주문 취소 : binance.cancel_order(orderId, 티커)

def trade_cancel(orderId, coin):
    binance = bnc()
    return binance.cancel_order(orderId, coin)

# 지정가 매매
def trade_limit(coin, order, amount, price):
    binance = bnc()
    if order == "buy":
        return binance.create_limit_buy_order(coin, amount, price)
    elif order == "sell":
        return binance.create_limit_sell_order(coin, amount, price)
    

# 시장가 매매
def trade_market(coin, order, amount):
    binance = bnc()
    if order == "buy":
        return binance.create_market_buy_order(coin, amount)
    elif order == "sell":
        return binance.create_market_sell_order(coin, amount)
    

def set_leverage(coin, leverage):
    binance = bnc()
    markets = binance.load_markets()
    market = binance.market(coin)
    resp = binance.fapiPrivate_post_leverage({
    'symbol': market['id'],
    'leverage': leverage
    })

def heiken_ashi_coin(coin='BTC/USDT', interval='1d', count=60):
        print(coin +" heiken_ashi_coin")
        df = fetch_ohlcvs(coin, interval, count)
        df_HA = df

        df_HA["Open"] = df["open"]       # 캔들 시가
        df_HA["Close"] = df["close"]     # 캔들 종가

        # HA 종가 = (현재캔들)(시가+종가+저가+고가)/4
        df_HA["close"] = (df["open"]+df["high"]+df["low"]+df["close"])/4 
        for i in range(df_HA.shape[0]):  
            if i > 0: 
                # HA 시가 = (이전 HA 시가+ 이전 HA 종가)/2
                df_HA.loc[df_HA.index[i],"open"] = (df_HA["open"][i-1] + df_HA["close"][i-1])/2   
                # HA 고가 = 최대(캔들고가, HA시가, HA종가)
                df_HA.loc[df_HA.index[i],"high"] = max(df["high"][i],df_HA["open"][i],df_HA["close"][i])
                # HA 저가 = 최소(캔들저가, HA시가, HA종가)
                df_HA.loc[df_HA.index[i],"low"] = min(df["low"][i],df_HA["open"][i],df_HA["close"][i]) 
        # 20일 이동평균
        df_HA["ma"] = df["close"].rolling(window=20).mean()
        # 8일 지수이동평균
        df_HA["ema"] = df["close"].ewm(span=8, adjust=False).mean()

        df_HA = df_HA.fillna(0) # NA 값을 0으로
        return df_HA    

def auto_trading():
    coin = 'BTC/USDT'
    print(coin+" auto_trading")

    interval1h = '1h'
    limit1h = 30
    interval5m = '5m'
    limit5m = limit1h * 12

    df_HA_m = heiken_ashi_coin(coin, interval5m, limit5m)
    df_HA_h = heiken_ashi_coin(coin, interval1h, limit1h)

 
def fetch_position(coin, balance):
    '''
    coin : "BTCUSDT"
    balance = binance.fetch_balance()
    '''
    positions = balance['info']['positions']

    for position in positions:
        if position["symbol"] == coin:
            return position
def fetch_open_order(coin):
    '''
    return {'id', 'amount'} or 0
    '''
    open_orders = bnc().fetch_open_orders(symbol=coin)
    if open_orders == []:
        return open_orders
    else:
        return open_orders[0]




try: # 작업
    coin = 'BTC/USDT'
    
    # order = trade_limit("BTC/USDT", "sell", 0.001, 40000, myApikey,mySecretkey)
    # btcBalance = fetch_position("BTCUSDT",fetch_balances(myApikey,mySecretkey))["positionAmt"]

    # if btcBalance == 0:
    # aa = "0.014"
    # print(float(aa)/2)
    # print(type(float(aa)/2))

    # open_orders = fetch_open_order('BTC/USDT')

    # pprint.pprint(open_orders)
 

    # print(fetch_ohlcvs(coin, interval, limit))   # 과거 데이터 불러옴 : 데이터프레임임
    # print(fetch_ticker(coin, "last")) # 현재 가격 불러옴
    # pprint.pprint(fetch_balance(myApikey,mySecretkey)['USDT'])  # 사용가능한 양
    pprint.pprint(fetch_position("BTCUSDT",fetch_balance('USDT')))  # 평단 "entryPrice", 수량"positionAmt", 포지션"positionSide"", 손익"unrealizedProfit"

    '''
    dualSidePosition = true 
    Open position: 
        Long : positionSide=LONG, side=BUY 
        Short: positionSide=SHORT, side=SELL 
    Close position: 
        Close long position: positionSide=LONG, side=SELL 
        Close short position: positionSide=SHORT, side=BUY

        
    '''
    # short_order={      "symbol":"BTCUSDT",
    #         "side": "BUY",
    #         "type": "LIMIT",
    #         "positionSide" : "SHORT",
    #         "quantity": "0.001"}
    # res = bnc().futures_create_order(**short_order)

    
    # 숏 -> buy 리듀스 온리로 클로즈 포지션
    # close_position = binance.create_order(symbol=symbol, type="MARKET", side="buy", amount=pos['positionAmt'], params={"reduceOnly": True})    
    
    # pprint.pprint(trade_limit(coin, "buy", 0.001, 30000))

    # set_leverage(coin, 20, myApikey, mySecretkey) # 레버리지 설정

    
    # print(order)
    # print(order['info']['orderId'])
    # cancel = trade_cancel(order['info']['orderId'], coin, myApikey, mySecretkey)
    # print(cancel)
    


except KeyboardInterrupt:
    # Ctrl+C 입력시 예외 발생
    print("control c")
    sys.exit() #종료




# 시간차이 확인
# #  h = dt.datetime.strptime(str(df_HA_h.index[-1]), "%Y-%m-%d %H:%M:%S")
#     m = dt.datetime.strptime(str(df_HA_m.index[-1]), "%Y-%m-%d %H:%M:%S")
#         if m - h >= dt.timedelta(minutes=0) and m - h < dt.timedelta(hours=1):  # 0분 <= 시간차이 < 60분