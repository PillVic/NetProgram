#! usr/env python3 

import socket
import os
import select

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

def FileServe(sc):
    print('Connect Start sock name:', sc.getsockname())
    reqLen=int(recvall(sc,32).decode('UTF-8'))
    request = recvall(sc,reqLen).decode('UTF-8')

    print('Request Get: '+request)
    SendFile(sc,Source+request)

def loopEvents(p):
    while True:
        for fd, event in p.poll():
            yield fd, event

def Serve(listenSock):
    sockets = {listenSock.fileno():listenSock}
    addresses = {}
    recvBytes = {listenSock.fileno():[-1,b'']}
    sendBytes = {listenSock.fileno():[-1,b'']}

    p = select.poll()
    p.register(listenSock, select.POLLIN)

    for fd, event in loopEvents(p):
        sock = sockets[fd]
        if event & (select.POLLHUP|select.POLLERR|select.POLLNVAL):
            # Socket closed:remove it
            address = addresses.pop(sock)
            rb = recvBytes.pop(sock, b'')
            sb = sendBytes.pop(sock,b'')
            if rb:
                print('Client {} sent {} but then closed.'.format(address, rb))
            elif sb:
                print('Client {} closed before we sent {}'.format(address,sb))
            else:
                print('Client {} closed socket normally'.format(address))
            p.unregister(fd)
        elif sock is listenSock:
            #New Socket:add it
            sock, address = sock.accept()
            print('Accepted connection from {}'.format(address))
            sock.setblocking(False)
            sockets[sock.fileno()] = sock
            addresses[sock] = address
            p.register(sock, select.POLLIN)
            recvBytes[sock.fileno()]=[-1,'']
        elif event & select.POLLIN:
            #Incoming data: 
            if recvBytes[sock.fileno()][0] ==-1:
                #Receive request length
                length = int(recvall(sock, 32).decode('UTF-8'))
                recvBytes[sock.fileno()][0] = length
                print('Request length get:'+str(length))
            elif recvBytes[sock.fileno()][1] == '':
                #Receive request 
                recvBytes[sock.fileno()][1] = recvall(sock, recvBytes[sock.fileno()][0]).decode('UTF-8')
                print('Request Get:'+recvBytes[sock.fileno()][1])
                p.modify(sock, select.POLLOUT)
        elif event & select.POLLOUT:
            #Socket ready to send:keep sending until all bytes are delivered
            request = recvBytes[sock.fileno()][1]
            print(request)
            if request != '':
                print('Request Start:'+request)
                SendFile(sock, 'Source/'+request)
                p.modify(sock, select.POLLIN)

            

PORT = 6666

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('',PORT))
s.listen(1)
Serve(s)


