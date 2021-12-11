import time
import datetime
from FinanceDataReader import data
from asyncio.transports import DatagramTransport
import schedule
import asyncio
import itertools
from itertools import filterfalse
from six import text_type

# 1 텔레그램 봇 #
import telegram

## 채널 주소 ##
teleGroup = '-579845295'

## 봇 API ##
Coin_Bot = telegram.Bot(token = '1811197670:AAFaSU2l8pKxT6tDA3tOl2Tpue-OiNC1Af0')

Coin_Bot.sendMessage(chat_id = teleGroup,text="start")

## 2-2 바이비트 ##
import bybit

### API - 엔드 포인트 ( https://api.bybit.com / 테스트넷 ( https://api-testnet.bybit.com ) ###
BB_Client = bybit.bybit( # 바이비트 API
    test = True,
    api_key = '9m6j9B6T8NtnzVdJBt', # 개발용
    api_secret = 'opbcGq48c5xhtYyscqmlesnvrra2LjxoAStV') # 개발용

#전역변수.. 마지막으로 저장된 값
global lastCall
lastCall = []


# async def BB_Liquidated_Orders(): # 청산 알림
def BB_Liquidated_Orders(): # 청산 알림
    global lastCall  #전역변수 불러옴

    Liquidated_Orders = BB_Client.Market.Market_liqRecords(
        symbol = 'BTCUSDT',
        limit = 10).result()[0]['result']

    if lastCall == []: #최근 값이 없으면
        leng = len(Liquidated_Orders) # 갯수
        lastCall = Liquidated_Orders # 값 저장

        for i in range(leng):
            LO_S = Liquidated_Orders[leng-i-1]['side'].replace('Sell', '숏').replace('Buy', '롱')
            LO_Q = Liquidated_Orders[leng-i-1]['qty']
            LO_P = Liquidated_Orders[leng-i-1]['price']
            LO_T = Liquidated_Orders[leng-i-1]['time']
            # 밀리초->문자열 변환
            timestamp_seconds = LO_T/1000
            LO_T = datetime.datetime.fromtimestamp(timestamp_seconds).isoformat().replace("T", " ")[:-7]

            print(LO_T)

            Coin_Bot.sendMessage(chat_id = teleGroup,
                text = '[ 바이비트 청산 ]' + '\n' +
                '포지션: ' + LO_S + '\n' +
                '수량: ' + str(LO_Q) + 'BTC' + '\n' +
                '규모: ' + format((float(LO_Q)*float(LO_P)), ',.4f') + 'USDT' + '\n' +
                '가격: ' + format((float(LO_P)), ',.1f') + '\n' +
                '시간: ' + LO_T
                )
    else:
        # 리스트 내 딕셔너리 - 차집합
        D = list(itertools.filterfalse(lambda x: x in Liquidated_Orders, lastCall)) + list(itertools.filterfalse(lambda x: x in lastCall, Liquidated_Orders))
        
        if D != []:  # 차집합이 비어있지 않으면 (다른게 존재하면)
            lengD = len(D)
            for i in range(lengD):
                LO_S = D[lengD-i-1]['side'].replace('Sell', '숏').replace('Buy', '롱')
                LO_Q = D[lengD-i-1]['qty']
                LO_P = D[lengD-i-1]['price']
                LO_T = D[lengD-i-1]['time']
                # 밀리초->문자열 변환
                timestamp_seconds = LO_T/1000
                LO_T = datetime.datetime.fromtimestamp(timestamp_seconds).isoformat().replace("T", " ")[:-7]

                print(LO_T)

                Coin_Bot.sendMessage(chat_id = teleGroup,
                text = '[ 바이비트 청산 ]' + '\n' +
                '포지션: ' + LO_S + '\n' +
                '수량: ' + str(LO_Q) + 'BTC' + '\n' +
                '규모: ' + format((float(LO_Q)*float(LO_P)), ',.4f') + 'USDT' + '\n' +
                '가격: ' + format((float(LO_P)), ',.1f') + '\n' +
                '시간: ' + LO_T
                )
            
            lastCall = Liquidated_Orders # 값 저장

schedule.every().seconds.do(lambda:BB_Liquidated_Orders()).tag('Liquidated_Orders')

try :

    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            Coin_Bot.sendMessage(chat_id = teleGroup,text="end")
            print(datetime.datetime.now())
            print(e)
            pass
except KeyboardInterrupt:
    # Ctrl+C 입력시 예외 발생
    Coin_Bot.sendMessage(chat_id = teleGroup,text="ctrl + C")
   