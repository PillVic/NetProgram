#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
使用Requests库获取天气信息
"""

import requests
import sys

def getWeather(city):
    #根据城市名称查询API 并解析返回的JSON对象

    #查询城市对应的内部编码
    base  = 'http://cdn.sojson.com/_city.json'
    response = requests.get(base)
    answer = response.json()
    code = -1
    for i in answer:
        if i['city_name'] == city:
            code = i['city_code']
            break
    if code == -1:
        return 'City %s Not Found'%(city)
    #根据内部编码找到对应城市的URL
    base = 'http://t.weather.sojson.com/api/weather/city/'
    response = requests.get(base+code)
    answer = response.json()
    #杭州：20180920，湿度95， 温度24， 空气质量优，各类人群可自由活动 
    data = answer['data']
    return '%s: %s, 湿度%s, 温度%s, 空气质量%s, %s' % \
           (city, code, data['shidu'][:-1], data['wendu'], data['quality'], data['ganmao'])

    #以字符串形式返回
if __name__ == '__main__':
    if len(sys.argv) >=2:
        print(getWeather(sys.argv[1]))
    else :
        city = input('Please input the city:')
        print(getWeather(city))
