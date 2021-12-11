# rest api access token : 
KAKAO_TOKEN = "JP0Mi3_sG5CHYmZmi0G3qmaducQuGcnU6LiUqQo9dRoAAAF6qnpCKw"


import os
import json
import requests

def sendToMeMessage(text):
    header = {"Authorization": 'Bearer ' + KAKAO_TOKEN}

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send" #나에게 보내기 주소

    #데이터 형식
    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    }
    data = {"template_object": json.dumps(post)}   # 데이터는 제이슨으로 변환해서 보내야함
    return requests.post(url, headers=header, data=data)

text = "Hello, This is KaKao Message Test!!("+os.path.basename(__file__).replace(".py", ")")


print(sendToMeMessage(text).text)