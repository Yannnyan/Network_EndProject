import json
import threading
import time
import socket
from Algorithms import Minheap
from Algorithms import checksum

BUFFERSIZE = 1024


class CC:
    def __init__(self, file: str, serversocket: socket.socket, addressClient):
        self.addressClient = addressClient
        self.sock = serversocket
        self.sequenceNumber = 0
        self.packets = {}  # {seq num: buffer}
        self.sendAgain = Minheap.MinHeap()  # (timeStamp, seq num ) min queue by timestamps for thread to send packets again
        self.windowsize = 1
        self.timeToWait = 2
        self.running = True
        self.timer = threading.Thread(target=self.resendPackets)
        self.listeningThread = threading.Thread(target= self.receiveARQ)
        try:
            self.reader = open(file, "rb")
        # probably the os couldn't find the specified file path
        except OSError:
            raise OSError
        # to seek into specific spot in the file, we just need to keep track of
        # the number of received packets, and multiplie that by the size of the buffer.
        # then we can know how much to seek into the file from the start.
        # meaning that if a client were to stop the file at a specific spot, we could recover the
        # last spot we stopped at.

    # main function to be called from the server side
    def startSending(self):
        self.listeningThread.start()
        self.timer.start()
        while len(self.packets) < self.windowsize and self.running:
            print("[SERVER] sending new packet " + self.sequenceNumber)
            self.sendNewPacket()
        self.reader.close()

    def resendPackets(self):
        while self.running:
            if len(self.sendAgain.isEmpty()):
                time.sleep(1)
            dt = self.sendAgain.heap[1][0] - time.time()
            if dt < 0:  # can resend packet now
                print("[SERVER] sending old packet " + str(self.sendAgain.heap[1][1]))
                self.sendOldPacket()
            else:  # still time to wait
                time.sleep(dt)

    # receives a constructed packet, encodes it and sends it to the client.
    def sendBuffer(self, buffer: str):
        buf = buffer.encode("utf - 8")
        self.sock.sendto(buf, self.addressClient)

    # reads buffer from the file, generates a buffer and returns it
    def readFromFile(self, n) -> str:
        try:
            buffer = self.reader.read(n).decode("utf - 8")
            return buffer
        # just in case, why would it happen?
        except OSError:
            raise OSError

    def lengthPacket(self, packet: dict):
        try:
            s = json.dumps(packet)
            return len(s)
        except ValueError:
            raise ValueError

    # return json string represents packet to be sent
    def generateNewPacket(self) -> str:
        global BUFFERSIZE
        packet = {
            "seq": self.sequenceNumber,
            "checksum": "",
            "data": "",
            "type": "new",
            "filler": ""
            # in [req , new] - from the server side the type would be new message, or request for ack
        }
        buffer = self.readFromFile(BUFFERSIZE - self.lengthPacket(packet) - 18) # len(checksum) = 18
        csum = checksum.checksum(buffer)
        packet["checksum"] = csum
        packet["data"] = buffer
        fil = ""
        lengthPac = self.lengthPacket(packet)
        while lengthPac < BUFFERSIZE:
            fil = fil + "s"
            lengthPac += 1
        packet["filler"] = fil
        self.packets[self.sequenceNumber] = packet
        self.sendAgain.insert(time.time() + self.timeToWait, self.sequenceNumber)
        self.sequenceNumber += 1
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
        self.sendBuffer(packet)

    def sendOldPacket(self):
        if len(self.sendAgain.heap) == 1:
            return
        packetSeq = self.sendAgain.heap[1][1]
        self.sendAgain.DecreaseKey(packetSeq, time.time() + self.timeToWait)
        self.sendBuffer(self.packets[packetSeq])

    # "{
    # "seq": ,
    # "checksum": ,
    # "data": ,
    # "type":
    #   }"                  <- packet formula expected
    # This method supposed to be a thread's func to receive messages constantly from the client.
    def receiveARQ(self):
        global BUFFERSIZE
        waiting = True
        # timeStamp = time.time()
        while waiting:
            data, addr = self.sock.recvfrom(BUFFERSIZE)
            # try to loads the dict if exception occurs then there was a corruption
            try:
                # raises ValueError
                dPacket: dict = self.readJsonIntoDict(data.decode("utf - 8"))
                packetSeq: int = dPacket["seq"]
                # handles the possible outcomes of the received packet
                self.handleARQ(packetSeq=packetSeq, dPacket=dPacket)
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

    def handleARQ(self, packetSeq: int, dPacket: dict):
        try:
            # value does not exist in dict- might be multiple ACK that are received after a timeout...
            # don't care
            if packetSeq not in self.packets.keys():
                return
            if dPacket["type"] == "ACK":
                # value exists in dict then remove it. No need to send it again it is received safely
                # send the next new packet
                self.packets.pop(packetSeq)
                self.sendAgain.remove(packetSeq)
                self.sendNewPacket()
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
        packet = {
            "seq": "",
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
        self.sendBuffer(json.dumps(packet))

    def stopServer(self):
        self.sendStopPacket()
        self.running = False
    # go back n, stop and wait, selective repeat,
    # slow start, threshold, cut in half,
