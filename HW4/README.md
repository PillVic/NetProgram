# TCP 聊天室

客户端发送的报文 采用json格式：
{
    "request": {login,register, public,private}
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


## 客户端

通过连接6666端口联系服务器

* 注册 输入账号， 密码，得到是否注册成功的消息
* 登录 输入账号，密码，登录成功后进入聊天室
* 聊天模式: 接收消息并可随时发送消息
  * 公共聊天  发送给所有在线用户
  * 私聊 发送消息给指定用户

消息格式   [user]:content

## 服务器

对外开放6666端口

* 接收注册请求，查看是否有重名，返回注册结果
* 接收登录请求，维持用户登录状态
* 接收登录用户的聊天请求: 公共聊天, 私聊

### 数据结构

* dict [userName:passwd] regDict
* dict [userName:passwd] newReg
* dict [user:socket] logDict


