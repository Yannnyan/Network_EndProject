import socket
import threading
import json
from Algorithms import checksum
import heapq

BUFFERSIZE = 1024


class RDT:
    def __init__(self, sock: socket.socket, serverAddress: (str, int)):
        self.sock = sock
        self.serverAddress = serverAddress
        self.running = True
        self.sequenceNumber = 0
        self.packets = {}  # {seq num: buffer}
        self.heapSequencePacket = []  # heap contains sequence numbers received
        self.files = {}  # {file_name : bytesDownloaded}
        self.currentFile = None
        self.listeningThread = threading.Thread(target=self.receivePackets)
        self.writer = None
        self.lock = threading.Lock()

    def HandShake(self):
        print("[CLIENT] sending SYN-ACK")
        try:
            message = {"seq": -1, "checksum": "", "data": self.files[self.currentFile], "type": "SYN-ACK", "fill": ""}
            mes = self.fillPacket(message)
            self.sendBuffer(json.dumps(mes))
            print("[CLIENT] sent buffer")
        except KeyError:
            self.files[self.currentFile] = 0
            message = {"seq": -1, "checksum": "", "data": 0, "type": "SYN-ACK", "fill": ""}
            mes = self.fillPacket(message)
            self.sendBuffer(json.dumps(mes))
            print("[CLIENT] sent buffer")

    def addFile(self, filename):
        self.currentFile = filename
        self.writer = open(filename, "wb")

    def stopClient(self, packetSeq):
        self.sendStopPacket(packetSeq=packetSeq)
        self.changeIsRunning("stop")

    # main function in this class
    def startReceiving(self):
        self.reset()
        self.listeningThread = threading.Thread(target=self.receivePackets)
        self.listeningThread.start()

    def reset(self):
        self.running = True
        self.sequenceNumber = 0
        self.heapSequencePacket = []
        self.packets = {}

    def receivePackets(self):
        print("[CLIENT] receiving packets")
        while self.changeIsRunning("get"):
            self.lock.release()
            data, addr = self.sock.recvfrom(BUFFERSIZE)
            print("[CLIENT] got packet")
            self.handlePacket(data.decode("utf - 8"))
        self.lock.release()
        self.writer.close()

    # "{
    # "seq": ,
    # "checksum": ,
    # "data": ,
    # "type": ,
    # "fill":
    #   }"                  <- packet formula expected
    def unpackPacket(self, packet) -> dict:
        try:
            print(packet)
            d: dict = json.loads(packet)
            return d
        except ValueError as v:
            # print(v.__cause__.__str__())
            raise ValueError

    # writer uses the heap to know in which order to write the packets received,
    # if the packets are received in the wrong order, the writer will not write those packets down
    # but it will wait until the sequence number matches
    # this way we can keep the file transfered the same as it was the server's hands
    # we do this instead of keeping all the packets in the dict because it saves space for more options
    # when the file is large it might be a problem to keep all the buffers in a data structure
    def writePacket(self):
        size = self.changeHeap("size")
        self.lock.release()
        if size == 0 or not self.changeIsRunning("get"):
            self.lock.release()
            return
        self.lock.release()
        seqNum = self.changeHeap("get")
        self.lock.release()
        while seqNum == self.changeSeq("get"):
            self.lock.release()
            self.changeHeap("pop")
            self.lock.release()
            buffer = self.changePackets("pop", seqNum)
            self.lock.release()
            if buffer is None:
                return
            self.writer.write(buffer.encode("utf - 8"))
            self.changeSeq("increment")
        self.lock.release()

    def changePackets(self, com, key=0, val=None):
        if val is None:
            val = {}
        self.lock.acquire()
        if com == "pop":
            print(str(key))
            print(self.packets)
            return self.packets.pop(key)
        elif com == "insert":
            self.packets[key] = val
        elif com == "size":
            return len(list(self.packets.keys()))
        elif com == "get":
            return self.packets[key]
        elif com == "getkeys":
            return self.packets.keys()
        self.lock.release()

    def changeHeap(self, com, val=""):
        self.lock.acquire()
        if com == "push":
            heapq.heappush(self.heapSequencePacket, val)
        elif com == "pop":
            return heapq.heappop(self.heapSequencePacket)
        elif com == "size":
            return len(self.heapSequencePacket)
        elif com == "get":
            return self.heapSequencePacket[0]
        self.lock.release()

    def changeIsRunning(self, com):
        self.lock.acquire()
        if com == "stop":
            self.running = False
        elif com == "get":
            return self.running
        self.lock.release()

    def changeSeq(self, com):
        self.lock.acquire()
        if com == "get":
            return self.sequenceNumber
        elif com == "increment":
            self.sequenceNumber += 1
        self.lock.release()

    def handlePacket(self, packet):
        try:
            dPacket = self.unpackPacket(packet=packet)
            if dPacket["checksum"] != "" and checksum.checkCurroption(dPacket["data"], dPacket["checksum"]):
                print("[CLIENT] received corrupted message")
                self.sendNACK(dPacket["seq"])  # currupted message, send another.
            else:
                print("[CLIENT] received valid message")
                if dPacket["type"] == "new":
                    print("[CLIENT] type is new")
                    packetSeq = dPacket["seq"]
                    try:
                        if not self.changePackets("getkeys").__contains__(packetSeq):
                            self.lock.release()
                            print("[CLIENT] does not contain")
                            self.changePackets("insert", packetSeq, dPacket["data"])
                            self.changeHeap("push", packetSeq)
                        else:
                            self.lock.release()
                    except (KeyError, ValueError):
                        self.lock.release()
                    self.sendACK(packetSeq=packetSeq)
                    # pegions holes
                    self.writePacket()  # each time good packet is received it checks whether the file can write
                elif dPacket["type"] == "req":
                    packetSeq = dPacket["seq"]
                    smallest = self.changeHeap("get")
                    self.lock.release()
                    if self.changePackets("getkeys").__contains__(packetSeq) or smallest > packetSeq:
                        self.lock.release()
                        self.sendACK(packetSeq=packetSeq)
                    self.lock.release()
                elif dPacket["type"] == "stop":
                    packetSeq = dPacket["seq"]
                    self.stopClient(packetSeq=packetSeq)
                elif dPacket["type"] == "SYN":
                    if dPacket["data"] == ("../FILES/" + self.currentFile):
                        self.HandShake()

        except ValueError as v:

            print("[CLIENT] value error " + str(v.__cause__))
            # don't care server will send another packet
            pass

    def lengthPacket(self, packet):
        try:
            return len(json.dumps(packet))
        except ValueError:
            raise ValueError

    def generateNACKPacket(self, seqNum: int) -> str:
        packet = {
            "seq": seqNum,
            "checksum": "",
            "data": "",
            "type": "NACK",
            "fill": ""
        }
        packet = self.fillPacket(packet)
        return json.dumps(packet)

    def generateACKPacket(self, seqNum: int) -> str:
        packet = {
            "seq": seqNum,
            "checksum": "",
            "data": "",
            "type": "ACK",
            "fill": ""
        }
        packet = self.fillPacket(packet)
        return json.dumps(packet)

    def sendBuffer(self, buffer: str):
        self.lock.acquire()
        self.sock.sendto(buffer.encode("utf - 8"), self.serverAddress)
        print("[CLIENT] sent buffersss")
        self.lock.release()

    def sendACK(self, packetSeq):
        print("[CLIENT] sending ACK")
        packet: str = self.generateACKPacket(packetSeq)
        self.sendBuffer(packet)

    def sendNACK(self, packetSeq):
        print("[CLIENT] sending NACK")
        packet = self.generateNACKPacket(packetSeq)
        self.sendBuffer(packet)

    def fillPacket(self, packet: dict) -> dict:
        lengthPack = self.lengthPacket(packet)
        fil = ""
        while lengthPack < BUFFERSIZE:
            fil = fil + "s"
            lengthPack += 1
        packet["fill"] = fil
        return packet

    def sendStopPacket(self, packetSeq):
        print("[CLIENT] sending stop packet")
        packet = {
            "seq": packetSeq,
            "checksum": "",
            "data": "",
            "type": "stop",
            "fill": ""
        }
        packet = self.fillPacket(packet)
        self.sendBuffer(json.dumps(packet))
