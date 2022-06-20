'''
https://pypi.org/project/dart-fss/

# 대한민국 금융감독원에서 운영하는 다트(DART) 사이트 크롤링 및 재무제표 추출을 위한 라이브러리
Source code: https://github.com/josw123/dart-fss

# 설치
pip install dart-fss
'''

# import dart_fss as dartf

# # Open DART API KEY 설정 : https://opendart.fss.or.kr/mng/apiUsageStatusView.do
# api_key='ee8c813e13cb41b2ae48596020ea4d8e444bc11e'
# dartf.set_api_key(api_key=api_key)


# # DART 에 공시된 회사 리스트 불러오기
# corp_list = dartf.get_corp_list()

# # 삼성전자 검색
# samsung = corp_list.find_by_corp_name('삼성전자', exactly=True)[0]

# # 2012년부터 연간 연결재무제표 불러오기
# fs = samsung.extract_fs(bgn_de='20210101')


# # 재무제표 검색 결과를 엑셀파일로 저장 ( 기본저장위치: 실행폴더/fsdata )
# fs.save()

#////////////////////////////////////////////////////////////////////////////////////

'''
OpenDartReader
https://github.com/FinanceData/OpenDartReader

pip install opendartreader
pip install --upgrade opendartreader 

'''

# import OpenDartReader

# ==== 0. 객체 생성 ====
# 객체 생성 (API KEY 지정) 
# api_key = 'ee8c813e13cb41b2ae48596020ea4d8e444bc11e'

# dart = OpenDartReader(api_key) 

# dart.find_by_name()


# 3분기보고서 : 11014
# 반기보고서 : 11012
# 1분기보고서 : 11013
# 사업보고서 : 11011

# # == 1. 공시정보 검색 ==
# # 삼성전자 2019-07-01 하루 동안 공시 목록 (날짜에 다양한 포맷이 가능합니다)
# dart.list('005930', end='2019-7-1')


# # 삼성전자 상장이후 모든 공시 목록 (5,142 건+)
# print(dart.list('005930', start='1900') )

# # 삼성전자 2010-01-01 ~ 2019-12-31 모든 공시 목록 (2,676 건)
# dart.list('005930', start='2010-01-01', end='2019-12-31') 

# # 삼성전자 1999-01-01 이후 모든 정기보고서
# dart.list('005930', start='1999-01-01', kind='A', final=False)

# # 삼성전자 1999년~2019년 모든 정기보고서(최종보고서)
# kind: 보고서 종류:  A=정기공시, B=주요사항보고, C=발행공시, D=지분공시, E=기타공시, 
#                                         F=외부감사관련, G=펀드공시, H=자산유동화, I=거래소공시, J=공정위공시
# dl = dart.list('005930', start='2010-01-01', end='2022-12-31', kind='I')
# dl = dl[dl['report_nm'].str.contains('연결재무')]
# dl = dl[~dl['report_nm'].str.contains('기재정정')]
# dl = dl[['corp_name','stock_code','report_nm','rcept_no']]
# print(dl)

# # 2020-07-01 하루동안 모든 공시목록
# dart.list(end='20200701')

# # 2020-01-01 ~ 2020-01-10 모든 회사의 모든 공시목록 (4,209 건)
# dart.list(start='2020-01-01', end='2020-01-10')

# # 2020-01-01 ~ 2020-01-10 모든 회사의 모든 공시목록 (정정된 공시포함) (4,876 건)
# dart.list(start='2020-01-01', end='2020-01-10', final=False)

# # 2020-07-01 부터 현재까지 모든 회사의 정기보고서
# dart.list(start='2020-07-01', kind='A')

# # 2019-01-01 ~ 2019-03-31 모든 회사의 정기보고서 (961건)
# dart.list(start='20190101', end='20190331', kind='A')

# # 기업의 개황정보
# print(dart.company('005930'))

# # 회사명에 삼성전자가 포함된 회사들에 대한 개황정보
# dart.company_by_name('삼성전자')

# # 삼성전자 사업보고서 (2018.12) 원문 텍스트
# xml_text = dart.document('20190401004781')
# print(xml_text)


# # ==== 2. 사업보고서 ====
# # 삼성전자(005930), 배당관련 사항, 2018년
# print(dart.report('005930', '배당', 2020) )

# # 삼성전자(005930), 주식총수 사항, 2018년
# print(dart.report('005930', '주식총수', 2020) )
# istc_totqy : 발행주식 총수 , distb_stock_co : 유통주식 총수

# # 서울반도체(046890), 최대주주 관한 사항, 2018년
# dart.report('046890', '최대주주', 2018) 

# # 서울반도체(046890), 임원 관한 사항, 2018년
# dart.report('046890', '임원', 2018) 

# # 삼성바이오로직스(207940), 2019년, 소액주주에 관한 사항
# dart.report('207940', '소액주주', '2019')


# # ==== 3. 상장기업 재무정보 ====
# # 삼성전자 2018 재무제표 
# dart.finstate('삼성전자', 2018) # 사업보고서

# # 삼성전자 2018Q1 재무제표
# df = dart.finstate('삼성전자', 2020, reprt_code='11011')
# print(df[['bsns_year','thstrm_nm','fs_nm','sj_nm','account_nm','thstrm_amount']])

# # 여러종목 한번에
# dart.finstate('00126380,00164779,00164742', 2018)
# dart.finstate('005930, 000660, 005380', 2018)
# dart.finstate('삼성전자, SK하이닉스, 현대자동차', 2018)

# # 단일기업 전체 재무제표 (삼성전자 2018 전체 재무제표)
# dart.finstate_all('005930', 2018)

# # 재무제표 XBRL 원본 파일 저장 (삼성전자 2018 사업보고서)
# dart.finstate_xml('20190401004781', save_as='삼성전자_2018_사업보고서_XBRL.zip')

# # XBRL 표준계정과목체계(계정과목)
# dart.xbrl_taxonomy('BS1')


# # ==== 4. 지분공시 ====
# # 대량보유 상황보고 (종목코드, 종목명, 고유번호 모두 지정 가능)
# dart.major_shareholders('삼성전자')

# # 임원ㆍ주요주주 소유보고 (종목코드, 종목명, 고유번호 모두 지정 가능)
# dart.major_shareholders_exec('005930')


# # ==== 5. 확장 기능 ====
# # 지정한 날짜의 공시목록 전체 (시간 정보 포함)
# dl = dart.list_date_ex('2020-01-03')
# print(dl)

# # 개별 문서 제목과 URL
# rcp_no = '20190401004781' # 삼성전자 2018년 사업보고서

# for i in dl['rcept_no']:
#     s = dart.sub_docs(i)['url']


# # 제목이 잘 매치되는 순서로 소트
# ds = dart.sub_docs('20190401004781', match='사업의 내용')
# print(ds)

# # 첨부 문서 제목과 URL
# dart.attach_doc_list(rcp_no)

# # 제목이 잘 매치되는 순서로 소트
# da = dart.attach_doc_list('20190401004781', match='감사보고서')
# print(da)

# # 첨부 파일 제목과 URL
# dart.attach_file_list(rcp_no)


'''
 특정 문자를 포함하는 행, 특정 조건에 해당하는 행 추출
 
 'w' 문자 포함하는 행 삭제  
 test_df = test_df[~test_df['contents'].str.contains('w')]

 'w' 문자 포함하는 행만 추출
 test_df = test_df[test_df['contents'].str.contains('w')]

 인덱스 초기화
 test_df.reset_index(drop=True, inplace=True)
 
'''

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import requests
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
네이버증권  https://finance.naver.com/item/coinfo.naver?code=005930
'''

from urllib import parse 
import pandas as pd 

def get_fnguide(code) : 
    '''
    [0] : 시세현황
    [1] : 실적이슈
    [2] : 운용사별 보유 현황
    [3] : 주주현황
    [4] : 주주구분 현황
    [5] : 신용등급현황 기업어음 (CP)
    [6] : 신용등급현황 회사채(Bond)
    [7] : 투자의견 컨센서스
    [8] : 업종 비교 (연결)
    [9] : 업종 비교 (별도)
    [10] : Financial Highlight (전체)
    [11] : Financial Highlight (연간)
    [12] : Financial Highlight (분기)
    '''
    get_param = { 
        'pGB':1, 
        'gicode':'A%s'%(code), 
        'cID':'', 
        'MenuYn':'Y', 
        'ReportGB':'', 
        'NewMenuID':101, 
        'stkGb':701, } 
    get_param = parse.urlencode(get_param) 

    url="http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?%s"%(get_param) 
    tables = pd.read_html(url, header=0) 
    return(tables) 

def get_stock_data(code, want):
'''
want : "발행주식수", "전일종가"
'''

    '''
            종가/ 전일대비                75,000/ +200            거래량             13,605,382
0         52주.최고가/ 최저가              86,000/ 68,800       거래대금(억원)                  10220        
1       수익률(1M/ 3M/ 6M/ 1Y)  -3.23/ +6.08/ +1.08/ -9.86       외국인 보유비중                  52.24
2      시가총액(상장예정포함,억원)                     5036077         베타(1년)                0.96299      
3         시가총액(보통주,억원)                     4477337            액면가                    100
4                  NaN                         NaN            NaN                    NaN
5      발행주식수(보통주/ 우선주)  5,969,782,550/ 822,886,700  유동주식수/비율(보통주)  4,460,370,393 / 74.72
    '''
    data = get_fnguide(code)[0]

    if want == "발행주식수":
        shareOfIssued = data.iloc[5][1].split('/')[0].replace(',','')
        print(shareOfIssued)
        return int(shareOfIssued)
    elif want == "전일종가":
        pricePre = data.columns[1].split('/')[0].replace(',','')
        return(int(pricePre))

get_stock_data('005930', "발행주식수")



def stock_DiscountRate(dy, rrr): 
    '''
    할인률 계산
    '''
    if dy < 1 : return rrr
    elif dy < 2 : return rrr-0.2
    elif dy < 3 : return rrr-0.4
    elif dy < 4 : return rrr-0.6
    elif dy < 5 : return rrr-0.8
    else: return rrr-1    

def send_stock_inform(code):
    # stockName = name # 주식이름
    stockCode = code # 주식코드
    stockBusinessType = ""
    stockPriceNow = 0 # 현재가격
    stockPricePre = get_stock_data(code, "전일종가") # 전일종가
    stockRateOfIncrease =  ((stockPriceNow/stockPricePre)-1)*100 #전일비 등락률
    stockNumOfSharesIssued = get_stock_data(code, "발행주식수") # 총발행 주식수
    stockNumOfSharesDistributed = 0 # 유통 주식수
    stockMarketCap = stockNumOfSharesIssued*stockPriceNow # 시가총액
    stockTotalCap = 0 # 자본총계(지배)
    stockYearSales = 0 # 1년 매출
    stockYearOperatingProfit = 0 #1년 영업이익
    stockYearNetProfit = 0 # 1년 순이익
    stockBPS = stockTotalCap/stockNumOfSharesDistributed # 주당순자산가치
    stockCapMagnification = stockBPS/stockPriceNow # 자본배율 : BPS 역수
    stockEPS = stockYearNetProfit/stockNumOfSharesIssued # 주당순이익
    stockROE = stockEPS/stockBPS*100 # 자기자본이익률
    stockDPS = 0 # 주당배당금
    stockDividendYield = stockDPS/stockPriceNow*100 # 주당배당률
    stockRRR = 7.5 # Requested rate of return
    stockDiscountRate = stock_DiscountRate(stockDividendYield, stockRRR) # 할인률 R
    stockROER = stockROE/stockDiscountRate # ROE/R
    stockRightPriceROE = stockPriceNow*stockROER # ROE 적정주가
    stockPER = stockPriceNow/stockEPS # 주가수익률
    stockBusinessTypePER = 0 # 업종PER
    stockRightPricePER = stockPriceNow*stockBusinessTypePER/stockPER # PER 적정주가
    stockPBR = stockPriceNow/stockBPS # 주가순자산비율
    stockBusinessTypePBR = 0 # 업종PBR
    stockRightPricePBR = stockPriceNow*stockBusinessTypePBR/stockPBR # PBR 적정주가
    


