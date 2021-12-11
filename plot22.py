from mpl_finance import candlestick2_ohlc
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data  
from datetime import datetime
from IPython.display import display

# # 데이터를 가져올 날짜 설정
# start_date = datetime(2020,5,8)
# end_date = datetime(2020,10,8)

# # 야후에서 코스피 데이터 가져오기
# kospi_df = data.get_data_yahoo("^KS11", start_date, end_date) 
# display(kospi_df.head(5))

# # 지수 이동평균선 데이터 구하기
# kospi_df['MA3'] = kospi_df['Close'].rolling(3).mean()
# kospi_df['MA5'] = kospi_df['Close'].rolling(5).mean()
# kospi_df['MA10'] = kospi_df['Close'].rolling(10).mean()
# kospi_df['MA20'] = kospi_df['Close'].rolling(20).mean()
# display(kospi_df.head(5))

# # 그래프 그리기
# fig, ax = plt.subplots(figsize=(10,5))

# ax.set_title('KOSPI INDEX', fontsize=15)
# ax.set_ylabel("KOSPI")
# ax.set_xlabel("Date Time")
# ax.plot(kospi_df.index, kospi_df[['Close','MA5','MA10']])   # 차트에 표시할 데이터
# ax.legend(['Close','MA5','MA10'])                           # 차트 범례
# plt.show()


fig = plt.figure(figsize=(20,10))                           # 차트 사이즈
ax = fig.add_subplot(111)                   # 차트 겹치기
index = kospi_df.index.astype('str') # 캔들스틱 x축이 str로 들어감

# 이동평균선 그리기
ax.plot(index, kospi_df['MA3'], label='MA3', linewidth=0.7)
ax.plot(index, kospi_df['MA5'], label='MA5', linewidth=0.7)
ax.plot(index, kospi_df['MA10'], label='MA10', linewidth=0.7)

# X축 티커 숫자 20개로 제한
ax.xaxis.set_major_locator(ticker.MaxNLocator(20))

# 그래프 title과 축 이름 지정
ax.set_title('KOSPI INDEX', fontsize=22)
ax.set_xlabel('Date')

# 캔들차트 그리기
candlestick2_ohlc(ax, kospi_df['Open'], kospi_df['High'], 
                  kospi_df['Low'], kospi_df['Close'],
                  width=0.5, colorup='r', colordown='b')
ax.legend()
plt.grid()
plt.show()