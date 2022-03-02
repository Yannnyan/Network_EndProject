import socket
import threading
import json
from Algorithms import checksum
import heapq

BUFFERSIZE = 1024


class CC:
    def __init__(self, filename: str, sock: socket.socket, serverAddress: (str, int)):
        self.sock = sock
        self.serverAddress = serverAddress
        self.running = True
        self.sequenceNumber = 0
        self.packets = {}  # {seq num: buffer}
        self.heapSequencePacket = []  # heap contains sequence numbers received
        self.listeningThread = threading.Thread(target=self.receivePackets)
        self.writer = open(filename, "wb")

    # main function in this class
    def startReceiving(self):
        self.listeningThread.start()
        while self.running:
            self.receivePackets()
        self.writer.close()

    def receivePackets(self):
        while self.running:
            data, addr = self.sock.recvfrom(BUFFERSIZE)
            self.handlePacket(data.decode("utf - 8"))

    # "{
    # "seq": ,
    # "checksum": ,
    # "data": ,
    # "type":
    #   }"                  <- packet formula expected
    def unpackPacket(self, packet) -> dict:
        try:
            d: dict = json.loads(packet)
            return d
        except ValueError:
            raise ValueError

    # writer uses the heap to know in which order to write the packets received,
    # if the packets are received in the wrong order, the writer will not write those packets down
    # but it will wait until the sequence number matches
    # this way we can keep the file transfered the same as it was the server's hands
    # we do this instead of keeping all the packets in the dict because it saves space for more options
    # when the file is large it might be a problem to keep all the buffers in a data structure
    def writePacket(self):
        seqNum = self.heapSequencePacket[0]
        while seqNum == self.sequenceNumber:
            heapq.heappop(self.heapSequencePacket)
            buffer = self.packets.pop(seqNum)
            self.writer.write(buffer)
            self.sequenceNumber += 1

    def handlePacket(self, packet):
        try:
            dPacket = self.unpackPacket(packet=packet)
            if checksum.checkCurroption(dPacket["data"], dPacket["checksum"]):
                self.sendNACK(dPacket["seq"]) # currupted message, send another.
            else:
                packetSeq = dPacket["seq"]
                self.packets[packetSeq] = dPacket["data"]
                heapq.heappush(self.heapSequencePacket, packetSeq)
                self.sendACK(packetSeq=packetSeq)
                self.writePacket() # each time good packet is received it checks whether the file can write
        except ValueError:
            # don't care server will send another packet
            pass

    def generateNACKPacket(self, seqNum: int)-> str:
        packet = {
            "seq": seqNum,
            "checksum": "",
            "data": "",
            "type": "NACK"
        }
        return json.dumps(packet)

    def generateACKPacket(self, seqNum: int) -> str:
        packet = {
            "seq": seqNum,
            "checksum": "",
            "data": "",
            "type": "ACK"
        }
        return json.dumps(packet)

    def sendACK(self, packetSeq):
        packet = self.generateACKPacket(packetSeq).encode("utf - 8")
        self.sock.sendto(packet, self.serverAddress)

    def sendNACK(self, packetSeq):
        packet = self.generateNACKPacket(packetSeq)
        self.sock.sendto(packet,self.serverAddress)
