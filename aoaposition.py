import requests
from bs4 import BeautifulSoup
import re
import time


from selenium import webdriver

url = "https://sigbtc.pro/"
driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
driver.implicitly_wait(30)
driver.get(url)


aoaPosition = driver.find_element_by_xpath("//div[@class='d-flex align-items-center text-hover-success']/div[@class='px-4 flex']/div[@class='text-highlight']")
print(aoaPosition.text) # 이름

aoaPosition2 = driver.find_element_by_xpath("//div[@class='d-flex align-items-center text-hover-success']/div[@class='px-4 flex']/div[@class='text-info mt-2 type1update']")
print(aoaPosition2.text) # 업데이트 시간

aoaPosition3 = driver.find_element_by_xpath("//div[@class='d-flex align-items-center text-hover-success']/a[@class='text-muted']")
print(aoaPosition3.text) # 포지션

driver.close()


# iframes = driver.find_elements_by_css_selector('iframe') #iframe이 여러개 있을 경우를 대비
# for iframe in iframes:
#     print(iframe.get_attribute('name')) #iframe들의 이름을 프린트
# driver.switch_to.frame('google_esf')

# aoaPosition = driver.find_element_by_class_name("text-info mt-2 type1update")





# from fake_useragent import UserAgent
# ua = UserAgent()

# header = {'user-agent':ua.chrome}
# def Whales_Position():
#     Whales_URL = requests.get('https://kimpya.site/apps/leaderboard.php', headers=header)
#     Whales = BeautifulSoup(Whales_URL.content, 'html.parser')
#     AOA = Whales.find('div', class_="tbl darklight")
#     print(AOA.table.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.
#     td.next_sibling.get_text()) # aoa
#     print(AOA.table.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.
#     td.next_sibling.next_sibling.get_text()) # position
#     print(AOA.table.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.
#     td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.get_text()) # 업데이트 날짜
    
# Whales_Position()

# def search():
#     session = requests.Session() 
#     addr = "https://hangang.ivlis.kr/"

#     session.encoding = 'utf-8'

#     req = session.get(addr)
#     time.sleep(2)
#     soup = BeautifulSoup(req.content, "html.parser")
#     print(soup)
#     table = soup.find(class_="display-4 display-title home-title decor anim-1")
#     print(table)

#     t_ary = list(table.stripped_strings)
#     print(t_ary)

#     result = t_ary[0]
#     return result


# def search():
#     URL = requests.get("https://hangang.ivlis.kr/aapi.php?type=dgr")
#     URL2= requests.get("https://hangang.ivlis.kr/aapi.php?type=text")

#     data = BeautifulSoup(URL.content, 'html.parser')
#     data2 = BeautifulSoup(URL2.content, 'html.parser')
#     print(data.get_text().replace("â„ƒ","℃"))
#     print(data2.get_text())
    
# search()

# COFIX_URL = RG('https://portal.kfb.or.kr/fingoods/cofix.php')
# COFIX_Data = BeautifulSoup(COFIX_URL.content, 'html.parser')
# COFIX_Find1 = COFIX_Data.tr.next_sibling.next_sibling.get_text()
# COFIX_Find2 = COFIX_Data.select('.resultList_ty02')[1].tr.next_sibling.next_sibling.get_text()


# xtml : parse.html -> lxml.xml


#[하랑] [오후 11:47] Headers = {
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36}
# [하랑] [오후 11:47] 가끔 헤더 요구하는 페이지가 있어요
# [하랑] [오후 11:47] 인베스팅같은 색기들
# [하랑] [오후 11:48] 사용법은 리퀘스트.겟
# [하랑] [오후 11:48] (url, headers = 헤더)

# from urllib.request import urlopen
# from urllib.parse import quote_plus
# import urllib.request

# def search():
#     URL = requests.get("https://thecatapi.com/")
#     print(URL)

#     data = BeautifulSoup(URL.content, 'html.parser')
#     # data.select("body.div.v-card.v-sheet.theme--light img")
#     dd = data.find_all("scr")
#     print(dd)

#     src=data.get("src")
#     print(src)

#     filename = src.split('/')[-1] #이미지 경로에서 날짜 부분뒤의 순 파일명만 추출
#     print(filename)
#     saveUrl = filename #저장 경로 결정
#     print(saveUrl)

#             # #파일 저장
#             # #user-agent 헤더를 가지고 있어야 접근 허용하는 사이트도 있을 수 있음(pixabay가 이에 해당)
#     req = urllib.request.Request(src)
#             # try:
#     imgUrl = urllib.request.urlopen(req).read() #웹 페이지 상의 이미지를 불러옴
#     with open(saveUrl,"wb") as f: #디렉토리 오픈
#         f.write(imgUrl) #파일 저장
            



# from urllib.request import Request, urlopen

# from requests.models import Response

# def search():

#     # URL = requests.get("https://cdn2.thecatapi.com/images/t6RhkPVH5.jpg")
#     # soup = BeautifulSoup(URL.content, 'html.parser')
#     # anchor = soup.select("body.img")
#     # print(anchor)
#     req = Request("https://cdn2.thecatapi.com/images/t6RhkPVH5.jpg",headers={'User-Agent': 'Mozilla/5.0'})
#     readTicker = urlopen(req).read()

#     with urlopen("https://cdn2.thecatapi.com/images/t6RhkPVH5.jpg") as f:
#         with open('image.png', 'wb') as b:
#             b.write(f.read())

# search()
