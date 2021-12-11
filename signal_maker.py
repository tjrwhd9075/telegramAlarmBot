from asyncio.windows_events import NULL
from os import close, name
from threading import Thread
from FinanceDataReader import data
from cufflinks.tools import subplots
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
from matplotlib import rc
import matplotlib.font_manager as fm
import mplfinance
import ccxt
import sys
import pandas as pd
import telegram as tel
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ccxt.binance import binance
import plotly
from plotly import subplots
import plotly.offline as plty
import plotly.graph_objs as pltygo
plotly.__version__


# # 보조지표 알리미

# 1. macd, macd 시그널, macd osc, rsi, HA, 이동평균선(8ema, 20ma), 볼린저밴드
# 2. 1일봉, 4시간봉, 1시간봉, 30분봉, 15분봉, 5분봉

# ## 알려주는 타이밍

# 1. 봉 -> 모든지표가 매수 or 매도 방향일때. 
# 2. 모든 봉 -> 한 지표가 모두 똑같은 시그널일때.

# ## 선택해서 보여주기

# 1. 코인 선택
# 2. 봉 / 지표 선택
#  - 봉 -> 해당봉의 모든 지표 표시
#  - 지표 -> 모든 봉의 해당 지표 값 표시

#텔레그램 봇
myToken = '1811197670:AAFGAP3NO6_vJmHeQTURZO-1rAsF3eLdmYQ'
telbot = tel.Bot(token=myToken)
channel_id = "@ha_alarm"                  # 업비트 채널
channel_id_binance = "@ha_alarm_binance"  # 바이낸스
channel_id_feedback = "@ha_alarm_feedback"  # 피드백채널
updater = Updater(myToken, use_context=True)

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
    ''' open, high, low, close, volume'''
    df = pd.DataFrame(dic, columns = ['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    return df

# 과거 데이터 호출
def fetch_ohlcvs(coin='BTC/USDT', timeframe='1d', limit=30):
    '''
     # 시간간격 :'1m','3m','5m','15m','30m','1h','2h','4h','6h','8h','12h','1d','3d','1w','1M'
    '''
    binance = bnc()
    ohlcv = binance.fetch_ohlcv(symbol=coin, timeframe=timeframe, limit=limit)   #데이터 불러오기                                         
    return dic2df(ohlcv)   # 딕셔너리를 데이터프레임으로 변환

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

def Ema(df, span=8):
    '''ema 지수이평선 '''
    df["ema"] = df["close"].ewm(span=span, adjust=False).mean()
    return df

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

def Macd(df, short=12, long=26, signal=9):
    ''' macd, macdSignal, macdOsc'''
    df['macd']=df['close'].ewm( span=short, min_periods= long-1, adjust=False).mean() - df['close'].ewm( span=long, min_periods=long-1, adjust=False).mean()
    df['macdSignal'] = df['macd'].ewm( span = signal, min_periods=signal-1, adjust=False).mean()
    df['macdOsc'] = df["macd"] - df['macdSignal']
    return df

#  - 봉 -> 해당봉의 모든 지표 표시
def display_all_signal(df, name, interval):
    print(name + " "+ interval+ " display_all_signal start")

    df.dropna(inplace=True)         # Na 값 있는 행은 지움

    ohlc = pltygo.Candlestick(x=df.index,
                        open=df['open'],high=df['high'],
                        low=df['low'], close=df['close'],
                        name = 'OHLC',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
    bolUp = pltygo.Scatter(x=df.index, y=df['bolUpper'], name="bolUpper",  mode='lines', line=dict( width=0.8))
    bolLow = pltygo.Scatter(x=df.index, y=df['bolLower'], name="bolLower",  mode='lines',line=dict( width=0.8))
    ma20 = pltygo.Scatter(x=df.index, y=df['20ma'], name="20ma",  mode='lines',line=dict( width=0.8))

    ha = pltygo.Candlestick(x=df.index,
                        open=df['Open'],high=df['High'],
                        low=df['Low'], close=df['Close'],
                        name = 'HA',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
    ema = pltygo.Scatter(x=df.index, y=df['ema'], name="8ema", mode='lines', line=dict( width=0.8))

    macd = pltygo.Scatter( x=df.index, y=df['macd'],  mode='lines',name="MACD") 
    signal = pltygo.Scatter( x=df.index, y=df['macdSignal'], mode='lines', name="Signal") 
    oscillator = pltygo.Bar( x=df.index, y=df['macdOsc'], name="oscillator") 

    rsi = pltygo.Scatter(x=df.index, y=df['rsi'],  mode='lines',name="RSI")
    line30 = pltygo.Scatter(x=df.index, y=df['line30'], name="30", mode='lines',
                            line=dict(color='firebrick', width=0.5))
    line70 = pltygo.Scatter(x=df.index, y=df['line70'], name="70", mode='lines',
                            line=dict(color='royalblue', width=0.5))

    # OHLC + RSI + MACD 차트
    fig1 = subplots.make_subplots(rows=3, cols=1, vertical_spacing=0.05,
                                row_width=[0.4, 0.4,1], shared_xaxes=True, 
                                subplot_titles=('Candle Chart', 'RSI', 'MACD' ))       # row : 행 , col : 열
    # OHLC + HA 차트
    fig2 = subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.05,
                                row_width=[1, 1], shared_xaxes=True, 
                                subplot_titles=('Candle Chart','Heiken Ashi'))       # row : 행 , col : 열

    # fig1 
    setOhlc = [ohlc, bolUp, bolLow, ma20]
    for ohlc in setOhlc: 
        fig1.add_trace(ohlc, 1,1) 
    
    setRsi = [rsi, line30, line70]
    for rsi in setRsi: 
        fig1.add_trace(rsi, 2,1)

    setMacd = [macd, signal, oscillator]
    for macd in setMacd: 
        fig1.add_trace(macd, 3,1) 

    fig1.update_xaxes(rangeslider_thickness = 0)     # 스크롤바 두께
    fig1.update_layout(title_text=name+ " " + interval +" chart")
    fig1.write_image("fig1.png")

    # fig2
    for ohlc in setOhlc: 
        fig2.add_trace(ohlc, 1,1) 

    setHa = [ha, ma20, ema]
    for ha in setHa: 
        fig2.add_trace(ha, 2,1)
    
    fig2.update_xaxes(rangeslider_thickness = 0)     # 스크롤바 두께
    fig2.update_layout(title_text=name+ " " + interval +" chart")
    fig2.write_image("fig2.png")

    print(name + " "+ interval+ " display_all_signal start end")

#  - 지표 -> 모든 봉의 해당 지표 값 표시
def display_all_interval(dfSet,intervalSet, name ,signal):
    '''
    signal : 'ohlc', 'ha', 'macd', 'rsi', 
    '''
    print(name +" " +signal +" display_all_interval start")

    if signal == 'ohlc':
        fig = subplots.make_subplots(rows=len(intervalSet), cols=1, 
                                vertical_spacing=0.05,
                                subplot_titles=intervalSet)
        for i in range(len(intervalSet)):
            dfSet[i].dropna(inplace=True)
            ohlc = pltygo.Candlestick(x=dfSet[i].index,
                        open=dfSet[i]['open'],high=dfSet[i]['high'],
                        low=dfSet[i]['low'], close=dfSet[i]['close'],
                        name =intervalSet[i]+ 'OHLC',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
            fig.add_trace(ohlc, i+1,1) 
            
    if signal == 'ha':
        fig = subplots.make_subplots(rows=len(intervalSet), cols=1, 
                                vertical_spacing=0.05,
                                subplot_titles=intervalSet, )
        for i in range(len(intervalSet)):
            dfSet[i] = Heiken_ashi(dfSet[i])
            dfSet[i].dropna(inplace=True)
            ha = pltygo.Candlestick(x=dfSet[i].index,
                        open=dfSet[i]['Open'],high=dfSet[i]['High'],
                        low=dfSet[i]['Low'], close=dfSet[i]['Close'],
                        name = intervalSet[i]+'HA',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
            fig.add_trace(ha, i+1,1) 
    
    if signal == 'macd':
        fig = subplots.make_subplots(rows=int(len(intervalSet)/2), cols=2, 
                                vertical_spacing=0.05,
                                subplot_titles=intervalSet)

        for i in range(len(intervalSet)):
            dfSet[i] = Macd(dfSet[i])
            dfSet[i].dropna(inplace=True)

            macd = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['macd'],
                                    marker=dict(color='red')) 
            macdSignal = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['macdSignal'], marker=dict(color='blue')) 
            oscillator = pltygo.Bar( x=dfSet[i].index, y=dfSet[i]['macdOsc']) 

            setMacd = [macd, macdSignal, oscillator]
            if i%2 == 0: # 짝수번일때 0,2,4
                for macd in setMacd: 
                    fig.add_trace(macd, int(i/2)+1,1)
            else:
                for macd in setMacd: 
                    fig.add_trace(macd, int(i/2)+1,2)

    if signal == 'rsi':
        fig = subplots.make_subplots(rows=int(len(intervalSet)/2), cols=2, 
                                vertical_spacing=0.05,
                                subplot_titles=intervalSet)

        for i in range(len(intervalSet)):
            dfSet[i] = Rsi(dfSet[i])
            dfSet[i].dropna(inplace=True)

            rsi = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['rsi'], marker=dict(color='black')) 
            line30 = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['line30'], marker=dict(color='blue')) 
            line70 = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['line70'], marker=dict(color='red')) 

            setRsi = [rsi, line30, line70]
            if i%2 == 0: # 짝수번일때 0,2,4
                for rsi in setRsi: 
                    fig.add_trace(rsi, int(i/2)+1,1)
            else:
                for rsi in setRsi: 
                    fig.add_trace(rsi, int(i/2)+1,2)

    fig.update_xaxes(rangeslider_thickness = 0)     # 스크롤바 두께
    fig.update_layout(title_text=name+ " " + signal +" chart")
    if signal == 'ha' or signal == 'ohlc':
        fig.update_annotations(yshift=-20,xshift=300)
    else:
        fig.update_annotations(yshift=-20,xshift=-160)    # 서브차트 제목 위치
    fig.update_layout(showlegend=False)             # 범례 안보이게
    fig.write_image("fig3.png")
        
    print(name + ' ' + signal + ' display_all_interval end')
    
# 시그널 메이커
def signal_maker(df):
    print("signal maker start")
    buyCnt = 0
    sellCnt= 0
    txt = []
    
    ### macd
    if df['macd'].iloc[-2] < df['macdSignal'].iloc[-2] and df['macd'].iloc[-1] > df['macdSignal'].iloc[-1]:
        print("macd 골든크로스 : 강한매수 신호")
        txt.append("macd 골든크로스 : 강한매수 신호")
        buyCnt += 2
    elif df['macd'].iloc[-2] > df['macdSignal'].iloc[-2] and df['macd'].iloc[-1] < df['macdSignal'].iloc[-1]:
        print("macd 데드크로스 : 강한매도 신호")
        txt.append("macd 데드크로스 : 강한매도 신호")
        sellCnt -= 2
    
    # 매수	
    if df['macd'].iloc[-1] > df['macdSignal'].iloc[-1] and df['macd'].iloc[-2] < df['macd'].iloc[-1]:
        print("macd 상향중 : 매수")
        txt.append("macd 상향중 : 매수")
        buyCnt += 1
    # 중립	
    elif df['macd'].iloc[-1] > df['macdSignal'].iloc[-1] and df['macd'].iloc[-2] > df['macd'].iloc[-1]:
        print("macd 상향중, 방향꺾임 : 중립")
        txt.append("macd 상향중, 방향꺾임 : 중립")
    elif df['macd'].iloc[-1] < df['macdSignal'].iloc[-1] and df['macd'].iloc[-2] < df['macd'].iloc[-1]:
        print("macd 하향중, 방향꺾임 : 중립")
        txt.append("macd 하향중, 방향꺾임 : 중립")
    # 매도
    elif df['macd'].iloc[-1] < df['macdSignal'].iloc[-1] and df['macd'].iloc[-2] > df['macd'].iloc[-1]:
        print("macd 하향중 : 매도")
        txt.append("macd 하향중 : 매도")
        sellCnt -= 1

    # ## macd osc
    if df['macdOsc'].iloc[-2] < df['macdOsc'].iloc[-1] :
        if df['macdOsc'].iloc[-2] < 0 and df['macdOsc'].iloc[-1] > 0 :
            print("macd osc 0선 상향돌파 : 강한매수 신호")
            txt.append("macd osc 0선 상향돌파 : 강한매수 신호")
            buyCnt += 3
        else:
            print("macd osc 상승중 : 매수")
            txt.append("macd osc 상승중 : 매수")
            buyCnt += 1
    elif df['macdOsc'].iloc[-2] > df['macdOsc'].iloc[-1] :
        if df['macdOsc'].iloc[-2] < 0 and df['macdOsc'].iloc[-1] > 0 :
            print("macd osc 0선 하향돌파 : 강한매도 신호")
            txt.append("macd osc 0선 하향돌파 : 강한매도 신호")
            sellCnt -= 3
        else:
            print("macd osc 하락중 : 매도")
            txt.append("macd osc 하락중 : 매도")
            sellCnt -= 1

    # ## rsi
    if df['rsi'].iloc[-1] < 31 :
        print("rsi 30 이하 : 매수")
        txt.append("rsi 30 이하 : 매수")
        buyCnt += 1
    elif df['rsi'].iloc[-1] > 69 :
        print("rsi 70 이상 : 매도")
        txt.append("rsi 70 이상 : 매도")
        sellCnt -= 1
    else:
        print("30< rsi <70 : 중립")
        txt.append("30< rsi <70 : 중립")

    if df['rsi'].iloc[-2] < 31 and df['rsi'].iloc[-2] < df['rsi'].iloc[-1]:
        print("rsi 30이하 반등 : 강한매수 신호")
        txt.append("rsi 30이하 반등 : 강한매수 신호")
        buyCnt += 2
    elif df['rsi'].iloc[-2] > 69 and df['rsi'].iloc[-2] > df['rsi'].iloc[-1]:
        print("rsi 70이상 꺾임 : 강한매도 신호")
        txt.append("rsi 70이상 꺾임 : 강한매도 신호")
        sellCnt -= 2

    # ## Heiken ashi
    if df['Open'].iloc[-1] < df['Close'].iloc[-1]:
        if df['Open'].iloc[-2] > df['Close'].iloc[-2]:
            print("HA 양봉전환 : 강한매수 신호")
            txt.append("HA 양봉전환 : 강한매수 신호")
            buyCnt += 3
        else:
            print("HA 양봉 : 매수")
            txt.append("HA 양봉 : 매수")
            buyCnt += 1
    elif df['Open'].iloc[-1] > df['Close'].iloc[-1]:
        if df['Open'].iloc[-2] < df['Close'].iloc[-2]:
            print("HA 음봉전환 : 강한매도 신호")
            txt.append("HA 음봉전환 : 강한매도 신호")
            sellCnt -= 3
        else:
            print("HA 음봉 : 매도")
            txt.append("HA 음봉 : 매도")
            sellCnt -= 1

    # ## 볼린저밴드
    if df['close'].iloc[-1] < df['bolLower'].iloc[-1] :
        print("볼밴 하한 미만 : 매수")
        txt.append("볼밴 하한 미만 : 매수")
        buyCnt += 1
    elif df['close'].iloc[-1] > df['bolUpper'].iloc[-1] :
        print("볼밴 상한 초과 : 매도")
        txt.append("볼밴 상한 초과 : 매도")
        sellCnt -= 1
    else:
        print("볼밴 내 : 중립")
        txt.append("볼밴 내 : 중립")

    if df['close'].iloc[-2] < df['bolLower'].iloc[-2] and df['open'].iloc[-1] < df['close'].iloc[-1]:
        print("볼밴 하한 반등 : 강한매수 신호")
        txt.append("볼밴 하한 반등 : 강한매수 신호")
        buyCnt += 3
    elif df['close'].iloc[-2] > df['bolUpper'].iloc[-2] and df['open'].iloc[-1] > df['close'].iloc[-1]:
        print("볼밴 상한 조정 : 강한매도 신호")
        txt.append("볼밴 상한 조정 : 강한매도 신호")
        sellCnt -= 3
    

    # ## 이동평균선 8ema, 20ma
    if df['ema'].iloc[-1] > df['20ma'].iloc[-1] and df['ema'].iloc[-2] < df['ema'].iloc[-1] and df['20ma'].iloc[-2] < df['20ma'].iloc[-1]:
        print("ma < ema 상향중 : 매수")
        txt.append("ma < ema 상향중 : 매수")
        buyCnt += 1
    elif df['ema'].iloc[-1] < df['20ma'].iloc[-1] and df['ema'].iloc[-2] > df['ema'].iloc[-1] and df['20ma'].iloc[-2] > df['20ma'].iloc[-1]:
        print("ma < ema 하향중 : 매도")
        txt.append("ma < ema 하향중 : 매도")
        sellCnt -= 1
    else:
        print("ma, ema : 중립")
        txt.append("ma, ema : 중립")

    if df['ema'].iloc[-2] < df['20ma'].iloc[-2] and df['ema'].iloc[-1] > df['20ma'].iloc[-1]:
        print("ma < ema 골든크로스 : 강한매수 신호")
        txt.append("ma < ema 골든크로스 : 강한매수 신호")
        buyCnt += 2
    elif df['ema'].iloc[-2] > df['20ma'].iloc[-2] and df['ema'].iloc[-1] < df['20ma'].iloc[-1]:
        print("ma > ema 데드크로스 : 강한매도 신호")
        txt.append("ma > ema 데드크로스 : 강한매도 신호")
        sellCnt -= 2

    txt.append(buyCnt + sellCnt)
    
    temp = ""
    for t in txt:
        if str(type(t)) == "<class 'int'>":
            if t > 0 :
                temp = temp + "** 매수 우위 : " + str(t)
            elif t < 0 :
                temp = temp + "** 매도 우위 : " + str(t)
            else :
                temp = temp + "** 중립 : " + str(t)
        else:
            temp = temp + t + "\n"

    print("signal maker end")
    return temp
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

coin = 'BTC/USDT'
interval = '1d'
# intervalSet = ('5m', '15m', '30m', '1h', '4h', '1d')
count = 50
# dfSet = []
# for interval in intervalSet:
#     df = fetch_ohlcvs(coin, interval, count)
#     dfSet.append(df)
# display_all_interval(dfSet, intervalSet, coin, 'rsi')



df = fetch_ohlcvs(coin, interval, count)
df = Macd(df)
df = BolingerBand(df)
df = Rsi(df)
df = Ema(df)
df = Heiken_ashi(df)
txt = signal_maker(df)
telbot.sendMessage(chat_id=channel_id_feedback, text="## binance "+coin+ " "+interval+" ##\n"+ txt)
    
display_all_signal(df, coin, interval)
telbot.send_photo(chat_id=channel_id_feedback, photo=open('fig1.png', 'rb'))
telbot.send_photo(chat_id=channel_id_feedback, photo=open('fig2.png', 'rb'))












