import json
import threading
import time
import socket
import os

from Algorithms import Minheap
from Algorithms import checksum
from Algorithms import CongestionControl

BUFFERSIZE = 1024


class RDT:
    def __init__(self, file: str, serversocket: socket.socket, addressClient):
        self.addressClient = addressClient
        self.sock = serversocket
        self.sequenceNumber = 0
        self.packets = {}  # {seq num: packet}
        self.sendAgain = Minheap.MinHeap()  # (timeStamp, seq num ) min queue by timestamps for thread to send packets again
        self.timeToWait = 2
        self.running = True
        self.bytesACK = 0
        self.cc = CongestionControl.CC(BUFFERSIZE)
        self.timer = threading.Thread(target=self.resendPackets)
        self.listeningThread = threading.Thread(target=self.receiveARQ)
        self.sendingThread = threading.Thread(target=self.startSending)
        self.lock = threading.Lock()
        File = "../FILES/" + file
        self.reader = open( File , "rb")
        # try:
        #
        #     extensions = file.split('.')
        #     # get the type of the document
        #     extension = extensions[len(extensions)-1]
        #     if extension == 'txt':
        #
        #     elif extension == 'jpeg':
        #         pass
        # # probably the os couldn't find the specified file path
        # except OSError:
        #     raise OSError
        self.sizeFile = os.stat(File).st_size
        # to seek into specific spot in the file, we just need to keep track of
        # the number of received packets, and multiplie that by the size of the buffer.
        # then we can know how much to seek into the file from the start.
        # meaning that if a client were to stop the file at a specific spot, we could recover the
        # last spot we stopped at.

    # main function to be called from the server side
    def startServer(self):
        self.listeningThread.start()
        self.timer.start()
        self.sendingThread.start()

    def startSending(self):
        while self.changeIsRunning("get"):
            self.lock.release()
            run = self.changeIsRunning("get")
            self.lock.release()
            cwnd = self.changeCC("getcwnd")
            self.lock.release()
            while self.changePackets("size") < cwnd and run:
                self.lock.release()
                print("[SERVER] sending new packet " + str(self.changeSeq("get")))
                self.lock.release()
                self.sendNewPacket()
                run = self.changeIsRunning("get")
                self.lock.release()
                cwnd = self.changeCC("getcwnd")
                self.lock.release()
            self.lock.release()
            time.sleep(1)
        self.lock.release()
        self.reader.close()

    def resendPackets(self):
        # self.running is False only when the file has ended.
        # self.sendAgain is empty only when the client received all the packets fully
        run = self.changeIsRunning("get")
        self.lock.release()
        while run:
            if self.changeHeap("isempty"):
                self.lock.release()
                print("[SERVER] no messages to be resent")
                time.sleep(1)
                run = self.changeIsRunning("get")
                self.lock.release()
                continue
            self.lock.release()
            dt = self.changeHeap("get", 0)[0] - time.time()
            self.lock.release()
            if dt < 0:  # can resend packet now
                print("[SERVER] sending old packet " + str(self.changeHeap("get")[1]))
                self.lock.release()
                self.changeCC("LOST")
                self.sendOldPacket()
                print(self.changeHeap("size"))
                self.lock.release()
            else:  # still time to wait
                time.sleep(dt)
            run = self.changeIsRunning("get")
            self.lock.release()
        print("[SERVER] done resending packets")

    # receives a constructed packet, encodes it and sends it to the client.
    def sendBuffer(self, buffer: str):
        try:
            self.lock.acquire()  # socket is not thread safe
            buf = buffer.encode("utf - 8")
            self.sock.sendto(buf, self.addressClient)
            self.lock.release()
        except OSError: # client closed connection
            self.lock.release()
            size = self.changePackets("size")
            self.lock.release()
            keys = list(self.changePackets("getkeys"))
            self.lock.release()
            for key in keys:
                self.changeHeap("remove")
                self.lock.release()
                self.changePackets("pop", key)
            return

    # reads buffer from the file, generates a buffer and returns it
    def readFromFile(self, n) -> str:
        if not self.changeIsRunning("get"):
            self.lock.release()
            return ""
        self.lock.release()
        try:
            d = n - 1 if self.sizeFile >= n else n - self.sizeFile
            buffer = self.reader.read(d)
            buffer = buffer.decode("utf - 8")
            return buffer
        # just in case, why would it happen?
        except (IOError, EOFError, OSError):
            print("IO ERROR")
            raise EOFError

    def lengthPacket(self, packet: dict):
        try:
            s = json.dumps(packet)
            return len(s)
        except ValueError:
            raise ValueError

    # return json string represents packet to be sent
    def generateNewPacket(self) -> str:
        global BUFFERSIZE
        seqNum = self.changeSeq("get")
        self.lock.release()
        packet = {
            "seq": seqNum,
            "checksum": "",
            "data": "",
            "type": "new",
            "filler": ""
            # in [req , new] - from the server side the type would be new message, or request for ack
        }
        buffer = self.readFromFile(BUFFERSIZE - self.lengthPacket(packet) - 18)  # len(checksum) = 18
        print(str(len(buffer)))
        if len(buffer) == 0 or buffer is None:
            print("failed reading")
            self.stopServer()
            return "failed"
        csum = checksum.checksum(buffer)
        packet["checksum"] = csum
        print(str(len(packet["checksum"])))
        packet["data"] = buffer
        fil = ""
        lengthPac = self.lengthPacket(packet)
        while lengthPac < BUFFERSIZE:
            fil = fil + "s"
            lengthPac += 1
        packet["filler"] = fil
        seqNum = self.changeSeq("get")
        self.lock.release()
        self.changePackets("insert", seqNum, packet)
        seqNum = self.changeSeq("get")
        self.lock.release()
        self.changeHeap("insert", seqNum)
        self.changeSeq("increment")

        return json.dumps(packet)

    def generateRequestForAckPacket(self, packetSeq: int) -> str:
        packet = {
            "seq": packetSeq,
            "checksum": "",
            "data": "",
            "type": "req",
            "filler": ""
        }
        lengthPack = self.lengthPacket(packet)
        fil = ""
        while lengthPack < BUFFERSIZE:
            fil = fil + "s"
            lengthPack += 1
        packet["filler"] = fil
        return json.dumps(packet)

    def sendRequestPacket(self, packetSeq: int):
        packet = self.generateRequestForAckPacket(packetSeq=packetSeq)
        self.sendBuffer(packet)

    def sendNewPacket(self):
        packet = self.generateNewPacket()
        if packet != "failed":
            print("[SERVER] sending new packet")
            self.sendBuffer(packet)

    def changeCC(self, com):
        self.lock.acquire()
        if com == "getcwnd":
            return self.cc.cwnd
        elif com == "ACK":
            self.cc.recvMessage("ACK")
        elif com == "LOST":
            self.cc.recvMessage("LOST")
        self.lock.release()
    # this function makes the access to the heap thread safe
    def changeHeap(self, com, packetSeq=0):
        self.lock.acquire()
        if com == "DecreaseKey":
            self.sendAgain.DecreaseKey(packetSeq, time.time() + self.timeToWait)
        elif com == "insert":
            self.sendAgain.insert(time.time() + self.timeToWait, packetSeq)
        elif com == "get":  # returns the () first value
            return self.sendAgain.heap[1]
        elif com == "isempty":
            return self.sendAgain.isEmpty()
        elif com == "size":
            return self.sendAgain.size() - 1
        elif com == "remove":
            return self.sendAgain.remove(packetSeq)
        self.lock.release()

    def changeSeq(self, com):
        self.lock.acquire()
        if com == "get":
            return self.sequenceNumber
        elif com == "increment":
            self.sequenceNumber += 1
        self.lock.release()

    def changeBytes(self, com, bytes = 0):
        self.lock.acquire()
        if com == "get":
            return self.bytesACK
        elif com == "increment":
            self.bytesACK += bytes
        self.lock.release()

    def changeIsRunning(self, com):
        self.lock.acquire()
        if com == "stop":
            self.running = False
        elif com == "get":
            return self.running
        self.lock.release()

    def sendOldPacket(self):
        # print(self.lock.locked())
        if self.changeHeap("size") == 0:
            self.lock.release()
            return
        self.lock.release()
        print(self.changeHeap("size"))
        self.lock.release()
        packetSeq = self.changeHeap("get")[1]
        self.lock.release()
        self.changeHeap("remove", packetSeq)
        self.lock.release()
        self.changeHeap("insert", packetSeq)
        packet = self.changePackets("get", packetSeq)
        self.lock.release()
        self.sendBuffer(json.dumps(packet))

    # "{
    # "seq": ,
    # "checksum": ,
    # "data": ,
    # "type": ,
    # "filler:
    #   }"                  <- packet formula expected
    # This method supposed to be a thread's func to receive messages constantly from the client.
    def receiveARQ(self):
        waiting = True
        while waiting:
            print("[SERVER] waiting to receive message")
            try:
                data, addr = self.sock.recvfrom(BUFFERSIZE)
            except OSError:
                self.changeIsRunning("stop")
                return
            # try to loads the dict if exception occurs then there was a corruption
            try:
                # raises ValueError
                dPacket: dict = self.readJsonIntoDict(data.decode("utf - 8"))
                packetSeq: int = dPacket["seq"]
                # handles the possible outcomes of the received packet
                self.handleARQ(packetSeq=packetSeq, dPacket=dPacket)
                if dPacket["type"] == "stop":
                    waiting = False
            # occurs if the json string is damaged, then send request the ack packet again.
            except ValueError:
                # can't know what is this message then send it again after timeout automatically
                continue

    # receives json string and reads it into dict
    def readJsonIntoDict(self, data) -> dict:
        try:
            dPacket: dict = json.loads(data)
            return dPacket
        except:
            raise ValueError()

    def changePackets(self, com, key=0, val=None):
        if val is None:
            val = {}
        self.lock.acquire()
        if com == "pop":
            self.packets.pop(key)
        elif com == "insert":
            self.packets[key] = val
        elif com == "size":
            return len(list(self.packets.keys()))
        elif com == "get":
            return self.packets[key]
        elif com == "getkeys":
            return self.packets.keys()
        self.lock.release()

    def handleARQ(self, packetSeq: int, dPacket: dict):
        try:
            # value does not exist in dict- might be multiple ACK that are received after a timeout...
            # don't care
            if packetSeq not in self.changePackets("getkeys"):
                self.lock.release()
                return
            self.lock.release()
            if dPacket["type"] == "ACK":
                # value exists in dict then remove it. No need to send it again it is received safely
                # send the next new packet
                print("[SERVER] received ACK about packet " + str(packetSeq))
                self.changeBytes("increment", len(self.packets[packetSeq]["data"]))
                self.changePackets("pop", packetSeq, "")
                self.changeHeap("remove", packetSeq)
                self.lock.release()
                self.changeCC("ACK")
            if dPacket["type"] == "stop":
                self.changeIsRunning("stop")
            # the packet with this specific seq num is corrupted
            # send it again.
            else:
                # send seq num packet again automatically.
                return
                # if the json is damaged -> the parsed json dict is damaged -> this error occurs
        # only if ARQ packet is corrupted.
        # send the request for the ARQ packet again
        except KeyError:
            self.sendRequestPacket(packetSeq=packetSeq)

    def sendStopPacket(self):
        print("[SERVER] sending stop packet")
        seqNum = self.changeSeq("get")
        self.lock.release()
        packet = {
            "seq": seqNum,
            "checksum": "",
            "data": "",
            "type": "stop",
            "filler": ""
        }
        packetlength = self.lengthPacket(packet)
        fil = ""
        while packetlength < BUFFERSIZE:
            fil = fil + "s"
            packetlength += 1
        packet["filler"] = fil
        seqNum = self.changeSeq("get")
        self.lock.release()
        self.changePackets("insert",seqNum ,packet)
        seqNum = self.changeSeq("get")
        self.lock.release()
        self.changeHeap("insert", seqNum)
        self.sendBuffer(json.dumps(packet))

    def stopServer(self):
        self.sendStopPacket()
    # go back n, stop and wait, selective repeat,
    # slow start, threshold, cut in half,
