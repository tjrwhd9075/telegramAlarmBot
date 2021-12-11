import pyupbit
import numpy as np
import requests
import time
import schedule
from fbprophet import Prophet
from bs4 import BeautifulSoup #웹 크롤링을 위한 라이브러리
import FinanceDataReader as fdr #종목 주가 정보 가져오기
import talib.abstract as ta #기술적 분석을 위한 지표
import datetime as dt

# 업비트 계좌
access = "Ig2xbjz67PIQIUWAQmkVU1opIwDMx1BUDtH1cX3d"
secret = "GqzXn8SepGJxh7ThAXPI4xc7UH1tFW8HbpPs2odR"
# 로그인
upbit = pyupbit.Upbit(access, secret)

# slack 봇
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)
myToken = "xoxb-2014329623457-2007907637812-E5pghvrBjFUhYOfJkJVnfIQO"

# 한국 코스피,코스닥 목록
krx = fdr.StockListing('KRX')
# 미국 주식 목록
sp500 = fdr.StockListing('S&P500')
nasdaq = fdr.StockListing('NASDAQ')
nyse = fdr.StockListing('NYSE')

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
"하이브", "한화솔루션", "씨에스윈드", "씨에스베어링", "대한항공","HMM","SK이노베이션", "삼성엔지니어링",
"더네이쳐홀딩스", "BGF", "이마트", "신세계", "빙그레", "신풍제약", "아이진", "위메이드", "데브시스터즈", "강원랜드",
"롯데칠성", "KODEX 자동차", "네비게이터 친환경자동차밸류체인액티브", "TIGER KRX BBIG K-뉴딜", 
"KBSTAR Fn수소경제테마", "TIGER KRX2차전지K-뉴딜","TIGER TOP10", "TIGER 금은선물(H)", "KODEX 바이오", 
"TIGER KRX바이오K-뉴딜", "TIGER 여행레저", "TIGER 우량가치", "TIGER 경기방어"}
jongmok2 = {"PFE", "PINS", "F", "PYPL", "FB", "NVDA", "CCL", "GM", "SNAP", "SNOW", "GOOGL", "KO", "GS",
"NET", "BRK", "AXP", "BLK", "ATVI", "SPCE", "DPZ","LMT", "MO", "BAC" ,"MSFT","AMZN", "V", "JNJ", "AMD", 
"AAPL", "SHOP", "ADBE","NKE","QCOM", "ZM","REAL","UAL","INTC","DIS","TWTR","UBER","NFLX","Z","U", "MRNA", 
"TSLA", "TSM", "ASML", "CPNG", "RBLX", "KEY", "FITB"}

today = dt.date.today()
delta = dt.timedelta(days=100)    # 100일 전
past = today-delta

print("@@@@@@@@@@ KOREA @@@@@@@@@ ")
post_message(myToken,"#stock","@@@@@@@@@@ KOREA @@@@@@@@@ ")
for jm in jongmok:
    df = fdr.DataReader(codefind(jm, "krx"), past, today )
    # MACD 
    macd, macdsignal, macdhist = ta.MACD(df['Close'], 12, 26, 9)
    df['macd'] = macd
    df['macd_signal'] = macdsignal
    df['macdhist'] = macdhist
    #rsi
    df['rsi14'] = ta.RSI(df['Close'],14)

    if df['rsi14'].iloc[-1] < 30 :
        post_message(myToken,"#stock",jm +" rsi : " + str(round(df['rsi14'].iloc[-1],2)))

    if df['macdhist'].iloc[-2] < 0 and df['macdhist'].iloc[-1] > 0 :  # macd osc 0선 상향 돌파
        post_message(myToken,"#stock",jm +" macd osc 0선 상향돌파 관망")
        post_message(myToken,"#stock", str(round(df['macdhist'].iloc[-2],2)) +" to "+ str(round(df['macdhist'].iloc[-1],2)))
    if df['macdhist'].iloc[-1] < 0 and df['macdhist'].iloc[-3] > df['macdhist'].iloc[-2] and df['macdhist'].iloc[-2] < df['macdhist'].iloc[-1]:  # 상승반등 : 2일전 > 1일전 < 오늘
        post_message(myToken,"#stock",jm +" macd osc 상승반등 매수 " + str(round(df['macdhist'].iloc[-1],2)))
    if df['macdhist'].iloc[-1] <0 and df['macdhist'].iloc[-3] < df['macdhist'].iloc[-2] and df['macdhist'].iloc[-2] < df['macdhist'].iloc[-1]:  # 0선 아래 2연속 상승
       post_message(myToken,"#stock",jm +" macd osc 0이하 상승세 " + str(round(df['macdhist'].iloc[-1],2)))  

print("@@@@@@@@@@ USA @@@@@@@@@ ")
post_message(myToken,"#stock","@@@@@@@@@@ USA @@@@@@@@@ ")
for jm in jongmok2:
    df = fdr.DataReader(jm, past, today )
    # MACD 
    macd, macdsignal, macdhist = ta.MACD(df['Close'], 12, 26, 9)
    df['macd'] = macd
    df['macd_signal'] = macdsignal
    df['macdhist'] = macdhist
    #rsi
    df['rsi14'] = ta.RSI(df['Close'],14)
    try:
        if df['rsi14'].iloc[-1] < 30 :
            post_message(myToken,"#stock",jm +" rsi : " + str(round(df['rsi14'].iloc[-1],2)) +" "+ namefind(jm))
        if df['macdhist'].iloc[-2] < 0 and df['macdhist'].iloc[-1] > 0 :  # macd osc 0선 상향 돌파
            post_message(myToken,"#stock",jm +" macd osc 0선 상향돌파 관망 : " + namefind(jm))
            post_message(myToken,"#stock", str(round(df['macdhist'].iloc[-2],2)) +" to "+ str(round(df['macdhist'].iloc[-1],2)) + namefind(jm))
        if df['macdhist'].iloc[-1] < 0 and df['macdhist'].iloc[-3] > df['macdhist'].iloc[-2] and df['macdhist'].iloc[-2] < df['macdhist'].iloc[-1]:  # 상승반등 : 2일전 > 1일전 < 오늘
            post_message(myToken,"#stock",jm +" macd osc 상승반등 매수 " + str(round(df['macdhist'].iloc[-1],2)) + namefind(jm))
        if  df['macdhist'].iloc[-1] <0 and df['macdhist'].iloc[-3] < df['macdhist'].iloc[-2] and df['macdhist'].iloc[-2] < df['macdhist'].iloc[-1]:  # 0선 아래 2연속 상승
            post_message(myToken,"#stock",jm +" macd osc 0이하 상승세 " + str(round(df['macdhist'].iloc[-1],2)))
    except Exception as e:
        print(e)
        post_message(myToken,"#stock",e)
        post_message(myToken,"#stock",jm)
        time.sleep(1)


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def avg_buy_price(ticker):
    """잔고 평단 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0

period = 14
count = 35
def RSI(token, interval, period=14):
    df = pyupbit.get_ohlcv(token, interval, count=count)
    df['U'] = np.where(df.diff(1)['close'] > 0, df.diff(1)['close'], 0)  # df.diff(1) : 기준일 종가 - 전일 종가, 0보다 크면 증가분을, 아니면 0을 넣음
    df['D'] = np.where(df.diff(1)['close'] < 0, df.diff(1)['close']*(-1), 0) # 기준일 종가 - 전일 종가, 0보다 작으면 감소분을, 아니면 0을 넣음
    df['AU'] = df['U'].rolling(window=period).mean() # period=14 동안의 U의 (이동)평균
    df['AD'] = df['D'].rolling(window=period).mean() # period=14 동안의 D의 (이동)평균
    RSI = df['AU'] / (df['AD']+df['AU']) * 100
    return RSI

def MACD(token, interval, short=12, long=26, signal=9):
    df2 = pyupbit.get_ohlcv(token, interval, count=count)
    df2['MACD']=df2['close'].ewm( span=short, min_periods= long-1, adjust=False).mean() - df2['close'].ewm( span=long, min_periods=long-1, adjust=False).mean()
    df2['MACD_Signal'] = df2['MACD'].ewm( span = signal, min_periods=signal-1, adjust=False).mean()
    df2['MACD_OSC'] = df2["MACD"] - df2['MACD_Signal']
    return df2

def predict_price(ticker, count=200, interval="minute60", period=24, freq='H'):
    predicted_close_price = 0                  # '24시간 뒤 종가예측값'
    df = pyupbit.get_ohlcv(ticker, count=count, interval=interval)
    df = df.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    data = df[['ds','y']]
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=period, freq=freq)  # 24시간 뒤까지
    forecast = model.predict(future)
    closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]       #현재 시간이 자정 이전일때
    if len(closeDf) == 0:
        closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]       #현재 시간이 자정 이후일때
    closeValue = closeDf['yhat'].values[0]                                              # yhat = 예측의 중간값
    predicted_close_price = closeValue
    return predicted_close_price

token = ["KRW-BTC", "KRW-ETH", "KRW-EOS", "KRW-DOGE"]
min = 25 
max = 75
start = 1

dic_rsi_60 = {}
dic_macd_60 = {}
dic_pp_60 = {}
dic_rsi_day = {}
dic_macd_day = {}
dic_pp_day = {}

for tk in token :
    dic_rsi_60[tk] = 0
    dic_macd_60[tk] = 0
    dic_pp_60[tk] = 0
    dic_rsi_day[tk] = 0
    dic_macd_day[tk] = 0
    dic_pp_day[tk] = 0

while True:
    try:
        if start == 1:
            post_message(myToken,"#stock","@@@@ coin detect running @@@@")
            start=0

        for tk in token :
            #1일봉 rsi 최소최대
            rsi_day = RSI(tk, "day", period)
            time.sleep(1)
            if dic_rsi_day[tk] != rsi_day.index[count-1] :
                if rsi_day.iloc[count-1] < min :
                    post_message(myToken,"#stock",tk + " day RSI : " + str(round(rsi_day.iloc[count-1],2)))
                    print(rsi_day.iloc[count-1])
                    dic_rsi_day[tk] = rsi_day.index[count-1]
                elif rsi_day.iloc[count-1] > max :
                    post_message(myToken,"#stock",tk + " day RSI : " + str(round(rsi_day.iloc[count-1],2)))
                    print(rsi_day.iloc[count-1])
                    dic_rsi_day[tk] = rsi_day.index[count-1]

            #1일봉 macd osc 추세
            macd_day = MACD(tk, "day")
            if dic_macd_day[tk] != macd_day.index[count-1] :
                if macd_day['MACD_OSC'][count-1] < 0 and macd_day['MACD_OSC'][count-3] > macd_day['MACD_OSC'][count-2] and macd_day['MACD_OSC'][count-2] < macd_day['MACD_OSC'][count-1]:
                    post_message(myToken,"#stock",tk + " day macd_osc 상승반등 매수") # 2일전 > 1일전 < 오늘
                    dic_macd_day[tk] = macd_day.index[count-1]
                if macd_day['MACD_OSC'][count-1] <0 and macd_day['MACD_OSC'][count-3]  < macd_day['MACD_OSC'][count-2] and macd_day['MACD_OSC'][count-2] < macd_day['MACD_OSC'][count-1]:
                    post_message(myToken,"#stock",tk + "day macd_osc 0선이하 상승세") # 0이하 2일 연속 상승
                    dic_macd_day[tk] = macd_day.index[count-1]        

            #1일봉 1일 뒤 종가예측값
            if dic_pp_day[tk] != macd_day.index[count-1] :
                pcp2 = predict_price(tk, 250, "day", 1, 'D') 
                if get_current_price(tk) < pcp2 :
                    per = (pcp2 / get_current_price(tk) - 1)*100   #퍼센티지
                    per = round(per,2)    # 퍼센트는 소수점 2자리까지
                    pcp2 = round(pcp2,0)    # 예측가격은 정수로
                    pcp2s = "{0:,}".format(pcp2)         # 3자리마다 , 붙이기
                    post_message(myToken,"#stock",tk + " day pcp is : (+" + str(per) +"%) " + str(pcp2s))
                    dic_pp_day[tk] = macd_day.index[count-1]
                elif get_current_price(tk) > pcp2 :
                    per = (1- pcp2 / get_current_price(tk))*100
                    per = round(per,2)    
                    pcp2 = round(pcp2,0) 
                    pcp2s = "{0:,}".format(pcp2)
                    post_message(myToken,"#stock",tk + " day pcp is : (-" + str(per) +"%) " + str(pcp2s))      
                    dic_pp_day[tk] = macd_day.index[count-1]

        for tk in token :       
            #60분봉 rsi 최소최대
            rsi_60 = RSI(tk, "minute60", period)     # 60분차트 RSI 구하기
            time.sleep(1)
            if dic_rsi_60[tk] != rsi_60.index[count-1] :
                if rsi_60.iloc[count-1] < min :
                    post_message(myToken,"#stock",tk + " 60min RSI : " + str(round(rsi_60.iloc[count-1],2)))
                    print(rsi_60.iloc[count-1])
                    dic_rsi_60[tk] = rsi_60.index[count-1]
                elif rsi_60.iloc[count-1] > max :
                    post_message(myToken,"#stock",tk + " 60min RSI : " + str(round(rsi_60.iloc[count-1],2)))
                    print(rsi_60.iloc[count-1])
                    dic_rsi_60[tk] = rsi_60.index[count-1]

            #60분봉 macd osc 추세
            macd_60 = MACD(tk, "minute60")
            if dic_macd_60[tk] != macd_60.index[count-1] :
                if macd_60['MACD_OSC'][count-1] < 0 and macd_60['MACD_OSC'][count-3] > macd_60['MACD_OSC'][count-2] and macd_60['MACD_OSC'][count-2] < macd_60['MACD_OSC'][count-1]:
                    post_message(myToken,"#stock",tk + " day macd_osc 상승반등 매수") # 2일전 > 1일전 < 오늘
                    dic_macd_60[tk] = macd_60.index[count-1] 
                if macd_60['MACD_OSC'][count-1] < 0 and macd_60['MACD_OSC'][count-3]  < macd_60['MACD_OSC'][count-2] and macd_60['MACD_OSC'][count-2] > macd_60['MACD_OSC'][count-1]:
                        post_message(myToken,"#stock",tk + "60min macd_osc 0이하 상승세") # 0이하 2연속 상승
                        dic_macd_60[tk] = macd_60.index[count-1]          

            #60분봉 6시간뒤 종가예측값
            if dic_pp_60[tk] != macd_60.index[count-1] :
                pcp = predict_price(tk, 1000, "minute60", 6, 'H')   #종가 예측값
                abp = avg_buy_price(tk[4:])  #평단가 조회
                gcp = get_current_price(tk)  #현재가 조회

                if gcp < pcp :
                    per = (pcp / gcp - 1)*100   #퍼센티지
                    per = round(per,2)    # 퍼센트는 소수점 2자리까지
                    pcp = round(pcp,0)    # 예측가격은 정수로
                    pcps = "{0:,}".format(pcp)         # 3자리마다 , 붙이기
                    post_message(myToken,"#stock",tk + " 60min pcp is : " + str(pcps))
                    post_message(myToken,"#stock", "gcp (+" + str(per) +"%) ")
                    dic_pp_60[tk] = macd_60.index[count-1]
                elif gcp > pcp :
                    per = (1- pcp / gcp)*100 
                    per = round(per,2)    
                    pcp = round(pcp,0) 
                    pcps = "{0:,}".format(pcp)
                    post_message(myToken,"#stock",tk + " 60min pcp is : " +  str(pcps))
                    post_message(myToken,"#stock", "gcp (-" + str(per) +"%) ")
                    dic_pp_60[tk] = macd_60.index[count-1]

                if abp < pcp :
                    per2 = (pcp / abp - 1)*100   #퍼센티지
                    per2 = round(per2,2)    # 퍼센트는 소수점 2자리까지
                    post_message(myToken,"#stock", "abp (+" + str(per2) +"%) ")
                elif abp > pcp :
                    per2 = (1- pcp / abp)*100 
                    per2 = round(per2,2)
                    post_message(myToken,"#stock", "abp (-" + str(per2) +"%) ")    

    except Exception as e:
        print(e)
        post_message(myToken,"#stock",e)
        time.sleep(1)