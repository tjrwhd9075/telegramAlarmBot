import time
import datetime
import pandas
import pickle
import pprint
import schedule
import asyncio

T_N = time.time()
DT_N = datetime.date.today()
DT_y = DT_N.strftime('%Y')
DT_m = DT_N.strftime('%m')
DT_d = DT_N.strftime('%d')
DT_Y = DT_N-datetime.timedelta(days = 1)
DT_JY = DT_N-datetime.timedelta(days = 2)
DT_T = DT_N+datetime.timedelta(days = 1)
DT_N_ISO = datetime.date.isoformat(DT_N)
PD = pandas.DataFrame
PPRT = pprint.pprint

# 1 텔레그램 봇 #
import telegram

## 채널 주소 ##
Kantalk_Test = ''

## 봇 API ##
Coin_Bot = telegram.Bot(token = '')

## 2-2 바이비트 ##
import bybit

import HRBybit_Dataframe

DF = HRBybit_Dataframe.BB_Dataframe()

### API - 엔드 포인트 ( https://api.bybit.com / 테스트넷 ( https://api-testnet.bybit.com ) ###
BB_Client = bybit.bybit( # 바이비트 API
    test = True,
    api_key = 'Lf5pYPRhYsXmemCc5B', # 개발용
    api_secret = 'IQ4cRab4F3uzQEXRkvm2I7h5r5lESQYXEVtv') # 개발용

## 트레이딩 ##
async def Coin():
    #### 지갑 잔고 ####
    async def BB_Equity(): # 총액
        Equity = BB_Client.Wallet.Wallet_getBalance(
            coin = 'USDT').result()[0]['result']['USDT']['equity']
        return Equity
    async def BB_Used_Margin(): # 사용중 자산
        try:
            Used_Margin = BB_Client.Wallet.Wallet_getBalance(
                coin = 'USDT').result()[0]['result']['USDT']['used_margin']
            return float(format(float(float(Used_Margin)*0.98), '.4f'))
        except TypeError:
            return BB_Order()

    #### 마감손익 ####
    async def BB_PnL():
        BB_PnL = BB_Client.LinearPositions.LinearPositions_closePnlRecords(
            symbol = 'BTCUSDT',
            limit = 1).result()[0]['result']['data'][0]['closed_pnl']
        return BB_PnL
    async def BB_Send_PnL(): # 손익 알림
        with open('Bybit/Data/Equity.txt', 'r', encoding = 'UTF-8') as f:
            Equity_Check = f.read()
        with open('Bybit/Data/Equity.txt', 'w', encoding = 'UTF-8') as f:
            Equity = f.write(str(await BB_Equity()))
        if float(Equity_Check) != float(await BB_Equity()):
            if float(await BB_PnL()) > 0:
                Coin_Bot.sendMessage(chat_id = Kantalk_Test,
                    text = '익절: ' + str(await BB_PnL()) + 'USDT' + '\n' +
                    '보유잔고: ' + str(await BB_Equity()) + 'USDT')
            elif float(await BB_PnL()) < 0:
                Coin_Bot.sendMessage(chat_id = Kantalk_Test,
                    text = '손절: ' + str(await BB_PnL()) + 'USDT' + '\n' +
                    '보유잔고: ' + str(await BB_Equity()) + 'USDT')
            return Equity

    #### 레버리지 설정 ####
    # def BB_Leverage(): # 4배
        # Leverage = BB_Client.LinearPositions.LinearPositions_saveLeverage(
        #     symbol = 'BTCUSDT',
        #     buy_leverage = 4,
        #     sell_leverage = 4).result()
        # return Leverage

    #### 호가 ####
    async def BB_Index_Price_Now(): # 최근 종가
        Now = BB_Client.Market.Market_symbolInfo().result()[0]['result'][4]['last_price']
        return float(Now)
    async def BB_Orderbook_Buy(): # 현재 매수가
        Buy = BB_Client.Market.Market_orderbook(
            symbol = 'BTCUSDT').result()[0]['result'][0]['price']
        return float(Buy)
    async def BB_Orderbook_Sell(): # 현재 매도가
        Sell = BB_Client.Market.Market_orderbook(
            symbol = 'BTCUSDT').result()[0]['result'][25]['price']
        return float(Sell)
    # async def BB_Trade_List(): # 거래
        # Find = BB_Client.LinearExecution.LinearExecution_getTrades(
        #     symbol = 'BTCUSDT',
        #     limit = 12).result()[0]['result']['data']
        # return Find
    # async def BB_Trade_Time(): # 마지막 거래시간
        # async def BB_Position():
            # Position = BB_Client.LinearExecution.LinearExecution_getTrades(
            #     symbol = 'BTCUSDT').result()[0]['result']['data'][i]['exec_type']
            # return Position
        # async def BB_Time():
            # Time = BB_Client.LinearExecution.LinearExecution_getTrades(
            #     symbol = 'BTCUSDT').result()[0]['result']['data'][i]['trade_time']
            # return Time
        # for i in range(len(await BB_Trade_List())):
        #     if await BB_Position() == 'Funding':
        #         continue
        #     elif await BB_Position() == 'Trade':
        #         return float(await BB_Time())

    #### 기본설정 ####
    async def BB_Open_qty(): # USDT -> BTC 가격 변환
        qty = format((float(await BB_Equity())/await BB_Index_Price_Now()*4*0.98), '.3f') # )*배수*비율)
        return float(qty)
    async def BB_Order_Status(): # 주문 체결 확인
        Check = BB_Client.LinearOrder.LinearOrder_getOrders(
            symbol = 'BTCUSDT',
            limit = str(1)).result()[0]['result']['data'][0]['order_status']
        return Check

    #### 포지션 설정 ####
    async def BB_Order_ID(): # 활성 대기주문 ID 확인
        ID = BB_Client.LinearOrder.LinearOrder_query( # 활성 대기주문 ID
            symbol = 'BTCUSDT').result()[0]['result'][0]['order_id']
        return str(ID)
    async def BB_Trade_Record(): # 마지막 거래 포지션
        Trade_Record = BB_Client.LinearExecution.LinearExecution_getTrades(
            symbol = 'BTCUSDT',
            limit = 1).result()[0]['result']['data'][0]['side']
        return Trade_Record
    async def BB_Position_Side(): # 현재 포지션
        async def Side_Long():
            try:
                Long = BB_Client.LinearPositions.LinearPositions_myPosition(
                    symbol = 'BTCUSDT').result()[0]['result'][0]['position_margin']
                return Long
            except TypeError:
                await BB_Order()
        async def Side_Short():
            try:
                Short = BB_Client.LinearPositions.LinearPositions_myPosition(
                    symbol = 'BTCUSDT').result()[0]['result'][1]['position_margin']
                return Short
            except TypeError:
                await BB_Order()
        if float(await Side_Long()) > 0:
            return 'Buy'
        elif float(await Side_Short()) > 0:
            return 'Sell'
    async def BB_Close_Size(): # 주문한 BTC 수량 확인
        if await BB_Position_Side() == 'Buy':
            Close_Long_Size = BB_Client.LinearPositions.LinearPositions_myPosition(
                symbol = 'BTCUSDT').result()[0]['result'][0]['size']
            return float(Close_Long_Size)
        elif await BB_Position_Side() == 'Sell':
            Close_Short_Size = BB_Client.LinearPositions.LinearPositions_myPosition(
                symbol = 'BTCUSDT').result()[0]['result'][1]['size']
            return float(Close_Short_Size)

    #### 주문 설정 ####
    async def BB_Open_Long(): # 롱 오픈
        Open_Long = BB_Client.LinearOrder.LinearOrder_new(
            side = 'Buy',
            symbol = 'BTCUSDT',
            order_type = 'Limit',
            qty = await BB_Open_qty(),
            price = await BB_Orderbook_Buy(),
            time_in_force = 'PostOnly',
            reduce_only = False,
            close_on_trigger = False).result()
        return Open_Long
    async def BB_Open_Short(): # 숏 오픈
        Open_Short = BB_Client.LinearOrder.LinearOrder_new(
            side = 'Sell',
            symbol = 'BTCUSDT',
            order_type = 'Limit',
            qty = await BB_Open_qty(),
            price = await BB_Orderbook_Sell(),
            time_in_force = 'PostOnly',
            reduce_only = False,
            close_on_trigger = False).result()
        return Open_Short
    async def BB_Order_Side(): # 활성 대기주문 포지션
        try:
            Order_Check = BB_Client.LinearOrder.LinearOrder_query(
                symbol = 'BTCUSDT').result()[0]['result'][0]['side']
            return Order_Check
        except IndexError:
            return await BB_Order()

    async def BB_Close_Long(): # 롱 클로즈
        Close_Long = BB_Client.LinearOrder.LinearOrder_new(
            side = 'Sell',
            symbol = 'BTCUSDT',
            order_type = 'Limit',
            qty = await BB_Close_Size(),
            price = await BB_Orderbook_Sell(),
            time_in_force = 'PostOnly',
            reduce_only = True,
            close_on_trigger = False).result()
        return Close_Long
    async def BB_Close_Short(): # 숏 클로즈
        Close_Short = BB_Client.LinearOrder.LinearOrder_new(
            side = 'Buy',
            symbol = 'BTCUSDT',
            order_type = 'Limit',
            qty = await BB_Close_Size(),
            price = await BB_Orderbook_Buy(),
            time_in_force = 'PostOnly',
            reduce_only = True,
            close_on_trigger = False).result()
        return Close_Short

    #### 오픈 ###
    async def BB_Open():
        if await BB_Trade_Record() == 'Buy': # 롱 오픈
            return await BB_Open_Long()
        elif await BB_Trade_Record() == 'Sell': # 숏 오픈
            return await BB_Open_Short()

    #### 트레일링 스탑 ####
    async def BB_High(): # 최근 최고가
        with open('Bybit/Data/Bybit_IP.pkl', 'rb') as f:
            High_Price = float(pickle.load(f)['high'].max(axis = 0))
        High_Cut = format((High_Price*0.999), '.2f')
        return float(High_Cut)
    async def BB_Low(): # 최근 최저가
            with open('Bybit/Data/Bybit_IP.pkl', 'rb') as f:
                Low_Price = float(pickle.load(f)['low'].min(axis = 0))
            Low_Cut = format((Low_Price*1.001), '.2f')
            return float(Low_Cut)

    # #### 데이터프레임 ####
    # async def BB_Dataframe(): # 데이터프레임 저장
        # async def BB_Index_Price1(): # 1분봉
            # Index_Price1 = PD(BB_Client.LinearKline.LinearKline_indexPrice(
            #     symbol = 'BTCUSDT',
            #     interval = '1',
            #     **{'from': await BB_Trade_Time()}).result()[0]['result'],
            #     columns = ['open_time', 'open', 'high', 'low', 'close'])
            # return Index_Price1
        # async def BB_Index_Price3(): # 3분봉
            # Index_Price3 = PD(BB_Client.LinearKline.LinearKline_indexPrice(
            #     symbol = 'BTCUSDT',
            #     interval = '3',
            #     **{'from': await BB_Trade_Time()}).result()[0]['result'],
            #         columns = ['open_time', 'open', 'high', 'low', 'close'])
            # return Index_Price3
        # async def BB_Index_Price5(): # 5분봉
            # Index_Price5 = PD(BB_Client.LinearKline.LinearKline_indexPrice(
            #     symbol = 'BTCUSDT',
            #     interval = '5',
            #     **{'from': await BB_Trade_Time()}).result()[0]['result'],
            #         columns = ['open_time', 'open', 'high', 'low', 'close'])
            # return Index_Price5
        # async def BB_Index_Price15(): # 15분봉
            # Index_Price15 = PD(BB_Client.LinearKline.LinearKline_indexPrice(
            #     symbol = 'BTCUSDT',
            #     interval = '15',
            #     **{'from': await BB_Trade_Time()}).result()[0]['result'],
            #         columns = ['open_time', 'open', 'high', 'low', 'close'])
            # return Index_Price15
        # if await BB_Order_Status() == 'Filled':
        #     if ((await BB_Trade_Time()*1000)+12000000) > T_N: # 3시간 20분 내 데이터
        #         with open('Bybit/Data/Bybit_IP.pkl', 'wb') as f:
        #             pickle.dump(await BB_Index_Price1(), f)
        #     elif ((await BB_Trade_Time()*1000)+36000000) > T_N: # 10시간 내 데이터
        #         with open('Bybit/Data/Bybit_IP.pkl', 'wb') as f:
        #             pickle.dump(await BB_Index_Price3(), f)
        #     elif ((await BB_Trade_Time()*1000)+60000000) > T_N: # 16시간 40분 내 데이터
        #         with open('Bybit/Data/Bybit_IP.pkl', 'wb') as f:
        #             pickle.dump(await BB_Index_Price5(), f)
        #     elif ((await BB_Trade_Time()*1000)+180000000) > T_N: # 50시간 내 데이터
        #         with open('Bybit/Data/Bybit_IP.pkl', 'wb') as f:
        #             pickle.dump(await BB_Index_Price15(), f)

    #### 클로즈 ####
    async def BB_Close(): # 청산
        if await BB_Position_Side() == 'Buy': # 롱 청산
            if await BB_Index_Price_Now() < await BB_High():
                return await BB_Close_Long()
        elif await BB_Position_Side() == 'Sell': # 숏 청산
            if await BB_Index_Price_Now() > await BB_Low():
                return await BB_Close_Short()

    #### 재주문 ####
    async def BB_Replace_Order(): # 재주문
        if await BB_Order_Side() == 'Buy': # 롱 재주문
            Replace_Open_Buy = BB_Client.LinearOrder.LinearOrder_replace(
                symbol = 'BTCUSDT',
                order_id = await BB_Order_ID(),
                p_r_price = await BB_Orderbook_Buy()).result()
            return Replace_Open_Buy
        elif await BB_Order_Side() == 'Sell': # 숏 재주문
            Replace_Open_Sell = BB_Client.LinearOrder.LinearOrder_replace(
                symbol = 'BTCUSDT',
                order_id = await BB_Order_ID(),
                p_r_price = await BB_Orderbook_Sell()).result()
            return Replace_Open_Sell

    #### 주문 ####
    async def BB_Order(): # 오픈
        DF
        if await BB_Used_Margin() == 0:
            if await BB_Order_Status() != 'New':
                await BB_Send_PnL()
                return await BB_Open()
        elif await BB_Order_Status() != 'Filled':
            return await BB_Replace_Order()
        else:
            return await BB_Close()
    return await BB_Order()

# schedule.every().seconds.do(lambda:asyncio.run(Coin())).tag('Coin')

while True:
    try:
        # schedule.run_pending()
        asyncio.run(Coin())
        time.sleep(1)
    except Exception as e:
        # Coin_Bot.sendMessage(chat_id = Kantalk_Test,
        #     text = '코인 오류 발생')
        print(datetime.datetime.now())
        print(e)
        time.sleep(1)
        pass