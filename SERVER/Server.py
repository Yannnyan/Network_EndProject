import json
import socket
import threading

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
        self.files = []  # [filenames]
        self.connectionDict = {}
        # self.threadPool = []
        # self.listeningThread = threading.Thread(target=self.acceptConnections)
        # self.listeningThread.start()
        self.acceptConnections()

    def acceptConnections(self):
        while len(self.connectionDict.keys()) <= 15:
            print("listening to connections")
            connection, addr = self.socket_.accept()
            thread = threading.Thread(target=self.listenThread, args=[addr])
            self.connectionDict[addr] = (connection, thread, True)  # True represents that the thread is alive
            print(self.connectionDict[addr])
            # self.threadPool.append(thread)
            thread.start()


    def listenThread(self, addressClient):
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
            self.clients.pop(val)
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

    def connectClient(self, addr: (str, int), name: str):
        if name not in self.clients.keys():
            self.clients[name] = addr
            print("[SERVER] Client " + name + " has connected.")
            print("[SERVER] " + str(self.clients[name][0]) + " , " + str(self.clients[name][1]))
            message = json.dumps({"connect": name})
            for client in self.clients:
                self.sendMessageToClient(message, self.clients[client])
        else:
            print("[SERVER] Client is already connected.")


def main():
    Server_()


if __name__ == '__main__':
    main()
