import json
import socket
import threading
import os
from functools import partial
from os.path import isfile, join
import time
import sys

sys.path.append(sys.path[0] + "/..")
from Algorithms import portsManager
import SERVER.RDTServer

PORT = 49153
IP = "127.0.0.1"
FORMAT = "utf - 8"
BUFFERSIZE = 1024


class Server_():

    def __init__(self):
        # The SOCK_STREAM represents TCP connection
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_.bind((IP, PORT))
        self.socket_.listen(15)

        self.clients = {}  # {name : (ip,port) }
        self.files = [f for f in os.listdir("../FILES") if isfile(join("../FILES", f))]  # [filenames]
        self.connectionDict = {}  # { addr : (connection, thread, isrunning, client port for udp, server port for udp)}
        self.udpsockets = {}  # { address client udp : server socket udp }
        self.acceptConnections()
        self.timer = None

    def acceptConnections(self):
        while len(self.connectionDict.keys()) <= 15:
            print("listening to connections")
            try:
                connection, addr = self.socket_.accept()
                thread = threading.Thread(target=self.listenThread, args=[addr])
                self.connectionDict[addr] = [connection, thread, True, None,
                                             portsManager.getPortServer()]  # True represents that the thread is alive
                print(self.connectionDict[addr])
                # self.threadPool.append(thread)
                thread.start()
            except (OSError, KeyboardInterrupt):
                self.socket_.close()
                portsManager.resetFile()
                break

    def listenThread(self, addressClient):
        try:
            while (self.connectionDict[addressClient])[2]:
                data, addr = (self.connectionDict[addressClient])[0].recvfrom(BUFFERSIZE)
                print("[SERVER] Received message from client. " + data.decode(FORMAT))
                listjsons = data.decode(FORMAT).split("}{")
                if len(listjsons) != 1:
                    for i in range(len(listjsons)):
                        if i % 2 == 0:
                            listjsons[i] = listjsons[i] + "}"
                        else:
                            listjsons[i] = "{" + listjsons[i]
                for son in listjsons:
                    self.executeCommand(son, addressClient)

        except (OSError, KeyError, ValueError):
            return

    # '{"connect" : "name"}'
    def executeCommand(self, command: str, addr: (str, int)):
        d: dict = json.loads(command)
        ex = list(d.keys())[0]
        val = list(d.values())[0]
        if ex == "whoOnline":
            message = self.onlineClients()
            self.sendMessageToClient(message, addr)
        elif ex == "updateOnline":
            message = self.updateOnlineClients()
            for address in self.clients.values():
                self.sendMessageToClient(message, address)
        elif ex == "connect":
            self.connectClient(addr, val)
        elif ex == "dc":
            self.connectionDict[addr][0].close()
            self.connectionDict.pop(addr)
            self.clients.pop(val)
            try:
                self.udpsockets[addr].sock.close()
            except KeyError:
                return
        elif ex == "msg":
            if val[0] in self.clients.keys():
                message1 = json.dumps({"msg": val[1]})
                self.sendMessageToClient(message1, self.clients[val[0]])
                if self.clients[val[0]] != addr:
                    self.sendMessageToClient(message1, addr)
            else:
                print("[SERVER] Client is not online!")
        elif ex == "msgall":
            message = json.dumps({"msg": val})
            for client in self.clients.keys():
                self.sendMessageToClient(message, self.clients[client])
        elif ex == "files":
            self.sendMessageToClient(self.listFiles(), addr)
        elif ex == "download":
            clientUdpPort = self.connectionDict[addr][3]
            print("creating socket")
            RDTsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(self.connectionDict[addr][4])
            RDTsock.bind((IP, self.connectionDict[addr][4]))
            clientIP = addr[0]
            print("creating rdt socket")
            self.udpsockets[(addr[0], clientUdpPort)] = SERVER.RDTServer.RDT(val, RDTsock,
                                                                             (clientIP, clientUdpPort))
            print(self.udpsockets[(addr[0], clientUdpPort)])
            sock = self.udpsockets[(addr[0], clientUdpPort)]
            sock.startServer()
            tellClient = partial(self.clientDownloadUpdate ,addr, sock)
            self.timer = threading.Thread(target= tellClient)
            self.timer.start()
        elif ex == "proceed":
            self.udpsockets[(addr[0], self.connectionDict[addr][3])]

    def clientDownloadUpdate(self, addr, sock):
        run = True
        while run:
            precent = (sock.changeBytes("get") / sock.sizeFile) * 100
            sock.lock.release()
            self.sendMessageToClient(json.dumps({"updateDownload": precent}), addr)
            time.sleep(2)
            if sock.changeIsRunning("get") is False:
                sock.lock.release()
                run = False
                continue
            sock.lock.release()


    # returns json format for the online clients connected to the server
    def onlineClients(self):
        dictin = {"whoOnline": list(self.clients.keys())}
        return json.dumps(dictin)

    def updateOnlineClients(self):
        dictin = {"updateOnline": list(self.clients.keys())}
        return json.dumps(dictin)

    def listFiles(self) -> str:
        return json.dumps({"files": self.files})

    def sendMessageToClient(self, message: str, addr: (str, int)):
        self.connectionDict[addr][0].sendall(message.encode(FORMAT))

    def connectClient(self, addr: (str, int), val: list):
        name = val[0]
        port = val[1]
        if name not in self.clients.keys():
            self.connectionDict[addr][3] = port
            self.clients[name] = addr
            print("[SERVER] Client " + name + " has connected.")
            print("[SERVER] " + str(self.clients[name][0]) + " , " + str(self.clients[name][1]))
            message = json.dumps({"connect": [name]})
            for client in self.clients:
                if client != name:
                    self.sendMessageToClient(message, self.clients[client])
            portServer = self.connectionDict[addr][4]
            print(portServer)
            message = json.dumps({"connect": [name, portServer]})
            self.sendMessageToClient(message, addr)
        else:
            print("[SERVER] Client is already connected.")


def main():
    Server_()


if __name__ == '__main__':
    main()
