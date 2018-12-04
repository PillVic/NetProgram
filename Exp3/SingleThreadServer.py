#! usr/env python3 

import socket
import os

Source = 'Source/'
AtomSize = 1024

# 文件读取操作
def SendContent(sendSock,f, length):
    #以二进制形式读取指定路径的文件
    content = f.read(length)
    sendSock.sendall(content)


# 网络编程部分

def FileInfo(filePath):
    if not os.path.exists(filePath):
        return 0
    else:
        return os.stat(filePath).st_size

def SendFile(sendSock, filePath):
    info = FileInfo(filePath)
    sendSock.sendall('{:032d}'.format(info).encode('UTF-8'))
    if info == 0:
        print('[Error]'+filePath+'Not Found')
        return
    remain = info - info%AtomSize
    f = open(filePath,'rb')
    SendContent(sendSock, f, info%AtomSize)
    while remain:
        SendContent(sendSock, f, AtomSize)
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

PORT = 6666

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('',PORT))
s.listen(1)

while True:
    sc,sockName = s.accept()
    print('Connect Start sock name:', sc.getsockname())
    reqLen=int(recvall(sc,32).decode('UTF-8'))
    request = recvall(sc,reqLen).decode('UTF-8')

    print('Request Get: '+request)
    SendFile(sc,Source+request)

