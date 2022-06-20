from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

data = pdr.get_data_yahoo("aapl")
print(data)
