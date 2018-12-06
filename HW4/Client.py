#! /usr/bin/env python3

import socket
import threading
import json
import getpass

# API
def recvall(sock, length):
    data = b''
    while len(data) <length:
        more = sock.recv(length-len(data))
        if not more:
            raise EOFError('Server ended unexpected.\n')
        data +=more
    return data

def getMessage(sock):
    length = int(recvall(sock, 32).decode('UTF-8'))
    bits = recvall(sock, length)
    return bits.decode('UTF-8')

def sendMessage(sock, text):
    bits = text.decode('UTF-8')
    length = len(bits)
    head = '{:032d}'.format(length)
    sock.sendall(head.encode('UTF-8'))
    sock.sendall(bits)

# 
def speak(s):
    while True:
        rawInput = input('plese input like user:content  ') 
        text = rawInput.split(':')
        chatname = text[0]
        content = text[1]
        request = 'private'
        if chatname =='public':
            request = 'public'
        data = {
            "request":request,
            "Address":ServerIP, 
            "userName":username,
            "content":content,
            "chatname":chatname
        }
        message = json.dumps(data)
        sendMessage(s, message)


def chat(s, s2,username):        #聊天状态，发送和接收使用单独的两个线程
    #        线程A: 接收并处理服务器发来的报文
    #        线程B: 向服务器发送报文
    print('chatting model.....')
    threads = []
    t1 = threading.Thread(target=receive, args=(s2,))
    t2 = threading.Thread(target=speak,args=(s,))
    threads.append(t1)
    threads.append(t2)
    for t in threads:
        t.start()
    
if sys.argv[1] == 'register':    #注册用户：等待用户输入用户名和密码 成功后退出，不登录
    username = input('please input the user name:')
    waitpass = True
    while waitpass:
        password = getpass.getpass('please input the password:')
        check = getpass.getpass('input it again to check:')
        if password != check:
            print('[Error]: Not Same')
        else:
            waitpass = False
            text  = {
            "request":'register',
            "userName":username,
            "password":password
            } 
            message = json.dumps(text)
            sendMessage(s, message)
            answer = getMessage(s2)
            print('\n'+answer)

elif sys.argv[1] == 'login':   #用户登录：等待用户输入用户名和密码，成功后进入聊天状态，否则重新输入用户名和密码 
    waitpass = True
    while waitpass:
        username = input('please input the user name:')
        s.close()
        s2.close()

        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        password = getpass.getpass('please input the password:')
        text = {
        "request":'login',
        "userName":username,
        "password":password
        }
        message = json.dumps(text)
        sendMessage(s, message)
        message = getMessage(s2)
        print(message)
        if message[1] == 'S': #Sucess 进入聊天模式
            waitpass = False
            break
    chat(s,s2, username)





