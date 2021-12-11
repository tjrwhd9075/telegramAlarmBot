import matplotlib.pyplot as plt #시각화
import pandas as pd  #데이터 전처리 및 저장, 불러오기
import requests #호출하기 위한 라이브러리
from bs4 import BeautifulSoup #웹 크롤링을 위한 라이브러리
import FinanceDataReader as fdr #종목 주가 정보 가져오기
import numpy as np
import talib.abstract as ta #기술적 분석을 위한 지표
import datetime as dt

# 한국 코스피,코스닥 목록
krx = fdr.StockListing('KRX')
# # 미국 주식 목록
sp500 = fdr.StockListing('S&P500')
nasdaq = fdr.StockListing('NASDAQ')
nyse = fdr.StockListing('NYSE')
# us = pd.concat([sp500, nasdaq, nyse])


# 코드 찾기 어려울 경우를 위해 code찾기 만들기
def codefind(name, country):
    if country == "krx" :
        search = list(krx['Name'])
        for i in range(len(krx)):
            if (search[i]==name):
                return krx['Symbol'][i]
    elif country == "sp500" :
        search = list(sp500['Name'])
        for i in range(len(sp500)):
            if (search[i]==name):
                return sp500['Symbol'][i]
    else :
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

jongmok = {"삼성전자", "SK하이닉스", "현대바이오", "카카오", "NAVER", "LG디스플레이", 
"DB하이텍", "LG화학", "LG전자", "삼성SDI", "현대차", "현대모비스", "기아","천보", 
"두산퓨얼셀", "JYP Ent.", "와이지엔터테인먼트", "대원미디어", "펄어비스", "스튜디오드래곤", 
"하이브", "한화솔루션", "씨에스윈드", "씨에스베어링", "대한항공","HMM","SK이노베이션", "KODEX 자동차",
"네비게이터 친환경자동차밸류체인액티브", "TIGER KRX BBIG K-뉴딜", "KBSTAR Fn수소경제테마", "TIGER KRX2차전지K-뉴딜",
"TIGER TOP10", "TIGER 금은선물(H)", "KODEX 바이오", "TIGER KRX바이오K-뉴딜", "TIGER 여행레저", "TIGER 우량가치", "TIGER 경기방어", "TIGER 가격조정"
}
jongmok2 = {"PFE", "PINS", "F", "PYPL", "FB", "NVDA", "CCL", "GM", "SNAP", "SNOW", "GOOGL", "KO", "GS",
"NET", "BRK", "AXP", "BLK", "ATVI", "SPCE", "DPZ","LMT", "MO", "BAC" ,"MSFT","AMZN", "V", "JNJ", "AMD", 
"AAPL", "SHOP", "ADBE","NKE","QCOM", "ZM","REAL","UAL","INTC","DIS","TWTR","UBER","NFLX","Z","U", "MRNA", 
"TSLA", "TSM", "ASML"}

today = dt.date.today()
delta = dt.timedelta(days=100)    # N일 전
past = today-delta

# 데이터 불러오기
print("@@@@@@@@@@ KOREA @@@@@@@@@ ")
for jm in jongmok:
    try:
        df = fdr.DataReader(codefind(jm, "krx"), past, today )
        print(jm + codefind(jm, "krx"))

        # MACD 
        macd, macdsignal, macdhist = ta.MACD(df['Close'], 12, 26, 9)
        df['macd'] = macd
        df['macd_signal'] = macdsignal
        df['macdhist'] = macdhist

        #rsi
        # df['rsi14'] = ta.RSI(df['Close'],14)

        # if df['rsi14'].iloc[-1] < 30 :
        #     print(jm +" rsi : " + str(df['rsi14'].iloc[-1]))
        # if df['macdhist'].iloc[-1] < 0 :
        #     print(jm +" macd osc : " + str(df['macdhist'].iloc[-1]))
        if df['macdhist'].iloc[-2] < 0 and df['macdhist'].iloc[-1] > 0 :
            print(jm +" macd osc : " + str(df['macdhist'].iloc[-2]))
            print(jm +" macd osc : " + str(df['macdhist'].iloc[-1]))

    except Exception as e:
        print(e)

print("@@@@@@@@@@ USA @@@@@@@@@ ")
for jm in jongmok2:

    df = fdr.DataReader(jm, past, today )

    # MACD 
    macd, macdsignal, macdhist = ta.MACD(df['Close'], 12, 26, 9)
    df['macd'] = macd
    df['macd_signal'] = macdsignal
    df['macdhist'] = macdhist

    #rsi
    df['rsi14'] = ta.RSI(df['Close'],14)

    if df['rsi14'].iloc[-1] < 30 :
        print(jm +" rsi : " + str(round(df['rsi14'].iloc[-1],2)) +" "+ namefind(jm))
    if df['macdhist'].iloc[-1] < 0 :
        print(jm +" macd osc : " + str(round(df['macdhist'].iloc[-1],2)) +" "+ namefind(jm))
    if df['macdhist'].iloc[-2] < 0 and df['macdhist'].iloc[-1] > 0 :
        print(jm +" macd osc : " + str(df['macdhist'].iloc[-2]) +" "+ namefind(jm))
        print(jm +" macd osc : " + str(df['macdhist'].iloc[-1]) +" "+ namefind(jm))



# # 차트 틀
# # plt.rcParams["font.family"] = 'NanumSquare' #글씨체 선택
# plt.rcParams["figure.figsize"] = (14,10) #전체 크기 
# plt.rcParams['lines.linewidth'] = 1.7 #선 굵기
# plt.rcParams['axes.grid'] = True #눈금선

# # 종가 시각화
# plt.subplot(3,1,1)
# plt.plot(df['Close'])

# #MACD 시각화
# plt.subplot(3,1,2)
# #plt.axhline(y=0, color = 'black') 
# plt.plot(df.index, df['macd'], "r-")
# plt.plot(df.index, df['macd_signal'], "b-")
# plt.bar(df.index, macdhist, alpha = 0.5)

# # rsi 시각화
# plt.subplot(3,1,3)
# plt.plot(df['rsi14'])
# plt.axhline(y=30, color = 'b', linewidth =1) 
# plt.axhline(y=70, color = 'r',linewidth = 1) 

# print(df)
# plt.show()



# 관심종목들... 
# 1. osc(macdhist) 가 마이너스인 종목 (5일 연속??)
# 2. rsi가 30이하인 종목
# => slack 