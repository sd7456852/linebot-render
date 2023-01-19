from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import json,requests,re

app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('+WddPIOMZ56D7Tre1fmARy1z1eiZGJ5uJEQut/9vq1O6LsM+6hFBHugc/fwD1+HF/KwMEVqQWz1/4ef/4PMhkPWCA7TZXZVwdqB5dZIelMnkukmZL744cTBSBoW1Ua0aCYI94OidHv+wH4uBVJI36QdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('e97792d24f1f087c95eec15736713fcd')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
cities = ['基隆市','嘉義市','臺北市','嘉義縣','新北市','臺南市','桃園縣','高雄市','新竹市','屏東縣','新竹縣','臺東縣','苗栗縣','花蓮縣','臺中市','宜蘭縣','彰化縣','澎湖縣','南投縣','金門縣','雲林縣','連江縣']

def get(city):
    token = 'CWB-CBE7DA58-A77F-45FD-9847-11C428FF256B'
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=' + str(city)
    Data = requests.get(url)
    Data = (json.loads(Data.text,encoding='utf-8'))['records']['location'][0]['weatherElement']
    res = [[] , [], []]
    for j in range(3):
        for i in Data:
            res[j].append(i['time'][j])
    return res

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    if(message[:2] == '天氣'):
        city = message[3:]
        city = city.replace('台','臺')
        if(not (city in cities)):
            line_bot_api.reply_message(reply_token,TextSendMessage(text="查詢格式為: 天氣 縣市"))
        else:
            res = get(city)
            line_bot_api.reply_message(reply_token, TemplateSendMessage(
                alt_text = city + '未來 36 小時天氣預測',
                template = CarouselTemplate(
                    columns = [
                        CarouselColumn(
                            thumbnail_image_url = 'https://i.imgur.com/Ex3Opfo.png',
                            title = '{} ~ {}'.format(data[0]['startTime'][5:-3],data[0]['endTime'][10:-3]),
                            text = '天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {}'.format(data[0]['parameter']['parameterName'],data[2]['parameter']['parameterName'],data[4]['parameter']['parameterName'],data[1]['parameter']['parameterName']),
                            actions = [
                                URIAction(
                                    label = '詳細內容',
                                    uri = 'https://www.cwb.gov.tw/V8/C/W/County/index.html'
                                )
                            ]
                        )for data in res
                    ]
                )
            ))
    elif re.match('台北',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('至善公園(室外)\n時間:星期二、四18:30~22:00\n星期六、日14:00~18:00\n聯絡人:劉恆智 02-28952365\n地圖:https://goo.gl/maps/bF2JFn6Vr391DHvq8 \n\n北投捷運會館(室內、限會員)\n時間:星期一、五12:00-15:00\n聯絡人:劉恆智 02-28952365\n地圖:https://goo.gl/maps/L6xjkG1oeWTHe2Yg8 \n\n萬華運動中心(室內)\n時間:星期三16:00-18:00\n聯絡人:劉恆智 02-28952365\n地圖:https://goo.gl/maps/AnRo1qYiGruPm5Pn9 \n\n北投運動中心(室內)\n時間:星期六16:00-18:00\n聯絡人:劉恆智 02-28952365\n地圖:https://goo.gl/maps/Dg2eQPAjNhkgeNLo7'))
    elif re.match('新北',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('五股公民會館(室內)\n時間:星期三、五17:30~21:30\n聯絡人:\n地圖:https://goo.gl/maps/vTNGexS9mXZ5469i8 \n\n新莊運動中心(室內、限會員)\n時間:星期四13:00~16:00\n聯絡人:\n地圖:https://goo.gl/maps/hAFTcZjZzZDuPUwv8'))
    elif re.match('桃園',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('元智大學體育館(室內)\n時間:星期六、日9:00~12:00 13:00~16:00\n聯絡人:梁鳳紋0934353010\n地圖:https://goo.gl/maps/BkPPwCGDxaTVVun48'))
    elif re.match('新竹',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('目前尚無場地'))
    elif re.match('台中',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('台中網球中心(室外)\n時間:星期一、星期三19:00~21:00\n費用:零打130\n聯絡人:中華民國匹克球協會 04-22395351\n地圖:https://goo.gl/maps/dBqGFVxX5XwtUAZx5 \nLINE群組：國際網球中心匹克球 http://line.me/ti/g/y2HUGPU7Qa \n\n舊社公園(室外)\n時間:星期一18:30\n星期日下午14:00\n聯絡人:張乃祥 0989103115\n地圖: https://goo.gl/maps/WcZ2ATFh4mqWET32A \n\n迷你網球場(室外)\n時間:禮拜二19;30\n聯絡人:\n 地圖:https://goo.gl/maps/AEKh9pzacH6S9pFe7 \n\n潭子國民暨兒童運動中心(室內)\n時間:星期一、三9:00～11:00\n星期五10:00～12:00\n聯絡人:魏彩玲志工 0926800571 孫維孝 0980009787\n地圖:https://goo.gl/maps/qtjaDxh7jQX88NPf9 \n\n台中長春國民運動中心(室內)\n時間:星期二20:00~22:00\n聯絡人:袁明馗 0939896878(周二周六) 張道統 0928337285(週三)\n地圖:https://goo.gl/maps/S1Bd825izHxrWf5C7'))
    elif re.match('彰化',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('秀水籃球場(室外)\n時間:星期一、三、五19:00\n地圖:https://goo.gl/maps/aFjkM8yXDbotN7FE6\n\n'))
    elif re.match('南投',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('埔里鎮立綜合球場(室外)\n時間:星期一~五16:00~20:00\n聯絡人:張永昌 0983711749\n地圖:https://goo.gl/maps/9d5UfW3KTyNYpmaW8'))
    elif re.match('嘉義',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('嘉義高工(室內)\n時間:星期一~五16:00~20:00(例假日須提前約)\n聯絡人:曾建儒 0953915400\n地圖:https://goo.gl/maps/57gsNKoB4ezCA3uT8'))
    elif re.match('台南',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('台南華府球場(室外)\n時間:每日8:00~11:00:、16:00~20:00\n聯絡人:孫維孝 0980009787 陳瑜申 0933909722 郭建宏 0919789200\n地圖:https://goo.gl/maps/FG6xaeU4XUm4aVqF7\n\n'))
    elif re.match('高雄',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('正勤活動中心(室內)\n時間:星期一、三17:00~20:00\n聯絡人:魏法徵0920429026\n地圖: https://goo.gl/maps/FgYJuLpaX2FMPm5K6 \n\n輔仁路匹克球場(室外)\n時間:每天18:00~21:00(下雨取消)\n聯絡人:楊典霖0987510990\n地圖:https://goo.gl/maps/GKbjnvnGAsk1XzZ4A'))
    elif re.match('屏東',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('屏東復興球場(室外)\n時間:每日18:30-21:30(有人數限制，需事先報名)\n聯絡人:楊敏宏 0927112880 張凱翔 0930313093\n地圖:https://goo.gl/maps/vdYBapaYQonxzNeD9 \n\n內埔國小操場旁(室外)\n時間:每天6:00～7:00點\n週六、日6:00~9:00(下午則會員會自行邀約)\n聯絡人:\n地圖:https://goo.gl/maps/Yxscyo7HZg7RaM259'))

    elif re.match('請輸入地區 例:台中',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('')) 
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('查詢場地請輸入 例:台中 高雄\n查詢天氣請輸入 例:天氣 台中市'))
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)    