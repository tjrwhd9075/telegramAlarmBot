
import requests
from bs4 import BeautifulSoup
import re
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from pyvirtualdisplay import Display


# display = Display(visible=0, size=(1024, 768)) 
# display.start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')    # 창 띄우지 X
chrome_options.add_argument('disable-gpu')  # gpu 사용 X
chrome_options.add_argument('no-sandbox')
chrome_options.add_argument("single-process")
chrome_options.add_argument("disable-dev-shm-usage")
# chrome_options.add_argument("--disableWarnings")


path = 'chromedriver'
# path = '/home/ubuntu/Downloads/chromedriver' 
# driver = webdriver.Chrome(path, options=chrome_options)

import asyncio

async def get_kaiPrice():
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.maximize_window()
    # driver.implicitly_wait(30)
    url = "https://kaiprotocol.fi/"
    driver.get(url)
    
    a= 0
    while a<20:
        kaiPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/body/div/div/section[2]/div/div/div[1]/div/div[1]/h6[2]")))
        if kaiPrice.text != "--" :
            break
        a +=1
    txt1 = "KAI : "+kaiPrice.text
    print(txt1) # 이름

    a=0
    while a<20:
        skaiPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/body/div/div/section[2]/div/div/div[2]/div/div[1]/h6[2]")))
        if skaiPrice.text != "--":
            break
        a+=1
    txt2 = "sKAI : "+skaiPrice.text
    print(txt2) # 이름

    driver.close()

    return txt1 + "\n"+ txt2


async def get_klayPrice():
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.maximize_window()
    # driver.implicitly_wait(30)
    url = "https://klayswap.com/dashboard"
    driver.get(url)
    
    a=0
    while a<20:
        kspPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main-view']/section/article[1]/div[2]/section[3]/div[1]/dl[1]/dd/span[2]")))
        if kspPrice.text != "--" :
            break
        a+=1
    txt1 = "KSP : $ "+kspPrice.text
    print(txt1) # 이름

    a=0
    while a<20:
        klayPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main-view']/section/article[1]/div[2]/section[3]/div[2]/dl[1]/dd")))
        if klayPrice.text != "--":            
            break
        a+=1
    txt2 = "KLAY : "+klayPrice.text
    print(txt2) # 이름

    driver.close()
    return txt1 + "\n" + txt2


async def get_kfiPrice():
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.maximize_window()
    # driver.implicitly_wait(30)
    url = "https://klayfi.finance/"
    driver.get(url)

    a=0    
    while a<20:
        kfiPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div[1]/div[2]/div[1]/span")))
        if kfiPrice.text != "--" :
            break
        a+=1
    txt1 = "KFI : "+kfiPrice.text
    print(txt1) # 이름

    driver.close()
    return txt1


async def get_housePrice():
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.maximize_window()
    # driver.implicitly_wait(30)
    url = "https://klaystake.house/"
    driver.get(url)
    
    a=0
    while a<20:
        housePrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/section/div[2]/div[2]/div[2]/p/span[1]")))
        if housePrice.text != "--" :
            break
        a+=1
    txt1 = "HOUSE : $ "+housePrice.text
    print(txt1) # 이름

    driver.close()
    return txt1


# asyncio.run( get_kaiPrice())
# asyncio.run( get_klayPrice())
# asyncio.run( get_kfiPrice())
# asyncio.run( get_housePrice())




async def get_aoaPosition():
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.maximize_window()
    # driver.implicitly_wait(30)
    url = "https://sigbtc.pro/"
    driver.get(url)

    txt = []

    a=0
    while a<20: # 워뇨띠
        aoaPosition3 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[6]/div/div/div/a/span")))
        if aoaPosition3.text != "" :
            txt.append(aoaPosition3.text)
            # print(txt) # 포지션
            break
        a+=1
    
    a=0
    while a<20:
        aoaPosition2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[6]/div/div/div/div[2]/div[2]")))
        if aoaPosition2.text != "" :
            txt.append(aoaPosition2.text.replace("\u3000", " "))
            # print(txt) # 업데이트 시간
            break
        a+=1

    a=0
    while a<20: # skitter
        aoaPosition3 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[7]/div/div/div/a/span")))
        if aoaPosition3.text != "" :
            txt.append(aoaPosition3.text)
            # print(txt) # 포지션
            break
        a+=1

    a=0
    while a<20:
        aoaPosition2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[7]/div/div/div/div[2]/div[2]")))
        if aoaPosition2.text != "" :
            txt.append(aoaPosition2.text.replace("\u3000", " "))
            # print(txt) # 업데이트 시간
            break
        a+=1
    a=0
    while a<20: # snapdragon
        aoaPosition3 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[8]/div/div/div/a/span")))
        if aoaPosition3.text != "" :
            txt.append(aoaPosition3.text)
            # print(txt) # 포지션
            break
        a+=1

    a=0
    while a<20:
        aoaPosition2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[8]/div/div/div/div[2]/div[2]")))
        if aoaPosition2.text != "" :
            txt.append(aoaPosition2.text.replace("\u3000", " "))
            # print(txt) # 업데이트 시간
            break
        a+=1

    a=0
    while a<20: # 박호두
        aoaPosition3 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[9]/div/div/div/a/span")))
        if aoaPosition3.text != "" :
            txt.append(aoaPosition3.text)
            # print(txt) # 포지두
            break
        a+=1

    a=0
    while a<20:
        aoaPosition2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[9]/div/div/div/div[2]/div[2]")))
        if aoaPosition2.text != "" :
            txt.append(aoaPosition2.text.replace("\u3000", " "))            # print(txt) # 업데이트 시간
            break
        a+=1
    
    print(txt)
    
    driver.close()
    return txt

# asyncio.run(get_aoaPosition())


# from bs4 import BeautifulSoup
# from fake_useragent import UserAgent

# def Whales_Position():
#     '''
#     aoa, aoaPosition, aoaTime
#     '''
#     ua = UserAgent()
#     header = {'user-agent':ua.chrome}

#     try:
#         Whales_URL = requests.get('https://kimpya.site/apps/leaderboard.php', headers=header)
#         Whales = BeautifulSoup(Whales_URL.content, 'html.parser')
#         AOA = Whales.find('div', class_="tbl darklight")
#     except Exception:
#         return "kimpya.site 접속에러"
#     aoa = AOA.table.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.td.next_sibling.get_text() # aoa
#     aoaPosition = AOA.table.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.td.next_sibling.next_sibling.get_text() # position
#     aoaTime = AOA.table.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.get_text() # 업데이트 날짜
#     # 
#     txt = []
#     txt.append(aoa)
#     txt.append(aoaPosition)
#     txt.append(aoaTime)
#     return txt 
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
