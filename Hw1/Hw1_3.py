#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import requests
import socket
import json

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
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = 't.weather.sojson.com'
    s.connect((host , 80))
    request = '''GET /api/weather/city/%s HTTP/1.1
Host: t.weather.sojson.com
User-Agent: Local Host
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,en-US;q=0.7,en;q=0.3
Cookie: _ga=GA1.2.77648417.1538467909; _gid=GA1.2.1865341186.1538824031
DNT: 1
Connection: keep-alive
Upgrade-Insecure-Requests: 1

''' % (getCode(city)) 
    s.sendall(request.encode('ascii'))
    rawReply = b''
    while True:
        more = s.recv(4096)
        if not more:
            break
        rawReply += more
    s.close()
   
    reply = rawReply.decode('utf-8')
    reply = reply[reply.find('{'):reply.rfind('}')+1]
    jsonRes = json.loads(reply)
    data = jsonRes['data']
    return '%s: %s, 湿度%s, 温度%s, 空气质量%s, %s' % \
          (city, getCode(city), data['shidu'][:-1], data['wendu'], data['quality'], data['ganmao'])

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(getWeather(sys.argv[1]))
    else:
        city = input('Please input the city:')
        print(getWeather(city))
