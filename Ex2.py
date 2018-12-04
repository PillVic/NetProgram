#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

def geocoder(address):
    parameters = {'address': address, 'sensor': 'false'}
    base = 'http://ditu.google.cn/maps/api/geocode/json'
    response = requests.get(base, params= parameters)
    answer = response.json()
    return answer['results'][0]['geometry']['location']

if __name__ == '__main__':
    print(geocoder2('杭州电子科技大学))
