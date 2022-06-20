import FinanceDataReader as fdr
import datetime as dt

# df_spx = fdr.StockListing('S&P500')
# df_spx.head()
# print(df_spx)

# df = fdr.DataReader(symbol='AAPL', start='2020') # 애플, 2020년~현재
# print(df)

def fetch_jusik(name, country, count):
    ''' country : krx, us'''
    today = dt.date.today()
    delta = dt.timedelta(days=count)    # count 봉 전부터
    past = today-delta

    # if country == "krx":
    #     df = fdr.DataReader(codefind(name, "krx"), past, today)
    if country == "us":
        df = fdr.DataReader(name, past, today)

    df.rename(columns = {'Open' : 'open', "Close" : "close", "High" : "high", "Low":"low"}, inplace = True)
    return df

print(fetch_jusik("tsla", "us", 120))
