#!/usr/bin/env python3

import scapy.all as scapy

packages = scapy.rdpcap('p.pcapng')

counter = 1

Server=list()
Client=list()

for p in packages:
    print('packages:'+str(counter))
    p.show()
    counter+=1
    print('#############################################################################')


