
# coding: utf-8

# In[1]:


#Server
import socket
PORT = 6666
MaxBytes = 65536


# In[2]:


def buildDict(fileName, encode,dictA):
    lines = open(fileName, encoding=encode).readlines()
    for line in lines:
        t = line.strip('\n').split('   ')
        dictA[t[0]] = t[1]
    return dictA


# In[3]:


EngDict = dict()
EngDict = buildDict('dict/新东方红宝书.txt','gb18030', buildDict('dict/研究生入学考试.txt', 'gb2312', EngDict))


# In[4]:


# 使用端口6666进行通信
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', PORT))


# In[8]:


while True:
    data, address = s.recvfrom(MaxBytes)
    message = data.decode('utf-8')
    answer = EngDict.get(message, 'Not Found the word')
    s.sendto(answer.encode('utf-8'), address)
    if message == 'EOF':
        print('EXIT......')
        break

