#! usr/env python3

import socket
import os
import asyncio

Source = 'Source/'
AtomSize = 1024

# 文件读取操作
def SendContent(writer,f, length):
    #以二进制形式读取指定路径的文件
    content = f.read(length)
    writer.write(content)
    yield from writer.drain()


# 网络编程部分

def FileInfo(filePath):
    if not os.path.exists(filePath):
        return 0
    else:
        return os.stat(filePath).st_size

def SendFile(writer, filePath):
    info = FileInfo(filePath)
    writer.write('{:032d}'.format(info).encode('UTF-8'))
    if info == 0:
        print('[Error]'+filePath+'Not Found')
        return
    remain = info - info%AtomSize
    f = open(filePath,'rb')
    SendContent(writer, f, info%AtomSize)
    while remain:
        SendContent(writer, f, AtomSize)
        remain -= AtomSize
    print('[Success]: File Send')


def recvall(sock,length):
    data = b''
    while len(data) < length:
        more = sock.recv(length-len(data))
        if not more:
            return data
        data +=more
    return data

@asyncio.coroutine
def FileServe(reader, writer):
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))
    length = int((yield from reader.readexactly(32)).decode('UTF-8'))
    request = (yield from reader.readexactly(length)).decode('UTF-8')
    SendFile(writer, Source+request)

PORT = 6666

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('',PORT))
s.listen(1)


loop = asyncio.get_event_loop()
coro = asyncio.start_server(FileServe, sock=s)
server = loop.run_until_complete(coro)
try:
    loop.run_forever()
finally:
    server.close()
    loop()


