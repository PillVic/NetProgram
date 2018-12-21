#!/usr/bin/env python3
#-*- coding:utf-8 -*-

'''
使用http.client等库来获取天气信息
'''

import sys
import requests
import json
import http.client

base = 'http://cdn.sojson.com/_city.json'
r = requests.get(base)
answer = r.json()
Code=dict()
for i in answer:
    Code[i['city_name']] = i['city_code']

def getCode(city):
    #解析json文件得到指定城市的编号并返回
    return Code[city]

def getWeather(city):
    code = getCode(city)
    connection = http.client.HTTPConnection('t.weather.sojson.com')
    connection.request('GET', '/api/weather/city/'+code)
    rawreply = connection.getresponse().read()
    reply = json.loads(rawreply.decode('utf-8'))
    print(reply)
    data = reply['data']
    return str(data['forecast'])
    return '湿度%s, 温度%s, 空气质量%s, %s' % \
           (data['shidu'][:-1], data['wendu'], data['quality'], data['ganmao'])

if __name__ == '__main__':
    if len(sys.argv) >=2:
        print(getWeather(sys.argv[1]))
    else :
        while True:
            city = input('Please input the city:')
            if city =='EOF':
                break
            print(getWeather(city))

