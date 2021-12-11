
# 한입에 웹크롤링 (BJ Public 출판, 김경록, 서영덕 지음) 책 참조

from urllib.request import urlopen
import json

import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import matplotlib.font_manager as fm
from matplotlib import rc

def RSI(df, period=14):
    df['U'] = np.where(df['Day_ConfirmN'].diff(1) > 0, df['Day_ConfirmN'].diff(1), 0)  # df.diff(1) : 기준일 종가 - 전일 종가, 0보다 크면 증가분을, 아니면 0을 넣음
    df['D'] = np.where(df['Day_ConfirmN'].diff(1) < 0, df['Day_ConfirmN'].diff(1)*(-1), 0) # 기준일 종가 - 전일 종가, 0보다 작으면 감소분을, 아니면 0을 넣음
    df['AU'] = df['U'].rolling(window=period).mean() # period=14 동안의 U의 (이동)평균
    df['AD'] = df['D'].rolling(window=period).mean() # period=14 동안의 D의 (이동)평균
    df['RSI'] = df['AU'] / (df['AD']+df['AU']) * 100
    return df

def MACD(df, short=12, long=26, signal=9):
    df['MACD']=df['Day_ConfirmN'].ewm( span=short, min_periods= long-1, adjust=False).mean() - df['Day_ConfirmN'].ewm( span=long, min_periods=long-1, adjust=False).mean()
    df['MACD_Signal'] = df['MACD'].ewm( span = signal, min_periods=signal-1, adjust=False).mean()
    df['MACD_OSC'] = df["MACD"] - df['MACD_Signal']
    return df

def fnBolingerBand(m_DF, n=20, k=2):
    # .rolling(window=20).mean()
    m_DF['20_ma'] = m_DF['Day_ConfirmN'].rolling(window=n).mean()  
    m_DF['bol_upper'] = m_DF['Day_ConfirmN'].rolling(window=n).mean() + k* m_DF['Day_ConfirmN'].rolling(window=n).std()
    m_DF['bol_lower'] = m_DF['Day_ConfirmN'].rolling(window=n).mean() - k* m_DF['Day_ConfirmN'].rolling(window=n).std()
    return m_DF


def main():
    # 한글 출력용 폰트 지정
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = fm.FontProperties(fname=path).get_name()
    rc('font', family=font_name)

    url = 'https://m.search.naver.com/p/csearch/content/nqapirender.nhn?where=nexearch&pkid=9005&key=accV2API'

    html = urlopen(url) # urllib로 html 가져오기
    # print(html.read())

    json_obj = json.load(html)
    # print(json_obj)
    
    dat_confirmed = json_obj['result']['emphasis'][0]['data']
    # print(dat_confirmed[-5:])

    dat_recovered = json_obj['result']['emphasis'][1]['data']
    # print(dat_recovered)
    
    dat_date = json_obj['result']['xAxis']
    # print(dat_date[-5:])

    dat_update = json_obj['result']['updatetime']

    # Pandas dataframe 변수에 담고 가공하기
    colList = list(zip(dat_date, dat_confirmed, dat_recovered))
    
    COVIDdf = pd.DataFrame(colList, columns = ['Date','AccuConfirm','AccuRecover'])
    # print(COVIDdf)

    # object형 데이터 콤마 없애고 정수화, 날짜 / 구분
    COVIDdf['AccuConfirmN'] = COVIDdf['AccuConfirm'].str.replace(',', '').astype(int)  # 누적확진자
    COVIDdf['AccuRecoverN'] = COVIDdf['AccuRecover'].str.replace(',', '').astype(int)  # 누적격리해제

    COVIDdf['Date'] = COVIDdf['Date'].str.replace('.', '/')
   
    # print(COVIDdf.dtypes)

    COVIDdf['Day_ConfirmN'] = COVIDdf['AccuConfirmN'].diff()    # 신규확진
    # COVIDdf['AccuValidConfN'] = COVIDdf['AccuConfirmN'] - COVIDdf['AccuRecoverN']
    # COVIDdf.set_index('Date', inplace=True)
    # print(COVIDdf.tail(10))
    COVIDdf['Day_ConfirmN'].iloc[0] = 0

    # 이동 평균 데이터 구하기 
    COVIDdf['ma7'] = COVIDdf['Day_ConfirmN'].rolling(window=7).mean()
    COVIDdf['ma30'] = COVIDdf['Day_ConfirmN'].rolling(window=30).mean()
    COVIDdf['ma90'] = COVIDdf['Day_ConfirmN'].rolling(window=90).mean()


    # RSI, MACD 구하기
    COVIDdf = RSI(COVIDdf)    # RSI
    COVIDdf = MACD(COVIDdf)   # MACD, MACD_signal, MACD_OSC
    COVIDdf = fnBolingerBand(COVIDdf) # bol_upper, 20_ma, bol_lower

    print(COVIDdf)



    COVIDdf.to_csv('Cases_Korea_'+dat_update[:10]+'.csv', index=False)






    # 그래프 그리기
    plt.figure(figsize=(12,8))
    
    pr_line = plt.subplot2grid((4,4), (0,0), rowspan=4, colspan=4)

    x_ym = np.arange(len(COVIDdf.index))

    pr_line.scatter(x_ym, COVIDdf['Day_ConfirmN'], s=5, c='black', label='확진자수')

    # pr_line.plot(x_ym, COVIDdf['ma7'], lw=1.5, c = 'orange', label='7일 이동평균선')
    # pr_line.plot(x_ym, COVIDdf['ma30'], lw=1.5, c = 'limegreen', label='30일 이동평균선')
    # pr_line.plot(x_ym, COVIDdf['ma90'], lw=1.5, c = 'violet', label='90일 이동평균선')
    pr_line.plot(x_ym, COVIDdf['bol_upper'], lw=1.5, c = 'red', label='볼밴상한')
    pr_line.plot(x_ym, COVIDdf['bol_lower'], lw=1.5, c = 'blue', label='볼밴하한')
    pr_line.plot(x_ym, COVIDdf['20_ma'], lw=1.5, c = 'orange', label='20일선')


    pr_line.set_xticks(x_ym)
    pr_line.set_xticklabels(COVIDdf['Date'], rotation=60, fontsize=10)

    every_nth = 10
    start = len(x_ym) % every_nth - 1
    if start < 0:
        start = every_nth - 1
                
    for n, label in enumerate(pr_line.xaxis.get_ticklabels()):
        #print('n: ', n, 'label', label)
        if (n - start) % every_nth != 0:
            label.set_visible(False)
            
    ##    pr_line.bar(x_ym, height=COVIDdf['Day_ConfirmN'], \
    ##        bottom = 0, width = 0.5, color='dodgerblue')
    
    # 그래프 x, y 범위 설정
    ##    pr_line.xlim(-5, 910)
    ##    pr_line.ylim(-1, 46)
    
    # plt.xticks(xData, ['{}'.format(i+1) for i in range(905)])
    plt.ylabel('확진자수 (명)', fontsize=18)
    plt.xlabel('날짜', fontsize=18)
    plt.grid(axis='y')
    plt.legend()
    plt.show()

    
# main 함수 로딩부
if __name__ == '__main__':
    main()

