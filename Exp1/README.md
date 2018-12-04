服务器文件
1. rootList  注册表， 记录所有用户的注册信息，用户名，密码

格式：
用户名:密码

2. regList   动态，登陆表， 记录所有登陆用户的用户名和对应的IP地址,使用的端口号

客户端发送的报文 采用json格式：
{
    "request": {login,register, public,private}
    "Address": //发送者的IP地址
    "Port"://发送者的接收端口号
    "userName":
//登录和注册需要    
    "password":
//private 时需要 
    "chatName":
//public private 都需要
    "content":
}

服务器端发送的报文格式 直接使用字符串
[]:

显示的消息格式

[userName@public]:消息内容
[userName@userName]:消息内容

