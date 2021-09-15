#정적 수집을 위한 패키지
import time
import requests
from bs4 import BeautifulSoup as bs

fileNews = 'news.txt'
fileQuery = 'query.txt'

def get_querys():
    with open(fileQuery, 'r', encoding = 'UTF-8') as f:
        querys = f.read().splitlines() 
    return querys

def find_query_line(name):
    i = 0
    querys = get_querys()

    for query in querys:
        i = i+1
        if query == name :
            return i
        
    return -1

def del_query(name):
    if find_query_line(name) < 0:
        print(name + " : 목록에 없습니다.")
        return 0

    else :
        print(name + " : 목록에 있습니다. 삭제합니다.")
        with open(fileQuery,'rt', encoding = 'UTF-8') as f: 
            querys=f.read().splitlines() 

        with open(fileQuery,'w', encoding = 'UTF-8') as f: 
            for query in querys: 
                if query != name: # 같으면 건너뜀
                    f.write(query + '\n')
        return 1

def add_query(name):
    '''
    return -> 0 (fail) / 1 (true)
    '''
    querys = get_querys()
    for query in querys:
        if query == name :
            print(name + " : 목록에 있습니다.")
            return 0 # 저장안하고 종료

    with open(fileQuery, 'a', encoding = 'UTF-8') as f:          
        f.write(name + "\n")
        print(name +" : 목록에 없습니다. 추가합니다.")
        return 1 # 저장함



#step6.네이버 뉴스 기사 링크 크롤링 함수 만들기 (매개변수는 이전에 수집해둔 링크가 담긴 리스트)
def get_links(oldLinks=[], querys=[]):
    '''
    querys : 관심종목 리스트
    '''    
    print("뉴스 기사 크롤링이 시작 되었습니다") 
    newLinks=[]
    for query in querys:
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={query}'
        response = requests.get(url)
        html = response.text 
        soup = bs(html, 'html.parser')

        newsList = soup.select('a.news_tit')

        links = []

        for news in newsList:
            link = news['href']
            links.append(link)

        for link in links:
            if link not in oldLinks:
                newLinks.append(link)
                with open(fileNews, 'a', encoding = 'UTF-8') as f:          # 새로운 링크 한줄씩 저장
                    f.write(link + "\n")
    return newLinks

#step7.텔레그램 기사 링크 전송 함수 만들기
def send_new_links(bot, chat_id):
    '''
    querys : 관심종목 리스트
    '''
    with open(fileNews, 'r', encoding = 'UTF-8') as f:
        oldLinks = f.read().splitlines() 
    
    newLinks = get_links(oldLinks, get_querys())

    if newLinks:
        for link in newLinks:
            bot.sendMessage(chat_id=chat_id, text=link)
            time.sleep(3)
    else:
        pass

    # 검색어 갯수 * 500 개보다 저장된 뉴스 갯수가 더 많으면 반퉁 지움
    lenQ = len(get_querys())
    if (lenQ * 500) < len(oldLinks):
        with open(fileNews,'rt', encoding = 'UTF-8') as f: 
            oldLinks=f.read().splitlines() 
        with open(fileNews, 'w', encoding = 'UTF-8') as f:
            for i, line in enumerate(oldLinks):
                if i > (lenQ*250) :
                    f.write(line + "\n")

    return newLinks


def get_send_link(query, bot, chat_id):
    '''
    query : 입력한 검색어
    '''
    url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={query}'
    response = requests.get(url)
    html = response.text 
    soup = bs(html, 'html.parser')

    newsList = soup.select('a.news_tit')

    links = []

    for news in newsList:
        link = news['href']
        links.append(link)

    if links:
        for link in links:
            bot.sendMessage(chat_id=chat_id, text=link)
            time.sleep(3)
    else:
        pass

    return links

