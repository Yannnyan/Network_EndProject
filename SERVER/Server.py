import json
import socket

PORT = 49153
IP = "127.0.0.1"
FORMAT = "utf - 8"
BUFFERSIZE = 1024


class Server_():

    def __init__(self):
        # The SOCK_STREAM represents UDP connection
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_.bind((IP, PORT))
        self.clients = {}  # {name : (ip,port) }
        self.files = []  # [filenames]

    def runServer(self):
        while True:
            data, addr = self.socket_.recvfrom(BUFFERSIZE)
            print("[SERVER] Received message from client. " + data.decode(FORMAT))
            self.executeCommand(data, addr)

    def executeCommand(self, command: bytes, addr: (str, int)):
        d: dict = json.loads(command.decode(FORMAT))
        ex = list(d.keys())[0]
        val = list(d.values())[0]
        print(addr)
        if ex == "whoOnline":
            message = self.onlineClients()
            self.sendMessageToClient(message, addr)
        elif ex == "connect":
            self.connectClient(addr, val)
        elif ex == "dc":
            self.clients.pop(val)
        elif ex == "msg":
            if val[0] in self.clients.keys():
                message = json.dumps({"msg": val[1]})
                self.sendMessageToClient(self.onlineClients(), addr)
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

    def listFiles(self) -> str:
        return json.dumps({"files": self.files})

    def sendMessageToClient(self, message: str, addr: (str, int)):
        self.socket_.sendto(message.encode(FORMAT), addr)

    def connectClient(self, addr: (str, int), name: str):
        if name not in self.clients.keys():
            self.clients[name] = addr
            print("[SERVER] Client " + name + " has connected.")
            print("[SERVER] " + str(self.clients[name][0]) + " , " + str(self.clients[name][1]))
            message = json.dumps({"connect": name})
            self.sendMessageToClient(message, self.clients[name])
        else:
            print("[SERVER] Client is already connected.")


def main():
    Server_().runServer()


if __name__ == '__main__':
    main()
