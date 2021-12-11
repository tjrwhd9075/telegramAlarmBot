import pandas
import bybit
import pickle
import time

PD = pandas.DataFrame
T_N = time.time()

BB_Client = bybit.bybit( # 바이비트 API
    test = True,
    # api_key = 'Q2bnma3dbisf3doAVA', # 테스트넷
    api_key = 'Lf5pYPRhYsXmemCc5B', # 개발용
    # api_key = 'IoadNkkeB7M4PT523G', # 실제_읽기전용
    # api_key = 'fVXy5v5866samx8uKB', # 실제
    # api_secret = 'xAhj4lrpUuYhdYUT7b92gLqtB8PmV4pXdPn8') # 테스트넷
    api_secret = 'IQ4cRab4F3uzQEXRkvm2I7h5r5lESQYXEVtv') # 개발용
    # api_secret = '3spzLKYltjnjzHU89l3FmEOV4kfmp9b23GbS') # 실제_읽기전용
    # api_secret = 't2xsvEDdiJHIZgxJ6gqy7VcJho32ipTUmbJQ') # 실제

def BB_Trade_List(symbol='BTCUSDT', limit=12): # 거래
    '''
    symbol : 'BTCUSDT' ...
    limit : int
    '''
    Find = BB_Client.LinearExecution.LinearExecution_getTrades(
        symbol = symbol,
        limit = limit).result()[0]['result']['data']
    return Find

# print(BB_Trade_List())

def BB_Trade_Time(): # 마지막 거래시간
    def BB_Position(i):
        Position = BB_Client.LinearExecution.LinearExecution_getTrades(
            symbol = 'BTCUSDT').result()[0]['result']['data'][i]['exec_type']
        return Position
    def BB_Time(i):
        Time = BB_Client.LinearExecution.LinearExecution_getTrades(
            symbol = 'BTCUSDT').result()[0]['result']['data'][i]['trade_time']
        return Time
    for i in range(len(BB_Trade_List())):
        if BB_Position(i) == 'Funding':
            continue
        elif BB_Position(i) == 'Trade':
            return float(BB_Time(i))

def BB_Order_Status(): # 주문 체결 확인 
    ''' return -> Filled'''
    Check = BB_Client.LinearOrder.LinearOrder_getOrders(
        symbol = 'BTCUSDT',
        limit = str(1)).result()[0]['result']['data'][0]['order_status']
    return Check



#### 데이터프레임 ####
def BB_Dataframe(symbol, interval): # 데이터프레임 저장
    '''
    symbol : 'BTCUSDT' ...
    interval : '1', '3' ...
    return -> df['open_time', 'open', 'high', 'low', 'close']
    '''
    df = PD(BB_Client.LinearKline.LinearKline_indexPrice(
            symbol = symbol,
            interval = interval,
            **{'from': BB_Trade_Time()}).result()[0]['result'],
            columns = ['open_time', 'open', 'high', 'low', 'close'])
    return df

print(BB_Dataframe('BTCUSDT', '1'))
print(BB_Dataframe('BTCUSDT', '1'))
print(BB_Dataframe('BTCUSDT', '1'))
print(BB_Dataframe('BTCUSDT', '1'))
print(BB_Dataframe('BTCUSDT', '1'))
print(BB_Dataframe('BTCUSDT', '1'))
print(BB_Dataframe('BTCUSDT', '1'))
print(BB_Dataframe('BTCUSDT', '1'))
print(BB_Dataframe('BTCUSDT', '1'))
print(BB_Dataframe('BTCUSDT', '1'))
print(BB_Dataframe('BTCUSDT', '1'))


# def BB_Dataframe(): # 데이터프레임 저장
#     def BB_Index_Price1(): # 1분봉
#         Index_Price1 = PD(BB_Client.LinearKline.LinearKline_indexPrice(
#             symbol = 'BTCUSDT',
#             interval = '1',
#             **{'from': BB_Trade_Time()}).result()[0]['result'],
#             columns = ['open_time', 'open', 'high', 'low', 'close'])
#         return Index_Price1
#     def BB_Index_Price3(): # 3분봉
#         Index_Price3 = PD(BB_Client.LinearKline.LinearKline_indexPrice(
#             symbol = 'BTCUSDT',
#             interval = '3',
#             **{'from': BB_Trade_Time()}).result()[0]['result'],
#                 columns = ['open_time', 'open', 'high', 'low', 'close'])
#         return Index_Price3
#     def BB_Index_Price5(): # 5분봉
#         Index_Price5 = PD(BB_Client.LinearKline.LinearKline_indexPrice(
#             symbol = 'BTCUSDT',
#             interval = '5',
#             **{'from': BB_Trade_Time()}).result()[0]['result'],
#                 columns = ['open_time', 'open', 'high', 'low', 'close'])
#         return Index_Price5
#     def BB_Index_Price15(): # 15분봉
#         Index_Price15 = PD(BB_Client.LinearKline.LinearKline_indexPrice(
#             symbol = 'BTCUSDT',
#             interval = '15',
#             **{'from': BB_Trade_Time()}).result()[0]['result'],
#                 columns = ['open_time', 'open', 'high', 'low', 'close'])
#         return Index_Price15
#     if BB_Order_Status() == 'Filled':
#         if ((BB_Trade_Time()*1000)+12000000) > T_N: # 3시간 20분 내 데이터
#             with open('Bybit/Data/Bybit_IP.pkl', 'wb') as f:
#                 pickle.dump(BB_Index_Price1(), f)
#         elif ((BB_Trade_Time()*1000)+36000000) > T_N: # 10시간 내 데이터
#             with open('Bybit/Data/Bybit_IP.pkl', 'wb') as f:
#                 pickle.dump(BB_Index_Price3(), f)
#         elif ((BB_Trade_Time()*1000)+60000000) > T_N: # 16시간 40분 내 데이터
#             with open('Bybit/Data/Bybit_IP.pkl', 'wb') as f:
#                 pickle.dump(BB_Index_Price5(), f)
#         elif ((BB_Trade_Time()*1000)+180000000) > T_N: # 50시간 내 데이터
#             with open('Bybit/Data/Bybit_IP.pkl', 'wb') as f:
#                 pickle.dump(BB_Index_Price15(), f)