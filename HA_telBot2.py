from asyncio.windows_events import NULL
from os import name
from threading import Thread
from FinanceDataReader import data
import matplotlib as mpl
import pyupbit
import numpy as np
import requests
import time
from requests.models import DEFAULT_REDIRECT_LIMIT
import schedule
from fbprophet import Prophet
from bs4 import BeautifulSoup #웹 크롤링을 위한 라이브러리
import FinanceDataReader as fdr
from scipy.integrate._ivp.radau import P #종목 주가 정보 가져오기
import talib.abstract as ta #기술적 분석을 위한 지표
import datetime as dt
import matplotlib.pyplot as plt
# import yfinance
import mplfinance
import ccxt
import sys
import pandas as pd
import telegram as tel
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ccxt.binance import binance



jongmok = {"강원랜드", "고려신용정보", "골프존","기아", "대원미디어", "대한항공", "대교","두산퓨얼셀", "두산중공업","더네이쳐홀딩스", 
        "데브시스터즈", "롯데칠성","빙그레", "삼성전자", "삼성엔지니어링", "삼성에스디에스","삼성SDI", "삼성바이오로직스","삼성제약","서린바이오",
        "셀트리온","셀트리온제약","셀트리온헬스케어", "스튜디오드래곤", "신세계", "신풍제약","신일제약", "씨젠","씨에스윈드", "씨에스베어링",
        "에스엠", "이마트","아이진","우리바이오", "와이지엔터테인먼트", "위메이드","용평리조트",
        "제일약품", "진매트릭스", "천보",  "카카오", "코오롱인더", "펄어비스","프로스테믹스", "하이브", "한화솔루션", "한전KPS","한국전력", "한미반도체", "현대차", "현대모비스", 
        "현대바이오", "휴마시스", "CJ ENM","CJ대한통운","CJ제일제당","CJ CGV","SK하이닉스", "BGF", "F&F", "NAVER", "LG디스플레이", "DB하이텍", "LG화학", "LG전자", 
        "HMM","SK이노베이션", "SK바이오사이언스","SK케미칼","JYP Ent.", "KT","KG ETS",
        "KODEX 자동차","KODEX 200","KODEX 200 중소형","KODEX 200ESG", "KODEX 200동일가중", "네비게이터 친환경자동차밸류체인액티브", "TIGER KRX BBIG K-뉴딜", 
        "KBSTAR Fn수소경제테마", "TIGER KRX2차전지K-뉴딜","TIGER TOP10", "TIGER 금은선물(H)", "KODEX 바이오", 
        "TIGER KRX바이오K-뉴딜", "TIGER 여행레저", "TIGER 우량가치", "TIGER 경기방어"}
jongmok2 = {"AAPL","ABNB","ADBE","ASML","ATVI","AMD","AMZN","AMCR","AXP","BA","BAC","BLK","BRK",
        "CCL","CPNG","COIN","DD","DIS","DISCK","DPZ","DOW","FITB","F","FB","GOOGL","GS","GM", "GLW","GPS",
        "INTC","IRM","JNJ","JPM",
        "KO","KEY","LMT","LEVI","NFLX","NVDA","NET","NEM","NKE", "MRNA","MET","MO","MSFT", "MRK","ORCL",
        "PFE", "PINS", "PLD", "PVH","PYPL","QCOM", "RL","REAL","RBLX","SNAP", "SNOW", "SPCE","SHOP",
        "TSLA", "TSM","TWTR", "U","UBER","UAL","V","VFC","VIAC","ZM","Z"}

try :
    
    myApikey = "hOpHmrM35aqoqakISj0m7PAy42bDLXBmhXIrOsvadPBU6bW8Gtin0ggp7UnzFg9f"
    mySecretkey = "rJp7j47DyzzvqRhaa9ExusnxrcPSF2I6Aa1B6bNvjlzxv3VP7fs3sl3cMNvSbEdU"

    #텔레그램 봇
    myToken = '1811197670:AAFGAP3NO6_vJmHeQTURZO-1rAsF3eLdmYQ'
    telbot = tel.Bot(token=myToken)
    channel_id = "@ha_alarm"                  # 업비트 채널
    channel_id_binance = "@ha_alarm_binance"  # 바이낸스 채널
    channel_id_korea = "@ha_alarm_korea"  # 한국 채널
    channel_id_usa = "@ha_alarm_usa"  # 미국 채널
    channel_id_feedback = "@ha_alarm_feedback"  # 피드백채널
    updater = Updater(myToken, use_context=True)

    # slack 봇
    tokenCoin = "xoxb-2014329623457-2188366688005-bv8E4uA8PR1VFVqEdCKDrTkP"
    channelUpbit = "#upbit"
    channelBNC = "#binance"
    channelUpdate = "#3업데이트상황"
    tokenKorea = "xoxb-2014329623457-2007907637812-PTbIufzrrrAHBzHvJT6UTlZB"
    channelKorea = "#korea"
    tokenUsa = "xoxb-2014329623457-2195893790725-rO81U1XXmHEvN6ePMnLY74Cq"
    channelUsa = "#usa"

    image = "jusik.png"
    msgOn = 1 # 1일때 메시지 켜짐, 0일때 메시지 꺼짐
    runtest = 0 # 0일때 코인 실행 꺼짐, 1일때 코인 실행
    run_ko = 0 # 0일때 한국 실행 꺼짐 1일때 실행
    run_us =0 # 0일때 미국 실행 꺼짐 1일때 실행


    # 한국 코스피,코스닥 목록
    krx = fdr.StockListing('KRX')
    # 미국 주식 목록
    sp500 = fdr.StockListing('S&P500')
    nasdaq = fdr.StockListing('NASDAQ')
    nyse = fdr.StockListing('NYSE')


    # 슬랙 메시지 전송
    def post_message(token, channel, text):
        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+token},
            data={"channel": channel,"text": text}
        )
        print(response)
    # 슬랙 이미지 전송
    from slack import WebClient
    def post_image(token, channel, image):
        client = WebClient(token=token)
        filepath = image # Your filepath
        response = client.files_upload(channels=channel, file=filepath)

    # 캔들차트 그리기
    def plot_candle_chart(df, title):  
        
        adp = [mplfinance.make_addplot(df["ema"], color='green')]  # 이평선
        fig = mplfinance.plot(df, type='candle', style='charles', mav=(20),
                        title=title, ylabel='price', show_nontrading=False,
                        savefig='jusik.png',
                        addplot=adp
                        )
        print(title + " plot candle chart")

    def find_in_list(name):
        for jm in jongmok:
            if jm == name:
                print(name + " 목록에 있습니다")
                return 1
        for jm in jongmok2:
            if jm==name:
                print(name + " 목록에 있습니다")
                return 2
        print(name + " 목록에 없습니다")
        return 0
    
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

    # 텔레그램 메시지 응답
    def get_name(bot, update):
        msg = bot.channel_post.text               #  최근 입력된 메시지의 텍스트
        chat_id = bot.channel_post.chat.id         # 최근 입력된 메시지의 챗아이디
        message_id=bot.channel_post.message_id      # 메시지의 아이디
        if korea == 1:
            # update.bot.send_message(chat_id, msg)      # 업데이트 실행. 메시지 재 전송 \\
            if codefind(msg,"krx") != 0 : # 종목이 목록에 있으면
                button_list = build_button(["1일봉","cancel"], msg)
                show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
                update.bot.edit_message_text(text=msg+" 봉을 선택해 주세요.",
                                            chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=show_markup)
            else:
                update.bot.edit_message_text(text=msg+"는 목록에 없습니다. (대소문자, 띄어쓰기 주의)",
                                            chat_id=chat_id,
                                            message_id=message_id)
        elif usa == 1:
            if namefind(msg) != 0 : # 종목이 목록에 있으면
                button_list = build_button(["1일봉","cancel"], msg)
                show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
                update.bot.edit_message_text(text=msg+" 봉을 선택해 주세요.",
                                            chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=show_markup)
            else:
                update.bot.edit_message_text(text=msg+"는 목록에 없습니다. (대소문자, 띄어쓰기 주의)",
                                            chat_id=chat_id,
                                            message_id=message_id)
        elif korea == 2:
            if codefind(msg,"krx") != 0 : # 종목이 목록에 있으면
                button_list = build_button(["30","100","200","500","1000","10000","cancel"], msg)
                show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
                update.bot.edit_message_text(text=msg+" 기간(봉 count)을 선택해 주세요.",
                                            chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=show_markup)
            else:
                update.bot.edit_message_text(text=msg+"는 목록에 없습니다. (대소문자, 띄어쓰기 주의)",
                                            chat_id=chat_id,
                                            message_id=message_id)
        elif usa == 2:
            if namefind(msg) != 0 : # 종목이 목록에 있으면
                button_list = build_button(["30","100","200","500","1000","10000","cancel"], msg)
                show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
                update.bot.edit_message_text(text=msg+" 기간(봉 count)을 선택해 주세요.",
                                            chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=show_markup)
            else:
                update.bot.edit_message_text(text=msg+"는 목록에 없습니다. (대소문자, 띄어쓰기 주의)",
                                            chat_id=chat_id,
                                            message_id=message_id)

    # 명령어 응답
    def get_command(bot, update):
        print("get")
        chat_id = bot.channel_post.chat.id         # 최근 입력된 메시지의 챗아이디
        msg = bot.channel_post.text               #  최근 입력된 메시지의 텍스트 

        show_list = []
        show_list.append(InlineKeyboardButton("binance", callback_data="binance")) # add on button
        show_list.append(InlineKeyboardButton("upbit", callback_data="upbit")) # add off button
        show_list.append(InlineKeyboardButton("korea", callback_data="korea")) # add off button
        show_list.append(InlineKeyboardButton("usa", callback_data="usa")) # add off button
        show_list.append(InlineKeyboardButton("cancel", callback_data="cancel")) # add cancel button
        show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup

        show_list2 = []
        show_list2.append(InlineKeyboardButton("binance", callback_data="binance2")) # add on button
        show_list2.append(InlineKeyboardButton("upbit", callback_data="upbit2")) # add off button
        show_list2.append(InlineKeyboardButton("korea", callback_data="korea2")) # add off button
        show_list2.append(InlineKeyboardButton("usa", callback_data="usa2")) # add off button
        show_list2.append(InlineKeyboardButton("cancel", callback_data="cancel")) # add cancel button
        show_markup2 = InlineKeyboardMarkup(build_menu(show_list2, len(show_list2) - 1)) # make markup

        if msg == "/s":
            bot.effective_message.reply_text("Heiken Ashi chart", reply_markup=show_markup)
        elif msg == "/t":
            bot.effective_message.reply_text("Heiken Ashi chart backtest", reply_markup=show_markup2)   
        elif msg == "/help":
            bot.effective_message.reply_text("/s 을 입력해보세요! \n1. 초록봉 : 상승추세 / 빨간봉 : 하락추세 \n2. 초록->빨강 전환 : 매도신호  \n3. 빨강->초록 전환 : 매수신호 \n4. 주황선 : 20이평선 / 초록선 : 8지수이평선  \n5. 초록선이 주황선 아래 : 장기상승추세 \n6. 초록선이 주황선 위 : 장기하락추세 \n\n하이킨 아시 차트에 대한 자세한 설명은 \n아래 사이트를 참고하세요.")
            bot.effective_message.reply_text("https://tailong.tistory.com/143")

    # 버튼 누르면 다시 호출되는
    def callback_get(bot, update):
        data_selected = bot.callback_query.data
        print("callback : ", data_selected)
        global korea; global usa; 
        # 취소 버튼
        if data_selected.find("cancel") != -1 :
            update.bot.edit_message_text(text="취소하였습니다.",
                                        chat_id=bot.callback_query.message.chat_id,
                                        message_id=bot.callback_query.message.message_id)
            korea =0; usa=0
            return

        # 시장 선택됨. 코인->봉선택 , 주식->종목명입력
        if len(data_selected.split(",")) == 1 :
            if data_selected == "binance": 
                button_list = build_button(["1일봉", "1시간봉", "5분봉", "cancel"], data_selected)
                show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
                update.bot.edit_message_text(text="봉을 선택해 주세요.",
                                            chat_id=bot.callback_query.message.chat_id,
                                            message_id=bot.callback_query.message.message_id,
                                            reply_markup=show_markup)
            if data_selected == "upbit": 
                button_list = build_button(["1일봉", "1시간봉", "5분봉", "cancel"], data_selected)
                show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
                update.bot.edit_message_text(text="봉을 선택해 주세요.",
                                            chat_id=bot.callback_query.message.chat_id,
                                            message_id=bot.callback_query.message.message_id,
                                            reply_markup=show_markup)
            if data_selected == "korea": 
                update.bot.edit_message_text(text="종목명을 입력해주세요(대소문자, 띄어쓰기 주의)",
                                            chat_id=bot.callback_query.message.chat_id,
                                            message_id=bot.callback_query.message.message_id)
                korea = 1
            if data_selected == "usa": 
                update.bot.edit_message_text(text="티커를 입력해주세요(대소문자 주의)",
                                            chat_id=bot.callback_query.message.chat_id,
                                            message_id=bot.callback_query.message.message_id)
                # global usa ; usa = 1 # 전역변수
                usa = 1
            if data_selected == "binance2": 
                button_list = build_button(["1d", "4h", "1h", "30m", "15m", "5m", "1m","cancel"], data_selected)
                show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
                update.bot.edit_message_text(text="봉을 선택해 주세요.",
                                            chat_id=bot.callback_query.message.chat_id,
                                            message_id=bot.callback_query.message.message_id,
                                            reply_markup=show_markup)
            if data_selected == "upbit2": 
                button_list = build_button(["1d", "4h", "1h", "30m", "15m", "5m", "1m", "cancel"], data_selected)
                show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
                update.bot.edit_message_text(text="봉을 선택해 주세요.",
                                            chat_id=bot.callback_query.message.chat_id,
                                            message_id=bot.callback_query.message.message_id,
                                            reply_markup=show_markup)
            if data_selected == "korea2": 
                update.bot.edit_message_text(text="종목명을 입력해주세요(대소문자, 띄어쓰기 주의)",
                                            chat_id=bot.callback_query.message.chat_id,
                                            message_id=bot.callback_query.message.message_id)
                korea = 2
            if data_selected == "usa2": 
                update.bot.edit_message_text(text="티커를 입력해주세요(대소문자 주의)",
                                            chat_id=bot.callback_query.message.chat_id,
                                            message_id=bot.callback_query.message.message_id)
                # global usa ; usa = 1 # 전역변수
                usa = 2
                
        elif len(data_selected.split(",")) == 2 :
            if data_selected.split(",")[-1] != "" :
                print(data_selected)
                name = data_selected.split(",")[0]  # 첫번째 선택된 것 
                if  name == "binance" :  # 바이낸스 검색
                    # 바이낸스 HA 계산, 차트 띄워
                    if data_selected.split(",")[-1] == "1일봉": interval = '1d'
                    elif data_selected.split(",")[-1] == "1시간봉": interval = '1h'
                    elif data_selected.split(",")[-1] == "5분봉": interval = '5m'
                    plot_candle_chart(heiken_ashi_coin("binance",'BTC/USDT', interval, 60),'BTC/USDT')
                    telbot.send_photo(chat_id=bot.callback_query.message.chat_id, photo=open(image, 'rb'))  # 사진보내기
                    time.sleep(1)
                    update.bot.edit_message_text(text=bot.callback_query.data + " BTC/USDT의 HA 차트입니다",
                                                chat_id=bot.callback_query.message.chat_id,
                                                message_id=bot.callback_query.message.message_id)
                elif  name == "upbit" :  # 업비트 검색
                    # 업비트 1일봉 HA 계산, 차트 띄워
                    if data_selected.split(",")[-1] == "1일봉": interval = "day"
                    elif data_selected.split(",")[-1] == "1시간봉": interval = "minute60"
                    elif data_selected.split(",")[-1] == "5분봉": interval = "minute5"
                    plot_candle_chart(heiken_ashi_coin("upbit","KRW-BTC", interval, 60),"KRW-BTC")
                    telbot.send_photo(chat_id=bot.callback_query.message.chat_id, photo=open(image, 'rb'))  # 사진보내기
                    time.sleep(1)
                    update.bot.edit_message_text(text=bot.callback_query.data + " KRW-BTC의 HA 차트입니다",
                                                chat_id=bot.callback_query.message.chat_id,
                                                message_id=bot.callback_query.message.message_id)
                elif  name == "binance2" :   # 바이낸스 백테스트
                    if data_selected.split(",")[-1] == "1d": interval = '1d'
                    elif data_selected.split(",")[-1] == "4h": interval = '4h'
                    elif data_selected.split(",")[-1] == "1h": interval = '1h'
                    elif data_selected.split(",")[-1] == "30m": interval = '30m'
                    elif data_selected.split(",")[-1] == "15m": interval = '15m'
                    elif data_selected.split(",")[-1] == "5m": interval = '5m'
                    elif data_selected.split(",")[-1] == "1m": interval = '1m'

                    coin = "BTC/USDT"
                    count = [30,100,200,500,1000]
                    for cnt in count :
                        df_HA = heiken_ashi_coin("binance",coin, interval, cnt)
                        df_HA_as = add_signal(df_HA, coin)
                        text = backtest(df_HA_as, coin, "binance")
                        update.bot.sendMessage(text=data_selected.split(",")[0] + " "+ data_selected.split(",")[-1] +" "+ coin +"\n\n원금 1,000달러\n" + text,
                                                    chat_id=bot.callback_query.message.chat_id)
                elif  name == "upbit2" :   # 업비트 백테스트
                    # 업비트 1일봉 HA 계산, 차트 띄워
                    if data_selected.split(",")[-1] == "1d": interval = "day"
                    elif data_selected.split(",")[-1] == "4h": interval = "minute240"
                    elif data_selected.split(",")[-1] == "1h": interval = "minute60"
                    elif data_selected.split(",")[-1] == "30m": interval = "minute30"
                    elif data_selected.split(",")[-1] == "15m": interval = "minute15"
                    elif data_selected.split(",")[-1] == "5m": interval = "minute5"
                    elif data_selected.split(",")[-1] == "1m": interval = "minute1"

                    coin = "KRW-BTC"
                    count = [30,100,200,500,1000,2000,10000]
                    for cnt in count :
                        df_HA = heiken_ashi_coin("upbit",coin, interval, cnt)
                        df_HA_as = add_signal(df_HA, coin)
                        text = backtest(df_HA_as, coin, "upbit")
                        update.bot.sendMessage(text= data_selected.split(",")[0] + " "+ data_selected.split(",")[-1] +" "+ coin +"\n\n원금 1,000,000원\n" + text,
                                                    chat_id=bot.callback_query.message.chat_id)
                
                if korea == 1:
                    if codefind(name, "krx") != 0: #한국종목 목록에 있으면
                        korea = 0
                        # 한국종목 HA 계산, 차트 띄워
                        plot_candle_chart(heiken_ashi_jusik(name, "krx", 60),name)
                        telbot.send_photo(chat_id=bot.callback_query.message.chat_id, photo=open(image, 'rb'))  # 사진보내기
                        time.sleep(1)
                        update.bot.edit_message_text(text=bot.callback_query.data+" 의 HA 차트입니다.",
                                                    chat_id=bot.callback_query.message.chat_id,
                                                    message_id=bot.callback_query.message.message_id)
                elif usa ==1:
                    if namefind(name) != 0: # 미국종목 목록에 있으면
                        usa = 0
                        # 미국종목 HA 계산, 차트 띄워
                        plot_candle_chart(heiken_ashi_jusik(name, "us", 60),name)
                        telbot.send_photo(chat_id=bot.callback_query.message.chat_id, photo=open(image, 'rb'))  # 사진보내기
                        time.sleep(1)
                        update.bot.edit_message_text(text=bot.callback_query.data+" 의 HA 차트입니다.",
                                                    chat_id=bot.callback_query.message.chat_id,
                                                    message_id=bot.callback_query.message.message_id)
                elif korea == 2:
                    if codefind(name, "krx") != 0: #한국종목 목록에 있으면
                        korea = 0
                        count = int(data_selected.split(",")[-1])
                        df_HA = heiken_ashi_jusik(name, "krx", count)
                        df_HA_as = add_signal(df_HA, name)
                        text = backtest(df_HA_as, name, "korea")
                        update.bot.edit_message_text(text=data_selected.split(",")[0] +" 1일봉 기준\n\n원금 1,000,000원\n" + text,
                                                    chat_id=bot.callback_query.message.chat_id,
                                                    message_id=bot.callback_query.message.message_id)
                elif usa ==2:
                    if namefind(name) != 0: # 미국종목 목록에 있으면
                        usa = 0
                        count = int(data_selected.split(",")[-1])
                        df_HA = heiken_ashi_jusik(name, "us", count)
                        df_HA_as = add_signal(df_HA, name)
                        text=backtest(df_HA_as, name, "usa")
                        update.bot.edit_message_text(text=data_selected.split(",")[0] +" 1일봉 기준\n\n원금 1,000달러\n" + text,
                                                    chat_id=bot.callback_query.message.chat_id,
                                                    message_id=bot.callback_query.message.message_id)
    
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
    
    # 현재가 조회
    def fetch_ticker(coin, ohlcvabl):
        '''
        ohlcvabl : "open" "high" "close" "volume" "ask"(매도1호가) "bid"(매수1호가) "last"(최근거래가격)
        '''
        binance = bnc()
        ticker = binance.fetch_ticker(coin)
        return ticker[ohlcvabl]
    
    # 잔고조회
    def fetch_balance(coin):
        '''
        coin : "BTC", "USDT" 
        fut : "free" 사용가능 "used" 주문넣은것 "total" 총합
        '''
        binance = bnc()
        return binance.fetch_balance(params={"type": "future"})[coin]     #선물 잔고 조회
    def fetch_balances():
        '''
        coin : "BTC", "USDT" 
        fut : "free" 사용가능 "used" 주문넣은것 "total" 총합
        '''
        binance = bnc()
        return binance.fetch_balance(params={"type": "future"})     #선물 잔고 조회 

    # 취소 주문
    def trade_cancel(orderId, coin):
        binance = bnc()
        return binance.cancel_order(orderId, coin)

    # 지정가 매매
    def trade_limit(coin, order, amount, price):
        binance = bnc()
        if order == "buy":
            return binance.create_limit_buy_order(coin, amount, price)
        elif order == "sell":
            return binance.create_limit_sell_order(coin, amount, price)

    # 시장가 매매
    def trade_market(coin, order, amount):
        binance = bnc()
        if order == "buy":
            return binance.create_market_buy_order(coin, amount)
        elif order == "sell":
            return binance.create_market_sell_order(coin, amount)
        
    # 레버리지 설정
    def set_leverage(coin, leverage):
        binance = bnc()
        markets = binance.load_markets()
        market = binance.market(coin)
        resp = binance.fapiPrivate_post_leverage({
        'symbol': market['id'],
        'leverage': leverage
        })
    def fetch_position(coin, balance):
        '''
        coin : "BTCUSDT"
        balance = binance.fetch_balance()
        '''
        positions = balance['info']['positions']
        for position in positions:
            if position["symbol"] == coin:
                return position

    # 대기주문 조회
    def fetch_open_order(coin):
        '''
        return {'id', 'amount'} or []
        '''
        open_orders = bnc().fetch_open_orders(symbol=coin)
        if open_orders == []:
            return open_orders
        else:
            return open_orders[0]

    def heiken_ashi_coin(country, coin='BTC/USDT', interval='1d', count=60):
        print(country + " " + coin +" heiken_ashi_coin")
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
        df_HA["ma"] = df["close"].rolling(window=20).mean()
        # 8일 지수이동평균
        df_HA["ema"] = df["close"].ewm(span=8, adjust=False).mean()

        df_HA = df_HA.fillna(0) # NA 값을 0으로
        return df_HA       

    def heiken_ashi_jusik(token, region, count):
        print(token+" heiken_ashi_jusik")
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

    def buy_signal(token, interval, df_HA, bot=None, channel=None, channel_id=None):
        print(token+" buy_signal")
        # ha음봉(ha_open > ha_close) -> ha양봉(ha_open < ha_close)  # 양전
        if df_HA["open"].iloc[-2] > df_HA["close"].iloc[-2] and df_HA["open"].iloc[-1] < df_HA["close"].iloc[-1] :
            # 8ema < 20ma   # 하락추세중 추세반전
            if df_HA["ema"].iloc[-1] < df_HA["ma"].iloc[-1]:
                # 8ema < ha_close  :  100% 매수
                if df_HA["ema"].iloc[-1] < df_HA["close"].iloc[-1]:
                    plot_candle_chart(df_HA, token)
                    if msgOn == 1:
                        post_message(bot, channel, token + " " + interval + " 양봉전환 : 100% 매수")
                        post_image(bot, channel, image)
                        telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 양봉전환 : 100% 매수") # 메세지 보내기
                        time.sleep(1)
                        telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
                    return 100
                # 8ema > ha_close  :  50% 매수
                if df_HA["ema"].iloc[-1] > df_HA["close"].iloc[-1]:
                    plot_candle_chart(df_HA, token)
                    if msgOn == 1:
                        post_message(bot, channel, token + " " + interval + " 양봉전환 : 50% 매수")
                        post_image(bot, channel, image)
                        telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 양봉전환 : 50% 매수") # 메세지 보내기
                        time.sleep(1)
                        telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
                    return 50
            # 8ema > 20ma   # 상승추세중 불타기 추세반전
            if df_HA["ema"].iloc[-1] > df_HA["ma"].iloc[-1]:
                plot_candle_chart(df_HA, token)
                if msgOn == 1:
                    post_message(bot, channel, token + " " + interval + " 양봉전환 : 10% 매수")
                    post_image(bot, channel, image)
                    telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 양봉전환 : 10% 매수") # 메세지 보내기
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
                return 10
        time.sleep(1)
        return 0

    def sell_signal(token, interval, df_HA, bot=None, channel=None, channel_id=None):
        print(token+" sell_signal")
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
                    if msgOn == 1:
                        post_message(bot, channel, token + " " + interval + " 음봉전환 : 50% 매도")
                        post_image(bot, channel, image)
                        telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 음봉전환 : 50% 매도") # 메세지 보내기
                        time.sleep(1)
                        telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
                    return 50
                # 큰 낙폭    
                if df_HA["close"].iloc[-1] < df_HA["ema"].iloc[-1] :
                    plot_candle_chart(df_HA, token)
                    if msgOn == 1:
                        post_message(bot, channel, token + " " + interval + " 음봉전환 : 80% 매도")
                        post_image(bot, channel, image)
                        telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 음봉전환 : 80% 매도") # 메세지 보내기
                        time.sleep(1)
                        telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
                    return 80
                # 떡락
                if df_HA["close"].iloc[-1] < df_HA["ma"].iloc[-1] :
                    plot_candle_chart(df_HA, token)
                    if msgOn == 1:
                        post_message(bot, channel, token + " " + interval + " 음봉전환 : 100% 매도")
                        post_image(bot, channel, image)
                        telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 음봉전환 : 100% 매도") # 메세지 보내기
                        time.sleep(1)
                        telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
                    return 100
            # 하락추세
            if df_HA["ema"].iloc[-1] < df_HA["ma"].iloc[-1] :
                plot_candle_chart(df_HA, token)
                if msgOn == 1:
                    post_message(bot, channel, token + " " + interval + " 음봉전환 : 100% 매도")
                    post_image(bot, channel, image)
                    telbot.sendMessage(chat_id=channel_id, text=token + " " + interval + " 음봉전환 : 100% 매도") # 메세지 보내기
                    time.sleep(1)
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))  # 사진보내기
                return 100
        time.sleep(1)
        return 0
        # (1봉전) 8ema > 20ma and (현재) 8ema < 20ma  : 전량매도

    # 백테스트용 매수 매도 시그널 첨가
    def add_signal(df_HA, name):
        print(name+" add_signal")
        df_HA["signal"] = 0

        for i in range(len(df_HA)):
            if i>0: # 맨첫줄은 넘어감
                # ha음봉(ha_open > ha_close) -> ha양봉(ha_open < ha_close)  # 양봉전환 : 매수
                if df_HA["open"].iloc[i-1] > df_HA["close"].iloc[i-1] and df_HA["open"].iloc[i] < df_HA["close"].iloc[i] :
                    df_HA["signal"].iloc[i] = 1
                # ha양봉(ha_open < ha_close) -> ha음봉(ha_open > ha_close)  # 음봉전환 : 매도
                elif df_HA["open"].iloc[i-1] < df_HA["close"].iloc[i-1] and df_HA["open"].iloc[i] > df_HA["close"].iloc[i]:
                    df_HA["signal"].iloc[i] = 2
                else:
                    df_HA["signal"].iloc[i] = 0
        return df_HA
    
    # 백테스트
    def backtest(df_HA_as, name, country):
        if country == "korea" or country == "upbit":
            money = 1000000 # 백만원
        elif country == "usa" or country == "binance":
            money = 1000 #달러
        num = 0 # 매수, 매도 가능한 주식 수
        buyMoney = 0 # 매수한 금액
        sellMoney = 0 # 매도한 금액
        recent_close = 0 # 최근 거래한 종가

        chk1st = 1  
        for i in range(len(df_HA_as)):
            signal = df_HA_as["signal"].iloc[i]

            if signal == 1:                        # 매수 시그널
                if country == "korea" or country == "usa":
                    num = int(money/df_HA_as["Close"].iloc[i])      # 매수가능한 주식수
                elif country == "binance" or country == "upbit":
                    num = (money/df_HA_as["Close"].iloc[i])      # 매수가능한 코인수

                buyMoney = num*df_HA_as["Close"].iloc[i]   # 매수한 금액
                money -= (buyMoney + buyMoney*0.0004)                  # 잔액
                recent_close = df_HA_as["Close"].iloc[i]
                # print("종가 " +str(df_HA_as["Close"].iloc[i])+" 매수량 : "+str(num)+ " 매수금액 : "+str(buyMoney) + " 예수금 : "+str(money) + " 총합 : " +str(money + num*recent_close))
                chk1st = 0
            elif signal == 2:                      # 매도 시그널
                if chk1st != 1:                    # 맨처음온게 매도 시그널이면 무시
                    sellMoney = num*df_HA_as["Close"].iloc[i]  # 매도한 금액
                    money += sellMoney                 # 잔액
                    recent_close = df_HA_as["Close"].iloc[i]
                    # print("종가 " +str(df_HA_as["Close"].iloc[i])+ " 매도량 : "+str(num)+ " 매도금액 : "+str(sellMoney) + " 예수금 : "+str(money) + " 총합 : "+str(money) )
                    num = 0; buyMoney = 0              # 매수 초기화

        if  country == "korea" or country == "upbit":
            ratio = (money+(num*recent_close)) / 1000000 # 수익률
        elif country == "usa" or country == "binance":
            ratio = (money+(num*recent_close)) / 1000 # 수익률
        
        if ratio > 0 :
            ratio = (ratio - 1) * 100
        elif ratio < 0:
            ratio = (1 - ratio) * 100

        text = (str(df_HA_as.index[0]) + " 부터\n" + str(df_HA_as.index[-1]) + " 까지\n총 "+ str(len(df_HA_as))+"봉을 조회했습니다"
                + "\n매수 횟수 : " + str(df_HA_as['signal'].value_counts().loc[1]) + " 매도 횟수 : " + str(df_HA_as['signal'].value_counts().loc[2]) 
                + "\n최종 수익률 : " + str(round(ratio,2))+"%" + "\n최종 예수금 : " +str(round(money,4))
                + "\n평가액 : " +str(round(num*recent_close,4)) + "\n총합 : " +str(round(money + num*recent_close,4)))
        print(text)
        return text
    
    
    def auto_trading():
        coin = 'BTC/USDT'
        print(coin+" auto_trading")

        interval1h = '1h'
        limit1h = 30
        interval5m = '5m'
        limit5m = limit1h * 12

        df_HA_m = heiken_ashi_coin("binance",coin, interval5m, limit5m)
        df_HA_h = heiken_ashi_coin("binance",coin, interval1h, limit1h)

        price = float(df_HA_m["Close"].iloc[-1])  # 현재가격

        open_order = fetch_open_order(coin)
        if  open_order != [] :  # 대기주문이 있다면 대기주문 취소
            trade_cancel(open_order['id'], coin)

###################### 롱 전략 ################################
        # ha음봉(ha_open > ha_close) -> ha양봉(ha_open < ha_close)  # 5분봉 양봉전환 : 매수
        if df_HA_m["open"].iloc[-2] > df_HA_m["close"].iloc[-2] and df_HA_m["open"].iloc[-1] < df_HA_m["close"].iloc[-1] :
            if df_HA_h["open"].iloc[-1] < df_HA_h["close"].iloc[-1] :   # 시간봉이 양봉일때
                btcBalance = float(fetch_position("BTCUSDT",fetch_balances())["positionAmt"])
                if btcBalance < 0 : # 숏포지션 들고 있다면
                    amount = round(fetch_balance("USDT")["free"]/price,3)*5   # 0.001 단위로 구매 가능.. 
                    order = trade_limit(coin, "buy", amount-btcBalance, price-5)    # 숏 청산, 롱 매수진행
                    print("숏 청산, 롱 진입가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "숏 청산, 롱 진입가격 : " +str(df_HA_m["Close"].iloc[-1]) + " id : "+ order["info"]["orderId"])
                elif btcBalance == 0 : # 표지션이 없다면 
                    amount = round(fetch_balance("USDT")["free"]/price,3)*5   # 0.001 단위로 구매 가능.. 
                    order = trade_limit(coin, "buy", amount, price-5)    # 롱 매수진행
                    print("롱 진입가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "롱 진입가격 : " +str(df_HA_m["Close"].iloc[-1]) + " id : " + order["info"]["orderId"])
            
            else: # 양봉전환 + 시간봉 음봉일때  :  숏 포지션 있으면 청산
                btcBalance = float(fetch_position("BTCUSDT",fetch_balances())["positionAmt"])  # 현재 보유중인 BTC : 음수면 숏, 양수면 롱
                if btcBalance < 0 : # 숏 포지션 들고 있는게 있다면 전부 매수
                    order = trade_limit(coin, "buy", -btcBalance, price-10)
                    print("숏 100% 매수가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "숏 100% 매수가격 : " +str(df_HA_m["Close"].iloc[-1]) +" id : " + order["info"]["orderId"])
            
        

        # if ha 양봉, 캔들 양봉 and ha전봉 양봉 : 연속 상승추세
        elif df_HA_m["open"].iloc[-1] < df_HA_m["close"].iloc[-1] and df_HA_m["Open"].iloc[-1] < df_HA_m["Close"].iloc[-1] and df_HA_m["open"].iloc[-2] < df_HA_m["close"].iloc[-2]:
            btcBalance = float(fetch_position("BTCUSDT",fetch_balances())["positionAmt"])
            if btcBalance > 0 : # 비트코인 들고 있는게 있다면 
                if round(btcBalance/10,3) >= 0.001:  # 10% 가 0.001 보다 크다면 10% 매도
                    order = trade_limit(coin, "sell", round(btcBalance/10,3), price+10)
                    print("롱 10% 매도가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "롱 10%매도가격 : " +str(df_HA_m["Close"].iloc[-1]) +" id : " + order["info"]["orderId"])
                elif round(btcBalance/5,3) >= 0.001:  # 20% 가 0.001 보다 크다면 20% 매도
                    order = trade_limit(coin, "sell", round(btcBalance/5,3), price+10)
                    print("롱 20% 매도가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "롱 20%매도가격 : " +str(df_HA_m["Close"].iloc[-1]) +" id : " + order["info"]["orderId"])
                elif round(btcBalance/2,3) >= 0.001:  # 50% 가 0.001 보다 크다면 50% 매도
                    order = trade_limit(coin, "sell", round(btcBalance/2,3), price+10)
                    print("롱 50% 매도가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "롱 50%매도가격 : " +str(df_HA_m["Close"].iloc[-1]) +" id : " + order["info"]["orderId"])
                else:                         # 50% 가 0.001보다 작으면 전량 매도
                    order =  trade_limit(coin, "sell", btcBalance, price+10)
                    print("롱 100% 매도가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "롱 100%매도가격 : " +str(df_HA_m["Close"].iloc[-1])+" id : " + order["info"]["orderId"])

###################### 숏 전략 ################################
        # ha양봉(ha_open < ha_close) -> ha음봉(ha_open > ha_close)  # 5분봉 음봉전환 : 매도
        if df_HA_m["open"].iloc[-2] < df_HA_m["close"].iloc[-2] and df_HA_m["open"].iloc[-1] > df_HA_m["close"].iloc[-1] :
            if df_HA_h["open"].iloc[-1] > df_HA_h["close"].iloc[-1] :   # 시간봉이 음봉일때
                btcBalance = float(fetch_position("BTCUSDT",fetch_balances())["positionAmt"])  # 현재 보유중인 BTC : 음수면 숏, 양수면 롱
                if btcBalance > 0: # 롱 포지션을 들고 있다면
                    amount = round(fetch_balance("USDT")["free"]/price,3)*5   # 0.001 단위로 구매 가능..
                    order = trade_limit(coin, "sell", amount+btcBalance, price+5)  # 롱포지션 청산과 동시에 숏포지션
                    # orderId = order["info"]["orderId"]
                    print("롱청산, 숏 진입가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "롱청산, 숏 진입가격 : " +str(df_HA_m["Close"].iloc[-1]) + " id : " + order["info"]["orderId"])
                else :   # 포지션이 없다면
                    amount = round(fetch_balance("USDT")["free"]/price,3)*5   # 0.001 단위로 구매 가능..
                    order = trade_limit(coin, "sell", amount, price+5)  # 숏포지션
                    # orderId = order["info"]["orderId"]
                    print("숏 진입가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "숏 진입가격 : " +str(df_HA_m["Close"].iloc[-1]) + " id : " + order["info"]["orderId"])
            
            else :  # 음봉전환 + 시간봉 양봉 : 롱 청산
                btcBalance = float(fetch_position("BTCUSDT",fetch_balances())["positionAmt"])
                if btcBalance > 0 : # 롱 들고 있는게 있다면 전부 매도
                    order = trade_limit(coin, "sell", btcBalance, price+10)
                    print("롱 100% 매도가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "롱 100% 매도가격 : " +str(df_HA_m["Close"].iloc[-1]) +" id : " + order["info"]["orderId"])

        # if ha 음봉, 캔들 음봉 and ha전봉 음봉 : 연속 하락추세
        elif df_HA_m["open"].iloc[-1] > df_HA_m["close"].iloc[-1] and df_HA_m["Open"].iloc[-1] > df_HA_m["Close"].iloc[-1] and df_HA_m["open"].iloc[-2] > df_HA_m["close"].iloc[-2]:
            btcBalance = float(fetch_position("BTCUSDT",fetch_balances())["positionAmt"])
            if btcBalance < 0 : # 숏 포지션 들고 있는게 있다면 음수
                if round(-btcBalance/10,3) >= 0.001:  # 10% 가 0.001 보다 크다면 10% 매수
                    order = trade_limit(coin, "buy", round(-btcBalance/10,3), price-10)
                    print("숏 10% 매수가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "숏 10% 매수가격 : " +str(df_HA_m["Close"].iloc[-1]) + " id : " + order["info"]["orderId"])
                elif round(-btcBalance/5,3)  >= 0.001:  # 20% 가 0.001 보다 크다면 20% 매수
                    order = trade_limit(coin, "buy", round(-btcBalance/5,3), price-10) 
                    print("숏 20% 매수가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "숏 20% 매수가격 : " +str(df_HA_m["Close"].iloc[-1]) +" id : "+ order["info"]["orderId"])
                elif round(-btcBalance/2,3) >= 0.001:  # 50% 가 0.001 보다 크다면 50% 매수
                    order = trade_limit(coin, "buy", round(-btcBalance/2,3), price-10)
                    print("숏 50% 매수가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "숏 50% 매수가격 : " +str(df_HA_m["Close"].iloc[-1]) +" id : " + order["info"]["orderId"])
                else:                         # 50% 가 0.001보다 작으면 전량 매도
                    order =  trade_limit(coin, "buy", -btcBalance, price-10)
                    print("숏 100% 매수가격 : " +str(df_HA_m["Close"].iloc[-1]))
                    telbot.sendMessage(chat_id=channel_id_binance, text = "숏 100% 매수가격 : " +str(df_HA_m["Close"].iloc[-1])+" id : " + order["info"]["orderId"])



    schedule.every().hour.at("04:55").do(lambda:auto_trading())
    schedule.every().hour.at("09:55").do(lambda:auto_trading())
    schedule.every().hour.at("14:55").do(lambda:auto_trading())
    schedule.every().hour.at("19:55").do(lambda:auto_trading())
    schedule.every().hour.at("24:55").do(lambda:auto_trading())
    schedule.every().hour.at("29:55").do(lambda:auto_trading())
    schedule.every().hour.at("34:55").do(lambda:auto_trading())
    schedule.every().hour.at("39:55").do(lambda:auto_trading())
    schedule.every().hour.at("44:55").do(lambda:auto_trading())
    schedule.every().hour.at("49:55").do(lambda:auto_trading())
    schedule.every().hour.at("54:55").do(lambda:auto_trading())
    schedule.every().hour.at("59:55").do(lambda:auto_trading())
    
    # 코드 찾기 어려울 경우를 위해 code찾기 만들기
    def codefind(name, country):
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
    
    ####################### jusik ##########################

    count = 60
    def krx_ha_check():
        print("krx_ha_check")
        if msgOn==1:
            post_message(tokenKorea,channelKorea, "@@@@@@@@@@ KOREA @@@@@@@@@ ")
        for token in jongmok: # krx
            df_HA = heiken_ashi_jusik(token, "krx", count)
            buy_signal(token, "day", df_HA, bot=tokenKorea, channel=channelKorea, channel_id=channel_id_korea)
            sell_signal(token, "day", df_HA, bot=tokenKorea, channel=channelKorea, channel_id=channel_id_korea)
    # 매일 정해진 시간에
    schedule.every().day.at("08:50").do(lambda:krx_ha_check())
    schedule.every().day.at("15:00").do(lambda:krx_ha_check())

    def us_ha_check():
        print("us_ha_check")
        if msgOn == 1 :
            post_message(tokenUsa,channelUsa,"@@@@@@@@@@ USA @@@@@@@@@ ")
        for token in jongmok2: #us
            df_HA = heiken_ashi_jusik(token, "us", count)
            buy_signal(token, "day", df_HA, bot=tokenUsa, channel=channelUsa, channel_id=channel_id_usa)
            sell_signal(token, "day", df_HA, bot=tokenUsa, channel=channelUsa, channel_id=channel_id_usa)
    # 매일 정해진 시간에
    schedule.every().day.at("17:50").do(lambda:us_ha_check()) 
    schedule.every().day.at("22:20").do(lambda:us_ha_check())
    schedule.every().day.at("05:30").do(lambda:us_ha_check())


    ########### upbit ####################
    coin = "KRW-BTC"

        # 5분봉
    def coin_ha_check_5min():
        print("coin_ha_check_5min")
        interval_5 = "minute5"
        df_HA_5 = heiken_ashi_coin("upbit",coin, interval_5, count)
        plot_candle_chart(df_HA_5, "test")
        buy_signal(coin, interval_5, df_HA_5, bot=tokenCoin, channel=channelUpbit, channel_id=channel_id)
        sell_signal(coin, interval_5, df_HA_5, bot=tokenCoin, channel=channelUpbit, channel_id=channel_id)
    # 5분에 한번씩 실행
    schedule.every().hour.at("04:30").do(lambda:coin_ha_check_5min())
    schedule.every().hour.at("09:30").do(lambda:coin_ha_check_5min())
    schedule.every().hour.at("14:30").do(lambda:coin_ha_check_5min())
    schedule.every().hour.at("19:30").do(lambda:coin_ha_check_5min())
    schedule.every().hour.at("24:30").do(lambda:coin_ha_check_5min())
    schedule.every().hour.at("29:30").do(lambda:coin_ha_check_5min())
    schedule.every().hour.at("34:30").do(lambda:coin_ha_check_5min())
    schedule.every().hour.at("39:30").do(lambda:coin_ha_check_5min())
    schedule.every().hour.at("44:30").do(lambda:coin_ha_check_5min())
    schedule.every().hour.at("49:30").do(lambda:coin_ha_check_5min())
    schedule.every().hour.at("54:30").do(lambda:coin_ha_check_5min())
    schedule.every().hour.at("59:30").do(lambda:coin_ha_check_5min())

        # 60분봉
    def coin_ha_check_60min():
        print("coin_ha_check_60min")
        interval_60 = "minute60"
        df_HA_h = heiken_ashi_coin("upbit",coin, interval_60, count)
        buy_signal(coin, interval_60, df_HA_h, bot=tokenCoin, channel=channelUpbit, channel_id=channel_id)
        sell_signal(coin, interval_60, df_HA_h, bot=tokenCoin, channel=channelUpbit, channel_id=channel_id)
    # 60분에 한번씩 실행
    schedule.every().hour.at("59:00").do(lambda:coin_ha_check_60min())
        # 1일봉
    def coin_ha_check_day():
        interval_day = "day"
        df_HA_d = heiken_ashi_coin("upbit",coin, interval_day, count)
        buy_signal(coin, interval_day, df_HA_d, bot=tokenCoin, channel=channelUpbit, channel_id=channel_id)
        sell_signal(coin, interval_day, df_HA_d, bot=tokenCoin, channel=channelUpbit, channel_id=channel_id)
    schedule.every().day.at("08:50").do(lambda:coin_ha_check_day())
    schedule.every().day.at("23:50").do(lambda:coin_ha_check_day())

    ############## binance ####################

    btc = 'BTC/USDT'

    def binance_ha_check_5min():
        print("binance_ha_check_5min")
        interval_5 = "5m"
        df_HA_5 = heiken_ashi_coin("binance", btc, interval_5, count)
        buy_signal(btc, interval_5, df_HA_5, bot=tokenCoin, channel=channelBNC, channel_id=channel_id_binance)
        sell_signal(btc, interval_5, df_HA_5, bot=tokenCoin, channel=channelBNC, channel_id=channel_id_binance)
    # 5분에 한번씩 실행
    schedule.every().hour.at("04:30").do(lambda:binance_ha_check_5min())
    schedule.every().hour.at("09:30").do(lambda:binance_ha_check_5min())
    schedule.every().hour.at("14:30").do(lambda:binance_ha_check_5min())
    schedule.every().hour.at("19:30").do(lambda:binance_ha_check_5min())
    schedule.every().hour.at("24:30").do(lambda:binance_ha_check_5min())
    schedule.every().hour.at("29:30").do(lambda:binance_ha_check_5min())
    schedule.every().hour.at("34:30").do(lambda:binance_ha_check_5min())
    schedule.every().hour.at("39:30").do(lambda:binance_ha_check_5min())
    schedule.every().hour.at("44:30").do(lambda:binance_ha_check_5min())
    schedule.every().hour.at("49:30").do(lambda:binance_ha_check_5min())
    schedule.every().hour.at("54:30").do(lambda:binance_ha_check_5min())
    schedule.every().hour.at("59:30").do(lambda:binance_ha_check_5min())

        # 60분봉
    def binance_ha_check_60min():
        print("binance_ha_check_60min")
        interval_60 = "1h"
        df_HA_h = heiken_ashi_coin("binance",btc, interval_60, count)
        buy_signal(btc, interval_60, df_HA_h, bot=tokenCoin, channel=channelBNC, channel_id=channel_id_binance)
        sell_signal(btc, interval_60, df_HA_h, bot=tokenCoin, channel=channelBNC, channel_id=channel_id_binance)
    # 60분에 한번씩 실행
    schedule.every().hour.at("57:00").do(lambda:binance_ha_check_60min())
        # 1일봉
    def binance_ha_check_day():
        print("binance_ha_check_day")
        interval_day = "1d"
        df_HA_d = heiken_ashi_coin("binance",btc, interval_day, count)
        buy_signal(btc, interval_day, df_HA_d, bot=tokenCoin, channel=channelBNC, channel_id=channel_id_binance)
        sell_signal(btc, interval_day, df_HA_d, bot=tokenCoin, channel=channelBNC, channel_id=channel_id_binance)
    schedule.every().day.at("08:50").do(lambda:binance_ha_check_day())
    schedule.every().day.at("23:50").do(lambda:binance_ha_check_day())

    if msgOn == 1 :
        post_message(tokenCoin,channelUpdate,"업데이트완료...")
        telbot.sendMessage(chat_id=channel_id_feedback, text=("업데이트완료...")) # 메세지 보내기
    # 작동 테스트
    if runtest==1:
        print("runtest")
        coin_ha_check_5min()
        binance_ha_check_5min()
        coin_ha_check_60min()
        coin_ha_check_day()
        binance_ha_check_day()
    if run_ko == 1:
        krx_ha_check()
    if run_us == 1:
        us_ha_check()

    def alarmi():
        print("쓰레딩이이잉")
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:       # Ctrl+C 입력시 예외 발생새
                print("개발중... 잠시 종료됩니다!")
                post_message(tokenCoin,channelUpdate,KeyboardInterrupt)
                post_message(tokenCoin,channelUpdate,"개발중... 잠시 종료됩니다!")
                telbot.sendMessage(chat_id=channel_id_feedback, text=("개발중... 잠시 종료됩니다!")) # 메세지 보내기
                sys.exit() #종료    
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
    post_message(tokenCoin,channelUpdate,e)
    post_message(tokenCoin,channelUpdate," 에러발생! 강제종료됨! ")
    telbot.sendMessage(chat_id=channel_id_feedback, text=("에러발생! 강제종료됨!")) # 메세지 보내기
    time.sleep(1)