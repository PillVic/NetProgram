
# coding: utf-8

# In[1]:


#Client


# In[2]:


import socket
PORT = 6666
MaxBytes = 65536


# In[3]:


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# In[7]:


while True:
    request = input('Please input a word:')
    s.sendto(request.encode('utf-8'), ('127.0.0.1', PORT))
    answer = s.recvfrom(MaxBytes)[0].decode('utf-8')
    if request == 'EOF':
        break
    print(answer)

