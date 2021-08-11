
from os import close, name
from re import S
from threading import Thread
from FinanceDataReader import data
import matplotlib as mpl
from matplotlib.colors import rgb2hex
from numpy.lib.polynomial import polysub
from pandas.core import tools
import pyupbit
import numpy as np
import requests
import time
from requests.models import DEFAULT_REDIRECT_LIMIT
import schedule
import FinanceDataReader as fdr
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import interactive, rc
import matplotlib.font_manager as fm
# import yfinance
import mplfinance
import ccxt
import sys
import pprint
import pandas as pd
import telegram as tel
from telegram import chat
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ccxt.binance import binance
import plotly
from plotly import plot, subplots
import plotly.offline as plty
import plotly.graph_objs as pltygo
import naver_weather
import naver_news
import watchlist
import asyncio
from pprint import pprint as pp

plotly.__version__

version = "사용법은 /help\n\
        \n\[version]\
        \n 1.1.0 명령어 수정\
        \n\n[메인 채널](ha_alarm_feedback)\
        \n[메인 그룹](signalmaker_chat))\
        \n[HA 추세전환 알림 한국 주식](t.me/ha_alarm_korea)\
        \n[HA 추세전환 알림 미국 주식](t.me/ha_alarm_usa)\
        \n[바이낸스 비트코인 HA 추세전환 알림](t.me/ha_alarm_binance)\
        \n[업비트 비트코인 HA 추세전환 알림](t.me/ha_alarm)\
        \n[앤톡 새글 알리미](t.me/antok_alarm)\
        \n[네이버 뉴스 알리미](t.me/naver_news_alarm)\
        "
updateText = "업데이트 완료 : " + version

textHelp = "\n / 를 입력하고 명령어를 선택하세요. \
            \n 또는 메시지 입력란 오른편에 / 버튼을 누르세요."

myApikey = "hOpHmrM35aqoqakISj0m7PAy42bDLXBmhXIrOsvadPBU6bW8Gtin0ggp7UnzFg9f"
mySecretkey = "rJp7j47DyzzvqRhaa9ExusnxrcPSF2I6Aa1B6bNvjlzxv3VP7fs3sl3cMNvSbEdU"

#텔레그램 봇
myToken = '1811197670:AAFaSU2l8pKxT6tDA3tOl2Tpue-OiNC1Af0'
telbot = tel.Bot(token=myToken)
myBotName = "alarm_haBot"
updater = Updater(myToken, use_context=True)

myToken2 = '1944946345:AAEffpHSAtU52pC06P6z8qM6x78OzJ0LwV8'  # 네이버 뉴스용
telbot2 = tel.Bot(token=myToken2) # 네이버 뉴스용
myBotName2 = "naver_news_alarm_bot"

channel_id = "@ha_alarm"                  # 업비트 채널
channel_id_binance = "@ha_alarm_binance"  # 바이낸스 채널=
channel_id_korea = "@ha_alarm_korea"  # 한국 채널
channel_id_usa = "@ha_alarm_usa"  # 미국 채널
channel_id_feedback = "@ha_alarm_feedback"  # 피드백채널
group_id_naver_news = '-1001173681896'


image = "jusik.png"
msgOn = 1 # 1일때 메시지 켜짐, 0일때 메시지 꺼짐
runtest = 0 # 0일때 코인 실행 꺼짐, 1일때 코인 실행
run_ko = 0 # 0일때 한국 실행 꺼짐 1일때 실행
run_us = 0 # 0일때 미국 실행 꺼짐 1일때 실행

# 한국 코스피,코스닥 목록
krx = fdr.StockListing('KRX')
# 미국 주식 목록
sp500 = fdr.StockListing('S&P500')
nasdaq = fdr.StockListing('NASDAQ')
nyse = fdr.StockListing('NYSE')

# 코드 찾기 어려울 경우를 위해 code찾기 만들기
def codefind(name, country):
    ''' country : "krx", "us "'''
    if country == "krx" :
        search = list(krx['Name'])
        for i in range(len(krx)):
            if (search[i]==name):
                return krx['Symbol'][i]
    elif country == "us" :
        search = list(sp500['Name'])
        for i in range(len(sp500)):
            if (search[i]==name):
                return sp500['Symbol'][i]
    return 0
def namefind(symbol):
    search = list(sp500['Symbol'])
    search2 = list(nasdaq['Symbol'])
    search3 = list(nyse['Symbol'])
    for i in range(len(sp500)):
        if (search[i]==symbol):
            return sp500['Name'][i]
    for i in range(len(nasdaq)):
        if (search2[i]==symbol):
            return nasdaq['Name'][i]
    for i in range(len(nyse)):
        if (search3[i]==symbol):
            return nyse['Name'][i] 
    return 0

# 캔들차트 그리기
def plot_candle_chart(df, title):  
    
    adp = [mplfinance.make_addplot(df["ema"], color='green')]  # 지수이평선
    fig = mplfinance.plot(df, type='candle', style='charles', mav=(20),  
                    title=title, ylabel='price', show_nontrading=False,
                    savefig='jusik.png',
                    addplot=adp,
                    block=False
                    )

# 캔들차트 그리기
def plot_candle_chart2(df, title):  
    # 한글 출력용 폰트 지정
    font_name = fm.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    
    adp1 = [mplfinance.make_addplot(df["bolUpper"], color='red')]  # 이평선
    adp2 = [mplfinance.make_addplot(df["20ma"], color='yellow')]  # 이평선
    adp3 = [mplfinance.make_addplot(df["bolLower"], color='blue')]  # 이평선
    fig = mplfinance.plot(df, type='candle', style='charles', mav=(20),
                    title=title, ylabel='price', show_nontrading=False,
                    savefig='jusik.png',
                    addplot= adp1 + adp2 +adp3,
                    block=False
                    )

# 캔들차트 그리기
def plot_candle_chart_ichimoku(df, title):  
    
    adp1 = [mplfinance.make_addplot(df["kijun"], color='gray')]  # 기준선
    adp2 = [mplfinance.make_addplot(df["tenkan"], color='red')]  # 전환선
    adp3 = [mplfinance.make_addplot(df["senkouSpanA"], color='green')]  # 선행A
    adp4 = [mplfinance.make_addplot(df["senkouSpanB"], color='green')]  # 선행B
    fig = mplfinance.plot(df, type='candle', style='charles',
                    title=title, ylabel='price', show_nontrading=False,
                    savefig='jusik.png',
                    addplot= adp1 + adp2 +adp3+adp4,
                    block=False,
                    fill_between = dict(y1=df['senkouSpanA'].values, y2=df['senkouSpanB'].values, color='#f2ad73', alpha=0.20)
                    )

def plot_candle_chart_jisu(df, name):
    '''
    ks11, kq11, dji, ixic, us500
    '''

    if name.upper() == "KS11": title = "KOSPI"
    elif name.upper() == "KQ11": title = "KOSDAQ"
    elif name.upper() == "DJI": title = "DOWJONES"
    elif name.upper() == "IXIC": title = "NASDAQ"
    elif name.upper() == "US500" : title = "S&P500"
    else: title = name.upper()

    if df["close"].iloc[-1]-df["close"].iloc[-2] > 0:
        txt = title+" now : "+str(format(round(df["close"].iloc[-1],2),','))\
             + " (+"+  str(round(df["close"].iloc[-1]-df["close"].iloc[-2],2))\
             +" +" + str(round((df["close"].iloc[-1]/df["close"].iloc[-2]-1)*100,2)) + "%)"
    elif df["close"].iloc[-1]-df["close"].iloc[-2] < 0:
        txt = title+" now : "+str(format(round(df["close"].iloc[-1],2),','))\
             + " ("+  str(round(df["close"].iloc[-1]-df["close"].iloc[-2],2))\
             +" " + str(round((df["close"].iloc[-1]/df["close"].iloc[-2]-1)*100,2)) + "%)"

    fig = mplfinance.plot(df, type='candle', style='charles', mav=(20,60,120),  
                    title=(txt), ylabel='price', show_nontrading=False,
                    savefig='jusik.png',
                    block=False
                    )

############# 텔레그램 봇 #######################
global korea; korea =0
global usa; usa =0

# 맨처음 메뉴버튼
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

# 이후 버튼 누를때 다음 생성되는 버튼들
def build_button(text_list, callback_header = "") : # make button list
    button_list = []
    text_header = callback_header
    
    if callback_header != "" : # 비어있는게 아니라면
        text_header += ","   # 제목 + 콤마 붙임

    for text in text_list :
        button_list.append(InlineKeyboardButton(text, callback_data=text_header + text))

    return button_list

COMMAND = ''
EXCHANGE =''
SELLECT = ''
def get_name(bot, update):
    if bot.channel_post is not None : tp = "channel_post"   #채널일 경우
    elif bot.message is not None : tp = "message"           #그룹일 경우
    elif bot.edited_channel_post is not None  : return      #봇이 채널에 에딧한 메세지일 경우
    # elif bot['message']['from']
    else : print(bot)
    
    chat_id = bot[tp]['chat']['id']
    msg = bot[tp]['text'].upper()
    message_id = bot[tp]['message_id']
    
    print("get_name  " + msg)

    global COMMAND
    global EXCHANGE
    global SELLECT

    if msg == "취소":
        telbot.send_message(chat_id=chat_id, text = '취소되었습니다.', reply_markup=ReplyKeyboardRemove())
        SELLECT = ''
        COMMAND = ''
        EXCHANGE = ''
        try :telbot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception:pass
        return

    if COMMAND == "/SHOWCHART": 
        if codefind(msg.lower().capitalize(), "us") != 0 : # 미국종목 이름름 검색 결과
            telbot.send_message(chat_id=chat_id, text = codefind(msg.lower().capitalize(), "us") + " : 검색되었습니다. 차트를 불러옵니다")
            df = fetch_jusik(codefind(msg.lower().capitalize(), "us"), "us", 120)
        elif namefind(msg) != 0: # 미국티커 검색 결과
            print(namefind(msg))
            telbot.send_message(chat_id=chat_id, text = namefind(msg) + " : 검색되었습니다. 차트를 불러옵니다")
            df = fetch_jusik(msg, "us", 120)
        elif codefind(msg, "krx") != 0: # 한국종목이름 검색 결과
            telbot.send_message(chat_id=chat_id, text = msg + "(" + codefind(msg, "krx") + ") : 검색되었습니다. 차트를 불러옵니다")
            df = fetch_jusik(msg, "krx", 120)
        else:
            telbot.send_message(chat_id=chat_id, text = msg + " : 검색되지 않는 종목명입니다.")
            return 
        
        df = Macd(df)
        df = BolingerBand(df)
        df = Rsi(df)
        df = Ema(df)
        df = Heiken_ashi(df)
        df = ichimoku(df)
        txt = signal_maker(df)
        temp = ""
        for t in txt:
            if str(type(t)) == "<class 'int'>":
                if t > 0 :
                    temp = temp + "\n❤️ " + str(t) + ". 〰️매수 우위"
                elif t < 0 :
                    temp = temp + "\n💙 " + str(-t) + ". 〰️매도 우위"
                else :
                    temp = temp + "\n⚠️ " + str(t) + ". 〰️중립" 
            else:
                temp = temp + t + "\n"

        display_all_signal(df, msg, "1day")
        telbot.send_photo(chat_id=chat_id, photo=open('fig1.png', 'rb'))
        telbot.send_photo(chat_id=chat_id, photo=open('fig2.png', 'rb'))
        telbot.send_photo(chat_id=chat_id, photo=open('fig3.png', 'rb'), caption="💲💲 "+ msg + " 1일봉 💲💲\n" +temp)  
    
    elif COMMAND == "/BTC" or COMMAND == "/ETH":    
        # 취소 버튼
        if msg == ("CANCEL"):
            telbot.send_message(text="취소하였습니다.",chat_id=chat_id, reply_markup=ReplyKeyboardRemove() )
            telbot.delete_message(chat_id=chat_id, message_id=message_id)
        
        
        elif msg == ("BINANCE") or msg == ("UPBIT"): # 비트코인
            reply_keyboard = [["1m", "5m", "15m", "30m"],["1h", "4h", "1d","cancel"]]
            telbot.send_message(text="봉을 선택해 주세요.",
                                        chat_id=chat_id,
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
            telbot.delete_message(chat_id= chat_id, message_id= message_id)
            EXCHANGE = msg
            return
    
        elif msg == ("BINANCE.") or msg == ("UPBIT."): # 이더리움
            # reply_keyboard = [["1m", "5m", "15m", "30m"],["1h", "4h", "1d","cancel"]]
            reply_keyboard = [["1m", "5m", "15m", "30m"],["1h", "4h", "1d","cancel"]]
            telbot.send_message(text="봉을 선택해 주세요.",
                                        chat_id= chat_id,
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
            telbot.delete_message(chat_id= chat_id, message_id= message_id)
            EXCHANGE = msg
            return

        elif COMMAND != '' and EXCHANGE != '':  # 코인 선택 -> 거래소 선택 -> msg = 'INTERVAL'
            interval = msg.lower()
            print(interval)
            count = 100
            if EXCHANGE == "BINANCE" : # 비트 바이낸스 선택
                coin = "BTC/USDT"
                df = ichimoku(Heiken_ashi(Ema(Rsi(BolingerBand(Macd(fetch_ohlcvs(coin, interval, count)))))))
            elif EXCHANGE == "BINANCE." : # 이더 바이낸스 선택
                coin = "ETH/USDT"
                df = ichimoku(Heiken_ashi(Ema(Rsi(BolingerBand(Macd(fetch_ohlcvs(coin, interval, count)))))))
            elif EXCHANGE == "UPBIT": # 비트 업비트 선택
                coin = "KRW-BTC"
                if interval == '1m' : interval = "minute1"
                elif interval == '5m' : interval = "minute5"
                elif interval == '15m' : interval = "minute15"
                elif interval == '30m' : interval = "minute30"
                elif interval == '1h' : interval = "minute60"
                elif interval == '4h' : interval = "minute240"
                elif interval == '1d' : interval = "1day"
                df = ichimoku(Heiken_ashi(Ema(Rsi(BolingerBand(Macd(pyupbit.get_ohlcv(coin, interval, count)))))))
            elif EXCHANGE == "UPBIT." : # 이더 업비트 선택
                coin = "KRW-BTC"
                if interval == '1m' : interval = "minute1"
                elif interval == '5m' : interval = "minute5"
                elif interval == '15m' : interval = "minute15"
                elif interval == '30m' : interval = "minute30"
                elif interval == '1h' : interval = "minute60"
                elif interval == '4h' : interval = "minute240"
                elif interval == '1d' : interval = "1day"
                coin = "KRW-ETH"
                df = ichimoku(Heiken_ashi(Ema(Rsi(BolingerBand(Macd(pyupbit.get_ohlcv(coin, interval, count)))))))
            
            print(coin)
            print(df)

            txt = signal_maker(df)
            temp = ""
            for t in txt:
                if str(type(t)) == "<class 'int'>":
                    if t > 0 : temp = temp + "\n❤️ " + str(t) + ". 〰️매수 우위"
                    elif t < 0 : temp = temp + "\n💙 " + str(-t) + ". 〰️매도 우위"
                    else : temp = temp + "\n⚠️ " + str(t) + ". 〰️중립" 
                else: temp = temp + t + "\n"

            display_all_signal(df, coin, interval)
            telbot.send_photo(chat_id=chat_id, photo=open('fig1.png', 'rb'))
            telbot.send_photo(chat_id=chat_id, photo=open('fig2.png', 'rb'))                        
            telbot.send_photo(chat_id=chat_id, photo=open('fig3.png', 'rb'),
                            caption="💲💲 "+ EXCHANGE + " "+ COMMAND[1:] +" " + interval +" 💲💲\n" +temp , reply_markup=ReplyKeyboardRemove())     

############### 기타
    elif COMMAND == "/FUN":
        if msg == "오늘내일 날씨":
            telbot.send_message(text="도시명을 입력해주세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return 
        elif msg == "1주일 내 비소식":
            telbot.send_message(text="도시명을 입력해주세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return 
        elif msg == "한강 수온 체크":
            telbot.send_message(text="🌊 현재 한강 수온 🌡 "+naver_weather.temperature()+ "\n\n"+ naver_weather.wise_saying()+"\n[한강수온](https://hangang.life/)",parse_mode="Markdown", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg == "김프" :
            dfBi = fetch_ohlcvs('BTC/USDT', '1d', 2)
            dfUp = pyupbit.get_ohlcv('KRW-BTC', 'day', 2)
            usd2krw = fetch_jisu('usd/krw',10)
            biWon = dfBi['close'].iloc[-1]*usd2krw['close'].iloc[-1]
            kimpWon = dfUp['close'].iloc[-1] - biWon
            kimpPer = (dfUp['close'].iloc[-1]/biWon - 1)*100

            telbot.send_message(text="[[ 비트코인 김프 ]]\
                                    \n\n업비트 현재가 : " + str(format(round(dfUp['close'].iloc[-1]),",")) + "₩\
                                    \n바이낸스 현재가 : " + str(format(round(dfBi['close'].iloc[-1],2),',')) + "$\
                                    \n\t\t = " + str(format(round(biWon),',')) +"₩"
                                    + "\n\n김프 : " + str(format(round(kimpWon),',')) +"₩ ("+ str(format(round(kimpPer,2),',')) + "%)"
                                    ,  chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg == "워뇨띠":
            txtList = Whales_Position()
            if txtList[1] == "SHORT":
                telbot.send_message(text=txtList[0] + " (워뇨띠) 현재 포지션 : " + txtList[1] + "⬇️\n업데이트 시간 : " + txtList[2]  + "\nhttps://kimpya.site/page/readerboard.php",  chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            elif txtList[1] == "LONG":
                telbot.send_message(text=txtList[0] + " (워뇨띠) 현재 포지션 : " + txtList[1] + "⬆️\n업데이트 시간 : " + txtList[2] + "\nhttps://kimpya.site/page/readerboard.php",  chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        
        elif SELLECT == "오늘내일 날씨":
            txt = naver_weather.search(msg)
            print(txt)
            telbot.send_message(text=txt, chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif SELLECT == "1주일 내 비소식":
            txt = naver_weather.rainday(msg)
            print(txt)
            telbot.send_message(text=txt, chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
    
################ HA
    elif COMMAND == "HA":
        if msg == "HA추가":
            print('추가할 종목의 이름 or 티커를 입력해주세요')
            telbot.send_message(text='추가할 종목의 이름 or 티커를 입력해주세요', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return
        elif msg == "HA삭제":
            print('추가할 종목의 이름 or 티커를 입력해주세요')
            telbot.send_message(text='추가할 종목의 이름 or 티커를 입력해주세요', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())  
            SELLECT = msg
            return
        elif msg == "HA목록":
            print("ha 관심 목록 조회")
            fileKo = 'korea_watchlist.txt'
            fileMi = 'usa_watchlist.txt'

            querysKo = watchlist.get_querys(fileKo)
            txt1 = "<한국종목>\n"
            for query in querysKo:
                txt1 = txt1 + query + ", "
            querysMi = watchlist.get_querys(fileMi)
            txt2 = "<미국종목>\n"
            for query in querysMi:
                txt2 = txt2 + query + ", "

            telbot.send_message(text="[HA 관심 목록]\n\n" + txt1 + "\n" + txt2, chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        
        elif SELLECT == "HA삭제":
            if codefind(msg, "krx") != 0 :
                fileHa = 'korea_watchlist.txt'
            elif  namefind(msg) != 0 :
                fileHa = 'usa_watchlist.txt'
            else:
                print(msg + ' : 한국, 미국 종목 DB에 없습니다.')
                telbot.send_message(text=msg[6:] + ' : 한국, 미국 종목 DB에 없습니다.', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
                return 

            rst = watchlist.del_query(msg, fileHa) 
            if rst == 0 : 
                print(msg + ' : HA 목록에 없습니다')
                telbot.send_message(text=msg + ' : HA 목록에 없습니다', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            elif rst == 1 :
                print(msg + ' : HA 목록에서 삭제했습니다.')
                telbot.send_message(text=msg + ' : HA 목록에서 삭제했습니다.', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif SELLECT == "HA추가":
            if codefind(msg, "krx") != 0 :
                fileHa = 'korea_watchlist.txt'
            elif  namefind(msg) != 0 :
                fileHa = 'usa_watchlist.txt'
                name = namefind(msg)
            else:
                print(msg + ' : 한국, 미국 종목 DB에 없습니다.')
                telbot.send_message(text=msg + ' : 한국, 미국 종목 DB에 없습니다.', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
                return 

            rst = watchlist.add_query(msg, fileHa)  
            if rst == 0 : 
                print(msg + ' : 이미 HA 목록에 있습니다')
                telbot.send_message(text=msg + ' : 이미 HA 목록에 있습니다.', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            elif rst == 1 :
                if namefind(msg) != 0 : # 미국종목이면
                    print(msg + " ("+ name + ') : HA 목록에 추가되었습니다.')
                    telbot.send_message(text=msg+ " ("+ name + ') : HA 목록에 추가되었습니다.', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
                else : # 한국종목이면
                    telbot.send_message(text=msg + ' : HA 목록에 추가되었습니다.', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())

############## 뉴스
    elif COMMAND == "/NEWS":
        if msg == "뉴스추가":
            telbot.send_message(text="추가할 검색어를 입력해주세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return
        elif msg == "뉴스삭제":
            telbot.send_message(text="삭제할 검색어를 입력해주세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return
        elif msg == "뉴스검색":
            telbot.send_message(text="뉴스 검색어를 입력해주세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return
        elif msg == "뉴스목록":
            querys = naver_news.get_querys()
            txt = ""
            for query in querys:
                txt = txt + query + ", "
            telbot.send_message(text="[뉴스 검색어 목록]\n\n" + txt, chat_id=chat_id, reply_markup=ReplyKeyboardRemove())

        elif SELLECT == "뉴스추가":
            rst = naver_news.add_query(msg)
            if rst == 1:
                telbot.send_message(text=msg + " : 뉴스 검색어 목록에 추가했습니다." , chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            elif rst == 0:
                telbot.send_message(text=msg + " : 뉴스 검색어 목록에 있습니다." , chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif SELLECT == "뉴스삭제":
            rst = naver_news.del_query(msg)
            if rst == 1:
                telbot.send_message(text=msg + " : 뉴스 검색어 목록에서 삭제했습니다." , chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            elif rst == 0:
                telbot.send_message(text=msg + " : 뉴스 검색어 목록에 없습니다." , chat_id=chat_id, reply_markup=ReplyKeyboardRemove())  
        elif SELLECT == "뉴스검색":
            if bot[tp]['chat']['username'] != 'naver_news_alarm':
                telbot.send_message(text="해당 방에는 [@naver_news_alarm] 봇이 없습니다.\
                                        \n봇을 초대하시거나 또는 [네이버 뉴스 알리미](t.me/naver_news_alarm) 에서 사용하세요",chat_id=chat_id, parse_mode='Markdown',disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
                return
            naver_news.get_send_link(msg, telbot2, chat_id)
        
############## 지수
    elif COMMAND == "/JISU":
        if msg == "전부" :
            telbot.send_message(chat_id=chat_id, text = "로딩중...")
            plot_candle_chart_jisu(fetch_jisu('ks11',300),'ks11')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'))
            plot_candle_chart_jisu(fetch_jisu('kq11',300),'kq11')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'))
            plot_candle_chart_jisu(fetch_jisu('dji',300),'dji')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'))
            plot_candle_chart_jisu(fetch_jisu('ixic',300),'ixic')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'))
            plot_candle_chart_jisu(fetch_jisu('US500',300),'US500')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        elif msg == "코스피":
            plot_candle_chart_jisu(fetch_jisu('ks11',300),'ks11')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        elif msg == "코스닥":
            plot_candle_chart_jisu(fetch_jisu('kq11',300),'kq11')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        elif msg == "나스닥":
            plot_candle_chart_jisu(fetch_jisu('ixic',300),'ixic')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        elif msg == "다우존스":
            plot_candle_chart_jisu(fetch_jisu('dji',300),'dji')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        elif msg == "S&P500":
            plot_candle_chart_jisu(fetch_jisu('US500',300),'US500')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        elif msg == "환율":
            plot_candle_chart_jisu(fetch_jisu('usd/krw',300),'usd/krw')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())

    SELLECT = ''
    COMMAND = ''
    EXCHANGE = ''

# 명령어 응답
def get_command(bot, update):
    if bot.channel_post is not None : tp = "channel_post"   #채널일 경우
    elif bot.message is not None : tp = "message"           #그룹일 경우
    elif bot.edited_channel_post is not None  : return      #봇이 채널에 에딧한 메세지일 경우
    else : print(bot)

    chat_id = bot[tp]['chat']['id']
    msg = bot[tp]['text'].split('@')[0].upper()    # / 제외하고, 대문자로 변환
    message_id = bot[tp]['message_id']

    if bot[tp]['text'].find('@') == 0 :
        return 0
    if bot[tp]['text'].split('@')[1] != myBotName :
        print(bot[tp]['text'].split('@')[1] + " : 날 부른게 아닌거 같아요")
        return

    print("get command : " + msg)

    global COMMAND
    if msg == "/BTC":
        reply_keyboard = [['binance', 'upbit', 'cancel']]
        telbot.send_message(text = msg + " 선택됨. 거래소를 선택하세요.", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'), chat_id=chat_id)
    elif msg == "/ETH":
        reply_keyboard = [['binance.', 'upbit.', 'cancel.']]
        telbot.send_message(text = msg + " 선택됨. 거래소를 선택하세요.", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'), chat_id=chat_id)
    
    elif msg == "/SHOWCHART": 
         telbot.send_message(text = "한국주식 이름 or 미국주식 티커를 입력하세요.\
                                    \n(띄어쓰기 조심, 대소문자 상관X)",chat_id=chat_id)
    
    elif msg == "/JISU":
        reply_keyboard = [['코스피','코스닥'],['나스닥','다우존스'],['S&P500','환율'],['전부'],['취소']]
        telbot.send_message(text="보고 싶은 차트를 선택해 주세요.",
                            chat_id=chat_id,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
    elif msg == "/NEWS":
        reply_keyboard = [['뉴스추가','뉴스삭제'],['뉴스검색','뉴스목록'],['취소']]
        telbot.send_message(text="메뉴를 선택해 주세요.",
                            chat_id=chat_id,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
    elif msg == "/HA":
        reply_keyboard = [['HA 알림추가','HA 목록삭제'],['HA 알림목록'],['취소']]
        telbot.send_message(text="메뉴를 선택해 주세요.",
                            chat_id=chat_id,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
    
    elif msg == "/FUN":
        reply_keyboard = [['오늘내일 날씨', '1주일 내 비소식'],['김프', '워뇨띠'],['한강 수온 체크'],['취소']]
        telbot.send_message(text="메뉴를 선택해 주세요.",
                            chat_id=chat_id,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
    
    elif msg == "/HELP":
        telbot.send_message(text = "* 검색방법 *\n" + textHelp,chat_id=chat_id)
    else :
        try: 
            update.bot.edit_message_text(text=msg + " : 잘못된 명령어입니다.\n" +textHelp, chat_id=chat_id, message_id=message_id)
            return
        except Exception : pass

    COMMAND = msg
    try : telbot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception: pass

# 바이낸스 정보 , 선물 설정
def bnc():
    binance = ccxt.binance({
        'apiKey': myApikey,
        'secret': mySecretkey,
        'enableRateLimit': True,
        'options': { 
        'defaultType': 'future'                # 선물거래
        }
    })
    return binance   

# 바이낸스 딕셔너리 데이터를 데이터 프레임으로 변환
def dic2df(dic):
    df = pd.DataFrame(dic, columns = ['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    return df

# 과거 데이터 호출
def fetch_ohlcvs(coin='BTC/USDT', timeframe='1d', limit=30):
    binance = bnc()
    ohlcv = binance.fetch_ohlcv(symbol=coin, timeframe=timeframe, limit=limit)   #데이터 불러오기  
                                        # 시간간격 :'1m','3m','5m','15m','30m','1h','2h','4h','6h','8h','12h','1d','3d','1w','1M'
    return dic2df(ohlcv)   # 딕셔너리를 데이터프레임으로 변환

def fetch_jusik(name, country, count):
    ''' country : krx, us'''
    today = dt.date.today()
    delta = dt.timedelta(days=count)    # count 봉 전부터
    past = today-delta
    if country == "krx":
        df = fdr.DataReader(codefind(name, "krx"), past, today)
    elif country == "us":
        df = fdr.DataReader(name, past, today)


    df.rename(columns = {'Open' : 'open', "Close" : "close", "High" : "high", "Low":"low"}, inplace = True)

    return df

def fetch_jisu(name, count):
    '''
    ks11, kq11, dji, ixic, us500, usd/krw
    '''
    today = dt.date.today()
    delta = dt.timedelta(days=count)    # count 봉 전부터
    past = today-delta
 
    df = fdr.DataReader(name, past, today)

    df.rename(columns = {'Open' : 'open', "Close" : "close", "High" : "high", "Low":"low"}, inplace = True)

    return df

def Ema(df, span=8):
    '''ema 지수이평선 '''
    df["ema"] = df["close"].ewm(span=span, adjust=False).mean()
    return df

def BolingerBand(df, n=20, k=2):
    '''
    20ma, bolUpper, bolLower
    '''
    df['20ma'] = df['close'].rolling(window=n).mean()  
    df['bolUpper'] = df['close'].rolling(window=n).mean() + k* df['close'].rolling(window=n).std()
    df['bolLower'] = df['close'].rolling(window=n).mean() - k* df['close'].rolling(window=n).std()
    return df

def Heiken_ashi(df):
    ''' 
    캔들 시가, 종가 : open, close
    HA캔들 시가, 종가, 고가, 저가 : Open, Close, High, Low
    '''
    df_HA = df
    df_HA['Open'] = df['open']

    # HA 종가 = (현재캔들)(시가+종가+저가+고가)/4
    df_HA["Close"] = (df["open"]+df["high"]+df["low"]+df["close"])/4 
    for i in range(df_HA.shape[0]):  
        if i > 0: 
            # HA 시가 = (이전 HA 시가+ 이전 HA 종가)/2
            df_HA.loc[df_HA.index[i],"Open"] = (df_HA["Open"][i-1] + df_HA["Close"][i-1])/2   
            # HA 고가 = 최대(캔들고가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"High"] = max(df["high"][i],df_HA["Open"][i],df_HA["Close"][i])
            # HA 저가 = 최소(캔들저가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"Low"] = min(df["low"][i],df_HA["Open"][i],df_HA["Close"][i]) 

    return df_HA    

def Rsi(df, period=14):
    ''' rsi, lin30, line70 '''
    dfRSI = df
    dfRSI['U'] = np.where(dfRSI.diff(1)['close'] > 0, dfRSI.diff(1)['close'], 0)  # df.diff(1) : 기준일 종가 - 전일 종가, 0보다 크면 증가분을, 아니면 0을 넣음
    dfRSI['D'] = np.where(dfRSI.diff(1)['close'] < 0, dfRSI.diff(1)['close']*(-1), 0) # 기준일 종가 - 전일 종가, 0보다 작으면 감소분을, 아니면 0을 넣음
    dfRSI['AU'] = dfRSI['U'].rolling(window=period).mean() # period=14 동안의 U의 (이동)평균
    dfRSI['AD'] = dfRSI['D'].rolling(window=period).mean() # period=14 동안의 D의 (이동)평균
    df['rsi'] = dfRSI['AU'] / (dfRSI['AD']+dfRSI['AU']) * 100
    df['line30'] = 30
    df['line70'] = 70
    return df

def Macd(df, short=12, long=26, signal=9):
    ''' macd, macdSignal, macdOsc'''
    df['macd']=df['close'].ewm( span=short, min_periods= long-1, adjust=False).mean() - df['close'].ewm( span=long, min_periods=long-1, adjust=False).mean()
    df['macdSignal'] = df['macd'].ewm( span = signal, min_periods=signal-1, adjust=False).mean()
    df['macdOsc'] = df["macd"] - df['macdSignal']
    return df

def ichimoku(df):
    '''
    tenkan, kijun, senkouSpanA, senkouSpanB, chikouSpan
    '''
    high_prices = df['high']
    close_prices = df['close']
    low_prices = df['low']
    dates = df.index
    
    nine_period_high =  df['high'].rolling(window=9).max()
    nine_period_low = df['low'].rolling(window=9).min()
    df['tenkan'] = (nine_period_high + nine_period_low) /2  #전환선
    
    period26_high = high_prices.rolling(window=26).max()
    period26_low = low_prices.rolling(window=26).min()
    df['kijun'] = (period26_high + period26_low) / 2    #기준선
    
    df['senkouSpanA'] = ((df['tenkan'] + df['kijun']) / 2).shift(26)  #선행스팬A
    
    period52_high = high_prices.rolling(window=52).max()
    period52_low = low_prices.rolling(window=52).min()
    df['senkouSpanB'] = ((period52_high + period52_low) / 2).shift(26)   #선행스팬B
    
    df['chikouSpan'] = close_prices.shift(-26)    #후행스팬

    return df

#  - 봉 -> 해당봉의 모든 지표 표시
def display_all_signal(df, name, interval):

    # df.dropna(inplace=True)         # Na 값 있는 행은 지움

    
    ha = pltygo.Candlestick(x=df.index,
                        open=df['Open'],high=df['High'],
                        low=df['Low'], close=df['Close'],
                        name = 'HA',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
    ema = pltygo.Scatter(x=df.index, y=df['ema'], name="8ema", mode='lines', line=dict(color="green", width=0.8))

    macd = pltygo.Scatter( x=df.index, y=df['macd'],  mode='lines',name="MACD") 
    signal = pltygo.Scatter( x=df.index, y=df['macdSignal'], mode='lines', name="Signal") 
    oscillator = pltygo.Bar( x=df.index, y=df['macdOsc'], name="oscillator") 

    rsi = pltygo.Scatter(x=df.index, y=df['rsi'],  mode='lines',name="RSI")
    line30 = pltygo.Scatter(x=df.index, y=df['line30'], name="30", mode='lines',
                            line=dict(color='firebrick', width=0.5))
    line70 = pltygo.Scatter(x=df.index, y=df['line70'], name="70", mode='lines',
                            line=dict(color='royalblue', width=0.5))

    # ichimoku
    kijun = pltygo.Scatter(x=df.index, y=df['kijun'], name="kijun",  mode='lines', line=dict(color='gray', width=2))
    tenkan = pltygo.Scatter(x=df.index, y=df['tenkan'], name="tenkan",  mode='lines',line=dict(color='red', width=2))
    senkouSpanA = pltygo.Scatter(x=df.index, y=df['senkouSpanA'], name="spanA",  mode='lines',line=dict(color='rgba(167, 59, 206, 0.9)', width=0.8),fill=None)#'tonexty',fillcolor ='rgba(235, 233, 102, 0.5)'
    senkouSpanB = pltygo.Scatter(x=df.index, y=df['senkouSpanB'], name="spanB",  mode='lines',line=dict(color='green', width=0.8),fill='tonexty',fillcolor ='rgba(111, 236, 203, 0.5)')


    ohlc = pltygo.Candlestick(x=df.index,
                        open=df['open'],high=df['high'],
                        low=df['low'], close=df['close'],
                        name = 'OHLC',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
    bolUp = pltygo.Scatter(x=df.index, y=df['bolUpper'], name="bolUpper",  mode='lines', line=dict(color='black', width=1))
    bolLow = pltygo.Scatter(x=df.index, y=df['bolLower'], name="bolLower",  mode='lines',line=dict(color='black', width=1))
    ma20 = pltygo.Scatter(x=df.index, y=df['20ma'], name="20ma",  mode='lines',line=dict(color='orange', width=0.8))

    # OHLC,볼밴 + RSI + MACD 차트
    fig1 = subplots.make_subplots(rows=3, cols=1, vertical_spacing=0.05,
                                row_width=[0.4, 0.4,1], shared_xaxes=True, 
                                subplot_titles=('Candle Chart, close : '+str(format(round(df['close'].iloc[-1],2),',')), 'RSI : '+str(round(df['rsi'].iloc[-1],2)), 'MACD' ))       # row : 행 , col : 열
    # HA 차트 + 20ma 8ema
    fig2 = subplots.make_subplots(rows=1, cols=1, shared_xaxes=True,
                                subplot_titles=('Heiken Ashi, close : '+str(format(round(df['close'].iloc[-1],2),',')),""))       # row : 행 , col : 열
    # OHLC,일목 차트
    fig3 = subplots.make_subplots(rows=1, cols=1, shared_xaxes=True,
                                subplot_titles=('ichimoku Chart, kijun : '+str(format(round(df['kijun'].iloc[-1],2),',')),""))       # row : 행 , col : 열


    # fig1 
    setOhlc = [ohlc, bolUp, bolLow, ma20]
    for ohlc in setOhlc: 
        fig1.add_trace(ohlc, 1,1) 
    
    setRsi = [rsi, line30, line70]
    for rsi in setRsi: 
        fig1.add_trace(rsi, 2,1)

    setMacd = [macd, signal, oscillator]
    for macd in setMacd: 
        fig1.add_trace(macd, 3,1) 

    fig1.update_xaxes(rangeslider_thickness = 0)     # 스크롤바 두께
    fig1.update_layout(title_text=name+ " " + interval +" chart")
    fig1.update_yaxes(side="right")
    fig1.update_layout(legend=dict(yanchor="top", y=1, xanchor="left", x=0))
    fig1.write_image("fig1.png")

    # fig2
    setHa = [ha, ma20, ema]
    for ha in setHa: 
        fig2.add_trace(ha, 1,1)
    
    fig2.update_xaxes(rangeslider_thickness = 0)     # 스크롤바 두께
    fig2.update_layout(title_text=name+ " " + interval +" chart")
    fig2.update_yaxes(side="right")
    fig2.update_layout(legend=dict(yanchor="top", y=1, xanchor="left", x=0))
    fig2.write_image("fig2.png")

    # fig3
    setIchimoku = [senkouSpanA, senkouSpanB, kijun, tenkan ]
    for ichi in setIchimoku: 
        fig3.add_trace(ichi, 1,1)

    for ohlc in setOhlc: 
        fig3.add_trace(ohlc, 1,1)    
    
    fig3.update_xaxes(rangeslider_thickness = 0)     # 스크롤바 두께
    fig3.update_layout(title_text=name+ " " + interval +" chart")
    fig3.update_yaxes(side="right")
    fig3.update_layout(legend=dict(yanchor="top", y=1, xanchor="left", x=0))
    fig3.write_image("fig3.png")

#  - 지표 -> 모든 봉의 해당 지표 값 표시
def display_all_interval(dfSet,intervalSet, name ,signal):
    '''
    signal : 'ohlc', 'ha', 'macd', 'rsi', 
    '''

    if signal == 'ohlc':
        fig = subplots.make_subplots(rows=len(intervalSet), cols=1, 
                                vertical_spacing=0.05,
                                subplot_titles=intervalSet)
        for i in range(len(intervalSet)):
            dfSet[i].dropna(inplace=True)
            ohlc = pltygo.Candlestick(x=dfSet[i].index,
                        open=dfSet[i]['open'],high=dfSet[i]['high'],
                        low=dfSet[i]['low'], close=dfSet[i]['close'],
                        name =intervalSet[i]+ 'OHLC',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
            fig.add_trace(ohlc, i+1,1) 
            
    if signal == 'ha':
        fig = subplots.make_subplots(rows=len(intervalSet), cols=1, 
                                vertical_spacing=0.05,
                                subplot_titles=intervalSet, )
        for i in range(len(intervalSet)):
            dfSet[i] = Heiken_ashi(dfSet[i])
            dfSet[i].dropna(inplace=True)
            ha = pltygo.Candlestick(x=dfSet[i].index,
                        open=dfSet[i]['Open'],high=dfSet[i]['High'],
                        low=dfSet[i]['Low'], close=dfSet[i]['Close'],
                        name = intervalSet[i]+'HA',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
            fig.add_trace(ha, i+1,1) 
    
    if signal == 'macd':
        fig = subplots.make_subplots(rows=int(len(intervalSet)/2), cols=2, 
                                vertical_spacing=0.05,
                                subplot_titles=intervalSet)

        for i in range(len(intervalSet)):
            dfSet[i] = Macd(dfSet[i])
            dfSet[i].dropna(inplace=True)

            macd = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['macd'],
                                    marker=dict(color='red')) 
            macdSignal = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['macdSignal'], marker=dict(color='blue')) 
            oscillator = pltygo.Bar( x=dfSet[i].index, y=dfSet[i]['macdOsc']) 

            setMacd = [macd, macdSignal, oscillator]
            if i%2 == 0: # 짝수번일때 0,2,4
                for macd in setMacd: 
                    fig.add_trace(macd, int(i/2)+1,1)
            else:
                for macd in setMacd: 
                    fig.add_trace(macd, int(i/2)+1,2)

    if signal == 'rsi':
        fig = subplots.make_subplots(rows=int(len(intervalSet)/2), cols=2, 
                                vertical_spacing=0.05,
                                subplot_titles=intervalSet)

        for i in range(len(intervalSet)):
            dfSet[i] = Rsi(dfSet[i])
            dfSet[i].dropna(inplace=True)

            rsi = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['rsi'], marker=dict(color='black')) 
            line30 = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['line30'], marker=dict(color='blue')) 
            line70 = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['line70'], marker=dict(color='red')) 

            setRsi = [rsi, line30, line70]
            if i%2 == 0: # 짝수번일때 0,2,4
                for rsi in setRsi: 
                    fig.add_trace(rsi, int(i/2)+1,1)
            else:
                for rsi in setRsi: 
                    fig.add_trace(rsi, int(i/2)+1,2)

    fig.update_xaxes(rangeslider_thickness = 0)     # 스크롤바 두께
    fig.update_layout(title_text=name+ " " + signal +" chart")
    if signal == 'ha' or signal == 'ohlc':
        fig.update_annotations(yshift=-20,xshift=300)
    else:
        fig.update_annotations(yshift=-20,xshift=-160)    # 서브차트 제목 위치
    fig.update_layout(showlegend=False)             # 범례 안보이게
    fig.write_image("fig3.png")
        
# 시그널 메이커
def signal_maker(df):
    buyCnt = 0
    sellCnt= 0
    txt = []
    # 1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟
    ### macdㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
   
    # 매수	
    if df['macd'].iloc[-1] > df['macdSignal'].iloc[-1] :  # macd > sign
        if df['macd'].iloc[-2] < df['macdSignal'].iloc[-2] : # 1봉전 macd < sign
            txt.append("\n❤️3. 〰️MACD > signal : 골든크로스🔀")
            buyCnt += 3
        elif df['macd'].iloc[-2] < df['macd'].iloc[-1]:   # 1봉전 macd < 0봉전 macd
            txt.append("\n❤️1. 〰️MACD > signal : 정배열↗️")
            buyCnt += 1
        elif  df['macd'].iloc[-2] > df['macd'].iloc[-1]:
            txt.append("\n⚠️0. 〰️MACD > signal : 정배열 조정↗️↘️")
        
    # 매도
    elif df['macd'].iloc[-1] < df['macdSignal'].iloc[-1]:
        if df['macd'].iloc[-2] > df['macdSignal'].iloc[-2]:
            txt.append("\n💙3. 〰️MACD < signal : 데드크로스🔀")
            sellCnt -= 3
        elif df['macd'].iloc[-2] > df['macd'].iloc[-1]:
            txt.append("\n💙1. 〰️MACD < signal : 역배열↘️")
            sellCnt -= 1
        elif df['macd'].iloc[-2] < df['macd'].iloc[-1]:
            txt.append("\n⚠️0. 〰️MACD < signal : 역배열 반등↘️↗️ ")
    
    # ## macd oscㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['macdOsc'].iloc[-2] < df['macdOsc'].iloc[-1] : # 1봉전 < 0봉전
        if df['macdOsc'].iloc[-3] > df['macdOsc'].iloc[-2] : # 2봉전 > 1봉전
            txt.append("❤️3. 〰️MACD OSC : 반등↘️↗️ ")
            buyCnt += 3
        elif df['macdOsc'].iloc[-1] > 0 and df['macdOsc'].iloc[-2] < 0 : 
            txt.append("❤️3. 〰️MACD OSC : ↗️0️⃣↗️ 돌파")
            buyCnt += 3
        else :
            txt.append("❤️1. 〰️MACD OSC : 상승↗️")
            buyCnt += 1

    elif df['macdOsc'].iloc[-2] > df['macdOsc'].iloc[-1] :
        if df['macdOsc'].iloc[-3] < df['macdOsc'].iloc[-2] :
            txt.append("💙3. 〰️MACD OSC : 조정↗️↘️")
            sellCnt -= 3
        elif df['macdOsc'].iloc[-2] < 0 and df['macdOsc'].iloc[-1] > 0 :
            txt.append("💙3. 〰️MACD OSC : ↘️0️⃣↘️ 돌파")
            sellCnt -= 3
        else:
            txt.append("💙1. 〰️MACD OSC : 하락↘️")
            sellCnt -= 1

    # ## rsiㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

    if df['rsi'].iloc[-2] < 31 and df['rsi'].iloc[-2] < df['rsi'].iloc[-1]:
        txt.append("❤️3. 〰️RSI : ↘️30선↗️ 반등")
        buyCnt += 3
    elif df['rsi'].iloc[-2] > 69 and df['rsi'].iloc[-2] > df['rsi'].iloc[-1]:
        txt.append("💙3. 〰️RSI : ↗️70선↘️ 조정")
        sellCnt -= 3
    elif df['rsi'].iloc[-1] < 31 :
        txt.append("❤️2. 〰️RSI : 30⬇️")
        buyCnt += 2
    elif df['rsi'].iloc[-1] > 69 :
        txt.append("💙2. 〰️RSI : 70⬆️")
        sellCnt -= 2
    else:
        txt.append("⚠️0. 〰️30 < RSI < 70")

    # ## Heiken ashiㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['Open'].iloc[-1] < df['Close'].iloc[-1]:
        if df['Open'].iloc[-2] > df['Close'].iloc[-2]:
            txt.append("❤️3. 〰️HA : 양봉전환↘️↗️ ")
            buyCnt += 3
        else:
            txt.append("❤️1. 〰️HA : 양봉↗️  ")
            buyCnt += 1
    elif df['Open'].iloc[-1] > df['Close'].iloc[-1]:
        if df['Open'].iloc[-2] < df['Close'].iloc[-2]:
            txt.append("💙3.  〰️HA : 음봉전환↗️↘️ ")
            sellCnt -= 3
        else:
            txt.append("💙1. 〰️HA : 음봉↘️")
            sellCnt -= 1

    # ## 볼린저밴드ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['close'].iloc[-2] < df['bolLower'].iloc[-2] and df['open'].iloc[-1] < df['close'].iloc[-1]:
        txt.append("❤️3. 〰️BB : ↘️하한↗️ 반등")
        buyCnt += 3
    elif df['close'].iloc[-2] > df['bolUpper'].iloc[-2] and df['open'].iloc[-1] > df['close'].iloc[-1]:
        txt.append("💙3. 〰️BB : ↗️상한↘️ 조정")
        sellCnt -= 3
    elif df['close'].iloc[-1] < df['bolLower'].iloc[-1] :
        txt.append("❤️2. 〰️BB하한 ⬇️")
        buyCnt += 2
    elif df['close'].iloc[-1] > df['bolUpper'].iloc[-1] :
        txt.append("💙2. 〰️BB상한 ⬆️")
        sellCnt -= 2
    elif df['20ma'].iloc[-1] < df['close'].iloc[-1] < df['bolUpper'].iloc[-1]:
        txt.append("❤️1. 〰️BB상한 > 종가 > 20ma : ↗️구간")
        buyCnt += 1
    elif df['bolLower'].iloc[-1] < df['close'].iloc[-1] < df['20ma'].iloc[-1]:
        txt.append("💙1. 〰️BB하한 < 종가 < 20ma : ↘️구간")
        sellCnt -= 1

    # ## 이동평균선 8ema, 20maㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['ema'].iloc[-1] > df['20ma'].iloc[-1] :
        if df['ema'].iloc[-2] < df['20ma'].iloc[-2]:
            txt.append("❤️3. 〰️20ma < 8ema : 골든크로스🔀")
            buyCnt += 3
        elif df['ema'].iloc[-2] < df['ema'].iloc[-1] and df['20ma'].iloc[-2] < df['20ma'].iloc[-1]:
            txt.append("❤️1. 〰️20ma < 8ema : 정배열 ↗️")
            buyCnt += 1
        else :
            txt.append("⚠️0. 〰️20ma < 8ema : 정배열 조정↗️↘️")
    elif df['ema'].iloc[-1] < df['20ma'].iloc[-1] :
        if df['ema'].iloc[-2] > df['20ma'].iloc[-2]:
            txt.append("💙3. 〰️20ma > 8ema : 데드크로스🔀")
            sellCnt -=3
        elif df['ema'].iloc[-2] > df['ema'].iloc[-1] and df['20ma'].iloc[-2] > df['20ma'].iloc[-1]:
            txt.append("💙1. 〰️20ma > 8ema : 역배열↘️")
            sellCnt -= 1
        else :
            txt.append("⚠️0. 〰️20ma > 8ema : 역배열 반등↘️↗️")
    
    ## 일목기준표
    if df['close'].iloc[-2] > df['kijun'].iloc[-2] and df['close'].iloc[-1] < df['kijun'].iloc[-1]:
        txt.append("💙3. 〰️일목 : 기준선 하향돌파⬇️")
        sellCnt -= 3
    elif df['close'].iloc[-2] < df['kijun'].iloc[-2] and df['close'].iloc[-1] > df['kijun'].iloc[-1]:
        txt.append("❤️3. 〰️일목 : 기준선 상향돌파⬆️")
        buyCnt += 3 
    elif df['senkouSpanB'].iloc[-1] > df['close'].iloc[-1] : # 선행스팬 아래
        if df['kijun'].iloc[-1] < df['tenkan'].iloc[-1] : # 기준 < 전환
            txt.append("💙2. 〰️일목 : 선행B⬇️ 저항구간")
            sellCnt -= 2
        elif df['kijun'].iloc[-1] > df['tenkan'].iloc[-1] : # 기준 > 전환
            txt.append("💙1. 〰️ 일복 : 선행B⬇️ 하락구간↘️")
            sellCnt -= 1
    elif df['senkouSpanB'].iloc[-1] < df['close'].iloc[-1] : # 선행스팬 위
        if df['kijun'].iloc[-1] < df['tenkan'].iloc[-1] : # 기준 < 전환
            txt.append("❤️1. 〰️일목 : 선행B⬆️ 상승구간↗️")
            buyCnt += 1
        elif df['kijun'].iloc[-1] > df['tenkan'].iloc[-1] : # 기준 > 전환
            txt.append("❤️2. 〰️일목 : 선행B⬆️ 지지구간")
            buyCnt += 2

    txt.append(buyCnt + sellCnt)
    return txt

# 시그널 메이커 시간 비교
async def signal_maker_time():
    coin = "BTC/USDT"
    count = 100
    intervalSet = ['1m','5m', '15m', '30m', '1h', '4h', '1d']
    plus = 0
    minus = 0
    plusIntervalSet = []
    minusIntervalSet = []
    close = 0

    rsiSet = {}
    bbSet ={}

    for interval in intervalSet:    
        df = ichimoku(Heiken_ashi(Ema(Rsi(BolingerBand(Macd(fetch_ohlcvs(coin, interval, count)))))))
        txt = signal_maker(df)

        if txt[-1] > 5: #매수 시그널
            plus += 1
            temp = ""
            for t in txt:
                if str(type(t)) == "<class 'int'>":
                    if t > 0 :  temp = temp + "\n❤️ " + str(t) + ". 〰️매수 우위"
                    elif t < 0 : temp = temp + "\n💙 " + str(-t) + ". 〰️매도 우위"
                    else : temp = temp + "\n⚠️ " + str(t) + ". 〰️중립" 
                else: temp = temp + t + "\n"
            temp = "💲💲 binance "+ coin +" " + interval +" 💲💲\n"+ temp
            plusIntervalSet.append(temp)
        elif txt[-1] <-5: #매도 시그널
            minus += 1
            temp = ""
            for t in txt:
                if str(type(t)) == "<class 'int'>":
                    if t > 0 : temp = temp + "\n❤️ " + str(t) + ". 〰️매수 우위"
                    elif t < 0 : temp = temp + "\n💙 " + str(-t) + ". 〰️매도 우위"
                    else : temp = temp + "\n⚠️ " + str(t) + ". 〰️중립" 
                else: temp = temp + t + "\n"
            temp = "💲💲 binance "+ coin +" " + interval +" 💲💲\n"+ temp
            minusIntervalSet.append(temp)
        
        # rsi
        if df['rsi'].iloc[-1] < 31:
            rsiSet[interval] =df['rsi'].iloc[-1]
        elif df['rsi'].iloc[-1] > 69:
            rsiSet[interval] =df['rsi'].iloc[-1]
        
        # BB
        close = df['close'].iloc[-1]
        if df['bolUpper'].iloc[-1] < df['high'].iloc[-1] :
            if df['bolUpper'].iloc[-1] < df['close'].iloc[-1] :
                bbSet[interval] =df['bolUpper'].iloc[-1]
            else:
                bbSet[interval] =df['bolUpper'].iloc[-1]
        elif df['bolLower'].iloc[-1] > df['low'].iloc[-1] :
            if df['bolLower'].iloc[-1] > df['close'].iloc[-1] :
                bbSet[interval] =df['bolLower'].iloc[-1]
            else:
                bbSet[interval] =df['bolLower'].iloc[-1]
    
    if plus >= 4 : # 매수시그널이 더 많을때
        for txt in plusIntervalSet:
            telbot.sendMessage(text=txt, chat_id=channel_id_binance)
    elif minus >= 4 : # 매도시그널이 더 많을때
        for txt in minusIntervalSet:
            telbot.sendMessage(text=txt, chat_id=channel_id_binance)
    
    if len(rsiSet) >=5:  # rsi <31 해당하는게 5개 이상있으면
        txtr="❗️❗️ RSI ❗️❗️\n"
        for key in rsiSet:
            txtr = txtr + (key + " : " + str(round(rsiSet[key],2)) + "\n")
        telbot.sendMessage(text=txtr, chat_id=channel_id_binance)
    
    if len(bbSet) >=5:  # BB 초과, 미만 5개 이상있으면
        txtbb ="❗️❗️ BB ❗️❗️ / close : " + str(format(round(close,2),',')) +"\n"
        for key in bbSet:
            txtbb = txtbb + (key + " : " + str(format(round(bbSet[key],2),',')) + "\n")
        telbot.sendMessage(text=txtbb, chat_id=channel_id_binance)
    
    
    ############## 5분마다 실행할 코드들 ############################

    global aoaLastTime
    try :
        txtList = Whales_Position()
        if txtList[2] != aoaLastTime:
            if txtList[1] == "SHORT":
                telbot.sendMessage(text=txtList[0] + " (워뇨띠) 현재 포지션 : " + txtList[1] + "⬇️\n업데이트 시간 : " + txtList[2] + "\nhttps://kimpya.site/page/readerboard.php", chat_id=channel_id_binance)
            elif txtList[1] == "LONG":
                telbot.sendMessage(text=txtList[0] + " (워뇨띠) 현재 포지션 : " + txtList[1] + "⬆️\n업데이트 시간 : " + txtList[2] + "\nhttps://kimpya.site/page/readerboard.php", chat_id=channel_id_binance)
            aoaLastTime = txtList[2]
    except Exception:
        pass
    
    naver_news.send_new_links(telbot2, group_id_naver_news)

# 5분에 한번씩 실행
schedule.every().hour.at("04:45").do(lambda:asyncio.run(signal_maker_time()))
schedule.every().hour.at("09:45").do(lambda:asyncio.run(signal_maker_time()))
schedule.every().hour.at("14:45").do(lambda:asyncio.run(signal_maker_time()))
schedule.every().hour.at("19:45").do(lambda:asyncio.run(signal_maker_time()))
schedule.every().hour.at("24:45").do(lambda:asyncio.run(signal_maker_time()))
schedule.every().hour.at("29:45").do(lambda:asyncio.run(signal_maker_time()))
schedule.every().hour.at("34:45").do(lambda:asyncio.run(signal_maker_time()))
schedule.every().hour.at("39:45").do(lambda:asyncio.run(signal_maker_time()))
schedule.every().hour.at("44:45").do(lambda:asyncio.run(signal_maker_time()))
schedule.every().hour.at("49:45").do(lambda:asyncio.run(signal_maker_time()))
schedule.every().hour.at("54:45").do(lambda:asyncio.run(signal_maker_time()))
schedule.every().hour.at("59:45").do(lambda:asyncio.run(signal_maker_time()))

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()
header = {'user-agent':ua.chrome}

aoaLastTime =""

def Whales_Position():
    '''
    aoa, aoaPosition, aoaTime
    '''
    try:
        Whales_URL = requests.get('https://kimpya.site/apps/leaderboard.php', headers=header)
        Whales = BeautifulSoup(Whales_URL.content, 'html.parser')
        AOA = Whales.find('div', class_="tbl darklight")
    except Exception:
        return "kimpya.site 접속에러"
    aoa = AOA.table.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.td.next_sibling.get_text() # aoa
    aoaPosition = AOA.table.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.td.next_sibling.next_sibling.get_text() # position
    aoaTime = AOA.table.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.get_text() # 업데이트 날짜
    # 
    txt = []
    txt.append(aoa)
    txt.append(aoaPosition)
    txt.append(aoaTime)
    return txt 

def heiken_ashi_coin(country, coin='BTC/USDT', interval='1d', count=60):
    if country == "binance":
        df = fetch_ohlcvs(coin, interval, count)
    elif country == "upbit":
        df = pyupbit.get_ohlcv(coin, interval, count)
    df_HA = df

    df_HA["Open"] = df["open"]       # 캔들 시가
    df_HA["Close"] = df["close"]     # 캔들 종가

    # HA 종가 = (현재캔들)(시가+종가+저가+고가)/4
    df_HA["close"] = (df["open"]+df["high"]+df["low"]+df["close"])/4 
    for i in range(df_HA.shape[0]):  
        if i > 0: 
            # HA 시가 = (이전 HA 시가+ 이전 HA 종가)/2
            df_HA.loc[df_HA.index[i],"open"] = (df_HA["open"][i-1] + df_HA["close"][i-1])/2   
            # HA 고가 = 최대(캔들고가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"high"] = max(df["high"][i],df_HA["open"][i],df_HA["close"][i])
            # HA 저가 = 최소(캔들저가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"low"] = min(df["low"][i],df_HA["open"][i],df_HA["close"][i]) 
    # 20일 이동평균
    df_HA["ma"] = df["Close"].rolling(window=20).mean()
    # 8일 지수이동평균
    df_HA["ema"] = df["Close"].ewm(span=8, adjust=False).mean()

    df_HA = df_HA.fillna(0) # NA 값을 0으로
    return df_HA       

def heiken_ashi_jusik(token, region, count):
    today = dt.date.today()
    delta = dt.timedelta(days=count)    # count 봉 전부터
    past = today-delta
    if region == "krx":
        df = fdr.DataReader(codefind(token, "krx"), past, today)
    if region == "us":
        df = fdr.DataReader(token, past, today)
    
    df_HA = df
    df_HA["open"] = df["Open"]
    df_HA["close"] = df["Close"]
    df_HA["low"] = df["Low"]
    df_HA["high"] = df["High"]
    df_HA["Ropen"] = df["Open"]       # 캔들 시가
    df_HA["Rclose"] = df["Close"]     # 캔들 종가

    # HA 종가 = (현재캔들)(시가+종가+저가+고가)/4
    df_HA["close"] = (df["Open"]+df["High"]+df["Low"]+df["Close"])/4 
    for i in range(df_HA.shape[0]):  
        if i > 0: 
            # HA 시가 = (이전 HA 시가+ 이전 HA 종가)/2
            df_HA.loc[df_HA.index[i],"open"] = (df_HA["open"][i-1] + df_HA["close"][i-1])/2   
            # HA 고가 = 최대(캔들고가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"high"] = max(df["High"][i],df_HA["open"][i],df_HA["close"][i])
            # HA 저가 = 최소(캔들저가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"low"] = min(df["Low"][i],df_HA["open"][i],df_HA["close"][i]) 
    # 20일 이동평균
    df_HA["ma"] = df["Close"].rolling(window=20).mean()
    # 8일 지수이동평균
    df_HA["ema"] = df["Close"].ewm(span=8, adjust=False).mean()

    df_HA = df_HA.fillna(0) # NA 값을 0으로
    return df_HA       

async def buy_signal(token, interval, df_HA, channel_id=None):
    # ha음봉(ha_open > ha_close) -> ha양봉(ha_open < ha_close)  # 양전
    if df_HA["open"].iloc[-2] > df_HA["close"].iloc[-2] and df_HA["open"].iloc[-1] < df_HA["close"].iloc[-1] :
        # 8ema < 20ma   # 하락추세중 추세반전
        if df_HA["ema"].iloc[-1] < df_HA["ma"].iloc[-1]:
            # 8ema < ha_close  :  100% 매수
            if df_HA["ema"].iloc[-1] < df_HA["close"].iloc[-1]:
                plot_candle_chart(df_HA, token)
                if namefind(token) != 0:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=namefind(token) + " ("+token+")\n" + interval + " 양봉전환 : 100% 매수\n\
                                            close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
                else :
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), caption=token + " " + interval + " 양봉전환 : 100% 매수\nclose : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
                return 100
            # 8ema > ha_close  :  50% 매수
            if df_HA["ema"].iloc[-1] > df_HA["close"].iloc[-1]:
                plot_candle_chart(df_HA, token)
                if namefind(token) != 0:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=namefind(token) + " ("+token+")\n" + interval + " 양봉전환 : 50% 매수\n\
                                            close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
                else :
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), caption=token + " " + interval + " 양봉전환 : 50% 매수\nclose : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
                return 50
        # 8ema > 20ma   # 상승추세중 불타기 추세반전
        if df_HA["ema"].iloc[-1] > df_HA["ma"].iloc[-1]:
            plot_candle_chart(df_HA, token)
            if namefind(token) != 0:
                telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                caption=namefind(token) + " ("+token+")\n" + interval + " 양봉전환 : 10% 매수\n\
                                        close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
            else :
                telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), caption=token + " " + interval + " 양봉전환 : 10% 매수\nclose : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
            return 10
    time.sleep(1)
    return 0

async def sell_signal(token, interval, df_HA, channel_id=None):
    # ha양봉(ha_open < ha_close) -> ha양봉(ha_open < ha_close)  # 양봉연속
    if df_HA["open"].iloc[-2] < df_HA["close"].iloc[-2] and df_HA["open"].iloc[-1] < df_HA["close"].iloc[-1]:
        # ha양봉 and 캔들양봉 : 10% 매도
        if df_HA["Open"].iloc[-1] < df_HA["Close"].iloc[-1]:
            # post_message(tokenCoin, channel, token + " " + interval + " 양봉연속 : 10% 매도")
            return 10
    # ha양봉(ha_open < ha_close) -> ha음봉(ha_open > ha_close)  # 음봉전환 : 전량매도
    if df_HA["open"].iloc[-2] < df_HA["close"].iloc[-2] and df_HA["open"].iloc[-1] > df_HA["close"].iloc[-1]:
        # 아직 상승추세
        if df_HA["ema"].iloc[-1] > df_HA["ma"].iloc[-1] :
            # 작은 낙폭
            if df_HA["close"].iloc[-1] > df_HA["ema"].iloc[-1] :
                plot_candle_chart(df_HA, token)
                if namefind(token) != 0:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=namefind(token)+" (" + token + ")\n"
                                    + interval + " 음봉전환 : 50% 매도\n\
                                    close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
                else:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), caption=token + " " + interval + " 음봉전환 : 50% 매도\nclose : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
                return 50
            # 큰 낙폭    
            if df_HA["close"].iloc[-1] < df_HA["ema"].iloc[-1] :
                plot_candle_chart(df_HA, token)
                if namefind(token) != 0:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=namefind(token)+" (" + token + ")\n"
                                    + interval + " 음봉전환 : 80% 매도\n\
                                    close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
                else:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), caption=token + " " + interval + " 음봉전환 : 80% 매도\nclose : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
                return 80
            # 떡락
            if df_HA["close"].iloc[-1] < df_HA["ma"].iloc[-1] :
                plot_candle_chart(df_HA, token)
                if namefind(token) != 0:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=namefind(token)+" (" + token + ")\n"
                                    + interval + " 음봉전환 : 100% 매도\n\
                                    close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
                else:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), caption=token + " " + interval + " 음봉전환 : 100% 매도\nclose : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
                return 100
        # 하락추세
        if df_HA["ema"].iloc[-1] < df_HA["ma"].iloc[-1] :
            plot_candle_chart(df_HA, token)
            if namefind(token) != 0:
                telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                caption=namefind(token)+" (" + token + ")\n"
                                + interval + " 음봉전환 : 100% 매도\n\
                                close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
            else:
                telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), caption=token + " " + interval + " 음봉전환 : 100% 매도\nclose : " + str(format(round(df_HA["Close"].iloc[-1],2),',')))  # 사진보내기
            return 100
    time.sleep(1)
    return 0
    # (1봉전) 8ema > 20ma and (현재) 8ema < 20ma  : 전량매도

####################### jusik ##########################

count = 60
async def krx_ha_check():
    jongmok = watchlist.get_querys('korea_watchlist.txt')
    for token in jongmok: # krx
        print(token)
        df_HA = heiken_ashi_jusik(token, "krx", count)
        await buy_signal(token, "day", df_HA, channel_id=channel_id_korea)
        await sell_signal(token, "day", df_HA, channel_id=channel_id_korea)
    telbot.sendMessage(text=naver_weather.rainday("순천"), chat_id=channel_id_feedback)    # 날씨 알림!!
# 매일 정해진 시간에
schedule.every().day.at("08:52").do(lambda:asyncio.run(krx_ha_check()))
schedule.every().day.at("15:02").do(lambda:asyncio.run(krx_ha_check()))
schedule.every().day.at("20:02").do(lambda:asyncio.run(krx_ha_check()))

async def us_ha_check():
    jongmok2 = watchlist.get_querys('usa_watchlist.txt')        
    for token in jongmok2: #us
        print(token)
        df_HA = heiken_ashi_jusik(token, "us", count)
        await buy_signal(token, "day", df_HA, channel_id=channel_id_usa)
        await sell_signal(token, "day", df_HA, channel_id=channel_id_usa)
# 매일 정해진 시간에
schedule.every().day.at("16:31").do(lambda:asyncio.run(us_ha_check())) 
schedule.every().day.at("22:31").do(lambda:asyncio.run(us_ha_check()))


########### upbit ####################
coin = "KRW-BTC"

    # 60분봉
async def coin_ha_check_60min():
    interval_60 = "minute60"
    df_HA_h = heiken_ashi_coin("upbit",coin, interval_60, count)
    await buy_signal(coin, interval_60, df_HA_h, channel_id=channel_id)
    await sell_signal(coin, interval_60, df_HA_h, channel_id=channel_id)
# 60분에 한번씩 실행
schedule.every().hour.at("59:00").do(lambda:asyncio.run(coin_ha_check_60min()))
    # 1일봉
async def coin_ha_check_day():
    interval_day = "day"
    df_HA_d = heiken_ashi_coin("upbit",coin, interval_day, count)
    await buy_signal(coin, interval_day, df_HA_d, channel_id=channel_id)
    await sell_signal(coin, interval_day, df_HA_d, channel_id=channel_id)
schedule.every().day.at("08:50").do(lambda:asyncio.run(coin_ha_check_day()))
schedule.every().day.at("23:50").do(lambda:asyncio.run(coin_ha_check_day()))

############## binance ####################

btc = 'BTC/USDT'

    # 60분봉
async def binance_ha_check_60min():
    interval_60 = "1h"
    df_HA_h = heiken_ashi_coin("binance",btc, interval_60, count)
    await buy_signal(btc, interval_60, df_HA_h, channel_id=channel_id_binance)
    await sell_signal(btc, interval_60, df_HA_h, channel_id=channel_id_binance)

# 60분에 한번씩 실행
schedule.every().hour.at("58:00").do(lambda:asyncio.run(binance_ha_check_60min()))
    # 1일봉
async def binance_ha_check_day():
    interval_day = "1d"
    df_HA_d = heiken_ashi_coin("binance",btc, interval_day, count)
    await buy_signal(btc, interval_day, df_HA_d, channel_id=channel_id_binance)
    await sell_signal(btc, interval_day, df_HA_d, channel_id=channel_id_binance)
schedule.every().day.at("08:52").do(lambda:asyncio.run(binance_ha_check_day()))
schedule.every().day.at("23:52").do(lambda:asyncio.run(binance_ha_check_day()))

# from telegram.utils.helpers import escape_markdown escape_markdown(,version=2)
telbot.sendMessage(chat_id=channel_id_feedback, text=updateText,parse_mode='Markdown',disable_web_page_preview=True) # 메세지 보내기

# 작동 테스트
if runtest==1:
    print("runtest")
    asyncio.run(coin_ha_check_60min())
    asyncio.run(coin_ha_check_day())
    asyncio.run( binance_ha_check_day())
if run_ko == 1:
    asyncio.run( krx_ha_check())
if run_us == 1:
    asyncio.run( us_ha_check())

def alarmi():
    print("쓰레딩이이잉")
    while True:
        try:
            schedule.run_pending()

        except Exception as e:   # 에러 발생시 예외 발생
            print(e)
            telbot.sendMessage(chat_id=channel_id_feedback, text=(e)) # 메세지 보내기
            telbot.sendMessage(chat_id=channel_id_feedback, text=("스레드 에러발생!")) # 메세지 보내기



try :
    # 스레드로 while문 따로 돌림
    t = Thread(target=alarmi, daemon=True)
    t.start()

    # 메시지 받아오는 곳
    message_handler = MessageHandler(Filters.text & (~Filters.command), get_name)
    updater.dispatcher.add_handler(message_handler)
    # 명령어 받아오는 곳
    message_handler2 = MessageHandler(Filters.command, get_command)
    updater.dispatcher.add_handler(message_handler2)
    # 버튼 콜백
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_get))
    updater.start_polling(timeout=3)
    updater.idle()
except Exception as e:               # 에러 발생시 예외 발생
    print(e)
    telbot.sendMessage(chat_id=channel_id_feedback, text=(e)) # 메세지 보내기
    telbot.sendMessage(chat_id=channel_id_feedback, text=("텔레그램발생!")) # 메세지 보내기
















# 관심종목 텍스트파일로 저장 -> 추가, 삭제 기능