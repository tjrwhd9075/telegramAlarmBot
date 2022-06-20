from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
from selenium import webdriver
import time
import asyncio

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

path = 'chromedriver'
header = {'user-agent':'Mozilla/5.0'}
filename = "sc.png"

def get_stockchart(ticker, type):
    '''
    ticker : $kospi $BTCUSD, aapl ...
    type : CANDLE, DETAIL, PNF, HA
    success : return 1
    '''
    # url = f"https://stockcharts.com/h-sc/ui?s={ticker}"
    # driver = webdriver.Chrome(path, options=chrome_options)
    # driver.get(url)
    # time.sleep(5)

    # source = driver.page_source
    # soup = bs(source, 'html.parser')

    # img = soup.select_one("#sharpCharts2 > form > div.chartImg-container > div > table > tbody > tr > td:nth-child(2) > div.chartnotes-container > img")
    # src = "http:"+img['src']
    # print(src)
    
    if type == "CANDLE": #candle-light
        url = f"https://stockcharts.com/c-sc/sc?s={ticker}&p=D&yr=1&mn=0&dy=0&i=t9225438292c&r=1643124910522"
    elif type == "DETAIL": #candle-detail
        url = f"https://stockcharts.com/c-sc/sc?s={ticker}&p=D&yr=1&mn=0&dy=0&i=t5124931867c&r=1643126799970"
    elif type == "PNF":
        url = f"https://stockcharts.com/pnf/chart?c={ticker},PGTADVYRBO[PA][D][F1!3!!!2!20]&r=4683&pnf=y"
    elif type == "HA": 
        url = f"https://stockcharts.com/c-sc/sc?s={ticker}&p=D&yr=0&mn=6&dy=0&i=t3606108084c&r=1643126520017"
                          
    try:        
        req = Request(url, headers=header)
        with urlopen(req) as response:
            html = response.read()
        with open(filename, 'wb') as f:
            f.write(html)
        return 1
    except Exception as e:
        return 0
    # driver.close()
    # driver.quit()
    

# async def get_pnfchart(ticker):
#     # url = f"https://stockcharts.com/freecharts/pnf.php?c={ticker},PGTADVYRBO[PA][D][F1!3!!!2!20]"
#     # driver = webdriver.Chrome(path, options=chrome_options)
#     # driver.get(url)
#     # time.sleep(5)

#     # source = driver.page_source
#     # soup = bs(source, 'html.parser')

#     # img = soup.select_one("#SCForm1 > div.chartImg-container > img")
#     # src = "http://stockcharts.com"+img['src']
#     # print(src)
    
#     url = f"https://stockcharts.com/pnf/chart?c={ticker},PGTADVYRBO[PA][D][F1!3!!!2!20]&r=4683&pnf=y"
#     req = Request(url, headers=header)
#     with urlopen(req) as response:
#         html = response.read()
#     with open(filename, 'wb') as f:
#         f.write(html)

#     # driver.close()
#     # driver.quit()

# asyncio.run(get_pnfchart("pypl"))
# # asyncio.run(get_stockchart("pypl"))


# '''
# 나이키 드로우  https://www.nike.com/kr/launch/?type=upcoming
# '''
# nikeimgfile = "nike.png"

# def get_nike():
#     url = "https://www.nike.com/kr/launch/?type=upcoming"
#     driver = webdriver.Chrome(path, options=chrome_options)
#     driver.get(url)
#     time.sleep(5)

#     source = driver.page_source
#     soup = bs(source, 'html.parser')
#     # print(soup)

#     nikes = soup.select("body > div.main-layout > div > div.ncss-col-sm-12.full > section > div.pt4-md.pt6-lg.feed-container > div > ul > li")


#     for nike in nikes:
#         try:
#             nikelink = nike.div.div.a["href"]
#             nikename = nike.div.div.a["title"]
#             nikedate = nike.div.div.a.div.div.get_text().split("\n")

#             if nike.div.div.a.img['src'].find("data:image") :
#                 nikeimg = nike.div.div.a.img['src']
#             else:
#                 nikeimg = nike.div.div.a.img['data-src']

#             req = Request(nikeimg, headers=header)

#             with urlopen(req) as response:
#                 html = response.read()
#             with open(nikeimgfile, 'wb') as f:
#                 f.write(html)
                
#             print("href : " + nikelink)
#             print("name : " + nikename)
#             print("month : " + nikedate[1])
#             print("day : " + nikedate[2])
#             print("img : " + nikeimg)
#             print("\n\n\n")
#         except Exception as e:
#             print(e)

    
# get_nike()


'''
<a class="card-link d-sm-b comingsoon" data-tag-pw-rank-product-id="DC8744-300" href="/kr/launch/t/men/fw/nike-sportswear/DC8744-300/zdev61/air-force-1-07-lx-nn" title="에어 포스 1">      
<div class="launch-time ta-sm-l d-sm-h d-md-b z10 mod-bg-grey pt6-sm pl6-sm">
<div class="launch-caption ta-sm-c">
<p class="headline-4" data-qa="draw-startDate">1월</p>
<p class="headline-1" data-qa="draw-day">30</p>
</div>
</div>
<img alt="Toasty" class="img-component image-component mod-image-component u-full-width" src="https://static-breeze.nike.co.kr/kr/ko_kr/cmsstatic/product/DC8744-300/75042a55-ae9c-42c1-85b4-132614cf6f07_primary.jpg?snkrBrowse" style="display: block;"/>
</a>
'''