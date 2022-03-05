import json
import socket
import unittest
import socket
import threading
import CLIENT.RDTClient
import SERVER.RDTServer
from Algorithms import checksum
from SERVER import RDTServer
from CLIENT import RDTClient

SERVERADDR = ("127.0.0.1", 55000)
CLIENTADDR = ("127.0.0.1", 55001)
files = ["../FILES/baby_shark.txt", "../FILES/image1.jpeg", "../FILES/trump.txt"]


class reliable(unittest.TestCase):
    def setUp(self):
        # The goal is to test different files and see whether we received them corrupt or not.
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serversock.bind(SERVERADDR)
        #self.serverCC = SERVER.RDTServer.RDT(files[0], self.serversock, CLIENTADDR)
        #self.serverCC = SERVER.RDTServer.RDT(files[1], self.serversock, CLIENTADDR)
        self.serverCC = SERVER.RDTServer.RDT(files[2], self.serversock, CLIENTADDR)

        self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientsock.bind(CLIENTADDR)
        #self.clientCC = CLIENT.RDTClient.RDT(self.clientsock, SERVERADDR)
        #self.clientCC = CLIENT.RDTClient.RDT("image1.jpeg", self.clientsock, SERVERADDR)
        self.clientCC = CLIENT.RDTClient.RDT(self.clientsock, SERVERADDR)
        self.clientCC.addFile("trump.txt")
        #self.clientCC.addFile("baby_shark.txt")

    def serverThreadFunc(self):
        self.serverCC.startServer()

    def clientThreadFunc(self):
        self.clientCC.startReceiving()

    ## SERVER TESTS
    def test_startServer(self):
        t1 = threading.Thread(target=self.serverThreadFunc)
        t2 = threading.Thread(target=self.clientThreadFunc)
        t2.start()
        t1.start()
        t1.join()
        t2.join()
        # self.serversock.close()
        # self.clientsock.close()

    def test_closeServer(self):
        pass

    def test_sendBuffer(self):
        pass

    def test_generateNewPacket(self):
        # check if the generated buffer matches the buffersize set
        packet = self.serverCC.generateNewPacket()
        print(packet)
        self.assertEqual(len(packet) + 2, 1024)
        d = json.loads(packet)
        self.assertFalse(checksum.checkCurroption(d["data"], d["checksum"]))
        self.serverCC.reader.close()

    def test_generateACKPacket(self):
        # check if req packet satisfies the buffersize
        self.assertEqual(len(self.serverCC.generateRequestForAckPacket(0)), 1024)

    def test_readFromFile(self):
        # check if the reader returns accurate number of bytes
        self.assertEqual(len(self.serverCC.readFromFile(1000)), 1000)

    def test_receiveARQ(self):
        pass

    ## CLIENT TESTS
    def test_startClient(self):
        pass
