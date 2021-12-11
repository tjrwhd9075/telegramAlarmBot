import time
import datetime
import pandas
import pickle
import pprint
import schedule

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
Kantalk_Test = '@ha_alarm_feedback'

## 봇 API ##
Coin_Bot = telegram.Bot(token = '1811197670:AAFaSU2l8pKxT6tDA3tOl2Tpue-OiNC1Af0')

## 2-2 바이비트 ##
import bybit
import HRBybit_Dataframe as DF

### API - 엔드 포인트 ( https://api.bybit.com / 테스트넷 ( https://api-testnet.bybit.com ) ###
BB_Client = bybit.bybit( # 바이비트 API
    test = True,
    api_key = 'Lf5pYPRhYsXmemCc5B', # 개발용
    api_secret = 'IQ4cRab4F3uzQEXRkvm2I7h5r5lESQYXEVtv') # 개발용

#### 지갑 잔고 ####
def BB_Equity(coin='USDT'): # 총액
    '''
    coin : 'USDT', 'BTC' ... \n
    return -> float(equity)
    '''
    Equity = BB_Client.Wallet.Wallet_getBalance(
        coin = coin).result()[0]['result'][coin]['equity']
    return Equity

def BB_Used_Margin(coin='USDT'): # 사용중 자산
    '''
    coin : 'USDT', 'BTC' ... \n
    return -> float(used_margin)
    '''
    Used_Margin = BB_Client.Wallet.Wallet_getBalance(
        coin = coin).result()[0]['result'][coin]['used_margin']
    return float(format(float(float(Used_Margin)*0.98), '.4f'))

#### 마감손익 ####
def BB_PnL(symbol='BTCUSDT'):
    ''' 
    symbol : 'BTCUSDT' \n
    return -> float(pnl)
    '''
    BB_PnL = BB_Client.LinearPositions.LinearPositions_closePnlRecords(
        symbol = symbol,
        limit = 1).result()[0]['result']['data'][0]['closed_pnl']
    return BB_PnL 

def BB_Send_PnL(): # 손익 알림
    with open('Bybit/Data/Equity.txt', 'r', encoding = 'UTF-8') as f:
        Equity_Check = f.read()
    with open('Bybit/Data/Equity.txt', 'w', encoding = 'UTF-8') as f:
        Equity = f.write(str(BB_Equity()))
    if float(Equity_Check) != float(BB_Equity()):
        if float(BB_PnL()) > 0:
            Coin_Bot.sendMessage(chat_id = Kantalk_Test,
                text = '익절: ' + str(BB_PnL()) + 'USDT' + '\n' +
                '보유잔고: ' + str(BB_Equity()) + 'USDT')
        elif float(BB_PnL()) < 0:
            Coin_Bot.sendMessage(chat_id = Kantalk_Test,
                text = '손절: ' + str(BB_PnL()) + 'USDT' + '\n' +
                '보유잔고: ' + str(BB_Equity()) + 'USDT')
        return Equity

#### 호가 ####
def BB_Index_Price_Now(): # 최근 종가
    Now = BB_Client.Market.Market_symbolInfo().result()[0]['result'][4]['last_price']
    return float(Now)
def BB_Orderbook_Buy(): # 현재 매수가
    Buy = BB_Client.Market.Market_orderbook(
        symbol = 'BTCUSDT').result()[0]['result'][0]['price']
    return float(Buy)
def BB_Orderbook_Sell(): # 현재 매도가
    Sell = BB_Client.Market.Market_orderbook(
        symbol = 'BTCUSDT').result()[0]['result'][25]['price']
    return float(Sell)

#### 기본설정 ####
def BB_Open_qty(): # USDT -> BTC 가격 변환
    qty = format((float(BB_Equity())/BB_Index_Price_Now()*4*0.98), '.3f') # )*배수*비율)
    return float(qty)
def BB_Order_Status(): # 주문 체결 확인
    Check = BB_Client.LinearOrder.LinearOrder_getOrders(
        symbol = 'BTCUSDT',
        limit = str(1)).result()[0]['result']['data'][0]['order_status']
    return Check

#### 포지션 설정 ####
def BB_Order_ID(): # 활성 대기주문 ID 확인
    ID = BB_Client.LinearOrder.LinearOrder_query( # 활성 대기주문 ID
        symbol = 'BTCUSDT').result()[0]['result'][0]['order_id']
    return str(ID)
def BB_Trade_Record(): # 마지막 거래 포지션
    Trade_Record = BB_Client.LinearExecution.LinearExecution_getTrades(
        symbol = 'BTCUSDT',
        limit = 1).result()[0]['result']['data'][0]['side']
    return Trade_Record

#### 레버리지 설정 ####
# def BB_Leverage(): # 4배
    # Leverage = BB_Client.LinearPositions.LinearPositions_saveLeverage(
    #     symbol = 'BTCUSDT',
    #     buy_leverage = 4,
    #     sell_leverage = 4).result()
    # return Leverage

def BB_Position_Side(): # 현재 포지션
    def Side_Long():
        try:
            Long = BB_Client.LinearPositions.LinearPositions_myPosition(
                symbol = 'BTCUSDT').result()[0]['result'][0]['position_margin']
            return Long
        except TypeError:
            BB_Order()
    def Side_Short():
        try:
            Short = BB_Client.LinearPositions.LinearPositions_myPosition(
                symbol = 'BTCUSDT').result()[0]['result'][1]['position_margin']
            return Short
        except TypeError:
            BB_Order()
    if float(Side_Long()) > 0:
        return 'Buy'
    elif float(Side_Short()) > 0:
        return 'Sell'

def BB_Close_Size(): # 주문한 BTC 수량 확인
    if BB_Position_Side() == 'Buy':
        Close_Long_Size = BB_Client.LinearPositions.LinearPositions_myPosition(
            symbol = 'BTCUSDT').result()[0]['result'][0]['size']
        return float(Close_Long_Size)
    elif BB_Position_Side() == 'Sell':
        Close_Short_Size = BB_Client.LinearPositions.LinearPositions_myPosition(
            symbol = 'BTCUSDT').result()[0]['result'][1]['size']
        return float(Close_Short_Size)


#### 주문 설정 ####
def BB_Open_Long(): # 롱 오픈
    Open_Long = BB_Client.LinearOrder.LinearOrder_new(
        side = 'Buy',
        symbol = 'BTCUSDT',
        order_type = 'Limit',
        qty = BB_Open_qty(),
        price = BB_Orderbook_Buy(),
        time_in_force = 'PostOnly',
        reduce_only = False,
        close_on_trigger = False).result()
    return Open_Long
def BB_Open_Short(): # 숏 오픈
    Open_Short = BB_Client.LinearOrder.LinearOrder_new(
        side = 'Sell',
        symbol = 'BTCUSDT',
        order_type = 'Limit',
        qty = BB_Open_qty(),
        price = BB_Orderbook_Sell(),
        time_in_force = 'PostOnly',
        reduce_only = False,
        close_on_trigger = False).result()
    return Open_Short
def BB_Order_Side(): # 활성 대기주문 포지션
    try:
        Order_Check = BB_Client.LinearOrder.LinearOrder_query(
            symbol = 'BTCUSDT').result()[0]['result'][0]['side']
        return Order_Check
    except IndexError:
        return BB_Order()

def BB_Close_Long(): # 롱 클로즈
    Close_Long = BB_Client.LinearOrder.LinearOrder_new(
        side = 'Sell',
        symbol = 'BTCUSDT',
        order_type = 'Limit',
        qty = BB_Close_Size(),
        price = BB_Orderbook_Sell(),
        time_in_force = 'PostOnly',
        reduce_only = True,
        close_on_trigger = False).result()
    return Close_Long
def BB_Close_Short(): # 숏 클로즈
    Close_Short = BB_Client.LinearOrder.LinearOrder_new(
        side = 'Buy',
        symbol = 'BTCUSDT',
        order_type = 'Limit',
        qty = BB_Close_Size(),
        price = BB_Orderbook_Buy(),
        time_in_force = 'PostOnly',
        reduce_only = True,
        close_on_trigger = False).result()
    return Close_Short


#### 트레일링 스탑 ####
def BB_High(): # 최근 최고가
    with open('Bybit/Data/Bybit_IP.pkl', 'rb') as f:
        High_Price = float(pickle.load(f)['high'].max(axis = 0))
    High_Cut = format((High_Price*0.999), '.2f')
    return float(High_Cut)
def BB_Low(): # 최근 최저가
        with open('Bybit/Data/Bybit_IP.pkl', 'rb') as f:
            Low_Price = float(pickle.load(f)['low'].min(axis = 0))
        Low_Cut = format((Low_Price*1.001), '.2f')
        return float(Low_Cut)

#### 클로즈 ####
def BB_Close(): # 청산
    if BB_Position_Side() == 'Buy': # 롱 청산
        if BB_Index_Price_Now() < BB_High():
            return BB_Close_Long()
    elif BB_Position_Side() == 'Sell': # 숏 청산
        if BB_Index_Price_Now() > BB_Low():
            return BB_Close_Short()

#### 오픈 ###
def BB_Open():
    if BB_Trade_Record() == 'Buy': # 롱 오픈
        return BB_Open_Long()
    elif BB_Trade_Record() == 'Sell': # 숏 오픈
        return BB_Open_Short()


#### 재주문 ####
def BB_Replace_Order(): # 재주문
    if BB_Order_Side() == 'Buy': # 롱 재주문
        Replace_Open_Buy = BB_Client.LinearOrder.LinearOrder_replace(
            symbol = 'BTCUSDT',
            order_id = BB_Order_ID(),
            p_r_price = BB_Orderbook_Buy()).result()
        return Replace_Open_Buy
    elif BB_Order_Side() == 'Sell': # 숏 재주문
        Replace_Open_Sell = BB_Client.LinearOrder.LinearOrder_replace(
            symbol = 'BTCUSDT',
            order_id = BB_Order_ID(),
            p_r_price = BB_Orderbook_Sell()).result()
        return Replace_Open_Sell


#### 주문 ####
def BB_Order(): # 오픈
    symbol = "BTCUSDT"
    limit = 12
    
    if BB_Used_Margin(symbol, limit) == 0:
        if BB_Order_Status() != 'New':
            BB_Send_PnL()
            return BB_Open()
    elif BB_Order_Status() != 'Filled':
        return BB_Replace_Order()
    else:
        return BB_Close()

    
# schedule.every().seconds.do(lambda:asyncio.run(Coin())).tag('Coin')

# while True:
#     try:
#         # schedule.run_pending()
#         Coin()
#         time.sleep(1)
#     except Exception as e:
#         # Coin_Bot.sendMessage(chat_id = Kantalk_Test,
#         #     text = '코인 오류 발생')
#         print(datetime.datetime.now())
#         print(e)
#         time.sleep(1)
#         pass