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
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('+WddPIOMZ56D7Tre1fmARy1z1eiZGJ5uJEQut/9vq1O6LsM+6hFBHugc/fwD1+HF/KwMEVqQWz1/4ef/4PMhkPWCA7TZXZVwdqB5dZIelMnkukmZL744cTBSBoW1Ua0aCYI94OidHv+wH4uBVJI36QdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('e97792d24f1f087c95eec15736713fcd')

# line_bot_api.push_message('U8d188af1584c5e78ab310184099a1bf5', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
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
    res = [[] , [] , []]
    for j in range(3):
        for i in Data:
            res[j].append(i['time'][j])
    return res


#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = text=event.message.text
    
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
                            title = '{} ~ {}'.format(res[0][0]['startTime'][5:-3],res[0][0]['endTime'][5:-3]),
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
        line_bot_api.reply_message(event.reply_token,TextSendMessage('北投捷運會館(限會員)\n時間:星期一、五12:00-15:00\n聯絡人:\n地圖:https://goo.gl/maps/L6xjkG1oeWTHe2Yg8\n\n 萬華運動中心\n時間:星期三下午4:00-6:00\n聯絡人:\n地圖:https://goo.gl/maps/AnRo1qYiGruPm5Pn9 \n\n五股公民會館\n時間:星期三、五晚上5:30-9:30\n聯絡人:\n地圖:https://goo.gl/maps/vTNGexS9mXZ5469i8 \n\n新莊運動中心(限會員)\n時間:星期四下午1:00-4:00\n聯絡人:\n地圖:https://goo.gl/maps/hAFTcZjZzZDuPUwv8 \n\n北投運動中心\n時間:星期六下午4:00-6:00\n聯絡人:\n地圖:https://goo.gl/maps/Dg2eQPAjNhkgeNLo7 '))
    elif re.match('新北',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('北投捷運會館(限會員)\n時間:星期一、五12:00-15:00\n聯絡人:\n地圖:https://goo.gl/maps/L6xjkG1oeWTHe2Yg8\n\n 萬華運動中心\n時間:星期三下午4:00-6:00\n聯絡人:\n地圖:https://goo.gl/maps/AnRo1qYiGruPm5Pn9 \n\n五股公民會館\n時間:星期三、五晚上5:30-9:30\n聯絡人:\n地圖:https://goo.gl/maps/vTNGexS9mXZ5469i8 \n\n新莊運動中心(限會員)\n時間:星期四下午1:00-4:00\n聯絡人:\n地圖:https://goo.gl/maps/hAFTcZjZzZDuPUwv8 \n\n北投運動中心\n時間:星期六下午4:00-6:00\n聯絡人:\n地圖:https://goo.gl/maps/Dg2eQPAjNhkgeNLo7 '))
    elif re.match('桃園',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('元智大學體育館(室內)\n時間:星期六、日\n早上9:00-12:00 下午1:00-4:00\n聯絡人:梁鳳紋0934353010\n地圖:https://goo.gl/maps/BkPPwCGDxaTVVun48'))
    elif re.match('新竹',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('\n時間:\n聯絡人:\n地圖:\nLINE群組：\n\n'))
    elif re.match('台中',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('台中網球中心\n時間:星期一、星期三\n晚上7:00~9:00\n費用:零打130\n聯絡人:\n地圖:https://goo.gl/maps/dBqGFVxX5XwtUAZx5 \nLINE群組：國際網球中心匹克球 http://line.me/ti/g/y2HUGPU7Qa \n\n舊社公園\n時間:星期一晚上6:30\n星期日下午2:00\n聯絡人:\n地圖: https://goo.gl/maps/WcZ2ATFh4mqWET32A \n\n迷你網球場\n時間:禮拜二晚上7;30\n聯絡人:\n 地圖:https://goo.gl/maps/AEKh9pzacH6S9pFe7'))
    elif re.match('彰化',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('秀水籃球場\n時間:星期一、三、五晚上7:00\n地圖:https://goo.gl/maps/aFjkM8yXDbotN7FE6\n\n'))
    elif re.match('南投',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('埔里鎮立綜合球場\n時間:星期一~五下午4:00~8:00\n聯絡人:張永昌 0983711749\n地圖:https://goo.gl/maps/9d5UfW3KTyNYpmaW8'))
    elif re.match('嘉義',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('嘉義高工\n時間:星期一~五下午4:00-晚上8:00(例假日須提前約)\n聯絡人:曾建儒 0953915400\n地圖:https://goo.gl/maps/57gsNKoB4ezCA3uT8'))
    elif re.match('台南',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('\n時間:\n聯絡人:\n地圖:\nLINE群組：\n\n'))
    elif re.match('高雄',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('正勤活動中心\n時間:星期一、三晚上5:00~8:00\n聯絡人:魏法徵0920429026\n地圖: https://goo.gl/maps/FgYJuLpaX2FMPm5K6 \n\n輔仁路匹克球場\n時間:每天晚上6:00~9:00(下雨取消)\n聯絡人:楊典霖0987510990\n地圖:https://goo.gl/maps/GKbjnvnGAsk1XzZ4A'))
    elif re.match('屏東',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('內埔國小操場旁\n時間:每天早上6點～7點\n週六、日可到9點\n下午則會員會自行邀約\n聯絡人:\n地圖:https://goo.gl/maps/Yxscyo7HZg7RaM259'))

    elif re.match('請輸入地區 例:台中',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(''))        
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('查詢場地請輸入 例:台中 高雄\n查詢天氣請輸入 例:天氣 台中 或傳送地標'))


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
# -*- coding: utf-8 -*-
# """
# Created on Wed Jun  2 21:16:35 2021

# @author: Ivan
# 版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

# Line Bot聊天機器人
# 第四章 選單功能
# 按鈕樣板TemplateSendMessage
# """
# #載入LineBot所需要的套件
# from flask import Flask, request, abort

# from linebot import (
#     LineBotApi, WebhookHandler
# )
# from linebot.exceptions import (
#     InvalidSignatureError
# )
# from linebot.models import *
# import re
# app = Flask(__name__)

# # 必須放上自己的Channel Access Token
# line_bot_api = LineBotApi('+WddPIOMZ56D7Tre1fmARy1z1eiZGJ5uJEQut/9vq1O6LsM+6hFBHugc/fwD1+HF/KwMEVqQWz1/4ef/4PMhkPWCA7TZXZVwdqB5dZIelMnkukmZL744cTBSBoW1Ua0aCYI94OidHv+wH4uBVJI36QdB04t89/1O/w1cDnyilFU=')
# # 必須放上自己的Channel Secret
# handler = WebhookHandler('e97792d24f1f087c95eec15736713fcd')

# # line_bot_api.push_message('你自己的ID', TextSendMessage(text='你可以開始了'))

# # 監聽所有來自 /callback 的 Post Request
# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']

#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     return 'OK'

# #訊息傳遞區塊
# ##### 基本上程式編輯都在這個function #####
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     message = text=event.message.text
#     if re.match('第一個',message):
#         buttons_template_message = TemplateSendMessage(
#         alt_text='這個看不到',
#         template=ButtonsTemplate(
#             thumbnail_image_url='https://i.imgur.com/wpM584d.jpg',
#             title='行銷搬進大程式',
#             text='選單功能－TemplateSendMessage',
#             actions=[
#                 PostbackAction(
#                     label='偷偷傳資料',
#                     display_text='檯面上',
#                     data='action=檯面下'
#                 ),
#                 MessageAction(
#                     label='光明正大傳資料',
#                     text='我就是資料'
#                 ),
#                 URIAction(
#                     label='行銷搬進大程式',
#                     uri='https://marketingliveincode.com/'
#                 )
#             ]
#         )
#     )
#         line_bot_api.reply_message(event.reply_token, buttons_template_message)
#     elif re.match('第二個',message):
#         buttons_template_message = TemplateSendMessage(
#         alt_text='這個看不到',
#         template=ButtonsTemplate(
#             thumbnail_image_url='https://i.imgur.com/wpM584d.jpg',
#             title='1-1',
#             text='選單功能－TemplateSendMessage',
#             actions=[
#                 PostbackAction(
#                     label='1-1',
#                     display_text='1-1',
#                     data='action=檯面下'
#                 ),
#                 MessageAction(
#                     label='1-1',
#                     text='1-1'
#                 ),
#                 URIAction(
#                     label='行銷搬進大程式',
#                     uri='https://marketingliveincode.com/'
#                 )
#             ]
#         )
#     )
#         line_bot_api.reply_message(event.reply_token, buttons_template_message)
#     elif re.match('第三個',message):
#         # Flex Message Simulator網頁：https://developers.line.biz/console/fx/
#         flex_message = FlexSendMessage(
#             alt_text='行銷搬進大程式',
#             contents={{
#                         "type": "carousel",
#                         "contents": [
#                             {
#                             "type": "bubble",
#                             "size": "micro",
#                             "hero": {
#                                 "type": "image",
#                                 "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip10.jpg",
#                                 "size": "full",
#                                 "aspectMode": "cover",
#                                 "aspectRatio": "320:213"
#                             },
#                             "body": {
#                                 "type": "box",
#                                 "layout": "vertical",
#                                 "contents": [
#                                 {
#                                     "type": "text",
#                                     "text": "Brown Cafe",
#                                     "weight": "bold",
#                                     "size": "sm",
#                                     "wrap": true
#                                 },
#                                 {
#                                     "type": "box",
#                                     "layout": "baseline",
#                                     "contents": [
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                     },
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                     },
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                     },
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                     },
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
#                                     },
#                                     {
#                                         "type": "text",
#                                         "text": "4.0",
#                                         "size": "xs",
#                                         "color": "#8c8c8c",
#                                         "margin": "md",
#                                         "flex": 0
#                                     }
#                                     ]
#                                 },
#                                 {
#                                     "type": "box",
#                                     "layout": "vertical",
#                                     "contents": [
#                                     {
#                                         "type": "box",
#                                         "layout": "baseline",
#                                         "spacing": "sm",
#                                         "contents": [
#                                         {
#                                             "type": "text",
#                                             "text": "東京旅行",
#                                             "wrap": true,
#                                             "color": "#8c8c8c",
#                                             "size": "xs",
#                                             "flex": 5
#                                         }
#                                         ]
#                                     }
#                                     ]
#                                 }
#                                 ],
#                                 "spacing": "sm",
#                                 "paddingAll": "13px"
#                             }
#                             },
#                             {
#                             "type": "bubble",
#                             "size": "micro",
#                             "hero": {
#                                 "type": "image",
#                                 "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip11.jpg",
#                                 "size": "full",
#                                 "aspectMode": "cover",
#                                 "aspectRatio": "320:213"
#                             },
#                             "body": {
#                                 "type": "box",
#                                 "layout": "vertical",
#                                 "contents": [
#                                 {
#                                     "type": "text",
#                                     "text": "Brow&Cony's Restaurant",
#                                     "weight": "bold",
#                                     "size": "sm",
#                                     "wrap": true
#                                 },
#                                 {
#                                     "type": "box",
#                                     "layout": "baseline",
#                                     "contents": [
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                     },
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                     },
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                     },
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                     },
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
#                                     },
#                                     {
#                                         "type": "text",
#                                         "text": "4.0",
#                                         "size": "sm",
#                                         "color": "#8c8c8c",
#                                         "margin": "md",
#                                         "flex": 0
#                                     }
#                                     ]
#                                 },
#                                 {
#                                     "type": "box",
#                                     "layout": "vertical",
#                                     "contents": [
#                                     {
#                                         "type": "box",
#                                         "layout": "baseline",
#                                         "spacing": "sm",
#                                         "contents": [
#                                         {
#                                             "type": "text",
#                                             "text": "東京旅行",
#                                             "wrap": true,
#                                             "color": "#8c8c8c",
#                                             "size": "xs",
#                                             "flex": 5
#                                         }
#                                         ]
#                                     }
#                                     ]
#                                 }
#                                 ],
#                                 "spacing": "sm",
#                                 "paddingAll": "13px"
#                             }
#                             },
#                             {
#                             "type": "bubble",
#                             "size": "micro",
#                             "hero": {
#                                 "type": "image",
#                                 "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip12.jpg",
#                                 "size": "full",
#                                 "aspectMode": "cover",
#                                 "aspectRatio": "320:213"
#                             },
#                             "body": {
#                                 "type": "box",
#                                 "layout": "vertical",
#                                 "contents": [
#                                 {
#                                     "type": "text",
#                                     "text": "Tata",
#                                     "weight": "bold",
#                                     "size": "sm"
#                                 },
#                                 {
#                                     "type": "box",
#                                     "layout": "baseline",
#                                     "contents": [
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                     },
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                     },
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                     },
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                     },
#                                     {
#                                         "type": "icon",
#                                         "size": "xs",
#                                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
#                                     },
#                                     {
#                                         "type": "text",
#                                         "text": "4.0",
#                                         "size": "sm",
#                                         "color": "#8c8c8c",
#                                         "margin": "md",
#                                         "flex": 0
#                                     }
#                                     ]
#                                 },
#                                 {
#                                     "type": "box",
#                                     "layout": "vertical",
#                                     "contents": [
#                                     {
#                                         "type": "box",
#                                         "layout": "baseline",
#                                         "spacing": "sm",
#                                         "contents": [
#                                         {
#                                             "type": "text",
#                                             "text": "東京旅行",
#                                             "wrap": true,
#                                             "color": "#8c8c8c",
#                                             "size": "xs",
#                                             "flex": 5
#                                         }
#                                         ]
#                                     }
#                                     ]
#                                 }
#                                 ],
#                                 "spacing": "sm",
#                                 "paddingAll": "13px"
#                             }
#                             }
#                         ]
#                         }} #json貼在這裡
#         )
#         line_bot_api.reply_message(event.reply_token, flex_message)
#     elif re.match('第四個',message):
#         # Flex Message Simulator網頁：https://developers.line.biz/console/fx/
#         flex_message = FlexSendMessage(
#             alt_text='行銷搬進大程式',
#             contents={
#                         "type": "bubble",
#                         "hero": {
#                             "type": "image",
#                             "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
#                             "size": "full",
#                             "aspectRatio": "20:13",
#                             "aspectMode": "cover",
#                             "action": {
#                             "type": "uri",
#                             "uri": "http://linecorp.com/"
#                             }
#                         },
#                         "body": {
#                             "type": "box",
#                             "layout": "vertical",
#                             "contents": [
#                             {
#                                 "type": "text",
#                                 "text": "Brown Cafe",
#                                 "weight": "bold",
#                                 "size": "xl"
#                             },
#                             {
#                                 "type": "box",
#                                 "layout": "baseline",
#                                 "margin": "md",
#                                 "contents": [
#                                 {
#                                     "type": "icon",
#                                     "size": "sm",
#                                     "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                 },
#                                 {
#                                     "type": "icon",
#                                     "size": "sm",
#                                     "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                 },
#                                 {
#                                     "type": "icon",
#                                     "size": "sm",
#                                     "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                 },
#                                 {
#                                     "type": "icon",
#                                     "size": "sm",
#                                     "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
#                                 },
#                                 {
#                                     "type": "icon",
#                                     "size": "sm",
#                                     "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
#                                 },
#                                 {
#                                     "type": "text",
#                                     "text": "4.0",
#                                     "size": "sm",
#                                     "color": "#999999",
#                                     "margin": "md",
#                                     "flex": 0
#                                 }
#                                 ]
#                             },
#                             {
#                                 "type": "box",
#                                 "layout": "vertical",
#                                 "margin": "lg",
#                                 "spacing": "sm",
#                                 "contents": [
#                                 {
#                                     "type": "box",
#                                     "layout": "baseline",
#                                     "spacing": "sm",
#                                     "contents": [
#                                     {
#                                         "type": "text",
#                                         "text": "Place",
#                                         "color": "#aaaaaa",
#                                         "size": "sm",
#                                         "flex": 1
#                                     },
#                                     {
#                                         "type": "text",
#                                         "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
#                                         "wrap": true,
#                                         "color": "#666666",
#                                         "size": "sm",
#                                         "flex": 5
#                                     }
#                                     ]
#                                 },
#                                 {
#                                     "type": "box",
#                                     "layout": "baseline",
#                                     "spacing": "sm",
#                                     "contents": [
#                                     {
#                                         "type": "text",
#                                         "text": "Time",
#                                         "color": "#aaaaaa",
#                                         "size": "sm",
#                                         "flex": 1
#                                     },
#                                     {
#                                         "type": "text",
#                                         "text": "10:00 - 23:00",
#                                         "wrap": true,
#                                         "color": "#666666",
#                                         "size": "sm",
#                                         "flex": 5
#                                     }
#                                     ]
#                                 }
#                                 ]
#                             }
#                             ]
#                         },
#                         "footer": {
#                             "type": "box",
#                             "layout": "vertical",
#                             "spacing": "sm",
#                             "contents": [
#                             {
#                                 "type": "button",
#                                 "style": "link",
#                                 "height": "sm",
#                                 "action": {
#                                 "type": "uri",
#                                 "label": "CALL",
#                                 "uri": "https://linecorp.com"
#                                 }
#                             },
#                             {
#                                 "type": "button",
#                                 "style": "link",
#                                 "height": "sm",
#                                 "action": {
#                                 "type": "uri",
#                                 "label": "WEBSITE",
#                                 "uri": "https://linecorp.com"
#                                 }
#                             },
#                             {
#                                 "type": "box",
#                                 "layout": "vertical",
#                                 "contents": [],
#                                 "margin": "sm"
#                             }
#                             ],
#                             "flex": 0
#                         }
#                         } #json貼在這裡
#         )
#         line_bot_api.reply_message(event.reply_token, flex_message)
#     elif re.match('第五個',message):
#         carousel_template_message = TemplateSendMessage(
#             alt_text='免費教學影片',
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url='https://i.imgur.com/wpM584d.jpg',
#                         title='Python基礎教學',
#                         text='萬丈高樓平地起',
#                         actions=[
#                             MessageAction(
#                                 label='教學內容',
#                                 text='拆解步驟詳細介紹安裝並使用Anaconda、Python、Spyder、VScode…'
#                             ),
#                             URIAction(
#                                 label='馬上查看',
#                                 uri='https://marketingliveincode.com/?page_id=270'
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url='https://i.imgur.com/W7nI6fg.jpg',
#                         title='Line Bot聊天機器人',
#                         text='台灣最廣泛使用的通訊軟體',
#                         actions=[
#                             MessageAction(
#                                 label='教學內容',
#                                 text='Line Bot申請與串接'
#                             ),
#                             URIAction(
#                                 label='馬上查看',
#                                 uri='https://marketingliveincode.com/?page_id=2532'
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url='https://i.imgur.com/l7rzfIK.jpg',
#                         title='Telegram Bot聊天機器人',
#                         text='唯有真正的方便，能帶來意想不到的價值',
#                         actions=[
#                             MessageAction(
#                                 label='教學內容',
#                                 text='Telegrame申請與串接'
#                             ),
#                             URIAction(
#                                 label='馬上查看',
#                                 uri='https://marketingliveincode.com/?page_id=2648'
#                             )
#                         ]
#                     )
#                 ]
#             )
#         )
#         line_bot_api.reply_message(event.reply_token, carousel_template_message)
#     elif re.match('第六個',message):
#         carousel_template_message = TemplateSendMessage(
#             alt_text='免費教學影片',
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url='https://i.imgur.com/wpM584d.jpg',
#                         title='3-3',
#                         text='萬丈高樓平地起',
#                         actions=[
#                             MessageAction(
#                                 label='教學內容',
#                                 text='拆解步驟詳細介紹安裝並使用Anaconda、Python、Spyder、VScode…'
#                             ),
#                             URIAction(
#                                 label='馬上查看',
#                                 uri='https://marketingliveincode.com/?page_id=270'
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url='https://i.imgur.com/W7nI6fg.jpg',
#                         title='Line 3-3',
#                         text='台灣最廣泛使用的通訊軟體',
#                         actions=[
#                             MessageAction(
#                                 label='教學內容',
#                                 text='Line Bot申請與串接'
#                             ),
#                             URIAction(
#                                 label='馬上查看',
#                                 uri='https://marketingliveincode.com/?page_id=2532'
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url='https://i.imgur.com/l7rzfIK.jpg',
#                         title='Telegram 3-3',
#                         text='唯有真正的方便，能帶來意想不到的價值',
#                         actions=[
#                             MessageAction(
#                                 label='教學內容',
#                                 text='Telegrame申請與串接'
#                             ),
#                             URIAction(
#                                 label='3-3',
#                                 uri='https://marketingliveincode.com/?page_id=2648'
#                             )
#                         ]
#                     )
#                 ]
#             )
#         )
#         line_bot_api.reply_message(event.reply_token, carousel_template_message)
#     else:
#         line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
# #主程式
# import os
# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)
