
# coding: utf-8

# In[1]:


#Client


import socket
PORT = 6666
MaxBytes = 65536

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

SendFile = open('send.dat','a+')
RecvFile = open('recv.dat','a+')

while True:
    request = input('Please input a word:')
    SendFile.write(request+'\n')
    s.sendto(request.encode('utf-8'), ('127.0.0.1', PORT))
    answer = s.recvfrom(MaxBytes)[0].decode('utf-8')
    if request == 'EOF':
        break
    print(answer)
    RecvFile.write(answer+'\n')

SendFile.close()
RecvFile.close()
