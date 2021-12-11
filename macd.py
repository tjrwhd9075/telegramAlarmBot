from matplotlib.pyplot import fill_between
import pyupbit
import numpy as np
import requests
import time

import mplfinance

token = "KRW-BTC"
interval = "minutes60"
count = 100
period = 14
 
df = pyupbit.get_ohlcv(token, interval, count=count)


# 캔들차트 그리기
def plot_candle_chart_ichimoku(df, title):  
    
    adp1 = [mplfinance.make_addplot(df["kijun"], color='gray')]  # 기준선
    adp2 = [mplfinance.make_addplot(df["tenkan"], color='red')]  # 전환선
    adp3 = [mplfinance.make_addplot(df["senkouSpanA"], color='green')]  # 선행A
    adp4 = [mplfinance.make_addplot(df["senkouSpanB"], color='green')]  # 선행B
    fig = mplfinance.plot(df, type='candle', style='charles',
                    title=title, ylabel='price', show_nontrading=False,
                    savefig='jusik.png',
                    addplot= adp1 + adp2 +adp3+adp4,
                    block=False,
                    fill_between = dict(y1=df['senkouSpanA'].values, y2=df['senkouSpanB'].values, color='#f2ad73', alpha=0.20)
                    )
    
    print(title + " plot candle chart")

def RSI(df, token, period=14):
    df['U'] = np.where(df.diff(1)['close'] > 0, df.diff(1)['close'], 0)  # df.diff(1) : 기준일 종가 - 전일 종가, 0보다 크면 증가분을, 아니면 0을 넣음
    df['D'] = np.where(df.diff(1)['close'] < 0, df.diff(1)['close']*(-1), 0) # 기준일 종가 - 전일 종가, 0보다 작으면 감소분을, 아니면 0을 넣음
    df['AU'] = df['U'].rolling(window=period).mean() # period=14 동안의 U의 (이동)평균
    df['AD'] = df['D'].rolling(window=period).mean() # period=14 동안의 D의 (이동)평균
    df['RSI'] = df['AU'] / (df['AD']+df['AU']) * 100
    return df

def MACD(df, short=12, long=26, signal=9):
    df['MACD']=df['close'].ewm( span=short, min_periods= long-1, adjust=False).mean() - df['close'].ewm( span=long, min_periods=long-1, adjust=False).mean()
    df['MACD_Signal'] = df['MACD'].ewm( span = signal, min_periods=signal-1, adjust=False).mean()
    df['MACD_OSC'] = df["MACD"] - df['MACD_Signal']
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


rsi = RSI(df, token, period)
rsi_macd = MACD(rsi)
ichimoku = ichimoku(rsi_macd)

plot_candle_chart_ichimoku(df,token)

# 엑셀에 저장
# df.to_excel("ichimoku.xlsx")