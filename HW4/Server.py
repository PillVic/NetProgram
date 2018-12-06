#! /usr/bin/evn python3

import asyncio
import json


def load():
    f = open('RegList')
    lines = f.readlines()
    regDict = dict()
    for line in lines:
        userName, passwd = line.split(':')
        regDict[userName] = passwd
    return regDict

def getMessage(reader):
    head = yield from reader.read(32)
    length = int(head.decode('UTF-8'))
    content = yield from reader.read(length)
    mesg = content.decode('UTF-8')
    return mesg

def sendMessage(writer, message):
    bits = message.encode('UTF-8')
    length = len(bits)
    writer.write(str(length).encode('UTF-8'))
    writer.write(bits)

@asyncio.coroutine
def Serve(reader, writer):
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))
    while True:
        message = getMessage(reader)
