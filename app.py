# -*- coding: utf-8 -*-
# """
# Created on Wed Jun  2 21:16:35 2021
# @author: Ivan
# 版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

# Line Bot聊天機器人
# 第一章 Line Bot申請與串接
# Line Bot機器人串接與測試
# """
#載入LineBot所需要的套件
import re
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

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
    if re.match('告訴我秘密',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('才不告訴你哩！'))
    elif re.match('地點',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('台中市'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)