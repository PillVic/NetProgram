#!/usr/bin/env python3

import matplotlib.patches as mpatches
import scapy.all as scapy
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

packages = scapy.rdpcap('p.pcapng')

sender=['Client', 'Server']
def getSender(package):
    #0 :Client
    #1 :Server
    if package['IP'].src=='192.168.102.15':
        return 0
    else:
        return 1


# 构建基本画图框架

fig, ax1 = plt.subplots()
ax1.set_title('TCP hand shake graph')
ax1.set_ylabel('TIME')
ax1.set_xlim(left='Server', right='Client')

# 处理每个报文

pgroup = [[],[]]
colors=['red', 'blue']

for p in packages: # 将报文按发送方分组
    pgroup[getSender(p)].append(p)

pgroup[0].sort(key=lambda x:x['TCP'].options[2][1][1])
pgroup[1].sort(key=lambda x:x['TCP'].options[2][1][0])



for i in range(3):
    #三次连接
    line = [(sender[1-i%2], 3-i), (sender[i%2], 4-i)]
    (line_xs, line_ys)=zip(*line)
    ax1.add_line(Line2D(line_xs, line_ys, linewidth=2, color=colors[i%2]))

plt.text(0.2, 3.5, 'ack = '+str(pgroup[0][0]['TCP'].ack)+' seq = '+str(pgroup[0][0]['TCP'].seq), fontsize=12)
plt.text(0.2, 2.5, 'ack = '+str(pgroup[1][0]['TCP'].ack)+' seq = '+str(pgroup[1][0]['TCP'].seq), fontsize=12)
plt.text(0.2, 1.5, 'ack = '+str(pgroup[0][1]['TCP'].ack)+' seq = '+str(pgroup[0][1]['TCP'].seq), fontsize=12)


plt.legend(handles=[mpatches.Patch(color='red', label='Sender:Client'),
                    mpatches.Patch(color='blue', label='Sender:Server')])


plt.yticks([])

plt.plot()

plt.show()
