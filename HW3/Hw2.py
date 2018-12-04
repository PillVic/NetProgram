import sys
import socket

PORT = 6666
MaxBytes = 65536

if __name__ == '__main__':
    if sys.argv[1] == 'server':
        def buildDict(fileName, encode,dictA):
            lines = open(fileName, encoding=encode).readlines()
            for line in lines:
                t = line.strip('\n').split('   ')
                dictA[t[0]] = t[1]
            return dictA
        EngDict = dict()
        EngDict = buildDict('dict/新东方红宝书.txt','gb18030', buildDict('dict/研究生入学考试.txt', 'gb2312', EngDict))

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('127.0.0.1', PORT))

        while True:
            data, address = s.recvfrom(MaxBytes)
            message = data.decode('utf-8')
            answer = EngDict.get(message, '查询不到')
            s.sendto(answer.encode('utf-8'), address)
            if message == 'EOF':
                print('EXIT......')
                break
    elif sys.argv[1] == 'client':
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while True:
            if len(sys.argv) == 2:
                request = input('Please input a word:')
            else:
                request = sys.argv[2]
            s.sendto(request.encode('utf-8'), ('127.0.0.1', PORT))
            answer = s.recvfrom(MaxBytes)[0].decode('utf-8')
            if request == 'EOF':
                break
            print(request+':'+answer)
            if len(sys.argv) !=2:
                break

