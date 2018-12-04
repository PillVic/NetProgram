#!/usr/bin/env python3
#-*- coding:utf-8 -*-

'''
使用http.client等库来获取天气信息
'''

import sys
import requests
import json
import http.client

def getCode(city):
    #解析json文件得到指定城市的编号并返回
    base = 'http://cdn.sojson.com/_city.json'
    r = requests.get(base)
    answer = r.json()
    code = -1
    for i in answer:
        if i['city_name'] == city:
            code = i['city_code']
            break
    return code
def getWeather(city):
    code = getCode(city)
    connection = http.client.HTTPConnection('t.weather.sojson.com')
    connection.request('GET', '/api/weather/city/'+code)
    rawreply = connection.getresponse().read()
    reply = json.loads(rawreply.decode('utf-8'))
    data = reply['data']
    return '%s: %s, 湿度%s, 温度%s, 空气质量%s, %s' % \
           (city, code, data['shidu'][:-1], data['wendu'], data['quality'], data['ganmao'])

if __name__ == '__main__':
    if len(sys.argv) >=2:
        print(getWeather(sys.argv[1]))
    else :
        city = input('Please input the city:')
        print(getWeather(city))

