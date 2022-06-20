
# https://goodthings4me.tistory.com/560
'''
import pathlib

## 파일명 변경 함수
def rename_file(filepath, filenames):
    # path = pathlib.Path('.') / 'rename' # pathlib.Path('./rename')과 동일
    path = pathlib.Path(filepath)
    print(path)  # rename
    file_count = len([f for f in path.iterdir()])  # 폴더내 파일수
    file_count_len = len(str(file_count))
    print(f'file_count: {file_count}/nlen: {file_count_len}')

    cnt = 1
    for file in path.iterdir():
        if not file.is_dir():
            # print(file)  # rename/test10.png
            print(file.name)  # test10.png
            # print(file.stem)  # test10
            # print(file.suffix)  # .png
            # print(file.parent)  # remame
            # print()

            directory = file.parent
            file_name_ext = file.name
            file_name = file.stem
            extension = file.suffix
            
            if file.is_file():
                new_filename = filenames + str(cnt).zfill(file_count_len) + extension
                # 숫자 앞에 0 채우기 .zfill(숫자길이)
                file.rename(path / new_filename)
            cnt += 1

    print('-' * 30)
    
    for f in path.iterdir():
        print(f.name)


file_dir = r'D:/rename/sub_rename'
new_filename = 'Anaconda 설치_'

rename_file(file_dir, new_filename)
'''
'''
#파일관리 함수

shutil.copy(a, b)
shutil.move(a, b)
shutil.rmtree(path) # 비어있는 directory만 삭제 가능
os.rename(a, b)
os.remove(f)

os.chdir(d) # change
os.mkdir(d) # make ☆ (이미 존재하면 예외)
os.rmdir(d) # remove
os.getcwd() # 현재 working directory 문자열 리턴
os.listdir(d) # directory 목록
glob.glob(pattern)
os.path.isabs(f) # 절대경로 검사
os.path.abspath(f) # 상대경로 -> 절대경로
os.path.realpath(f)
os.path.exists(f) # 경로 존재 검사 ☆
os.path.isfile(f) # 파일인지 검사
os.path.isdir(f) # directory인지 검사
'''

from cProfile import label
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
from matplotlib.pyplot import title
from numpy import setxor1d
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pprint import pprint

from sympy import EX

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

# import chromedriver_autoinstaller
# chromedriver_autoinstaller.install()    

# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())

# https://chromedriver.chromium.org/downloads  크롬드라이버 다운로드 사이트

path = 'chromedriver'
header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'}




def replaceTxt(txt):
    dic = {'\\':' ', '/':" ", ":" :" ", "*" :" ", "?" :" ", "<" :" ", ">" :" ", "|" :" ", '"' :" ","●":" ",
            "화장실" :"#화장sil ", "로리":"#로Li ","롤리":"#로Li ","유부녀":"#유Bu녀 ","아내":"#아내 ","선생님":"#선생님 ","페라":"#페라 ","펠라":"#페라 ","부카케":"#부카케 ",
            "조교":"#조교 ","절륜":"#절륜 ","NTR":"#NTR ","옆집":"#옆집 ","누나":"#누나 ","난교":"#난교 ","3P":"#3P ","아르바이트":"#아르바이트 ","알바":"#아르바이트 ",
            "매직미러":"#매직미러 ","매직 미러":"#매직미러 ","비서":"#비서 ","OL":"#OL ","회사":"#회사 ","상사":"#상사 ","부하":"#부하 ","학원":"#학원 ","학교":"#학교 ",
            "여학생":"#여학생 ","여동생":"#여동생 ","가정교사":"#가정교사 ","요가":"#요가 ","오일":"#오일 ","에스테":"#에스테틱 ","마사지":"#마사지 ","정조대":"#정조대 ",
            "방뇨":"#방뇨 ","아내":"#아내 ","빼앗겨소망":"#빼앗겨소망 ", "츤데레":"#츤데레 ","레2프":"#레2프 ","윤간":"#윤gan ","레깅스":"#레깅스 ", "차내":"#차내 ",
            "근친상간":"#근chin상gan ","근친 상간":"#근chin상gan ", "근친":"#근chin상gan ", "키스":"#키스 ","며느리":"#며느리 ","시아버지":"#시아버지 ","지근거리":"#지근거리 ",
            "7내4정":"#7내4정 ","질내사정":"#7내4정","질 내 사 정":"#7내4정","질내 사정":"#7내4정", "질 사":"#7내4정 ","질 정액 샷":"#7내4정 ", "병원":"#병원 ","동정":"#동정 ","엉덩이":"#엉덩이 ","파이 빵":"#파이빵 ","치한":"#치한 ","치하철":"#지하철 ",
            "버스":"#버스 ","항문":"#항문 ", "아날":"#애널 ", "애널":"#애널 ", "모델":"#모델 ","강제":"#강je #레2프 ","커플":"#커플 ","수영복":"#수영복 ","수영장":"#수영장 ","강사":"#강사 ",
            "친구":"#친구 ","구속":"#구속 ","치매":"#치한 ","임신":"#임신 ","헌팅":"#헌팅 ","난파":"#난파 ","남파":"#난파 ","자취방":"#자취방 ","데이트":"#데이트 ",
            "코스프레":"#코스프레 ","풍속":"#풍속 ","실사화":"실사화 #만화원작 ","여대생":"#여대생 ","DEBUT":"#데뷔 ","슬로우":"#슬로우 ","아저씨":"#아저씨 ","쓰레기방":"#쓰레기방 ",
            "언니":"#언니 ","농밀":"#농밀 ","불륜":"#불륜 ","관장":"#관장 ","애인":"#애인 ","변태":"변Tae","자매":"#자매 ","가족":"#가족 ","흑인":"#흑인 ","실금":"#실금 ",
            "스커트":"#스커트 ","미니스커트":"#미니스커트 ","미니 스커트":"#미니스커트 ","원피스":"#원피s","스타킹":"#스타킹 ","스마타":"#스마타 ","비비기":"#비비기 ","코기":"#코기 ",
            "시골":"#시골 ","부인":"#부인 ","중출":"#7내4정 ","이라마":"#이라마 ","최음":"#최음 ","수면":"#수면 ","수면간":"#수면간 ","수면제":"#수면je ", "만취":"#만취 ","만취간":"#만취간 ",
            "최면":"#최면 ", "미약":"#미약 ","강간":"#강gan ", "레이프":"#레2프 ","도촬":"#Do촬 ","몰래 카메라":"#Mol카 ", "미용사":"#미용사 ","미용실":"#미용실 ","미장원":"#미용실 ",
            "메이드":"#메이드 ","봉사":"#봉사 ", "이웃":"#이웃 ", "이웃집":"#이웃집 ","중년":"#중년 ","호텔":"#호텔 ", "부부":"#부부 ", "야외":"#야외 ","옥외":"#야외 ",
            "로션":"#로션 ",
            "##":"#","   ":" ","  ":" ","#_":"#"}

    for key in dic.keys():
        txt = txt.replace(key, dic[key])

    print(txt)

    return txt
  

import googletrans

def gtranslate():
    translator = googletrans.Translator()
    
    for filename in os.listdir(file_path): #현재 위치 (.) 의 파일을 모두 가져온다
        name, ext = os.path.splitext(filename)
        print("파일명 : " + name + ", 확장자 : " + ext) 

        sname = name.split(" ")

        if sname[0].upper() == "FC2-PPV":
            named = " ".join(sname[2:]) #품번을 제외한 제목
            pum = " ".join(sname[:2])
        else:
            named = " ".join(sname[1:]) #품번을 제외한 제목
            pum = sname[0]

        if named != None : #제목이 없는지 확인
            newName = translator.translate(named, dest='ko') #번역
            newName = replaceTxt(newName.text) #수정
            newName = pum +" " + newName + ext
        else :
            newName = pum + ext

        print("새파일명 : " + newName)

        file_oldname = os.path.join(file_path,filename)
        file_newname = os.path.join(file_path,newName)
        os.renames(file_oldname, file_newname) 
        print(" 파일명 수정 완료!\n\n")



avdbs = "https://www.avdbs.com/"
def get_pumInfo(pumnum):
    url = f'https://www.avdbs.com/menu/search.php?kwd={pumnum}&seq=0&tab=2'
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.get(url)

    source = driver.page_source
    soup = bs(source, 'html.parser')

    #로그인
    chk = soup.select('#contants > ul.page_tab > li.tab_2.on > a > span')[0].get_text()
    print(chk)
    if chk == '(-1)':
        login = soup.select('#srch-bar > div.hdr_menu > ul > li:nth-child(1) > a')[0]['href']
        login = avdbs + login
        print(login)
        driver.get(login)
        user_id = 'tjrwhd9075'
        user_pwd = 'ysj7953!'
        driver.find_element(By.ID,'member_uid').send_keys(user_id)
        driver.find_element(By.ID,'member_pwd').send_keys(user_pwd)
        driver.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/button[1]').click()

        time.sleep(3)
        
        driver.get(url)
        source = driver.page_source
        soup = bs(source, 'html.parser')

    time.sleep(5)

    try : 
        pum = soup.select("#contants > ul.container > li.page.page_2 > div > ul > li > div > div.dscr > p.title > a.lnk_dvd_dtl")[0]
        print(pum)         
    except Exception as e:
        print(e)
        pum = soup.select("#contants > ul.container > li.page.page_2 > div > ul > li:nth-child(1) > div > div.dscr > p.title > a.lnk_dvd_dtl")[0]
        print(soup) 


    pumlink = avdbs + pum['href']
    print(pumlink)
    pumtitle = pum.get_text()
    print(pumtitle)

    url = pumlink
    driver.get(url)
    # time.sleep(100)

    source = driver.page_source
    soup = bs(source, 'html.parser')
    pumactor = soup.select("#ranking_tab1 > div.profile_view_top > div.path_row > ul > li:nth-child(2) > h1 > a > span:nth-child(2) > span:nth-child(3)")[0].get_text()
    print(pumactor)
    pumdate = soup.select("#ranking_tab1 > div.profile_view_top > div.profile_view_inner > div.profile_picture > div > div.profile_detail > p:nth-child(1)")[0].get_text()
    print(pumdate.split(" ")[1])

    pumname = " ["+pumactor+"] "+pumtitle+" ("+pumdate.split(" ")[1]+")"
    # pumname = " ["+pumactor+"] "+" ("+pumdate.split(" ")[1]+")"

    return pumname


from selenium.webdriver.common.keys import Keys

def get_pumInfo_fc2(pumnum):
    url = f'https://db.msin.jp/jp.search/movie?str={pumnum}'
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, 'body > div.modalouter > div > a.close_modal').click()
    # time.sleep(5)

    source = driver.page_source
    soup = bs(source, 'html.parser')

    try :
        pum = soup.select("#content > a")[0]
        pumlink = pum['href']
        print(pumlink)
    except Exception as e :
            print(e)
            print("검색결과 없음")
            return ""

    url = pumlink
    driver.get(url)
    # time.sleep(5)

    source = driver.page_source
    soup = bs(source, 'html.parser')

    translator = googletrans.Translator()

    try:
        title = soup.select('#content > div.movie_info_ditail > div.mv_title')[0].get_text()
        print("제목 : "+title)
        
        title = translator.translate(title, src='ja', dest='ko') #번역
        title = " " + replaceTxt(title.text) #수정
        print("수정 제목 : " + title)

    except Exception as e :
        print(e)
        print("제목 없음 ? 검색결과 없음")
        title =""

    try:
        actor = soup.select('#content > div.movie_info_ditail > div.mv_artist')[0].get_text()
        actor = actor.replace("（FC2動画）","")
        print("배우 : "+actor)

        actor1 = translator.translate(actor, src='ja', dest='ko') #번역
        actor1 = " #"+replaceTxt(actor1.text).replace(" ","_").replace("#","").replace("-","") #수정

        actor1 = actor1 + " " + actor
        print("수정 배우 :" + actor1)

    except Exception as e :
        print(e)
        print("배우명 없음")
        actor1 = ""

    try:
        createDate = soup.select('#content > div.movie_info_ditail > div.mv_createDate')[0].get_text()
        createDate = " ("+ createDate +")"
        print("날짜 : "+createDate)
    except Exception as e :
        print(e)
        print("날짜 없음")
        createDate = ""
    try :
        writer = soup.select('#content > div.movie_info_ditail > div.mv_writer')[0].get_text()
        print("제작자 : "+writer)

        writer1 = translator.translate(writer, src='ja', dest='ko') #번역
        writer1 = " #"+replaceTxt(writer1.text).replace("   ","_").replace("  ","_").replace(" ","_").replace("#","").replace("-","") #수정
        writer1 = writer1 + " " + writer
        
        print("수정 제작자 :" + writer1)

    except Exception as e :
        print(e)
        print("제작자 없음")
        writer1 = ""

    pumname = writer1 + actor1 + title + createDate 
    return pumname

def get_pumInfo_ama(pumnum):
    url = 'https://db.msin.jp/'
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.get(url)
    # time.sleep(5)

    inputBox = driver.find_element(By.ID,"mbox")
    inputBox.send_keys(pumnum)
    inputBox.submit()

    source = driver.page_source
    soup = bs(source, 'html.parser')
    
    try:
        title = soup.select('#content > div:nth-child(3) > div.mv_title')[0].get_text()
        print("제목 : " + title)
        
        translator = googletrans.Translator()
        title = translator.translate(title, src='ja', dest='ko') #번역
        title = " " + replaceTxt(title.text) #수정
        print("수정 제목 : " + title)
    except Exception as e:
        print(e)
        print("제목 없음 ? 검색결과 없음")
        createDate =""

    try:
        createDate = soup.select('#content > div:nth-child(3) > div.mv_createDate')[0].get_text()
        createDate = " ("+ createDate +")"
        print("날짜 : " + createDate)
    except Exception as e:
        print(e)
        print("날짜 없음")
        createDate =""


    try:
        actor = soup.select('#content > div:nth-child(3) > div.mv_artist > span > a')[0].get_text()
        print("배우 :" + actor)
        actor = translator.translate(actor, src='ja', dest='ko') #번역
        actor = " #"+replaceTxt(actor.text).replace(" ","_").replace("#","").replace("-","") #수정
        print("수정 배우 :" + actor)
    except Exception as e :
        print(e)
        print("배우명 없음")
        actor =""

    newName = actor + title +  createDate
    return newName




from pathlib import Path

import os
file_path = "I:\\가마우지\\0. 파일명정리중"
# file_path = "C:\\Users\\seokjong_2\\Desktop\\img\\음표"

def rename_file():
    for filename in os.listdir(file_path): #현재 위치 (.) 의 파일을 모두 가져온다
        name, ext = os.path.splitext(filename)
        print("파일명 : " + name + ", 확장자 : " + ext) 

        pumnum = name.split(" ")[0]  # " " 단위로 파일명 분리->품번 추출
        print("품번 : " + pumnum)
        if pumnum.upper() != "FC2-PPV" and pumnum.upper() != "FC2PPV": #fc2 파일 건너뛰기
            try:
                if len(pumnum.split("-")) < 3 :  #ABC 나눠진 파일 확인
                    pumname = get_pumInfo(pumnum)
                else :
                    pumname = get_pumInfo(pumnum[:-2])
                print("작품 제목 : "+pumname)

            except Exception as e:  #아마추어 품번일때
                print(e)
                print("ama : " + pumnum)
                try :
                    if len(pumnum.split("-")) < 3 :  #ABC 나눠진 파일 확인
                        pumname = get_pumInfo_ama(pumnum)
                    else :
                         pumname = get_pumInfo_ama(pumnum[:-2])
                except Exception as e: #검색안되면 스킵
                    print(e)
                    print("fail : " + pumnum)
                    continue
            #파일명 변경
            new_filename = pumnum + pumname + ext
            print("새파일명 : " + new_filename)
                
        elif pumnum.upper() == "FC2-PPV" or pumnum.upper() == "FC2PPV" : #fc2 파일일때
            pumnum = name.split(" ")[1]
            if pumnum[-2] == '_' or pumnum[-2] == '-': # -n 또는 _n 로 나눠진 파일일때
                pumname = get_pumInfo_fc2(pumnum[:-3])
            else:
                pumname = get_pumInfo_fc2(pumnum)

            #파일명 변경
            new_filename = "FC2-PPV "+ pumnum + pumname + ext
            print("새파일명 : " + new_filename)
        
        new_filename=replaceTxt(new_filename)
        print("수정된 새파일명 : " + new_filename)
        if len(new_filename) > 250 :
            new_filename = new_filename[:250] + ext

        file_oldname = os.path.join(file_path,filename)
        file_newname = os.path.join(file_path,new_filename)
        os.renames(file_oldname, file_newname) 
        print(pumnum + " 파일명 수정 완료!\n\n")    



# gtranslate()
# get_pumInfo_ama('261ARA-537')
# get_pumInfo_fc2('2941898')
rename_file()

