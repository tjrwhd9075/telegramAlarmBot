
import FinanceDataReader as fdr #pip install finance-datareader --upgrade
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

import datetime as dt

# 한국 코스피,코스닥 목록
krx = fdr.StockListing('KRX')
# # 미국 주식 목록
# sp500 = fdr.StockListing('S&P500')
# nasdaq = fdr.StockListing('NASDAQ')
# nyse = fdr.StockListing('NYSE')

def codefind(name, country):
    ''' country : "krx", "us "'''
    if country == "krx" :
        search = list(krx['Name'])
        for i in range(len(krx)):
            if (search[i]==name):
                return krx['Symbol'][i]
    # elif country == "us" :
    #     search = list(sp500['Name'])
    #     search2 = list(nasdaq['Symbol'])
    #     search3 = list(nyse['Symbol'])
    #     for i in range(len(sp500)):
    #         if (search[i]==name):
    #             return sp500['Symbol'][i]
    #     for i in range(len(nasdaq)):
    #         if (search2[i]==name):
    #             return nasdaq['Name'][i]
    #     for i in range(len(nyse)):
    #         if (search3[i]==name):
    #             return nyse['Name'][i] 
    return 0


def fetch_jusik(name, country, count):
    ''' country : krx, us'''
    today = dt.date.today()
    delta = dt.timedelta(days=count)    # count 봉 전부터
    past = today-delta

    if country == "krx":
        df = fdr.DataReader(codefind(name, "krx"), past, today)
    elif country == "us":
        # df = fdr.DataReader(name, past, today)
        df = pdr.get_data_yahoo(name, past, today)

    df.rename(columns = {'Open' : 'open', "Close" : "close", "High" : "high", "Low":"low"}, inplace = True)
    return df



df = fetch_jusik("brk-b","us",500)

print(df.head())

# 엑셀에 저장
# df.to_excel("dd.xlsx")