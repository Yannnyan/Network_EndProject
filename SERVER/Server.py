import json
import socket

PORT = 5050
IP = "127.0.0.1"
FORMAT = "utf - 8"
BUFFERSIZE = 1024


class Server_():

    def __init__(self):
        # The SOCK_STREAM represents UDP connection
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_.bind((IP, PORT))
        self.clients = {}  # {name : (ip,port) }

    def runServer(self):
        while True:
            data, addr = self.socket_.recvfrom(BUFFERSIZE)
            self.executeCommand(data, addr)

    def executeCommand(self, command: bytes, addr: (str, int)):
        d: dict = json.loads(command.decode(FORMAT))
        ex = list(d.keys())[0]
        val = list(d.values())[0]
        if ex == "whoOnline":
            self.sendMessageToClient(self.onlineClients(), addr)
        if ex == "connect":
            self.connectClient(addr, val)

    def onlineClients(self) -> str:
        return json.dumps(self.clients)

    def sendMessageToClient(self, message: str, addr: (str, int)):
        self.socket_.sendto(message.encode(FORMAT), addr)

    def connectClient(self, addr: (str, int), name: str):
        if name not in self.clients.keys():
            self.clients[name] = addr
        else:
            print("[SERVER] Client is already connected.")


def main():
    Server_().runServer()


if __name__ == '__main__':
    main()
