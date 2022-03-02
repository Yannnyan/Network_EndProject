import socket
import unittest
import socket
import threading
import CLIENT.CongestionControl
import SERVER.CongestionControl
from SERVER import CongestionControl
from CLIENT import CongestionControl

SERVERADDR = ("127.0.0.1", 55000)
CLIENTADDR = ("127.0.0.1", 55001)
files = ["../FILES/baby_shark.txt"]


class reliable(unittest.TestCase):
    def setUp(self):
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serversock.bind(SERVERADDR)
        self.serverCC = SERVER.CongestionControl.CC(files[0], self.serversock, CLIENTADDR)
        self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientsock.bind(CLIENTADDR)
        self.clientCC = CLIENT.CongestionControl.CC("baby_shark_client.txt", self.clientsock, SERVERADDR)

    def serverThreadFunc(self):
        self.serverCC.startSending()

    def clientThreadFunc(self):
        self.clientCC.startReceiving()

    ## SERVER TESTS
    def test_startServer(self):
        t1 = threading.Thread(target=self.serverThreadFunc)
        t2 = threading.Thread(target=self.clientThreadFunc)
        t1.start()
        t2.start()

    def test_sendBuffer(self):
        pass

    def test_generateNewPacket(self):
        # check if the generated buffer matches the buffersize set
        self.assertEqual(len(self.serverCC.generateNewPacket()), 1024)
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
