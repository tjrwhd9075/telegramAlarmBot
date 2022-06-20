from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
from selenium import webdriver
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument('headless')    # 창 띄우지 X
chrome_options.add_argument('disable-gpu')  # gpu 사용 X
chrome_options.add_argument('no-sandbox')
chrome_options.add_argument("single-process")
chrome_options.add_argument("disable-dev-shm-usage")
chrome_options.add_argument("--disableWarnings")
chrome_options.add_argument('--log-level=1')   # 에러메시지 안뜨게?

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()   

path = 'chromedriver'
header = {'user-agent':'Mozilla/5.0'}
nikeimgfile = "nike.png"



#텔레그램 봇
import telegram as tel
myToken = '1811197670:AAFaSU2l8pKxT6tDA3tOl2Tpue-OiNC1Af0'
telbot = tel.Bot(token=myToken)

channel_id_korea = "@ha_alarm_korea"



'''
나이키 드로우  https://www.nike.com/kr/launch/?type=upcoming
'''

def get_nike():
    url = "https://www.nike.com/kr/launch/?type=upcoming"
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.get(url)
    time.sleep(5)

    source = driver.page_source
    soup = bs(source, 'html.parser')
    nikes = soup.select("body > div.main-layout > div > div.ncss-col-sm-12.full > section > div.pt4-md.pt6-lg.feed-container > div > ul > li")

    for nike in nikes:
        try:
            nikelink = "https://www.nike.com"+ nike.div.div.a["href"]
            nikename = nike.div.div.a["title"]
            nikedate = nike.div.div.a.div.div.get_text().split("\n")

            if nike.div.div.a.img['src'].find("data:image") :
                nikeimg = nike.div.div.a.img['src']
            else:
                nikeimg = nike.div.div.a.img['data-src']

            req = Request(nikeimg, headers=header)

            with urlopen(req) as response:
                html = response.read()
            with open(nikeimgfile, 'wb') as f:
                f.write(html)
                
            print("href : " + nikelink)
            print("name : " + nikename)
            print("month : " + nikedate[1])
            print("day : " + nikedate[2])
            print("img : " + nikeimg)
            print("\n")
            telbot.send_photo(chat_id=channel_id_korea, photo=open('nike.png', 'rb'), 
                            caption="👟 나이키 드로우 👟\n이름 : " + nikename + "\n날짜 : " + nikedate[1] + " " + nikedate[2] +"일\n링크 : " + nikelink)

        except Exception as e:
            print(e)
    
# get_nike()


# https://www.nike.com/kr/launch/t/men/fw/nike-sportswear/DC8744-300/zdev61/air-force-1-07-lx-nn