
import pyupbit
import numpy as np
import requests
import time
from requests.models import DEFAULT_REDIRECT_LIMIT
import schedule
from fbprophet import Prophet
from bs4 import BeautifulSoup #웹 크롤링을 위한 라이브러리
import FinanceDataReader as fdr #종목 주가 정보 가져오기
import talib.abstract as ta #기술적 분석을 위한 지표
import datetime as dt
import matplotlib.pyplot as plt
# import yfinance
import mplfinance

# 캔들차트 그리기
def plot_candle_chart(df, title): 
    df["ema"] = df["close"].ewm(span=8, adjust=False).mean()     # 이평선

    adp = [mplfinance.make_addplot(df["ema"], color='green')]
    fig = mplfinance.plot(df, type='candle', style='charles', mav=(20),
                    title=title, ylabel='price', show_nontrading=False, 
                    savefig='jusik.png',
                    addplot=adp)
    plt.show()

coin = "KRW-BTC"
interval = "day"
count = 30
df = pyupbit.get_ohlcv(coin, interval, count)


plot_candle_chart(df, coin)