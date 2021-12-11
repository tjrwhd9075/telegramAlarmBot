import pyupbit
import numpy as np

# ohlcv : 당일 시가, 고가, 저가, 종가, 거래량 데이터
df = pyupbit.get_ohlcv("KRW-SSX", interval="minute5", count=120)

# 변동폭 * K = (고가-저가) * K
df['range'] = (df['high'] - df['low']) * 0.4

# targer(매수가) = 오늘 시가 + 전날 변동폭*k  어제변동폭을 이용해야하니 range 컬럼을 한칸씩 밑으로 내림(.shitf(1)), 
df['target'] = df['open'] + df['range'].shift(1)



# fee = 0.0032
#df['ror'] = np.where(df['high'] > df['target'],
#                     df['close'] / df['target'] - fee,
#                     1)

# ror(수익률), np.where(조건문, 참일때 반환할 값, 거짓일때 반환할 값)
df['ror'] = np.where(df['high'] > df['target'], # 고가가 타켓보다 높으면 매수 진행됐을것임.
                     df['close'] / df['target'], # 매수가 됐으면 종가에 매도했으니 종가/매수가 = 수익률
                     1) # 매수가 안됐으니 수익률 1

# 누적 곱 계산(cumprod) => hpr(누적 수익률)
df['hpr'] = df['ror'].cumprod()

# draw down 계산
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

print(df)

# mdd 계산
print("MDD(%): ", df['dd'].max())

# 엑셀에 저장
df.to_excel("dd.xlsx")