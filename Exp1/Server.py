#使用端口: 6666
#服务端实现功能：
#    注册：
#          检测用户名是否被注册，若没有，将信息添加到其中
#    登录：服务器检查客户的用户名，密码 若正确，记录客户的IP地址
#    公聊： 接受某个客户发来的信息，发送到公告栏，所有用户都接收
#    私聊： 发送给logList[UserName] 和发送者

import socket 
import json
import sys

ServerPort = 6666
MaxBytes = 65535

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('', ServerPort))  #接受来自该端口下的所有报文



#user = (addr, port)
def sendMessage(s,user, text):
    data = text.encode('utf-8')
    addr, port = user
    print(addr, port)
    s.sendto(data, user)

def getMessage(s):
    data, address = s.recvfrom(MaxBytes)
    text = data.decode('utf-8')
    return text

#加载注册信息
regList = dict()

with open('regList', 'r') as f:
    lines = f.readlines()
    for line in lines:
        t = line.split(':')
        userName = t[0]
        passWord = t[1].rstrip('\n')
        regList[userName] = passWord

newReg = dict() #用于记录新注册的用户，定期写入RegList

def register(userName, passWord, user):
    print(userName+' trying to retister')
    if regList.get(userName) !=None or newReg.get(userName) !=None:
        print(userName+'Exist!')
        result = '[Error]: User Exist!'
    else:
        newReg[userName] = passWord
        print(userName+' Register Success')
        result = '[Success]: Register Success!'
    sendMessage(s, user, result)

logList = dict()
def login(userName, passWord, user):
    print(userName+' trying to log in ')
    if regList.get(userName) !=None:
        if regList[userName] == passWord:
            logList[userName] = user
            result = '[Success]:'+ userName+' Log in Sucess'
        else:
            result = '[Error]: PassWord Error'
    elif newReg.get(userName) !=None:
        if newReg.get(userName) == passWord:
            logList[userName] = user
            print(userName+'log in Sucess')
            result = '[Sucess]: Log in Sucess'
        else:
            result = '[Error]: PassWord Error'
    else:
        result = '[Error]: User Does Not Exist!'
    print(result)
    sendMessage(s, user, result)
def analyse(text):
    #解析报文并作出反应
    message = json.loads(text)
    request = message["request"]
    userName = message['userName']
    user = message['Address'], message['Port']
    if request == 'login':            #处理用户登陆
        login(userName, message["password"], user)
    elif request == 'register':    #处理用户注册
        register(userName, message['password'], user)
    else:                             #进行公共/私密聊天
        #确认登陆用户是否合法
        if user == logList[userName]:
            content = message['content']
            if request == 'private':
                user = logList[message['chatname']]
                if user == None:
                    sendMessage(s, user,'[Error]: sorry the user in not online.')
                text = '[%s@%s]:%s'%(userName, message['chatname'], content)
                
                sendMessage(s, user,text)
            elif request == 'public':
                text = '[%s@public]:%s'%(userName, content)
                for i in logList:
                    user = logList[i]
                    sendMessage(s, user, text)
#######运行的主程序
while True:
    message = getMessage(s)
    analyse(message)

