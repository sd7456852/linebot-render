# # -*- coding: utf-8 -*-
# """
# Created on Wed Jun  2 21:16:35 2021

# @author: Ivan
# 版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

# Line Bot聊天機器人
# 第三章 互動回傳功能
# 推播push_message與回覆reply_message
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

# line_bot_api.push_message('U8d188af1584c5e78ab310184099a1bf5', TextSendMessage(text='你可以開始了'))

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
#     # 場地 按鈕
#     if re.match('場地',message):
#         carousel_template_message = TemplateSendMessage(
#             # 前面看不到
#             alt_text='場地地點',
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url='https://upload.cc/i1/2022/12/30/2i7cN1.jpg'
# ',
#                         title='北部',
#                         text='選擇場地',
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
#                         title='中部',
#                         text='選擇場地',
#                         actions=[
#                             MessageAction(
#                                 label='台中網球中心',
#                                 text=''
#                                 location_message = LocationSendMessage(
#                                 title='匹克球場地',
#                                 address='台中網球中心 星期一、星期三 晚上7:00~9:00',
#                                 latitude=24.164931358000565,
#                                 longitude=120.7297540396959
#                                 )
                                
#                             ),
#                             URIAction(
#                                 label='馬上查看',
#                                 uri='https://marketingliveincode.com/?page_id=2532'
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url='https://i.imgur.com/l7rzfIK.jpg',
#                         title='南部',
#                         text='選擇場地',
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
#     # if re.match('台中',message):
#     #     location_message = LocationSendMessage(
#     #         title='匹克球場地',
#     #         address='台中網球中心 星期一、星期三 晚上7:00~9:00',
#     #         latitude=24.164931358000565,
#     #         longitude=120.7297540396959
#     #     )
#     #     line_bot_api.reply_message(event.reply_token, location_message)
        
#     # elif re.match('台中',message):
#     #     location_message = LocationSendMessage(
#     #         title='匹克球場地',
#     #         address='舊社公園 星期一晚上6:30 星期日下午2:00(夏天3:00)',
#     #         latitude=24.18113046915357,
#     #         longitude=120.70055242380153
#     #     )
#     #     line_bot_api.reply_message(event.reply_token, location_message)
#     # elif re.match('嘉義',message):
#     #     location_message = LocationSendMessage(
#     #         title='匹克球場地',
#     #         address='嘉義高工',
#     #         latitude=23.472062366797523,
#     #         longitude=120.46423061269472
#     #     )
#     #     line_bot_api.reply_message(event.reply_token, location_message)
#     else:
#         line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
# #主程式
# import os
# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第四章 選單功能
多樣版組合按鈕CarouselTemplate
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('+WddPIOMZ56D7Tre1fmARy1z1eiZGJ5uJEQut/9vq1O6LsM+6hFBHugc/fwD1+HF/KwMEVqQWz1/4ef/4PMhkPWCA7TZXZVwdqB5dZIelMnkukmZL744cTBSBoW1Ua0aCYI94OidHv+wH4uBVJI36QdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('e97792d24f1f087c95eec15736713fcd')

line_bot_api.push_message('U8d188af1584c5e78ab310184099a1bf5', TextSendMessage(text='你可以開始了'))

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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('場地',message):
        carousel_template_message = TemplateSendMessage(
            alt_text='匹克球場地',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/12/30/2i7cN1.jpg',
                        title='北部',
                        text='請選擇場地',
                        actions=[
                            MessageAction(
                                label='教學內容',
                                text='拆解步驟詳細介紹安裝並使用Anaconda、Python、Spyder、VScode…'
                            ),
                            URIAction(
                                label='台中網球中心',
                                uri='https://goo.gl/maps/3BVyr4AmitdjYySn6'
                            ),
                            URIAction(
                                label='台中網球中心',
                                uri='https://goo.gl/maps/3BVyr4AmitdjYySn6'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/12/30/2i7cN1.jpg',
                        title='中部',
                        text='請選擇場地',
                        actions=[
                            MessageAction(
                                label='教學內容',
                                text='Line Bot申請與串接'
                            ),
                            URIAction(
                                label='台中網球中心',
                                uri='https://goo.gl/maps/3BVyr4AmitdjYySn6'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/l7rzfIK.jpg',
                        title='Telegram Bot聊天機器人',
                        text='唯有真正的方便，能帶來意想不到的價值',
                        actions=[
                            MessageAction(
                                label='教學內容',
                                text='Telegrame申請與串接'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://marketingliveincode.com/?page_id=2648'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    elif re.match('台中',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('台中網球中心(收費) \n時間:星期一、星期三 \n晚上7:00~9:00 聯絡人:'))
    elif re.match('請輸入地區 例:台中',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(''))
        
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
