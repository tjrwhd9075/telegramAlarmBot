
#정적 수집을 위한 패키지
import time
import requests
from bs4 import BeautifulSoup as bs

#사용자에게 메시지 전송을 위한 패키지
import telegram

#주기적으로 프로그램을 작동시키기 위한 패키지
from apscheduler.schedulers.blocking import BlockingScheduler

#step2.텔레그램 봇 불러오기

#토큰을 변수에 저장
bot_token ='1811197670:AAFaSU2l8pKxT6tDA3tOl2Tpue-OiNC1Af0'

#telegram 패키지의 Bot 함수를 사용하여 내가 만든 bot 사용
bot = telegram.Bot(token = bot_token)

#bot과의 채팅 정보 및 메세지 업데이트 
#예전(불과 어제)의 정보를 못 불러오는 것으로 파악됨. 프로그램 시작 전에 bot에게 아무 메시지나 보내주어야함

#아래 for문 까지는 bot.getUpdates()의 자료구조를 파악하기 위한 확인용 코드
updates = bot.getUpdates()
for i in updates :
    print(i) #update_id와 message로 크게 두 가지 정보가 딕셔너리 형태로 존재

#가장 최근에 온 메세지의 정보 중, chat id만 가져옴 (이 chat id는 사용자(나)의 계정 id임)
# chat_id = bot.getUpdates()[-1].message.chat.id
chat_id = '-579845295'

#위에서 얻은 chat id로 bot이 메세지를 보냄.
bot.sendMessage(chat_id = chat_id, text="뉴스 기사 크롤링이 시작 되었습니다") 

#step3.주기적으로 명령을 실행할 스케쥴러 생성
sched = BlockingScheduler()

antokKO = "https://antok.co.kr/kstock"

#step6.네이버 뉴스 기사 링크 크롤링 함수 만들기 (매개변수는 이전에 수집해둔 링크가 담긴 리스트)
def get_links(old_links=[]):
    new_links=[]
    
    url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={query}'
    response = requests.get(url)
    html = response.text 
    soup = bs(html, 'html.parser')

    news_list = soup.select('a.news_tit')

    links = []

    for news in news_list:
        link = news['href']
        links.append(link)

    for link in links:
        if link not in old_links:
            new_links.append(link)
            with open('C:/Users/seokjong_2/Desktop/Programming/cryptoauto/news.txt', 'a', encoding = 'UTF-8') as f:          # 새로운 링크 한줄씩 저장
                f.write(link + "\n")
    return new_links

#step7.텔레그램 기사 링크 전송 함수 만들기
def send_links():
    #step5.기존에 보냈던 링크를 담아둘 리스트 만들기
    with open('C:/Users/seokjong_2/Desktop/Programming/cryptoauto/news.txt', 'r', encoding = 'UTF-8') as f:
        old_links = f.read().splitlines() 

    new_links = get_links(old_links)

    if new_links:
        for link in new_links:
            bot.sendMessage(chat_id=chat_id, text=link)
            time.sleep(3)
    else:
        pass
        #else일 때 아무것도 안보내고 싶으면 그냥 pass로 바꾸면 됨. 실제 사용 때는 pass로 할 것


#step8.최초 시작, 스케쥴러 세팅 및 작동
send_links()

# hours는 시, minutes는 분, seconds는 초
sched.add_job(send_links, 'interval', minutes=5)

sched.start()

# ## 파일 읽고 쓰기
# with open('Bybit/Data/Equity.txt', 'r', encoding = 'UTF-8') as f:
#     Equity_Check = f.read()
# with open('Bybit/Data/Equity.txt', 'w', encoding = 'UTF-8') as f:
#     Equity = f.write(str())