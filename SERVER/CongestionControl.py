import threading
import time
import socket


class CC:
    def __init__(self, file: str, serversocket: socket.socket, addressClient):
        self.addressClient = addressClient
        self.sock = serversocket
        self.sequenceNumber = 0
        self.packets = []
        self.windowsize = 1
        self.timeToWait = 2
        self.timer = threading.Timer(2, self.sendFile)
        self.buffersize = 1024
        self.file = file
        self.reader = open(self.file, "r")

    def sendFile(self):
        if len(self.packets) == 0:
            self.sendBunch(self.addressClient)

    def receiveACKS(self):
        waiting = True
        timeStamp = time.time()
        while waiting:
            # "{ {"seq": },{"checksum": }, {"data": } }                  <- packet formula
            data, addr = self.sock.recvfrom(self.buffersize)
            sendOld = False
            # for i in range(len(listSequence)):
            #     if self.sequenceNumber - self.windowsize <= listSequence[i] <= self.sequenceNumber:
            #         pass

    def sendOldBunch(self):
        for i in range(self.windowsize):
            self.sendBuffer(self.packets[i])

    def sendNewBunch(self):
        buffer = None
        for i in range(self.windowsize):
            buffer = self.reader.read(self.buffersize)
            self.sendBuffer(buffer)

    def sendBuffer(self, buffer: str):
        buf = buffer.encode("utf - 8")
        self.packets.append(buffer)
        self.sequenceNumber += 1
        self.packets.append(buffer)
        self.sock.sendto(buf, self.addressClient)


def conv16bits(num):
    if num == 0:
        return binaryStringByte('\0') + binaryStringByte('\0')
    else:
        l = num
        res = ""
        while l != 0:
            if l % 2 == 1:
                res = '1' + res
            else:
                res = '0' + res
            l = int(l / 2)
        while len(res) < 16:
            res = '0' + res
        return res


def oneComplement(buf):
    res = list(buf)
    for i in range(2,len(buf)):
        if buf[i] == '0':
            res[i] = '1'
        else:
            res[i] = '0'
    return "".join(res)


def checksum(buffer: str):
    listbytesbuffer = divBy16Bits(buffer)
    sum = 0
    for i in range(len(listbytesbuffer)):
        sum += int(listbytesbuffer[i], 2)
    bsum = bin(sum)
    print(bsum)
    print(len(bsum))
    print(sum)
    carry = 0
    if len(bsum) > 18:  # 0b1111... for some reason
        carry = len(bsum) - 18
        sum = sum + carry
        bsum = bin(sum)
        s = bin(int(bsum[-16:],2))
        return oneComplement(s)
    p = len(bsum)
    if len(bsum) < 18:
        bSum = "0b" + conv16bits(sum)
        return oneComplement(bSum)
    if len(bsum) == 18:
        return oneComplement(bsum)



# go back n, stop and wait, selective repeat,
# slow start, threshold, cut in half,

def divBy16Bits(buffer: str) -> []:
    listbuf = []
    if len(buffer) % 2 == 0:
        for i in range(0, len(buffer) - 1, 2):
            listbuf.append(binaryStringByte(buffer[i]) + binaryStringByte(buffer[i + 1]))
    else:
        for i in range(0, len(buffer) - 2, 2):
            listbuf.append(binaryStringByte(buffer[i]) + binaryStringByte(buffer[i + 1]))
        listbuf.append(binaryStringByte('\0') + binaryStringByte(buffer[len(buffer) - 1]))
    return listbuf


def binaryStringByte(cHar):
    l = ord(cHar)
    if l == 0:
        return "00000000"
    ret = ''
    while l != 0:
        if l % 2 == 1:
            ret = '1' + ret
        else:
            ret = '0' + ret
        l = int(l / 2)
    while len(ret) < 8:
        ret = '0' + ret
    return ret
