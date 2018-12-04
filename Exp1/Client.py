#客户端实现功能：
#   注册：发送用户名和密码给服务器，接收服务器得到的反馈(成功，失败)
#   登录：发送用户名和密码给服务器，接收服务器得到反馈(成功，失败)
#   公告：[user@public]:......
#   私聊：[user@chatName]:......

# 服务器的IP地址,端口是公开的
# 客户端的IP地址，使用端口号由客户端自己定义，并通过json报文传递

import socket
import sys
import getpass
import json
import threading


ServerIP = '127.0.0.1'
ServerPort = 6666
MaxBytes = 65535
InPort = 8848  #接收端口
OutPort = 9982 #发送端口


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('',OutPort))

s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2.bind(('',InPort))

#address = socket.gethostbyname(socket.gethostname())
address = '127.0.0.1'

def sendMessage(s, text):
    data = text.encode('utf-8')
    s.sendto(data, (ServerIP, ServerPort))

def getMessage(s):
    data, address = s.recvfrom(MaxBytes)
    text = data.decode('utf-8')
    return text

def receive(s):
    while True:
        t = getMessage(s)
        print(t)
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
            "Port":InPort,
            "userName":username,
            "content":content,
            "chatname":chatname
        }
        message = json.dumps(data)
        sendMessage(s, message)


def chat(s, username):        #聊天状态，发送和接收使用单独的两个线程
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
            "Address":address,
            "Port":InPort,
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
        InPort = int(input('please input the input port number:'))
        OutPort = int(input('please input the output port number:'))

        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind(('',OutPort))
        s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s2.bind(('',InPort))

        password = getpass.getpass('please input the password:')
        text = {
        "request":'login',
        "Address":address,
        "Port":InPort,
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
    chat(s,username)

