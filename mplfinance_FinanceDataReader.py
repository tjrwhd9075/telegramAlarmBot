import pandas as pd
from sklearn import preprocessing
import numpy as np
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import mplfinance #캔들 차트 만들기 위한 라이브러리 
from matplotlib import rc
import matplotlib.font_manager as fm

from matplotlib import font_manager
import matplotlib 

matplotlib.font_manager._rebuild()

font_name = fm.FontProperties(fname="C:\\Windows\\Fonts\\NanumMyeongjoBold.ttf").get_name() 
rc('font', family=font_name)

print(fdr.__version__)

# KRX 데이터 가져오기 (KRX는 코스피, 코스닥, 코넥스를 포함)
krx = fdr.StockListing('KRX')
# print(krx.head())

# S&P 전체 종목 정보 가져오기
# sp500 = fdr.StockListing('S&P500')
# print(sp500.head())

# # DataReader 함수 사용하기 ('symbol', '시작날짜', '끝날짜')
# # 국내주식은 가격데이터 사용하기 
# samsungelect = fdr.DataReader( '005930', '2020' ) #삼성전자 종목코드, 2020년부터 현재까지
# # print(samsungelect.head(10))

# 코드 찾기 어려울 경우를 위해 code찾기 만들기
def codefind(name):
    search = list(krx['Name'])
    for i in range(len(krx)):
        if (search[i]==name):
            return krx['Symbol'][i]
# print(codefind('카카오'))

# samsungelect = fdr.DataReader( '005930', '2020')
# # samsungelect['Close'].plot() #아까 만들어준 plot 틀에 close 정보 담기
# # plt.show()

# # 미국 가격의 종목코드는 'AAPL'처럼 되어있음
# apple = fdr.DataReader('AAPL', '2020-01-01','2020-08-01')
# apple.tail()
# apple['Close'].plot()
# plt.show()

#* 한국지수 : KS11 (KOSPI지수), SQ11 (KOSDAQ), KS50 (KOSPI50), KS100 (KOSPI100) ,KRX100 (KRX100), KS200 (코스피200)
#* 미국지수 : DJI (다우존스) , IXIC (나스닥) , US500 (S&P500)
#* 국가별 주요 지수 : JP500 (니케이225선물), STOXX50E(유로스톡스50) , CSI300 (중국), HSI(항셍), FTSE(영국) , DAX(독일), CAC(프랑스)
# KOSPI = fdr.DataReader('KS11', '2019')
# KOSPI.head()
# KOSPI['Close'].plot()
# plt.show()

# 환율
# wondollar = fdr.DataReader('USD/KRW', '2019')
# wondollar['Close'].plot()
# plt.show()

# 비트코인
# bitcoin = fdr.DataReader('BTC/KRW', '2016')
# bitcoin['Close'].plot()


####  봉차트 그리기
SDI = fdr.DataReader(codefind('삼성SDI'), '2021-01-01', '2021-05-31')
mplfinance.plot(SDI, type='candle', style='charles', mav=(5,20,60), volume=True, title='삼성SDI', ylabel='price', show_nontrading=False)
plt.rc
plt.show()


# 봉차트 틀 만들기
# fig = plt.figure(figsize=(12, 8))
# ax = fig.add_subplot(111)
# mpl_finance.candlestick2_ohlc(ax, SDI['Open'], SDI['High'], SDI['Low'], SDI['Close'], width=0.5, colorup='r', colordown='b')
# plt.show()

####  종가 거래량 차트 만들기
# 전체 차트 틀 만들기
# fig = plt.figure(figsize=(12, 8))

# # 위에 차트 / 밑에 차트 만들기
# top_axes = plt.subplot2grid((4,4),(0,0), rowspan=3, colspan=4)
# bottom_axes = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)

# # 윗 차트에 들어갈 정보(캔들 차트)
# mplfinance.candlestick2_ohlc(top_axes, SDI['Open'], SDI['High'], SDI['Low'], SDI['Close'], width=0.5, colorup='r', colordown='b')

# # 범례
# top_axes.legend(loc='best')

# # 밑 차트에 들어갈 정보 (거래량)
# bottom_axes.bar(SDI.index, SDI['Volume'])
# plt.show()