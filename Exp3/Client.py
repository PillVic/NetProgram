#! usr/env python3 

import socket

downFile = 'DownFile/'
AtomSize = 1024

def recvall(sock,length):
    data = b''
    while len(data) < length:
        more = sock.recv(length-len(data))
        if not more:
            return data
        data +=more
    return data

def downLoad(s, fileName, length):
    f = open(fileName, 'wb+')
    content = recvall(s, length%AtomSize)
    f.write(content)
    remain = length - length%AtomSize
    while remain:
        content = recvall(s, AtomSize)
        f.write(content)
        remain -= AtomSize

ServerPort=6666

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',ServerPort))
print('Client connect done')

request = input('Please input the source file name:')

reqLen ='{:032d}'.format(len(request))
s.sendall(reqLen.encode('UTF-8'))
s.sendall(request.encode('UTF-8'))


replyLen = int(recvall(s,32).decode('UTF-8'))
if replyLen == 0:
    print(request+' Not Found')
else:
    fileName = input('Please input the download file name ')
    downLoad(s, downFile+fileName, replyLen)
