import yfinance as yf
import mplfinance as mpf
import numpy as np 

df = yf.download('BTC-USD', start='2008-01-04', end='2021-06-3', interval='1d').tail(50)

buy = np.where((df['Close'] > df['Open']) & (df['Close'].shift(1) < df['Open'].shift(1)), 1, np.nan) * 0.95 * df['Low']

apd = [mpf.make_addplot(buy, scatter=True, markersize=100, marker=r'$\Uparrow$', color='green')]  # 화살표

mpf.plot(df, type='candle', volume=True, addplot=apd)