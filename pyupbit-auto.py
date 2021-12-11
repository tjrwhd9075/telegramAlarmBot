import time
import pyupbit
import datetime
import requests
 
 # slack 봇
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)
 
myToken = "xoxb-2014329623457-2007907637812-E5pghvrBjFUhYOfJkJVnfIQO"
 
#메시지 구동부
# post_message(myToken,"#stock","what")
#

access = "Ig2xbjz67PIQIUWAQmkVU1opIwDMx1BUDtH1cX3d"
secret = "GqzXn8SepGJxh7ThAXPI4xc7UH1tFW8HbpPs2odR"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)  # 일봉
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
post_message(myToken,"#stock", "autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")  # 9:00
        end_time = start_time + datetime.timedelta(days=1) # 9:00 + 1일

        # 9:00 ~ 현재 ~ 다음날 8:59:50 까지
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5) # 변동성 돌파전략 목표값
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price:
                krw = get_balance("KRW")         # 잔고조회
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995) # 수수료 0.05%
                    post_message(myToken,"#stock", "BTC buy : " +str(buy_result))
        else:
            btc = get_balance("BTC")    # 코인잔고 조회
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995) # 수수료 0.05%, 전량매도 
                post_message(myToken,"#stock", "BTC buy : " +str(sell_result))
        time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken,"#stock", e)
        time.sleep(1)