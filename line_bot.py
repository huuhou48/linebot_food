# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:50:24 2020

@author: jacky

version: 3.0
"""

from __future__ import unicode_literals
import order_lib
import random


from flask import Flask, request, abort, render_template
#from PIL import Image, ImageDraw, ImageFont

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


app = Flask(__name__)
line_bot_api = LineBotApi('NRYJRBNY5+R4Owlz39xqrbXj6QjXUIxM0jFikC+nSMSJHfi+fqDCkbjbDWw6dbpHT3Wt/mLhotu5MPsTwOIbXX2Yp4EUYO3N1LQBcayT44G6/tmbhs6Bss4QMoZWzqYKIjGbG0mjMlRghbieIZwWDQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6f6840dac6dd85aadc37a8d2ce0686b0')
app_name = 'huuhou48'
domain_name = 'https://' + app_name + '.herokuapp.com/'


restaurants = ['大盛','小煮角','六星','日日佳','甲一','皇上皇','華圓','大芳麵店','八方雲集','十方緣','可莉','好味麵食館','開心','福德炒飯','北平餃子館','小林便當']

@app.route("/")
def home():
    return 'Hi'

# Webhook callback endpoint
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@app.route("/detail")
def showDetail():
    print('show detail')
    return render_template('detail.html')
    

description = '指令輸入格式:\n\
(指令)/(內容1)/(內容2)...\n\
\n\
指令:\n\
說明、餐廳、吃、點、取消、統計、截止、clear\n\
詳細說明請見https://github.com/huuhou48/linebot_food'

# decorator 判斷 event 為 MessageEvent
# event.message 為 TextMessage 
# 所以此為處理 TextMessage 的 handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    print(event)
    
    # get user id and message
    userId = event.source.user_id
    message = event.message.text
    
    # handle command and string processing
    if '/' not in message:
        return
    message = message.replace(' ','').replace('\n','').split('/',1)
    command = message[0]
    parameters = message[1]  
    reply = ''
    
    if command == '說明':
        reply = description

    elif command == '餐廳':
        for restaurant in restaurants:
            reply += ( restaurant + '\n' )

    elif command == '抽餐廳':
            reply += ( '今天修美食雷達選的餐廳是 : ' + random.choice(restaurants) + ', 恭喜幸運兒!!!' + '\n' )
    
    elif command == '推薦':
        if parameters == '八方雲集':
            reply += ( '招牌鍋貼不錯吃,推薦指數四顆星' + '\n' )
        elif parameters == '十方緣':
            reply += ( '白乾加醋味道更絕,炒麵只有早上有QQ' + '\n' )    

    elif command == '吃':
        admin = order_lib.checkAuthority(userId)
        if not admin:
            return         
        restaurant = parameters
        if order_lib.hasMenu(restaurant):
            order_lib.setRestaurant(restaurant)
            reply = order_lib.printMenu(restaurant)
        else:
            reply = '查無此餐廳'
            
    elif command == 'clear': 
        admin = order_lib.checkAuthority(userId)
        if not admin:
            return    
        order_lib.clear()
        reply = '清除資料'  
        
    if order_lib.hasRestaurant(): 
                       
        if command == '點':            
            user_name = line_bot_api.get_profile(userId).display_name
            reply = order_lib.addOrder(user_name, parameters)
                          
        elif command == '取消':
            user_name = line_bot_api.get_profile(userId).display_name
            reply = order_lib.cancelOrder(user_name, parameters)
            
        elif command == '統計':      
            orders = order_lib.getOrder()  
            restaurant = order_lib.getRestaurant()
            menu = order_lib.getMenu(restaurant)        
            foods = order_lib.countOrder(orders)      
            reply = order_lib.printStatistic(foods, menu)
            reply += ('\n' + order_lib.showDetailAsHtml(orders, menu, domain_name))
            
        elif command == '明細':
            orders = order_lib.getOrder()  
            restaurant = order_lib.getRestaurant()
            menu = order_lib.getMenu(restaurant)  
            reply = order_lib.printDetail(orders, menu)

           
        elif command == '截止': 
            admin = order_lib.checkAuthority(userId)
            if not admin:
                return
            order_lib.setRestaurant('')   
        
    
    
    if reply:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(reply))


if __name__ == '__main__': # 意思是直接執行此文件沒有import其他文件
    app.run()