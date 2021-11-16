# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 15:50:24 2021

@author: jacky
"""

import json
import csv
import os

order_path = 'data/order.csv'
detail_path = 'static/detail.txt'
detail_url = 'https://huuhou48.herokuapp.com/detail'


def getData():
    with open('data/data.json', 'r', encoding = 'utf-8') as jsonFile: 
        data = json.load(jsonFile)
    return data 

def setData(data):
    with open('data/data.json', 'w', encoding = 'utf-8') as jsonFile: 
        json.dump(data, jsonFile)

def checkAuthority(userId):
    data = getData()
    admins = data['admin']
    return True if userId in admins.values() else False
'''
    if userId in admins.values():
        return True
    else:
        return False
'''

def hasRestaurant():
    data = getData()
    return True if data['restaurant'] else False
    
'''    
    if os.path.isfile(restaurant_path):
        return True
    else:
        return False
'''

def getRestaurant():
    data = getData()
    return data['restaurant']

def setRestaurant(restaurant):
    data = getData()
    data['restaurant'] = restaurant
    setData(data)

def hasMenu(restaurant):
    restaurant_path = 'data/restaurant/' + restaurant + '.csv'
    return True if os.path.isfile(restaurant_path) else False

def getMenu(restaurant):
    with open('data/restaurant/' + restaurant + '.csv', newline = '', encoding = 'utf-8') as menuFile:
        menu = list(csv.reader(menuFile))
        return menu
    
def printMenu(restaurant):
    reply = ''
    menu = getMenu(restaurant)
    for food in menu:
        reply += ( food[0] + '. ' + food[1] + ' ' + food[2] + '\n' )  
    return reply
  
def checkValidity(order):
    menu = getMenu(getRestaurant())
    if order.isnumeric():
        if int(order) > 0 and int(order) < len(menu):
            return True
    return False
    
def addOrder(user_name, orders):
    orders = orders.split('/')  
    with open('data/order.csv', 'a+', encoding = 'utf-8') as orderFile:        
        for order in orders:
            if checkValidity(order):
                orderFile.write(user_name + ',' + order + '\n')          
            else:
                return '請依照格式輸入'
    return '收到'

def cancelOrder(user_name, cancel_orders):
    orders = getOrder()
    os.remove('data/order.csv')
    if cancel_orders:
        cancel_orders = cancel_orders.split('/')
        for order in orders:
            if order[0] != user_name:
                addOrder(order[0], order[1])
            elif order[1] not in cancel_orders:
                  addOrder(order[0], order[1])
    else:
        for order in orders:
            if order[0] != user_name:
                addOrder(order[0], order[1])
    return '取消訂單'
    
def getOrder():
    with open('data/order.csv', newline = '', encoding = 'utf-8') as orderFile:
        orders = list(csv.reader(orderFile))
    return orders


def countOrder(orders):
    foods = {}
    for order in orders:
        if order[1] in foods:
            foods[order[1]] += 1
        else:
            foods[order[1]] = 1
    return foods

def printStatistic(foods, menu):
    reply = ''
    total = 0
    total_price = 0          
    for food in foods:
        food_name = menu[int(food)][1]
        food_price = menu[int(food)][2]
        reply += ( food_name + ' ' + str(foods[food]) + '份\n')
        total += foods[food]
        total_price += ( int(food_price) * foods[food] )    
    reply += ( '共' + str(total) + '份' + str(total_price) + '元' )
    return reply
    
def showDetailAsHtml(orders, menu, domain_name):
    if os.path.isfile(detail_path):
        os.remove(detail_path)
    order_no = 1          
    for order in orders:
        food_name = menu[int(order[1])][1]
        food_price = menu[int(order[1])][2]
        with open(detail_path, 'a+', encoding = 'utf-8') as detailFile:    
            detailFile.write( str(order_no) + '. ' + order[0] + ' / ' + food_name + ' / ' + food_price + '元\n' )
        order_no += 1
    return domain_name + 'detail'


def printDetail(orders, menu):
    order_no = 1
    reply = ''            
    for order in orders:
        food_name = menu[int(order[1])][1]
        food_price = menu[int(order[1])][2]
        reply += ( str(order_no) + '. ' + order[0] + '/' + food_name + '/' + food_price + '元\n' )
        order_no += 1
    return reply


def clear():
    os.remove(order_path)
    os.remove(detail_path)
    

    
    
    
    
    
    
    