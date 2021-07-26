import requests
from bs4 import BeautifulSoup
import re

def search(area):
    session = requests.Session() 
    addr = "https://weather.naver.com/today/"
    map_cityNum = {     # 지역 번호 매핑
                '가평':"001001", '강화':"001002", '고양':"001003", '과천':'001004','광명':"001005" , 
                '광주시':"001006", '구리':"001007", '군포':"001008", '김포':"001009", '남양주':"001010",
                '동두천':"001011", '문산':"001035", '부천':"001012", '서울':"001013", '성남':'001014',
                '수원':"001015", '시흥':"001016", '신갈':"001034", '안산':"001017", '안성':'001018',
                '안양':"001019", '양주':"001020", '양평':"001021", '여주':"001036", '연천':"001022", 
                '오산':"001023", '용인':"001024", '의왕':"001025", '의정부':"001026", '이천':"001027", 
                '인천':"001028", '파주':"001029", '평택':"001030", '포천':"001031", '하남':"001032", '화성':"001033",

                '백령도':"002001", '소청도':"002002", '연평도':"002003",

                '양구':"003001", '영월':"003002", '원주':"003003", '인제':"003004", '정선':"003005", 
                '철원':"003006", '춘천':"003007", '평창':"003008", '홍천':"003009", '화천':"003010", 
                '횡계':"003012", '횡성':"003011",
                
                '강릉':"004001", '강원':"004002", '산간':"004003", '고성':"004004", '대관령':"004005", 
                '동해':"004006", '삼척':"004007", '새말':"004011", '속초':"004007", '양양':"004008", 
                '태백':"004009",

                '괴산':"005001", '남이':"005013", '단양':"005002", '보은':"005003", '영동':"005004", 
                '옥천':"005005", '음성':"005006", '제천':"005007", '증평':"005008", '진천':"005009", 
                '청원':"005014", '청주':"005010", '추풍령':"005011", '충주':"005012",

                '계룡':"006016", '공주':"006001", '금산':"006002", '논산':"006003", '당진':"006004", 
                '대전':"006005", '보령':"006006", '부여':"006007", '서산':"006008", '서천':"006009", 
                '세종':"006017", '아산':"006010", '예산':"006011", '천안':"006012", '청양':"006013", 
                '태안':"006014", '홍성':"006015",

                '경산':"007001", '경주':"007002", '고령':"007003", '구미':"007004", '군위':"007005", 
                '김천':"007006", '대구':"007007", '문경':"007008", '봉화':"007009", '상주':"007010", 
                '성주':"007011", '안동':"007012", '영덕':"007013", '영양':"007014", '영주':"007015", 
                '영천':"007016", '예천':"007017", '울진':"007018", '의성':"007019", '청도':"007020", 
                '청송':"007021", '칠곡':"007022", '포항':"007023",

                '거제':"008001", '거창':"008002", '고성':"008003", '김해':"008004", '남해':"008005", 
                '밀양':"008007", '부산':"008008", '사천':"008009", '산청':"008010", '서상':"008024", 
                '양산':"008011", '울산':"008012", '의령':"008013", '진주':"008014", '창녕':"008016", 
                '창원':"008017", '통영':"008018", '하동':"008019", '하동(내륙)':"008020", '함안':"008021", 
                '함양':"008022", '합천':"008023",

                '독도':"009001", '울릉도':"009002",

                '고창':"010001", '군산':"010002", '김제':"010003", '남원':"010004", '무주':"010005", 
                '부안':"010006", '순창':"010007", '완주':"010014", '익산':"010008", '임실':"010009", 
                '장수':"010010", '전주':"010011", '정읍':"010012", '진안':"010013",

                '강진':"011001", '고흥':"011002", '곡성':"011003", '광양':"011004", '광주광역시':"011005", 
                '구례':"011006", '나주':"011007", '담양':"011008", '목포':"011009", '무안':"011010", 
                '보성':"011011", '순천':"011012", '신안':"011013", '여수':"011014", '영광':"011015", 
                '영암':"011016", '완도':"011017", '장성':"011018", '장흥':"011019", '진도':"011020", 
                '함평':"011021", '해남':"011022", '화순':"011024", '흑산도':"011023",

                '고산':"012001", '서귀포':"012002", '성산포':"012003", '윗세오름':"012004", 
                '제주':"012005"
                }

    if area == "광주" :
        return ("광주 -> 광주시 or 광주광역시 로 검색해주세요")
    if map_cityNum.get(area) == None:
        return area + "는 도시 목록에 없습니다"
    else:
        cityNum = map_cityNum[area]
    addr = addr + cityNum

    session.encoding = 'utf-8'

    req = session.get(addr)
    soup = BeautifulSoup(req.text, "html.parser")
    table = soup.find(class_="card card_week")
    
    t_ary = list(table.stripped_strings)

    result = (
            "["+ area + " 날씨 검색 결과]\n"
            + "- 오늘(" + t_ary[24] + ")\n"
            + "\t강수확률 - 오전: " + t_ary[27] +" "+ add_emoji(t_ary[28]) + ", 오후: " + t_ary[31] +" "+ add_emoji(t_ary[32]) + "\n"
            + "\t최저기온: " + t_ary[34] + ", 최고기온: " + t_ary[37] +"\n"
            + "- 내일(" + t_ary[39] + ")\n"
            + "\t강수확률 - 오전: " + t_ary[42] +" "+ add_emoji(t_ary[43]) + ", 오후: " + t_ary[46] +" "+ add_emoji(t_ary[47]) + "\n"
            + "\t최저기온: " + t_ary[49] + ", 최고기온: " + t_ary[52] +"\n"
            )
    return result

def rainday(area):
    '''
    return txt
    '''
    cityNum =""
    session = requests.Session() 
    addr = "https://weather.naver.com/today/"
    map_cityNum = {     # 지역 번호 매핑
                '가평':"001001", '강화':"001002", '고양':"001003", '과천':'001004','광명':"001005" , 
                '광주시':"001006", '구리':"001007", '군포':"001008", '김포':"001009", '남양주':"001010",
                '동두천':"001011", '문산':"001035", '부천':"001012", '서울':"001013", '성남':'001014',
                '수원':"001015", '시흥':"001016", '신갈':"001034", '안산':"001017", '안성':'001018',
                '안양':"001019", '양주':"001020", '양평':"001021", '여주':"001036", '연천':"001022", 
                '오산':"001023", '용인':"001024", '의왕':"001025", '의정부':"001026", '이천':"001027", 
                '인천':"001028", '파주':"001029", '평택':"001030", '포천':"001031", '하남':"001032", '화성':"001033",

                '백령도':"002001", '소청도':"002002", '연평도':"002003",

                '양구':"003001", '영월':"003002", '원주':"003003", '인제':"003004", '정선':"003005", 
                '철원':"003006", '춘천':"003007", '평창':"003008", '홍천':"003009", '화천':"003010", 
                '횡계':"003012", '횡성':"003011",
                
                '강릉':"004001", '강원':"004002", '산간':"004003", '고성':"004004", '대관령':"004005", 
                '동해':"004006", '삼척':"004007", '새말':"004011", '속초':"004007", '양양':"004008", 
                '태백':"004009",

                '괴산':"005001", '남이':"005013", '단양':"005002", '보은':"005003", '영동':"005004", 
                '옥천':"005005", '음성':"005006", '제천':"005007", '증평':"005008", '진천':"005009", 
                '청원':"005014", '청주':"005010", '추풍령':"005011", '충주':"005012",

                '계룡':"006016", '공주':"006001", '금산':"006002", '논산':"006003", '당진':"006004", 
                '대전':"006005", '보령':"006006", '부여':"006007", '서산':"006008", '서천':"006009", 
                '세종':"006017", '아산':"006010", '예산':"006011", '천안':"006012", '청양':"006013", 
                '태안':"006014", '홍성':"006015",

                '경산':"007001", '경주':"007002", '고령':"007003", '구미':"007004", '군위':"007005", 
                '김천':"007006", '대구':"007007", '문경':"007008", '봉화':"007009", '상주':"007010", 
                '성주':"007011", '안동':"007012", '영덕':"007013", '영양':"007014", '영주':"007015", 
                '영천':"007016", '예천':"007017", '울진':"007018", '의성':"007019", '청도':"007020", 
                '청송':"007021", '칠곡':"007022", '포항':"007023",

                '거제':"008001", '거창':"008002", '고성':"008003", '김해':"008004", '남해':"008005", 
                '밀양':"008007", '부산':"008008", '사천':"008009", '산청':"008010", '서상':"008024", 
                '양산':"008011", '울산':"008012", '의령':"008013", '진주':"008014", '창녕':"008016", 
                '창원':"008017", '통영':"008018", '하동':"008019", '하동(내륙)':"008020", '함안':"008021", 
                '함양':"008022", '합천':"008023",

                '독도':"009001", '울릉도':"009002",

                '고창':"010001", '군산':"010002", '김제':"010003", '남원':"010004", '무주':"010005", 
                '부안':"010006", '순창':"010007", '완주':"010014", '익산':"010008", '임실':"010009", 
                '장수':"010010", '전주':"010011", '정읍':"010012", '진안':"010013",

                '강진':"011001", '고흥':"011002", '곡성':"011003", '광양':"011004", '광주광역시':"011005", 
                '구례':"011006", '나주':"011007", '담양':"011008", '목포':"011009", '무안':"011010", 
                '보성':"011011", '순천':"011012", '신안':"011013", '여수':"011014", '영광':"011015", 
                '영암':"011016", '완도':"011017", '장성':"011018", '장흥':"011019", '진도':"011020", 
                '함평':"011021", '해남':"011022", '화순':"011024", '흑산도':"011023",

                '고산':"012001", '서귀포':"012002", '성산포':"012003", '윗세오름':"012004", 
                '제주':"012005"
                }

    if area == "광주" :
        return ("광주 -> 광주시 or 광주광역시 로 검색해주세요")
    if map_cityNum.get(area) == None:
        return area + "는 도시 목록에 없습니다"
    else:
        cityNum = map_cityNum[area]

    addr = addr + cityNum

    session.encoding = 'utf-8'

    req = session.get(addr)
    soup = BeautifulSoup(req.text, "html.parser")
    table = soup.find(class_="card card_week")
    
    t_ary = list(table.stripped_strings)
    # ☀️ 맑음 🌤 ⛅️ 구름많음 🌥☁️ 흐림 🌦 구름많고 비 🌧 비 ⛈ 번개비 🌩 번개 🌨 ❄️눈


    tmp = ""
    for i in range(len(t_ary)):
        if t_ary[i].find("비") >= 0 :
            if t_ary[i-3] == "오후":
                tmp += (t_ary[i-8]  +"(" + t_ary[i-9]+ ") 오후 강수확률: " + t_ary[i-1] + " " + add_emoji(t_ary[i]) +"\n")
            elif t_ary[i-3] == "오전":
                tmp += (t_ary[i-5] +"(" + t_ary[i-4]+ ") 오전 강수확률: " + t_ary[i-1] + " " + add_emoji(t_ary[i]) +"\n")

    return tmp
    
def add_emoji(txt):
    if txt == "맑음":
        return txt+" ☀️"
    elif txt == "구름많음":
        return txt+ " ⛅️"
    elif txt == "흐림":
        return txt+ " ☁️"
    elif txt == "구름많고 비":
        return txt+ " 🌦"
    elif txt == "비":
        return txt+ " 🌧"
    elif txt == "번개비":
        return txt+ " ⛈"
    elif txt == "번개":
        return txt+ " 🌩"
    elif txt == "눈":
        return txt+ " ❄️"

def temperature():
    URL = requests.get("https://hangang.ivlis.kr/aapi.php?type=dgr")
    data = BeautifulSoup(URL.content, 'html.parser')
    
    return data.get_text().replace("â„ƒ","℃")
    

def wise_saying():
    URL= requests.get("https://hangang.ivlis.kr/aapi.php?type=text")
    data = BeautifulSoup(URL.content, 'html.parser')
    return data.get_text()