import datetime as dt

#===========================================================================================

import telegram as tel  # pip install python-telegram-bot --upgrade
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

#텔레그램 봇
myToken = '1811197670:AAFaSU2l8pKxT6tDA3tOl2Tpue-OiNC1Af0'
telbot = tel.Bot(token=myToken)
myBotName = "alarm_haBot"
updater = Updater(myToken, use_context=True)

#텔레그램 채널
channel_id_korea = "@ha_alarm_korea"  

#===========================================================================================

import FinanceDataReader as fdr #pip install finance-datareader --upgrade
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

import numpy as np
import plotly
from plotly import plot, subplots
import plotly.offline as plty
import plotly.graph_objs as pltygo
import asyncio
import watchlist
import stockchart as sc
import time

# 한국 코스피,코스닥 목록
krx = fdr.StockListing('KRX')
# 미국 주식 목록
sp500 = fdr.StockListing('S&P500')
nasdaq = fdr.StockListing('NASDAQ')
nyse = fdr.StockListing('NYSE')

# 코드 찾기 어려울 경우를 위해 code찾기 만들기
def codefind(name, country):
    ''' country : "krx", "us "'''
    if country == "krx" :
        search = list(krx['Name'])
        for i in range(len(krx)):
            if (search[i]==name):
                return krx['Symbol'][i]
    elif country == "us" :
        search = list(sp500['Name'])
        search2 = list(nasdaq['Symbol'])
        search3 = list(nyse['Symbol'])
        for i in range(len(sp500)):
            if (search[i]==name):
                return sp500['Symbol'][i]
        for i in range(len(nasdaq)):
            if (search2[i]==name):
                return nasdaq['Name'][i]
        for i in range(len(nyse)):
            if (search3[i]==name):
                return nyse['Name'][i] 
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

#주식데이터 불러오기
def fetch_jusik(name, country, count):
    ''' country : krx, us'''
    today = dt.date.today()
    delta = dt.timedelta(days=count)    # count 봉 전부터
    past = today-delta

    if country == "krx":
        df = fdr.DataReader(codefind(name, "krx"), past, today)
    elif country == "us":
        df = pdr.get_data_yahoo(name, past, today)

    df.rename(columns = {'Open' : 'open', "Close" : "close", "High" : "high", "Low":"low","Volume":"volume"}, inplace = True)
    return df 

#dataframe에 지표 추가하기
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
def Macd(df, short=12, long=26, signal=9):
    ''' macd, macdSignal, macdOsc'''
    df['macd']=df['close'].ewm( span=short, min_periods= long-1, adjust=False).mean() - df['close'].ewm( span=long, min_periods=long-1, adjust=False).mean()
    df['macdSignal'] = df['macd'].ewm( span = signal, min_periods=signal-1, adjust=False).mean()
    df['macdOsc'] = df["macd"] - df['macdSignal']
    return df
def ichimoku(df):
    '''
    tenkan, kijun, senkouSpanA, senkouSpanB, chikouSpan
    '''
    high_prices = df['high']
    close_prices = df['close']
    low_prices = df['low']
    dates = df.index
    
    nine_period_high =  df['high'].rolling(window=9).max()
    nine_period_low = df['low'].rolling(window=9).min()
    df['tenkan'] = (nine_period_high + nine_period_low) /2  #전환선
    
    period26_high = high_prices.rolling(window=26).max()
    period26_low = low_prices.rolling(window=26).min()
    df['kijun'] = (period26_high + period26_low) / 2    #기준선
    
    df['senkouSpanA'] = ((df['tenkan'] + df['kijun']) / 2).shift(26)  #선행스팬A
    
    period52_high = high_prices.rolling(window=52).max()
    period52_low = low_prices.rolling(window=52).min()
    df['senkouSpanB'] = ((period52_high + period52_low) / 2).shift(26)   #선행스팬B
    
    df['chikouSpan'] = close_prices.shift(-26)    #후행스팬

    return df

# rsi반등신호, MACD저점반등신호, HA전환신호, 5일고점돌파신호, 기준선 돌파신호
def signal_maker2(df):
    buyCnt = 0
    txt = []
    # 1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟
    
    # ## macd oscㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['macdOsc'].iloc[-2] < 0 and df['macdOsc'].iloc[-2] < df['macdOsc'].iloc[-1] : # 1봉전 < 0봉전
        if df['macdOsc'].iloc[-3] > df['macdOsc'].iloc[-2] : # 2봉전 > 1봉전
            txt.append("❤️. 〰️MACD OSC : 저점반등↘️↗️ ")
            buyCnt += 1

    # ## rsiㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

    if df['rsi'].iloc[-2] < 31 and df['rsi'].iloc[-2] < df['rsi'].iloc[-1]:
        txt.append("❤️. 〰️RSI : ↘️30이하↗️ 반등")
        buyCnt += 1
    elif df['rsi'].iloc[-1] < 31 :
        txt.append("❤️. 〰️RSI : 30이하⬇️")
        buyCnt += 1

    # ## Heiken ashiㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['Open'].iloc[-1] < df['Close'].iloc[-1]:
        if df['Open'].iloc[-2] > df['Close'].iloc[-2]:
            txt.append("❤️. 〰️HA : 양봉전환↘️↗️ ")
            buyCnt += 1
    
    # 5일 최고점 돌파ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['high'].iloc[-1] > df['high'].iloc[-2] and df['high'].iloc[-1] > df['high'].iloc[-3] and df['high'].iloc[-1] > df['high'].iloc[-4] and df['high'].iloc[-1] > df['high'].iloc[-5] and df['high'].iloc[-1] > df['high'].iloc[-6]:
        if df['close'].iloc[-1] > df['open'].iloc[-1]: # 5일 최고점, 양봉일때
            txt.append("❤️. 〰️5일 최고점 돌파")
            buyCnt += 1
            
    
    ## 일목기준표
    if df['close'].iloc[-2] < df['kijun'].iloc[-2] and df['close'].iloc[-1] > df['kijun'].iloc[-1]:
        txt.append("❤️. 〰️일목 : 기준선 상향돌파⬆️")
        buyCnt += 1 

    txt.append(buyCnt)
    return txt

#  - 봉 -> 해당봉의 모든 지표 표시
def display_all_signal(df, name, interval):
    # df.dropna(inplace=True)         # Na 값 있는 행은 지움
    df = df.rename_axis("Date").reset_index()
    # print(df.head)
    if name == "KRW-BTC" or name == "KRW-ETH" or name == "BTC/USDT" or name == "ETH/USDT":
        df['Date'] = df['Date'].apply(lambda x : dt.datetime.strftime(x, '%y-%m-%d %H:%M')) # Datetime to str
    else:
        df['Date'] = df['Date'].apply(lambda x : dt.datetime.strftime(x, '%y-%m-%d')) # Datetime to str
    df_date = df['Date']
    
    ha = pltygo.Candlestick(x=df_date,
                        open=df['Open'],high=df['High'],
                        low=df['Low'], close=df['Close'],
                        name = 'HA',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
    ema = pltygo.Scatter(x=df_date, y=df['ema'], name="8ema", mode='lines', line=dict(color="green", width=0.8))

    macd = pltygo.Scatter( x=df_date, y=df['macd'],  mode='lines',name="MACD") 
    signal = pltygo.Scatter( x=df_date, y=df['macdSignal'], mode='lines', name="Signal") 
    oscillator = pltygo.Bar( x=df_date, y=df['macdOsc'], name="oscillator") 

    rsi = pltygo.Scatter(x=df_date, y=df['rsi'],  mode='lines',name="RSI")
    line30 = pltygo.Scatter(x=df_date, y=df['line30'], name="30", mode='lines',
                            line=dict(color='firebrick', width=0.5))
    line70 = pltygo.Scatter(x=df_date, y=df['line70'], name="70", mode='lines',
                            line=dict(color='royalblue', width=0.5))

    # ichimoku
    kijun = pltygo.Scatter(x=df_date, y=df['kijun'], name="kijun",  mode='lines', line=dict(color='gray', width=2))
    tenkan = pltygo.Scatter(x=df_date, y=df['tenkan'], name="tenkan",  mode='lines',line=dict(color='red', width=2))
    senkouSpanA = pltygo.Scatter(x=df_date, y=df['senkouSpanA'], name="spanA",  mode='lines',line=dict(color='rgba(167, 59, 206, 0.9)', width=0.8),fill=None)#'tonexty',fillcolor ='rgba(235, 233, 102, 0.5)'
    senkouSpanB = pltygo.Scatter(x=df_date, y=df['senkouSpanB'], name="spanB",  mode='lines',line=dict(color='green', width=0.8),fill='tonexty',fillcolor ='rgba(111, 236, 203, 0.5)')


    ohlc = pltygo.Candlestick(x=df_date,
                        open=df['open'],high=df['high'],
                        low=df['low'], close=df['close'],
                        name = 'OHLC',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
    bolUp = pltygo.Scatter(x=df_date, y=df['bolUpper'], name="bolUpper",  mode='lines', line=dict(color='black', width=1))
    bolLow = pltygo.Scatter(x=df_date, y=df['bolLower'], name="bolLower",  mode='lines',line=dict(color='black', width=1))
    ma20 = pltygo.Scatter(x=df_date, y=df['20ma'], name="20ma",  mode='lines',line=dict(color='orange', width=0.8))


    # OHLC,일목 차트
    fig1 = subplots.make_subplots(rows=1, cols=1, shared_xaxes=True,
                                subplot_titles=('ichimoku Chart, kijun : '+str(format(round(df['kijun'].iloc[-1],2),',')),""))       # row : 행 , col : 열

    # HA 차트 + 20ma 8ema
    fig2 = subplots.make_subplots(rows=1, cols=1, shared_xaxes=True,
                                subplot_titles=('Heiken Ashi, close : '+str(format(round(df['close'].iloc[-1],2),',')),""))       # row : 행 , col : 열

    # OHLC,볼밴 + RSI + MACD 차트
    fig3 = subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.05,
                                row_width=[1,1], shared_xaxes=True, 
                                subplot_titles=('RSI : '+str(round(df['rsi'].iloc[-1],2)), 'MACD' ))       # row : 행 , col : 열
    

    # fig3 
    # setOhlc = [ohlc, bolUp, bolLow, ma20]
    # for ohlc_ in setOhlc: 
    #     fig1.add_trace(ohlc_, 1,1) 

    
    
    setRsi = [rsi, line30, line70]
    for rsi in setRsi: 
        fig3.add_trace(rsi, 1,1)

    setMacd = [macd, signal, oscillator]
    for macd in setMacd: 
        fig3.add_trace(macd, 2,1) 

    fig3.update_xaxes(rangeslider_thickness = 0, nticks = 5, type='category')     # 스크롤바 두께
    fig3.update_layout(title_text=name+ " " + interval +" chart", showlegend=False)
    fig3.update_yaxes(side="right")
    # fig3.update_layout(legend=dict(yanchor="top", y=1, xanchor="left", x=0))
    fig3.write_image("fig3.png")

    # fig2

    setHa = [ha, ma20, ema]
    for ha in setHa: 
        fig2.add_trace(ha, 1,1)
    
    fig2.update_xaxes(rangeslider_thickness = 0, nticks = 5, type='category')     # 스크롤바 두께
    fig2.update_layout(title_text=name+ " " + interval +" chart", showlegend=False)
    fig2.update_yaxes(side="right", nticks =10)
    # fig2.update_layout(legend=dict(yanchor="top", y=1, xanchor="left", x=0))
    fig2.write_image("fig2.png")

    # fig1

    setIchimoku = [ohlc, senkouSpanA, senkouSpanB, kijun]
    for ichi in setIchimoku: 
        fig1.add_trace(ichi, 1,1)
    
    fig1.update_xaxes(rangeslider_thickness = 0, nticks = 5, type='category')     # 스크롤바 두께
    fig1.update_layout(title_text=name+ " " + interval +" chart", showlegend=False)
    fig1.update_yaxes(side="right", nticks =10)
    fig1.update_layout(legend=dict(yanchor="top", y=1, xanchor="left", x=0))
    fig1.write_image("fig1.png")

#async def krx_bs_check():
def krx_bs_check():
    jongmok = watchlist.get_querys('korea_watchlist.txt')
    for token in jongmok: # krx
        print(token)
        df = fetch_jusik(token, "krx", 120)
        df = Macd(df)
        df = BolingerBand(df)
        df = Rsi(df)
        df = Ema(df)
        df = Heiken_ashi(df)
        df = ichimoku(df)
        txt = signal_maker2(df)

        temp = ""
        for t in txt:
            if str(type(t)) == "<class 'int'>":
                temp = temp + "\n총점 : ❤️ " + str(t)
            else:
                temp = temp + t + "\n"

        if txt[0] == "❤️. 〰️MACD OSC : 저점반등↘️↗️ ":
            display_all_signal(df, token, "1day")
            telbot.send_photo(chat_id=channel_id_korea, photo=open('fig1.png', 'rb'))
            telbot.send_photo(chat_id=channel_id_korea, photo=open('fig2.png', 'rb'))
            telbot.send_photo(chat_id=channel_id_korea, photo=open('fig3.png', 'rb'), caption="💲💲 "+ token + " 1일봉 💲💲\n" +temp)  
            time.sleep(5)

def us_bs_check():
    jongmok2 = watchlist.get_querys('usa_watchlist.txt')     

    for token in jongmok2: #us
        print(token)
        
        try:
            df = fetch_jusik(token, "us", 120)
            df = Macd(df)
            df = BolingerBand(df)
            df = Rsi(df)
            df = Ema(df)
            df = Heiken_ashi(df)
            df = ichimoku(df)
            txt = signal_maker2(df)

            temp = ""
            for t in txt:
                if str(type(t)) == "<class 'int'>":
                    temp = temp + "\n총점 : ❤️ " + str(t)
                else:
                    temp = temp + t + "\n"

            if txt[0] == "❤️. 〰️MACD OSC : 저점반등↘️↗️ ":
                sc.get_stockchart(token,"DETAIL")
                telbot.send_photo(chat_id=channel_id_korea, photo=open('sc.png', 'rb'), caption="💲💲 "+ token + " 1일봉 💲💲\n")
                # display_all_signal(df, token, "1day")
                # telbot.send_photo(chat_id=channel_id_korea, photo=open('fig1.png', 'rb'))
                # telbot.send_photo(chat_id=channel_id_korea, photo=open('fig2.png', 'rb'))
                # telbot.send_photo(chat_id=channel_id_korea, photo=open('fig3.png', 'rb'), caption="💲💲 "+ token + " 1일봉 💲💲\n" +temp)  
        except Exception as e:
            print(e)
            print("왜 에러뜨냐 쓰벌")

#===========================================================================================

#바이낸스키
myApikey = "hOpHmrM35aqoqakISj0m7PAy42bDLXBmhXIrOsvadPBU6bW8Gtin0ggp7UnzFg9f"
mySecretkey = "rJp7j47DyzzvqRhaa9ExusnxrcPSF2I6Aa1B6bNvjlzxv3VP7fs3sl3cMNvSbEdU"

#사진 파일 이름
image = "jusik.png"

#===========================================================================================

from threading import Thread
import schedule

# schedule.every().day.at("15:30").do(lambda:krx_bs_check())
# krx_bs_check()
us_bs_check()

while True:
    try:
        schedule.run_pending()
    except Exception as e:   # 에러 발생시 예외 발생
        print(e)
        print("쓰레드 에러발생")

# 매일 정해진 시간에
# schedule.every().day.at("16:00").do(lambda:asyncio.run(krx_bs_check()))
# asyncio.run(krx_bs_check())
# krx_bs_check()
