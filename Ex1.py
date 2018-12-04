#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pygeocoder

if __name__ == '__main__':
    address = 'hangzhou dianzi university'
    print(pygeocoder.Geocoder.geocode(address)[0].coordinates)
