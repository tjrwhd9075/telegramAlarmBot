from asyncio.windows_events import NULL
from os import name
from threading import Thread
import matplotlib as mpl
from pandas.core.frame import DataFrame
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
import sys
import pandas as pd
import telegram as tel
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

on = 0
if on == 1:
    # 한국 코스피,코스닥 목록
    krx = fdr.StockListing('KRX')
    # 미국 주식 목록
    sp500 = fdr.StockListing('S&P500')
    nasdaq = fdr.StockListing('NASDAQ')
    nyse = fdr.StockListing('NYSE')

def codefind(name, country):
    if country == "krx" :
        search = list(krx['Name'])
        for i in range(len(krx)):
            if (search[i]==name):
                return krx['Symbol'][i]
    elif country == "us" :
        search = list(sp500['Name'])
        for i in range(len(sp500)):
            if (search[i]==name):
                return sp500['Symbol'][i]
    return 0

def namefind(symbol):
    search = list(sp500['Symbol'])
    search2 = list(nasdaq['Symbol'])
    search3 = list(nyse['Symbol'])
    for i in range(len(sp500)):
        if (search[i]==symbol):
            return sp500['Name'][i]
    for i in range(len(nasdaq)):
        if (search2[i]==symbol):
            return nasdaq['Name'][i]
    for i in range(len(nyse)):
        if (search3[i]==symbol):
            return nyse['Name'][i] 
    return 0

# 캔들차트 그리기
def plot_candle_chart(df, title):  
    adp = [mplfinance.make_addplot(df["ema"], color='green')]  # 이평선
    fig = mplfinance.plot(df, type='candle', style='charles', mav=(20),
                    title=title, ylabel='price', show_nontrading=False,
                    savefig='jusik.png',
                    addplot=adp
                    )
    print(title + " plot candle chart")

def heiken_ashi_jusik(token, region, count):

    print(token+" heiken_ashi_jusik")
    today = dt.date.today()
    delta = dt.timedelta(days=count)    # count 봉 전부터
    past = today-delta
    if region == "krx":
        df = fdr.DataReader(codefind(token, "krx"), past, today)
    if region == "us":
        df = fdr.DataReader(token, past, today)

    df_HA = df
    df_HA["open"] = df["Open"]
    df_HA["close"] = df["Close"]
    df_HA["low"] = df["Low"]
    df_HA["high"] = df["High"]
    df_HA["Ropen"] = df["Open"]       # 캔들 시가
    df_HA["Rclose"] = df["Close"]     # 캔들 종가

    # HA 종가 = (현재캔들)(시가+종가+저가+고가)/4
    df_HA["close"] = (df["Open"]+df["High"]+df["Low"]+df["Close"])/4 
    for i in range(df_HA.shape[0]):  
        if i > 0: 
            # HA 시가 = (이전 HA 시가+ 이전 HA 종가)/2
            df_HA.loc[df_HA.index[i],"open"] = (df_HA["open"][i-1] + df_HA["close"][i-1])/2   
            # HA 고가 = 최대(캔들고가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"high"] = max(df["High"][i],df_HA["open"][i],df_HA["close"][i])
            # HA 저가 = 최소(캔들저가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"low"] = min(df["Low"][i],df_HA["open"][i],df_HA["close"][i]) 
    # 20일 이동평균
    df_HA["ma"] = df["Close"].rolling(window=20).mean()
    # 8일 지수이동평균
    df_HA["ema"] = df["Close"].ewm(span=8, adjust=False).mean()

    df_HA = df_HA.fillna(0) # NA 값을 0으로
    return df_HA       

def buy_signal(token, interval, df_HA, bot=None, channel=None, channel_id=None):
    print(token+" buy_signal")
    # ha음봉(ha_open > ha_close) -> ha양봉(ha_open < ha_close)  # 양전
    if df_HA["open"].iloc[-2] > df_HA["close"].iloc[-2] and df_HA["open"].iloc[-1] < df_HA["close"].iloc[-1] :
        # 8ema < 20ma   # 하락추세중 추세반전
        if df_HA["ema"].iloc[-1] < df_HA["ma"].iloc[-1]:
            # 8ema < ha_close  :  100% 매수
            if df_HA["ema"].iloc[-1] < df_HA["close"].iloc[-1]:
                plot_candle_chart(df_HA, token)
                # if msgOn == 1:
                #     post_message(bot, channel, token + " " + interval + " 양봉전환 : 100% 매수")
                #     post_image(bot, channel, image)
                #     telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 양봉전환 : 100% 매수") # 메세지 보내기
                #     telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
                return 100
            # 8ema > ha_close  :  50% 매수
            if df_HA["ema"].iloc[-1] > df_HA["close"].iloc[-1]:
                plot_candle_chart(df_HA, token)
                # if msgOn == 1:
                #     post_message(bot, channel, token + " " + interval + " 양봉전환 : 50% 매수")
                #     post_image(bot, channel, image)
                #     telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 양봉전환 : 50% 매수") # 메세지 보내기
                #     telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
                return 50
        # 8ema > 20ma   # 상승추세중 불타기 추세반전
        if df_HA["ema"].iloc[-1] > df_HA["ma"].iloc[-1]:
            plot_candle_chart(df_HA, token)
            # if msgOn == 1:
            #     post_message(bot, channel, token + " " + interval + " 양봉전환 : 10% 매수")
            #     post_image(bot, channel, image)
            #     telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 양봉전환 : 10% 매수") # 메세지 보내기
            #     telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
            return 10
    time.sleep(1)
    return 0

def sell_signal(token, interval, df_HA, bot=None, channel=None, channel_id=None):

    print(token+" sell_signal")
    # ha양봉(ha_open < ha_close) -> ha양봉(ha_open < ha_close)  # 양봉연속
    if df_HA["open"].iloc[-2] < df_HA["close"].iloc[-2] and df_HA["open"].iloc[-1] < df_HA["close"].iloc[-1]:
        # ha양봉 and 캔들양봉 : 10% 매도
        if df_HA["Ropen"].iloc[-1] < df_HA["Rclose"].iloc[-1]:
            # post_message(tokenCoin, channel, token + " " + interval + " 양봉연속 : 10% 매도")
            return 10
    # ha양봉(ha_open < ha_close) -> ha음봉(ha_open > ha_close)  # 음봉전환 : 전량매도
    if df_HA["open"].iloc[-2] < df_HA["close"].iloc[-2] and df_HA["open"].iloc[-1] > df_HA["close"].iloc[-1]:
        # 아직 상승추세
        if df_HA["ema"].iloc[-1] > df_HA["ma"].iloc[-1] :
            # 작은 낙폭
            if df_HA["close"].iloc[-1] > df_HA["ema"].iloc[-1] :
                plot_candle_chart(df_HA, token)
                # if msgOn == 1:
                    # post_message(bot, channel, token + " " + interval + " 음봉전환 : 50% 매도")
                    # post_image(bot, channel, image)
                    # telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 음봉전환 : 50% 매도") # 메세지 보내기
                    # telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
                return 50
            # 큰 낙폭    
            if df_HA["close"].iloc[-1] < df_HA["ema"].iloc[-1] :
                plot_candle_chart(df_HA, token)
                # if msgOn == 1:
                #     post_message(bot, channel, token + " " + interval + " 음봉전환 : 80% 매도")
                #     post_image(bot, channel, image)
                #     telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 음봉전환 : 80% 매도") # 메세지 보내기
                #     telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
                return 80
            # 떡락
            if df_HA["close"].iloc[-1] < df_HA["ma"].iloc[-1] :
                plot_candle_chart(df_HA, token)
                # if msgOn == 1:
                #     post_message(bot, channel, token + " " + interval + " 음봉전환 : 100% 매도")
                #     post_image(bot, channel, image)
                #     telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 음봉전환 : 100% 매도") # 메세지 보내기
                #     telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
                return 100
        # 하락추세
        if df_HA["ema"].iloc[-1] < df_HA["ma"].iloc[-1] :
            plot_candle_chart(df_HA, token)
            # if msgOn == 1:
            #     post_message(bot, channel, token + " " + interval + " 음봉전환 : 100% 매도")
            #     post_image(bot, channel, image)
            #     telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 음봉전환 : 100% 매도") # 메세지 보내기
            #     telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
            return 100
    time.sleep(1)
    return 0

def add_signal(df_HA_m, df_HA_h, name):
    print(name+" add_signal")
    df_HA_m["signal"] = 0

    for i in range(len(df_HA_m)):
        print(i)
        if i>0: # 맨첫줄은 넘어감
            # ha음봉(ha_open > ha_close) -> ha양봉(ha_open < ha_close)  # 양봉전환 : 매수
            if df_HA_m["open"].iloc[i-1] > df_HA_m["close"].iloc[i-1] and df_HA_m["open"].iloc[i] < df_HA_m["close"].iloc[i] :
            
                for j in range(len(df_HA_h)):
                    if df_HA_h["open"].iloc[j] < df_HA_h["close"].iloc[j] :   # 시간봉이 양봉일때
                        h = dt.datetime.strptime(str(df_HA_h.index[j]), "%Y-%m-%d %H:%M:%S")
                        m = dt.datetime.strptime(str(df_HA_m.index[i]), "%Y-%m-%d %H:%M:%S")
                        if m - h >= dt.timedelta(hours=0) and m - h < dt.timedelta(days=1):  # 0분 <= 시간차이 < 60분
                            df_HA_m["signal"].iloc[i] = 1
            # ha양봉(ha_open < ha_close) -> ha음봉(ha_open > ha_close)  # 음봉전환 : 매도
            elif df_HA_m["open"].iloc[i-1] < df_HA_m["close"].iloc[i-1] and df_HA_m["open"].iloc[i] > df_HA_m["close"].iloc[i]:
                df_HA_m["signal"].iloc[i] = 2
    return df_HA_m
            
def krx_ha_check(name, count):
    print("krx_ha_check")
    if codefind(name, 'krx') != 0:   # 입력한 종목이 목록에 있으면
        print(name + "을 백테스팅 합니다.")
        df_HA = heiken_ashi_jusik(name, "krx", count)
        df_HA_as = add_signal(df_HA, name)
        return df_HA_as

    else:
        print("해당 종목은 목록에 없습니다")
        return 0

def us_ha_check(ticker, count):
    print("us_ha_check")
    if namefind(ticker) != 0:   # 입력한 종목이 목록에 있으면
        print(ticker + "을 백테스팅 합니다.")
        df_HA = heiken_ashi_jusik(ticker, "us", count)
        df_HA_as = add_signal(df_HA, ticker)
        return df_HA_as

    else:
        print("해당 종목은 목록에 없습니다")
        return 0

def backtest(df_HA_as, name, country):
    if country == "korea" or country == "upbit":
        money = 1000000 # 백만원
    elif country == "usa" or country == "binance":
        money = 1000 #달러
    num = 0 # 매수, 매도 가능한 주식 수
    buyMoney = 0 # 매수한 금액
    sellMoney = 0 # 매도한 금액
    recent_close = 0 # 최근 거래한 종가
    commission = 0  # 누적 수수료

    chk1st = 1  
    for i in range(len(df_HA_as)):
        signal = df_HA_as["signal"].iloc[i]

        if signal == 1:                        # 매수 시그널
            if country == "korea" or country == "usa":
                num = int(money/df_HA_as["Close"].iloc[i])      # 매수가능한 주식수
            elif country == "binance" or country == "upbit":
                num = (money/df_HA_as["Close"].iloc[i])      # 매수가능한 코인수

            buyMoney = num*df_HA_as["Close"].iloc[i]   # 매수한 금액
            money -= buyMoney                # 잔액
            commission = commission + buyMoney*0.0004 # 수수료
            recent_close = df_HA_as["Close"].iloc[i]
            print("종가 " +str(df_HA_as["Close"].iloc[i])+" 매수량 : "+str(num)+ " 매수금액 : "+str(buyMoney) + " 예수금 : "+str(money) + " 총합 : " +str(money + num*recent_close))
            chk1st = 0
        elif signal == 2:                      # 매도 시그널
            if chk1st != 1:                    # 맨처음온게 매도 시그널이면 무시
                sellMoney = num*df_HA_as["Close"].iloc[i]  # 매도한 금액
                money += sellMoney               # 잔액
                commission = commission + sellMoney*0.0004 # 수수료
                recent_close = df_HA_as["Close"].iloc[i]
                print("종가 " +str(df_HA_as["Close"].iloc[i])+ " 매도량 : "+str(num)+ " 매도금액 : "+str(sellMoney) + " 예수금 : "+str(money) + " 총합 : "+str(money) )
                num = 0; buyMoney = 0              # 매수 초기화

    if  country == "korea" or country == "upbit":
        ratio = (money+(num*recent_close)-commission) / 1000000 # 수익률
    elif country == "usa" or country == "binance":
        ratio = (money+(num*recent_close)-commission) / 1000 # 수익률
    
    if ratio > 0 :
        ratio = (ratio - 1) * 100
    elif ratio < 0:
        ratio = (1 - ratio) * 100

    print("\n"+name)
    print(str(df_HA_as.index[0]) + " 부터 " + str(df_HA_as.index[-1]) + " 까지 ")
    print("매수 횟수 : " + str(df_HA_as['signal'].value_counts().loc[1]) + " 매도 횟수 : " + str(df_HA_as['signal'].value_counts().loc[2]))
    print("누적 수수료 : " + str(round(commission,4)) + " 최종 예수금 : " +str(round(money,4)) + " 평가액 : " +str(round(num*recent_close,4)))
    print("최종 수익률 : " + str(round(ratio,4))+"%" + " 총합 : " +str(round(money + num*recent_close - commission,4)))




# 바이낸스 딕셔너리 데이터를 데이터 프레임으로 변환
def dic2df(dic):
    df = pd.DataFrame(dic, columns = ['time', 'open', 'high', 'low', 'close', 'volume'])
    df['time'] = [dt.datetime.fromtimestamp(float(time)/1000) for time in df['time']]
    df.set_index('time', inplace=True)
    return df

# 바낸에서 코인값 불러오기 
def fetch_ohlcvs(coin='BTC/USDT', timeframe='1d', limit=30):
    binance = ccxt.binance()
    now = dt.datetime.utcnow()   # 현재 시간을 millsecond로 변환
    # tck = find_ticker(coin)      # /usdt 붙이기
    ohlcv = binance.fetch_ohlcv(symbol=coin, timeframe=timeframe, limit=limit)   #데이터 불러오기  # 시간간격 :'1m','3m','5m','15m','30m','1h','2h','4h','6h','8h','12h','1d','3d','1w','1M'
    df = dic2df(ohlcv)   # 딕셔너리를 데이터프레임으로 변환
    return df

def heiken_ashi_coin(country ,coin='BTC/USDT', interval='1d', count=60):
    print(coin+ " "+ country+" heiken_ashi")

    if country == "binance":
        df = fetch_ohlcvs(coin, interval, count)
    elif country == "upbit":
        df = pyupbit.get_ohlcv(coin, interval, count)
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


countDay = 100
countH4 = countDay *6
countH1 = countDay *24
countM30 = countDay *48
countM5 = countM30 *6
countM1 = countM5 * 5


haDay = heiken_ashi_coin("upbit", "KRW-BTC", "day", countDay)
haH4 = heiken_ashi_coin("upbit", "KRW-BTC", "minute240", countH4)
haH1 = heiken_ashi_coin("upbit", "KRW-BTC", "minute60", countH1)
haM30 = heiken_ashi_coin("upbit", "KRW-BTC", "minute30", countM30)
haM5 = heiken_ashi_coin("upbit", "KRW-BTC", "minute5", countM5)
haM1 = heiken_ashi_coin("upbit", "KRW-BTC", "minute1", countM1)
