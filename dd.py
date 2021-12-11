import datetime as dt
import FinanceDataReader as fdr #종목 주가 정보 가져오기
import pandas as pd  #데이터 전처리 및 저장, 불러오기

krx = fdr.StockListing('KRX')
sp500 = fdr.StockListing('S&P500')
nasdaq = fdr.StockListing('NASDAQ')
nyse = fdr.StockListing('NYSE')
us = pd.concat([sp500, nasdaq, nyse])

jongmok = {"삼성전자", "SK하이닉스", "현대바이오", "카카오", "NAVER", "LG디스플레이", 
"DB하이텍", "LG화학", "LG전자", "삼성SDI", "현대차", "현대모비스", "기아","천보", 
"두산퓨얼셀", "JYP Ent.", "와이지엔터테인먼트", "대원미디어", "펄어비스", "스튜디오드래곤", 
"하이브", "한화솔루션", "씨에스윈드", "씨에스베어링", "대한항공","HMM","SK이노베이션", "KODEX 자동차"
}
jongmok2 = {"BRK.B", "PFE", "PINS", "F", "PYPL", "FB", "NVDA", "CCL", "GM", "SNAP", "SNOW", "GOOGL", "KO", "GS",
"NET", "AXP", "BLK", "ATVI", "SPCE", "DPZ","LMT", "MO", "BAC" ,"MSFT","AMZN", "V", "JNJ", "AMD", 
"AAPL", "SHOP", "ADBE","NKE","QCOM", "ZM","REAL","UAL","INTC","DIS","TWTR","UBER","NFLX","Z","U"}
# "BRK.B"

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
def codefind1(Symbol):
    search = list(us['Symbol'])
    for i in range(len(us)):
        if (search[i]==Symbol):
                return us['Name'][i]
def codefind2(Name):
    search = list(us['Name'])
    for i in range(len(us)):
        if (search[i]==Name):
                return us['Symbol'][i]                

# for jm in jongmok:
#     print(jm)
#     print(codefind(jm, "krx"))


today = dt.date.today()
delta = dt.timedelta(days=100)    # N일 전
past = today-delta

# for jm2 in jongmok2:
#     print(jm2)
#     df = fdr.DataReader(jm2, past, today )차

print(us)