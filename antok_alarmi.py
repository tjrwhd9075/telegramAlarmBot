from os import linesep
import time
from numpy import pi
import requests
from bs4 import BeautifulSoup as bs

import telegram

bot_token ='1811197670:AAFaSU2l8pKxT6tDA3tOl2Tpue-OiNC1Af0'
bot = telegram.Bot(token = bot_token)
chat_id =  '-1001587542844'


antokKo = "https://antok.co.kr/kstock/"
antokMi = "https://antok.co.kr/ustock/"
antokCo = "https://antok.co.kr/coin/"
antokFi = "https://antok.co.kr/finance/"
antokUm = "https://antok.co.kr/free/"


fileAntok = 'antok_news.txt'

# def send_new(bot, chat_id):
def send_new():

    # 기존 데이터 불러오기
    with open(fileAntok, 'r', encoding = 'UTF-8') as f:
        oldLinks = f.read().splitlines() 

    antoks= [antokKo, antokCo, antokFi, antokMi, antokUm]
    for antok in antoks:
        response = requests.get(antok)
        html = response.text 
        soup = bs(html, 'html.parser')

        news_list = soup.select('#board-list > div:nth-child(2) > table > tbody > tr')
        lines = []
        for news in news_list:
            link = antok + news.select_one('#board-list > div:nth-child(2) > table > tbody > tr > td.title > a')['href'].split('/')[2]
            # print(link)
            title = news.select_one('#board-list > div:nth-child(2) > table > tbody > tr > td.title > a > span.title-link').get_text()
            # print(title)
            try:
                name = news.select_one('#board-list > div:nth-child(2) > table > tbody > tr > td.author > div > img')['title']
            except:
                name = news.select_one('#board-list > div:nth-child(2) > table > tbody > tr > td.author > div > a').get_text()
            # print(name + "\n")
            line =link + "@" + title + "@" + name
            # print(line)
            lines.append(line)
            # print(line.split('@'))

        
        justLinks = []
        for oldLink in oldLinks:
            justLinks.append(oldLink.split('@')[0])
            
        # 새로운 링크 한줄씩 저장
        newlines = []
        for line in lines:
            if line.split('@')[0] not in justLinks:
                newlines.append(line)
                with open(fileAntok, 'a', encoding = 'UTF-8') as f:          
                    f.write(line + "\n")
        

        if newlines:
            for line in newlines:
                gesipan = ""
                if line.split('@')[0].find("free"):gesipan="유머 & 잡담"
                elif line.split('@')[0].find("kstock"):gesipan="한국 증시"
                elif line.split('@')[0].find("ustock"):gesipan="미국 증시"
                elif line.split('@')[0].find("coin"):gesipan="암호 화폐"
                elif line.split('@')[0].find("finance"):gesipan="재태크 & 부동산"

                txt = "[앤톡 새글 알림]\n"+\
                    "\n게시판 : "+ gesipan +\
                    "\n제목 : " + line.split('@')[1] + \
                    "\n글쓴이 : " + line.split('@')[2] + \
                    "\n링크 : " + line.split('@')[0]
                print(line.split('@'))
                bot.sendMessage(chat_id=chat_id, text=txt)
                time.sleep(3)
        else:
            pass

    # 저장된 행이 300줄 이상이면, 절반 삭제
    if len(oldLinks) >= 300:
        with open(fileAntok, 'a', encoding = 'UTF-8') as f:
            for i, line in enumerate(oldLinks):
                if i > 150 :
                    f.write(line + "\n")


    return newlines

import schedule
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

try:
    try :
        send_new()
        sched.add_job(send_new, 'interval', minutes=2)
        sched.start()
    except Exception as e:
        print(e)
        bot.sendMessage(chat_id=chat_id, text=e)
except KeyboardInterrupt:
    print("ctrl + C")
    bot.sendMessage(chat_id=chat_id, text="ctrl + C")