import threading
import requests
import json
import time
import datetime
import pprint
from requests.models import Response
import schedule

from bs4 import BeautifulSoup

RG = requests.get
T_N = time.time()
DT_N = datetime.datetime.today()
PPRT = pprint.pprint

#반복 구문
# while True :
#     time.sleep(1)

# 1 구글 스프레드시트 #
import gspread
from oauth2client.service_account import ServiceAccountCredentials

Google_Spreadsheet = [ # 구글 스프레드시트 엔드포인트
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
#GS_API = 

# 2 텔레그램 봇 #
import telegram

## 채널 주소
Kantalk_Ch = '주소'

## 봇 API
Stock_Bot = telegram.Bot(token = '토큰')
Coin_Bot = telegram.Bot(token = '토큰')

## 알람 조건
# def Alarm():
    # if a:
    #     b()
    #     if c:
    #         d()
    #     elif e:
    #         f()
    #     else:
    #         g()
    # elif h:
    #     i()
    # else:
    #     g()

# 3 주식 #
# Alarm = 

    # Stock_Bot.sendMessage(chat_id = Kantalk_Ch, text = Alarm)

# 4 코인 #
## 4-1 바이낸스 ##
import ccxt

### API 엔드 포인트 ( https://api.binance.com )

### 정의
# binance = ccxt.binance()
# markets = binance.fetch_tickers()
# ticker = binance.fetch_tickers()
# ohlcvs = binance.fetch_ohlcvc(ticker)

### 출력
# print(markets.keys())
# print(ticker['open'], ticker['high'], ticker['low'], ticker['close'])

### 알람 출력
# Alarm = 
# Coin_Bot.sendMessage(chat_id = Kantalk_Ch, text = Alarm)

## 4-2 바이비트 ##
import bybit

### API - 엔드 포인트 ( https://api.bybit.com )
BB_Client = bybit.bybit( # 바이비트 API
    test = True,
    api_key = '키',
    api_secret = '비번')

### 서버시간
Bybit_Server_time_AD = 'https://api.bybit.com/v2/public/time'
BB_ST = RG(Bybit_Server_time_AD)
# print(BB_ST.json()) # 핑 테스트

### 호가창
Bybit_Order_Book_AD = 'https://api.bybit.com/v2/public/orderBook/L2'
BB_OB = RG(Bybit_Order_Book_AD)
# print(BB_OB) # 핑 테스트

# PPRT(BB_Client.Market.Market_orderbook(symbol = 'BTCUSDT').result())

### 차트
Bybit_Kline_AD = 'https://api.bybit.com/public/linear/kline'
BB_KL = RG(Bybit_Kline_AD)
# print(BB_KL) # 핑 테스트

#### 바이비트 차트 데이터
def BB_KL_1D(): # 일봉
    PPRT(BB_Client.LinearKline.LinearKline_get(
        symbol = 'BTCUSDT',
        interval = 'D',
        **{'from': T_N-2592000}).result())
def BB_KL_4H(): # 4시간봉
    PPRT(BB_Client.LinearKline.LinearKline_get(
        symbol = 'BTCUSDT',
        interval = '240',
        **{'from': T_N-432000}).result())
def BB_KL_2H(): # 2시간봉
    PPRT(BB_Client.LinearKline.LinearKline_get(
        symbol = 'BTCUSDT',
        interval = '120',
        **{'from': T_N-216000}).result())
def BB_KL_1H(): # 1시간봉
    PPRT(BB_Client.LinearKline.LinearKline_get(
        symbol = 'BTCUSDT',
        interval = '60',
        **{'from': T_N-108000}).result())
def BB_KL_30m(): # 30분봉
    PPRT(BB_Client.LinearKline.LinearKline_get(
        symbol = 'BTCUSDT',
        interval = '30',
        **{'from': T_N-54000}).result())
def BB_KL_15m(): # 15분봉
    PPRT(BB_Client.LinearKline.LinearKline_get(
        symbol = 'BTCUSDT',
        interval = '15',
        **{'from': T_N-27000}).result())
def BB_KL_5m(): # 5분봉
    PPRT(BB_Client.LinearKline.LinearKline_get(
        symbol = 'BTCUSDT',
        interval = '5',
        **{'from': T_N-9000}).result())
def BB_KL_1m(): # 1분봉
    PPRT(BB_Client.LinearKline.LinearKline_get(
        symbol = 'BTCUSDT',
        interval = '1',
        **{'from': T_N-1800}).result())

#BB_Kl2 = RG(Bybit_Kline_AD, params = 'interval = 1 & symbol = BTCUSDT & from = 1624909140')

#### 시장가 데이터
def BB_KL_MP(self): # 시장 평균가격
    PPRT(BB_Client.LinearKline.LinearKline_markPrice(
        symbol = 'BTCUSDT',
        interval = 'min',
        limit = 10,
        **{'from': 1}).result())

BB_KL_MP

## 심볼 조회
Bybit_Symbol_AD = 'https://api.bybit.com/v2/public/symbols'
BB_Sb = RG(Bybit_Symbol_AD)
# print(client.Symbol.Symbol_get().result()) # 핑 테스트

### 청산 알림
Bybit_LO_AD = 'https://api.bybit.com/v2/public/liq-records'

# def BB_LR(): # 청산 기록
#     RG(BB_Client.Market.Market_liqRecords(
#         symbol = 'BTCUSDT',
#         **{'limit': 30},
#         **{'start_time': int(T_N-9000)}).result())

# PPRT(BB_Client.Market.Market_liqRecords(
#     symbol = 'BTCUSDT',
#     **{'limit': 30},
#     **{'start_time': int(T_N-9000)}).result())

# Alarm = 