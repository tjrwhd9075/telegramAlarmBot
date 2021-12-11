import ccxt
import pandas as pd
import pprint
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
import mplfinance
from ccxt.binance import binance

myApikey = "hOpHmrM35aqoqakISj0m7PAy42bDLXBmhXIrOsvadPBU6bW8Gtin0ggp7UnzFg9f"
mySecretkey = "rJp7j47DyzzvqRhaa9ExusnxrcPSF2I6Aa1B6bNvjlzxv3VP7fs3sl3cMNvSbEdU"

# 바이낸스 정보 , 선물 설정
def bnc():
    binance = ccxt.binance({
        'apiKey': myApikey,
        'secret': mySecretkey,
        'enableRateLimit': True,
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
def fetch_ohlcvs(coin='BTC/USDT', timeframe='1d', limit=30):
    binance = bnc()
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
    return ticker[ohlcvabl]

# 잔고조회
def fetch_balance(coin):
    '''
    coin :"USDT" 
    fut : "free" 사용가능 "used" 주문넣은것 "total" 총합
    '''
    binance = bnc()
    return binance.fetch_balance(params={"type": "future"})[coin]     #선물 잔고 조회

def fetch_balances():
    '''
    coin : "BTC", "USDT" 
    fut : "free" 사용가능 "used" 주문넣은것 "total" 총합
    '''
    binance = bnc()
    return binance.fetch_balance(params={"type": "future"})     #선물 잔고 조회 

# 취소 주문
def order_cancel(orderId, coin):
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

# 헷지모드
def order_hedge_limit(coin, side, amount, price, positionside, test):
    '''
        ** Open position **
        Long : positionSide= 'LONG', side= 'BUY' 
        Short: positionSide= 'SHORT', side= 'SELL'
        ** Close position **
        Close long position: positionSide=LONG, side=SELL 
        Close short position: positionSide=SHORT, side=BUY 

        test : True (test), False (real)
    '''
    binance = bnc()
    return binance.create_order(coin, 'limit', side, amount, price, params={'positionSide' : positionside, 'test': test})

def order_hedge_market(coin, side, amount, positionside, test):
    '''
        ** Open position **
        Long : positionSide= 'LONG', side= 'BUY' 
        Short: positionSide= 'SHORT', side= 'SELL'
        ** Close position **
        Close long position: positionSide=LONG, side=SELL 
        Close short position: positionSide=SHORT, side=BUY 

        test : True (test), False (real)
    '''
    binance = bnc()
    return binance.create_order(coin, 'market', side, amount, params={'positionSide' : positionside, 'test' :test})

def Ema(df, span=8):
    '''ema 지수이평선 '''
    df["ema"] = df["close"].ewm(span=span, adjust=False).mean()
    return df

def BolingerBand(df, n=20, k=2):
    '''
    20ma, bolUpper, bolLower
    '''
    df['20ma'] = df['close'].rolling(window=n).mean()  
    df['bolUpper'] = df['close'].rolling(window=n).mean() + k* df['close'].rolling(window=n).std()
    df['bolLower'] = df['close'].rolling(window=n).mean() - k* df['close'].rolling(window=n).std()
    return df

def Heiken_ashi(df):
    ''' 
    캔들 시가, 종가 : open, close
    HA캔들 시가, 종가, 고가, 저가 : Open, Close, High, Low
    '''
    df_HA = df
    df_HA['Open'] = df['open']

    # HA 종가 = (현재캔들)(시가+종가+저가+고가)/4
    df_HA["Close"] = (df["open"]+df["high"]+df["low"]+df["close"])/4 
    for i in range(df_HA.shape[0]):  
        if i > 0: 
            # HA 시가 = (이전 HA 시가+ 이전 HA 종가)/2
            df_HA.loc[df_HA.index[i],"Open"] = (df_HA["Open"][i-1] + df_HA["Close"][i-1])/2   
            # HA 고가 = 최대(캔들고가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"High"] = max(df["high"][i],df_HA["Open"][i],df_HA["Close"][i])
            # HA 저가 = 최소(캔들저가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"Low"] = min(df["low"][i],df_HA["Open"][i],df_HA["Close"][i]) 

    return df_HA    

def Rsi(df, period=14):
    ''' rsi, lin30, line70 '''
    dfRSI = df
    dfRSI['U'] = np.where(dfRSI.diff(1)['close'] > 0, dfRSI.diff(1)['close'], 0)  # df.diff(1) : 기준일 종가 - 전일 종가, 0보다 크면 증가분을, 아니면 0을 넣음
    dfRSI['D'] = np.where(dfRSI.diff(1)['close'] < 0, dfRSI.diff(1)['close']*(-1), 0) # 기준일 종가 - 전일 종가, 0보다 작으면 감소분을, 아니면 0을 넣음
    dfRSI['AU'] = dfRSI['U'].rolling(window=period).mean() # period=14 동안의 U의 (이동)평균
    dfRSI['AD'] = dfRSI['D'].rolling(window=period).mean() # period=14 동안의 D의 (이동)평균
    df['rsi'] = dfRSI['AU'] / (dfRSI['AD']+dfRSI['AU']) * 100
    df['line30'] = 30
    df['line70'] = 70
    return df

def fetch_position(coin, balance):
    '''
    coin : "BTCUSDT"
    balance = binance.fetch_balance()
    '''
    positions = balance['info']['positions']
    for position in positions:
        if position["symbol"] == coin:
            return position

def fetch_position2(coin, balance, longshort):            # 들고있는 포지션 조회
    '''
    coin : "BTCUSDT"
    balance = binance.fetch_balance()
    '''
    positions = balance['info']['positions']
    for position in positions:
        if position["symbol"] == coin and position["positionSide"] == longshort: 
            return position

# 대기주문 조회
def fetch_open_order(coin, side, positionSide):
    '''
    return {'id', 'amount'} or []
    '''
    open_orders = bnc().fetch_open_orders(symbol=coin)
    for open_order in open_orders:
        if open_order['symbol'] == coin:
            if open_order['info']['side'] == side and open_order['info']['positionSide'] == positionSide:
                return open_order
    return []    

# 대기주문 조회
def fetch_open_orders(coin):
    '''
    return [{'id', 'amount'},{}...] or []
    '''
    open_orders = bnc().fetch_open_orders(symbol=coin)
    if open_orders == []:
        return []
    else:
        return open_orders

def set_signal(df):
    df1 = BolingerBand(df)
    df2 = Rsi(df1)
    df3 = Heiken_ashi(df2)
    return df3



def auto() :
    print(dt.datetime.now())
    coin = 'BTC/USDT'
    intervalSet = ['1m','5m', '15m', '30m', '1h']
    limit = 50

    df5m = set_signal(fetch_ohlcvs(coin, intervalSet[1], limit))
    # df15m = set_signal(fetch_ohlcvs(coin, intervalSet[2], limit))
    # df30m = set_signal(fetch_ohlcvs(coin, intervalSet[3], limit))
    # df1h = set_signal(fetch_ohlcvs(coin, intervalSet[4], limit))
            
    # closePrice = float(df5m['close'].iloc[-1])            # 종가
    # amount = round(float((fetch_balance('USDT')['free'] / df5m['close'].iloc[-1])/2),3)   # 구매 가능한 수량

    # longPosition = fetch_position2('BTCUSDT', fetch_balances(), "LONG")                 # 포지션 상세 정보    
    # longAmt = float(longPosition['positionAmt'])
    # longAvgPrice = float(longPosition['entryPrice'])     # 평단
    # longOpenOrder = fetch_open_order(coin, "SELL", "LONG")   # 클로즈 주문이 있는지 확인

    # shortPosition = fetch_position2('BTCUSDT', fetch_balances(), "SHORT")
    # shortAmt = -float(shortPosition['positionAmt'])
    # shortAvgPrice = float(shortPosition['entryPrice'])
    # shortOpenOrder = fetch_open_order(coin, "BUY", "SHORT")   # 클로즈 주문이 있는지 확인

    # rst = order_hedge_limit(coin, "BUY", 0.001, df5m['close'].iloc[-1], "LONG", True)
    # print(rst)

    fb = fetch_balance("USDT" , True)
    print(fb)

    ########### 롱 매수조건  ##################
    
    # # 롱포지션이 없을때
    # if longAmt == 0: 
    #     # 모든 rsi < 31 일때.
    #     if df5m['rsi'].iloc[-1] < 31 and df15m['rsi'].iloc[-1] < 31 and df30m['rsi'].iloc[-1] < 31 and df1h['rsi'].iloc[-1] < 31 :
    #         # 매수가는 볼밴 최하단
    #         buyTarget = min(df5m['bolLow'].iloc[-1], df15m['bolLow'].iloc[-1], df30m['bolLow'].iloc[-1], df1h['bolLow'].iloc[-1])
    #         if buyTarget > closePrice : # 종가가 더 낮으면 시장가로
    #             buyTarget = closePrice
    #             order_hedge_market(coin, 'BUY', amount, 'LONG')
    #             order_hedge_limit(coin, 'BUY', amount, buyTarget-200, 'LONG')
    #         elif buyTarget < closePrice :  # 종가가 더 높으면 볼밴 최하단 가격으로
    #             order_hedge_limit(coin, 'BUY', amount, buyTarget, 'LONG')
    #             order_hedge_limit(coin, 'BUY', amount, buyTarget-200, 'LONG')
    
    # ########### 숏 매수조건  ##################

    # # 숏 포지션이 없을때
    # if shortAmt == 0: 
    #     # 모든 rsi > 69 일때.
    #     if df5m['rsi'].iloc[-1] > 69 and df15m['rsi'].iloc[-1] > 69 and df30m['rsi'].iloc[-1] > 69 and df1h['rsi'].iloc[-1] > 69 :
    #         # 매수가는 볼밴 최상단
    #         buyTarget = max(df5m['bolUpper'].iloc[-1], df15m['bolUpper'].iloc[-1], df30m['bolUpper'].iloc[-1], df1h['bolUpper'].iloc[-1])
    #         if buyTarget < closePrice : # 종가가 더 높으면 시장가로
    #             order_hedge_market(coin, 'SELL', amount, 'SHORT')
    #             order_hedge_limit(coin, 'SELL', amount, buyTarget+200, 'SHORT')
    #         elif buyTarget > closePrice :  # 종가가 더 낮으면 볼밴 최상단 가격으로
    #             buyTarget = closePrice
    #             order_hedge_limit(coin, 'SELL', amount, buyTarget, 'SHORT')
    #             order_hedge_limit(coin, 'SELL', amount, buyTarget+200, 'SHORT')

    # ############# 롱 매도 조건  ###################

    # #롱포지션이 있을때
    # if longAmt > 0:
    #     if longOpenOrder == []: # 클로즈 주문이 없다면
    #         if longAmt/2 >= 0.001 :
    #             order_hedge_limit(coin, 'SELL', longAmt/2, longAvgPrice+100, 'LONG')
    #             if (longAmt/2 - longAmt/4) >= 0.001 :
    #                 order_hedge_limit(coin, 'SELL', longAmt/4, longAvgPrice+150, 'LONG')
    #                 order_hedge_limit(coin, 'SELL', longAmt/4, longAvgPrice+200, 'LONG')
    #     else : # 클로즈 주문이 있다면
    #         longOpenOrders =fetch_open_orders(coin)
    #         for longOpenOrder in longOpenOrders:
    #             if longOpenOrder['symbol'] == coin:
    #                 if longOpenOrder['info']['side'] == "SELL" and longOpenOrder['info']['positionSide'] == "LONG":
    #                     order_cancel(longOpenOrder['id'], coin)   # 클로즈 주문 전부 취소
    #         if longAmt/2 >= 0.001 :   # 클로즈 주문 재설정
    #             order_hedge_limit(coin, 'SELL', longAmt/2, longAvgPrice+100, 'LONG')
    #             if (longAmt/2 - longAmt/4) >= 0.001 :
    #                 order_hedge_limit(coin, 'SELL', longAmt/4, longAvgPrice+150, 'LONG')
    #                 order_hedge_limit(coin, 'SELL', longAmt/4, longAvgPrice+200, 'LONG')

    # ############# 숏 매도 조건  ###################

    # #숏포지션이 있을때
    # if shortAmt > 0:
    #     if shortOpenOrder == []: # 클로즈 주문이 없다면
    #         if shortAmt/2 >= 0.001 :
    #             order_hedge_limit(coin, 'BUY', shortAmt/2, shortAvgPrice-100, 'SHORT')
    #             if (shortAmt/2 - shortAmt/4) >= 0.001 :
    #                 order_hedge_limit(coin, 'BUY', shortAmt/4, shortAvgPrice-150, 'SHORT')
    #                 order_hedge_limit(coin, 'BUY', shortAmt/4, shortAvgPrice-200, 'SHORT')
    #     else : # 클로즈 주문이 있다면
    #         shortOpenOrders =fetch_open_orders(coin)
    #         for shortOpenOrder in shortOpenOrders:
    #             if shortOpenOrder['symbol'] == coin:
    #                 if shortOpenOrder['info']['side'] == "BUY" and shortOpenOrder['info']['positionSide'] == "SHORT":
    #                     order_cancel(shortOpenOrder['id'], coin)   # 클로즈 주문 전부 취소
    #         if shortAmt/2 >= 0.001 :   # 클로즈 주문 재설정
    #             order_hedge_limit(coin, 'BUY', shortAmt/2, shortAvgPrice-100, 'SHORT')
    #             if (shortAmt/2 - shortAmt/4) >= 0.001 :
    #                 order_hedge_limit(coin, 'BUY', shortAmt/4, shortAvgPrice-150, 'SHORT')
    #                 order_hedge_limit(coin, 'BUY', shortAmt/4, shortAvgPrice-200, 'SHORT')


auto()           

         
