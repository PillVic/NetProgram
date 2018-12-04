
# coding: utf-8

# In[1]:


import socket
import json


# In[2]:


s = socket.socket()
s.connect(('t.weather.sojson.com', 80))


# In[3]:


request = '''GET /api/weather/city/101030100 HTTP/1.1
Host: t.weather.sojson.com
User-Agent: Local Host
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,en-US;q=0.7,en;q=0.3
Cookie: _ga=GA1.2.77648417.1538467909; _gid=GA1.2.1865341186.1538824031
DNT: 1
Connection: keep-alive
Upgrade-Insecure-Requests: 1

'''


# In[4]:


s.sendall(request.encode('ascii'))

rawReply = b''

while True:
    more = s.recv(4096)
    if not more:
        break
    rawReply += more
s.close()

reply = rawReply.decode('utf-8')


# In[12]:


t = reply[reply.find('{'):reply.rfind('}')+1]


# In[14]:


reply


# In[13]:


print(t)


# In[18]:


jsonRep = json.loads(t)


# In[19]:


print(jsonRep)

