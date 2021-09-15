
from matplotlib.pyplot import text
import requests
from bs4 import BeautifulSoup
import re
import time
import asyncio
from pandas import Series, DataFrame

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

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
# chrome_options.add_argument("--disableWarnings")
chrome_options.add_argument('--log-level=1')   # 에러메시지 안뜨게?
# permissions-policy: interest-cohort=()

# path = 'chromedriver'
path = '/home/ubuntu/Downloads/chromedriver' 

async def get_skaiPrice():
    driver = webdriver.Chrome(path, options=chrome_options)
    # driver.maximize_window()    
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/92.0.4515.159'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    url = "https://kaiprotocol.fi/"
    driver.get(url)

    count = 0
    while True:
        skaiPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div[2]/div/section[2]/div[2]/div[1]/span")))
        if skaiPrice.text != "--":
            break
        count += 1
        print("count : " + str(count)) 

    txt2 = "sKAI : "+skaiPrice.text
    print(txt2) # 이름
    
    driver.close()
    driver.quit()
    return txt2

async def get_kaiPrice():
    driver = webdriver.Chrome(path, options=chrome_options)
    # driver.maximize_window()  
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/92.0.4515.159'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    url = "https://kaiprotocol.fi/"
    driver.get(url)
    
    count = 0
    while True:
        kaiPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div[2]/div/section[2]/div[1]/div[1]/span")))
        if kaiPrice.text != "--":
            break
        count += 1
        print("count : " + str(count))

    txt1 = "KAI : "+kaiPrice.text
    print(txt1) # 이름
    
    driver.close()
    driver.quit()
    return txt1

# 접속이 안되누.. ㅠㅠ
async def get_kspPrice():
    driver = webdriver.Chrome(path, options=chrome_options)
    # driver.maximize_window()  
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/92.0.4515.159'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    url = "https://klayswap.com/dashboard"
    driver.get(url)

    txt1 = ""
    try:
        kspPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main-view']/section/article[1]/div[2]/section[3]/div[1]/dl[1]/dd/span[2]")))
        txt1 = "KSP : $ "+kspPrice.text
        print(txt1) # 이름
    except Exception as e:
        print(e)
        txt1 = "KSP : error"
        print(txt1) # 이름

    driver.close()
    driver.quit()
    return txt1

async def get_klayPrice():
    driver = webdriver.Chrome(path, options=chrome_options)
    # driver.maximize_window()  
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/92.0.4515.159'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    url = "https://klayswap.com/dashboard"
    driver.get(url)

    txt1 = ""
    try:
        klayPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main-view']/section/article[1]/div[2]/section[3]/div[2]/dl[1]/dd")))

        txt2 = "KLAY : "+klayPrice.text
        print(txt2) # 이름
    except Exception as e:
        print(e)
        txt2 = "KLAY : error"
        print(txt2) # 이름

    driver.close()
    driver.quit()
    return txt2

async def get_aklayPrice():
    driver = webdriver.Chrome(path, options=chrome_options)
    # driver.maximize_window()  
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/92.0.4515.159'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    url = "https://klayswap.com/exchange/pool/detail/0xE74C8D8137541C0EE2C471cdAF4DCf03C383Cd22"
    driver.get(url)

    txt1 = ""
    try:
        klayPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='exchange-page']/div/section[2]/article[1]/ul[1]/li/div[2]/span")))

        k2ak = float(klayPrice.text.split(" ")[3])
        kp = float(klayPrice.text.split(" ")[5].replace("($", "").replace(")",""))
        akp = round(kp/k2ak,3)
        txt2 = "aKLAY : " + str(akp)
        print(txt2) # 이름
    except Exception as e:
        print(e)
        txt2 = "aKLAY : error"
        print(txt2) # 이름

    driver.close()
    driver.quit()
    return txt2

async def get_aklayRatio():
    driver = webdriver.Chrome(path, options=chrome_options)
    # driver.maximize_window()  
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/93.0.4577.63'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    url = "https://klayswap.com/exchange/pool/detail/0xE74C8D8137541C0EE2C471cdAF4DCf03C383Cd22"
    driver.get(url)

    txt1 = ""
    try:
        klayPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='exchange-page']/div/section[2]/article[1]/ul[1]/li/div[2]/span")))

        txt2 = float(klayPrice.text.split(" ")[3])
        print(txt2) # 이름
    except Exception as e:
        print(e)
        txt2 = "aKLAY ratio : error"
        print(txt2) # 이름

    driver.close()
    driver.quit()
    return txt2

async def get_kfiPrice():
    driver = webdriver.Chrome(path, options=chrome_options)
    # driver.maximize_window()  
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/92.0.4515.159'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # url = "https://klayfi.finance/"
    url = "https://klayswap.com/exchange/pool/detail/0xD74D4B4d2FB186BB7F31E4000c59ADE70BbD8a23"
    driver.get(url)

    count = 0
    while True:
        # kfiPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div[1]/div[1]/div/div[1]/span")))
        kfiPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='exchange-page']/div/section[2]/article[1]/ul[1]/li/div[2]/span")))
        if kfiPrice.text != "":                                                                 
            break
        count += 1
        print("count : " + str(count)) 

    kfiRatio = float(kfiPrice.text.split(" ")[3])
    klayPrice = float(kfiPrice.text.split("$")[1].replace(")",""))
    kfiPri = round(klayPrice/kfiRatio,3)

    txt1 = "KFI : $ "+ str(kfiPri)
    print(txt1) # 이름

    driver.close()
    driver.quit()
    return txt1

async def get_housePrice():
    driver = webdriver.Chrome(path, options=chrome_options)
    # driver.maximize_window()  
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/92.0.4515.159'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    url = "https://klaystake.house/"
    driver.get(url)
    
    element = driver.find_element_by_xpath("//*[@id='app']/div[1]/div/div[2]/div/div/div/button")
    driver.execute_script("(arguments[0]).click();", element)

    count = 0
    while True:
        housePrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/section/div[2]/div[2]/div[2]/p/span[1]")))
        if housePrice.text != "":
            break
        count += 1
        print("count : " + str(count)) 
    txt1 = "HOUSE : $ "+housePrice.text
    print(txt1) # 이름

    driver.close()
    driver.quit()
    return txt1

# 수정필요
async def kaiChart():
    driver = webdriver.Chrome(path, options=chrome_options)
    # driver.maximize_window()  
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/92.0.4515.159'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    url = "https://kaiprotocol.fi/"
    driver.get(url)
    # 
    button = driver.find_element_by_xpath("//*[@id='root']/body/div/div/section[2]/div/div/div[1]/h5/button[1]")
    button.click()

    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='reactgooglegraph-10']/div/div[1]/div")))
    element_png = element.screenshot_as_png 
    with open("test1.png", "wb") as file: 
        file.write(element_png)

    driver.close()

# asyncio.run( get_skaiPrice())
# asyncio.run( get_kaiPrice())
# asyncio.run( get_kspPrice())
# asyncio.run( get_klayPrice())
# asyncio.run( get_aklayRatio())
# asyncio.run( get_kfiPrice())
# asyncio.run( get_housePrice())
# asyncio.run( kaiChart())


from fake_useragent import UserAgent

async def Whales_Position():
    '''
    '''
    ua = UserAgent()
    header = {'user-agent':ua.chrome}

    Whales_URL = requests.get('https://kimpya.site/apps/leaderboard.php', headers=header)
    Whales = BeautifulSoup(Whales_URL.content, 'html.parser')
    text = []

    AOA_NAME= Whales.select("body > main > div > main > div > div.tbl.darklight > table > tbody > tr:nth-child(5) > td:nth-child(2)")
    AOA_POSI= Whales.select("body > main > div > main > div > div.tbl.darklight > table > tbody > tr:nth-child(5) > td:nth-child(3) > span")
    AOA_24BTC =  Whales.select("body > main > div > main > div > div.tbl.darklight > table > tbody > tr:nth-child(5) > td:nth-child(5) > span")
    AOA_UPDATETIME =  Whales.select("body > main > div > main > div > div.tbl.darklight > table > tbody > tr:nth-child(5) > td:nth-child(8)")

    text.append(AOA_NAME[0].get_text())
    text.append(AOA_POSI[0].get_text())
    text.append(AOA_24BTC[0].get_text())
    text.append(AOA_UPDATETIME[0].get_text())

    SNAP_NAME= Whales.select("body > main > div > main > div > div.tbl.darklight > table > tbody > tr:nth-child(9) > td:nth-child(2)")
    SNAP_POSI= Whales.select("body > main > div > main > div > div.tbl.darklight > table > tbody > tr:nth-child(9) > td:nth-child(3) > span")
    SNAP_24BTC =  Whales.select("body > main > div > main > div > div.tbl.darklight > table > tbody > tr:nth-child(9) > td:nth-child(5) > span")
    SNAP_UPDATETIME =  Whales.select("body > main > div > main > div > div.tbl.darklight > table > tbody > tr:nth-child(9) > td:nth-child(8)")

    
    text.append(SNAP_NAME[0].get_text().split("-")[0])
    text.append(SNAP_POSI[0].get_text())
    text.append(SNAP_24BTC[0].get_text())
    text.append(SNAP_UPDATETIME[0].get_text())

    SKIT_NAME= Whales.select("body > main > div > main > div > div.tbl.darklight > table > tbody > tr:nth-child(17) > td:nth-child(2)")
    SKIT_POSI= Whales.select("body > main > div > main > div > div.tbl.darklight > table > tbody > tr:nth-child(17) > td:nth-child(3) > span")
    SKIT_24BTC =  Whales.select("body > main > div > main > div > div.tbl.darklight > table > tbody > tr:nth-child(17) > td:nth-child(5) > span")
    SKIT_UPDATETIME =  Whales.select("body > main > div > main > div > div.tbl.darklight > table > tbody > tr:nth-child(17) > td:nth-child(8)")

    text.append(SKIT_NAME[0].get_text().split("-")[0])
    text.append(SKIT_POSI[0].get_text())
    text.append(SKIT_24BTC[0].get_text())
    text.append(SKIT_UPDATETIME[0].get_text())

    print(text)

    return text

    # # except Exception:
    # #     return "kimpya.site 접속에러"
    # aoa = AOA.table.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.td.next_sibling.get_text() # aoa
    # aoaPosition = AOA.table.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.td.next_sibling.next_sibling.get_text() # position
    # aoaTime = AOA.table.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.get_text() # 업데이트 날짜
    # # 
    # txt = []
    # txt.append(aoa)
    # txt.append(aoaPosition)
    # txt.append(aoaTime)
    # return txt

# Whales_Position()


def pool():
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/92.0.4515.159'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    url = "https://klaywatch.com/swap"
    driver.get(url)

    # count = 0
    # while True:
    skaiPrice = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div[1]/div/div[2]/div[2]/div[3]/div[1]")))
                                                                                            # //*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[3]/div[1]

    print(skaiPrice.text) # 이름
    
    driver.close()
    driver.quit()
# pool()


# async def get_aoaPosition():
#     driver = webdriver.Chrome(path, options=chrome_options)
#     driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/92.0.4515.159'})
#     driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#     # print(driver.execute_script("return navigator.userAgent;"))
#     # driver.implicitly_wait(30)
#     url = "https://sigbtc.pro/"
#     driver.get(url)

#     txt = []

#     time.sleep(100)

#     print(txt)
    
#     driver.close()
#     # driver.quit()
#     return txt

    # aoaPosition3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mainMenu']/div/div[6]/div/div/div/a/span"))) #//*[@id="mainMenu"]/div/div[6]/div/div/div/a/span
    # print(aoaPosition3.text)


    # count = 0
    # while True: # 워뇨띠
    #     try:
    #         aoaPosition3 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mainMenu']/div/div[6]/div/div/div/a/span"))) #//*[@id="mainMenu"]/div/div[6]/div/div/div/a/span
    #         if aoaPosition3.text != "" : 
    #             txt.append(aoaPosition3.text)
    #             print(txt) # 포지션
    #             break
    #         count+=1
    #         print("count : " + str(count))
    #     except Exception :
    #         count+=1
    #         print("e count : " + str(count))
    
    # count = 0
    # while True:
    #     aoaPosition2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[6]/div/div/div/div[2]/div[2]")))
    #     if aoaPosition2.text != "" :
    #         txt.append(aoaPosition2.text.replace("\u3000", " "))
    #         print(txt) # 업데이트 시간
    #         break
    #     count+=1
    #     print("count : " + str(count))

    # count = 0
    # while True: # skitter
    #     aoaPosition3 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[7]/div/div/div/a/span")))
    #     if aoaPosition3.text != "" :
    #         txt.append(aoaPosition3.text)
    #         # print(txt) # 포지션
    #         break
    #     count+=1
    #     # print("count : " + str(count))

    # count = 0
    # while True: 
    #     aoaPosition2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[7]/div/div/div/div[2]/div[2]")))
    #     if aoaPosition2.text != "" :
    #         txt.append(aoaPosition2.text.replace("\u3000", " "))
    #         # print(txt) # 업데이트 시간
    #         break
    #     count+=1
    #     # print("count : " + str(count))

    # count = 0
    # while True:  # snapdragon
    #     aoaPosition3 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[8]/div/div/div/a/span")))
    #     if aoaPosition3.text != "" :
    #         txt.append(aoaPosition3.text)
    #         # print(txt) # 포지션
    #         break
    #     count+=1
    #     # print("count : " + str(count))

    # count = 0
    # while True:
    #     aoaPosition2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[8]/div/div/div/div[2]/div[2]")))
    #     if aoaPosition2.text != "" :
    #         txt.append(aoaPosition2.text.replace("\u3000", " "))
    #         # print(txt) # 업데이트 시간
    #         break
    #     count+=1
    #     # print("count : " + str(count))

    # count = 0
    # while True: # 박호두
    #     aoaPosition3 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[9]/div/div/div/a/span")))
    #     if aoaPosition3.text != "" :
    #         txt.append(aoaPosition3.text)
    #         # print(txt) # 포지두
    #         break
    #     count+=1
    #     # print("count : " + str(count))

    # count = 0
    # while True:
    #     aoaPosition2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-content']/div/div/div[9]/div/div/div/div[2]/div[2]")))
    #     if aoaPosition2.text != "" :
    #         txt.append(aoaPosition2.text.replace("\u3000", " "))            # print(txt) # 업데이트 시간
    #         break
    #     count+=1
    #     # print("count : " + str(count))
    


# asyncio.run(get_aoaPosition())



    #######

    # 내 클립주소 : 0x89730F1e0416762eb65c77F86259e1bA00d3C529
    # 거래내역 : 
    # -> 스왑, 예치, 인출, 보상 데이터 저장하기..

def save_klayWatch():
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.maximize_window()
    url = "https://klaywatch.com/history/0x89730F1e0416762eb65c77F86259e1bA00d3C529"
    driver.get(url)

    #거래내역버튼
    driver.implicitly_wait(10)
    transactionHistoryButton = driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div/div[1]/div[2]/div/a[2]")
    print(transactionHistoryButton.text)
    transactionHistoryButton.click()

    #########거래내역 -> 스왑     
    i=4; j=0
    dfSwap = DataFrame(columns=['date','coin_from', 'amount_from', 'value_from', 'price_from', 'coin_to', 'amount_to', 'value_to', 'price_to']) #              
    while True:
        try:
            a = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div[1]/div/div[2]/div[2]/div[" +str(i)+"]/div")))
            # print(a.text.split("\n"))
            txt = a.text.split("\n")

            t = DataFrame(data=[[txt[1], txt[2], txt[3].split(" ")[0], txt[3].split(" ")[-2].replace("(","").replace(",",""),
            txt[4].split(" ")[2].replace(",",""), txt[5], txt[6].split(" ")[0], txt[6].split("(")[-1][:-3].replace(",",""), txt[7].split(" ")[2].replace(",","")]], columns=['date','coin_from', 'amount_from', 'value_from', 'price_from', 'coin_to', 'amount_to', 'value_to', 'price_to'])
            dfSwap = dfSwap.append(t)

            i+=1; j+=1
        except Exception:
            break
    dfSwap = dfSwap.set_index("date")
    print(dfSwap)
    print("\n")

    ###########거래내역 -> 예치
    driver.implicitly_wait(1)
    depositButton = driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div/div[2]/div[2]/div[2]/label[2]")
    print(depositButton.text)
    depositButton.click()

    i=4; j=0   
    dfDeposit = DataFrame(columns=['date','coin1_from', 'amount1_from', 'value1_from', 'price1_from','coin2_from', 'amount2_from', 'value2_from', 'price2_from', 'pair_to', 'value_to']) 
    while True:
        try:
            b = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div[1]/div/div[2]/div[2]/div[" +str(i)+"]/div")))
            print(b.text.split("\n"))
            txt = b.text.split("\n")

            print(txt[1])
            print(txt[2])
            print(txt[3].split(" ")[0])
            print(txt[4].split(" ")[0].replace("원","").replace(",",""))
            print(txt[4].split(" ")[-2].replace(",",""))
            print(txt[5])
            print(txt[6].split(" ")[0])
            print(txt[7].split(" ")[0].replace(",",""))
            print(txt[7].split(" ")[-2].replace(",",""))
            print(txt[8])
            print(txt[9].replace("원","").replace(",",""))


            t = DataFrame(data=[
                [txt[1], # date
                txt[2],  # coin1
                txt[3].split(" ")[0], #amt1
                txt[4].split(" ")[0].replace("원","").replace(",",""), #val1
                txt[4].split(" ")[-2].replace(",",""),  # price1
                txt[5],  # coin2
                txt[6].split(" ")[0], #amt2
                txt[7].split(" ")[0].replace(",",""), #val2
                txt[7].split(" ")[-2].replace(",",""),  # price2
                txt[8], #pair
                txt[9].replace("원","").replace(",","")]],  # value
                columns=['date','coin1_from', 'amount1_from', 'value1_from', 'price1_from','coin2_from', 'amount2_from', 'value2_from', 'price2_from', 'pair_to', 'value_to'])
            dfDeposit = dfDeposit.append(t)

            i+=1; j+=1
        except Exception:
            break
    dfDeposit = dfDeposit.set_index("date")
    print(dfDeposit)
    print("\n")
    
    ##########거래내역 -> 인출
    driver.implicitly_wait(1)
    withdrawButton = driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div/div[2]/div[2]/div[2]/label[3]")
    print(withdrawButton.text)
    withdrawButton.click()

    i=4; j=0   
    dfWithdraw = DataFrame(columns=['date','pair_from', 'value_from','coin1_to','amount1_to', 'value1_to', 'coin2_to','amount2_to', 'value2_to'])               
    while True:
        try:
            c = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div[1]/div/div[2]/div[2]/div[" +str(i)+"]/div")))
            # print(c.text.split("\n"))
            txt = c.text.split("\n")

            t = DataFrame(data=[[
                txt[1], # date
                txt[2],  # pair_from
                txt[3].replace("원","").replace(",",""), #value_from
                txt[4], #coin1_to
                txt[5].split(" ")[0],  # amount1_to
                txt[6].replace("원","").replace(",",""),  # value1_to
                txt[7], #coin2_to
                txt[8].split(" ")[0], #amount2_to
                txt[9].replace("원","").replace(",","")  # value2_to
                ]], columns=['date','pair_from', 'value_from','coin1_to','amount1_to', 'value1_to', 'coin2_to','amount2_to', 'value2_to'])
            dfWithdraw = dfWithdraw.append(t)

            i+=1; j+=1
        except Exception:
            break
    dfWithdraw = dfWithdraw.set_index("date")
    print(dfWithdraw)
    print("\n")

    ###########거래내역 -> 보상
    driver.implicitly_wait(1)
    apyButton = driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div/div[2]/div[2]/div[2]/label[4]")
    print(apyButton.text)
    apyButton.click()

    i=4; j=0   
    dfApy = DataFrame(columns=['date','pool','coin','amount','value','price'])               
    while True:
        try:
            d = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div[1]/div/div[2]/div[2]/div[" +str(i)+"]/div")))
            # print(d.text.split("\n"))
            txt = d.text.split("\n")

            t = DataFrame(data=[[
                txt[1], # date
                txt[2],  # pool
                txt[3].split(" ")[-1],# coin
                txt[3].split(" ")[0],  # apy_amount
                txt[4].split(" ")[0].replace("원","").replace(",",""),  # value
                txt[4].split(" ")[-2].replace(",",""), # price
                ]], columns=['date','pool','coin','amount','value','price'])
            dfApy = dfApy.append(t)

            i+=1; j+=1
        except Exception:
            break
    dfApy = dfApy.set_index("date")
    print(dfApy)
    print("\n")

    driver.quit()

# save_klayWatch()





















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
