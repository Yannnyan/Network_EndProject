import json
import socket
import threading
from CLIENT import portsManager

PORT = None
PORTSERVER = 49153
FORMAT = "utf - 8"
BUFFERSIZE = 1024


class Client_:

    def __init__(self, IP, name):
        self.SERVERIP = IP
        self.name = name
        self.client_Running = True
        self.sock_ = None

    # '{"connect" : "Joseph"}
    def connect(self):
        global PORT, PORTSERVER
        PORT = portsManager.getPort()
        self.sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_.bind((self.SERVERIP, PORT))
        addr = (self.SERVERIP, PORTSERVER)
        self.sock_.connect(addr)

        message = json.dumps({"connect": self.name})
        self.sock_.sendall(message.encode(FORMAT))

    # '{"whoOnline" : ""}'
    def get_users(self):
        message = json.dumps({"whoOnline": ""})
        self.sock_.sendall(message.encode(FORMAT))

    # '{"dc" : ""}'
    def disconnect(self):
        message = json.dumps({"dc": self.name})
        self.sock_.sendall(message.encode(FORMAT))
        self.client_Running = False
        self.sock_.close()
        portsManager.disconnectPort(PORT)
        print("[CLIENT] Disconnected!")

    # '{"msg" : "message text"}'
    def sendMessage(self, msg: str, receiver: str):
        message = json.dumps({"msg": [receiver, msg]})
        self.sock_.sendall(message.encode(FORMAT))

    # '{"msgall" : "message text"}'
    def set_msg_all(self, msg):
        message = json.dumps({"msgall": msg})
        self.sock_.sendall(message.encode(FORMAT))

    # '{"files" : ""}'
    def get_list_file(self):
        self.client_Running = False
        message = json.dumps({"files": ""})
        self.sock_.sendall(message.encode(FORMAT))

    # '{"download" : "name_of_file"}'
    def download_file(self, name_of_file):
        pass

    # '{"proceed" : ""}'
    # proceed to download file ?
    def proceed(self):
        pass

    def listenClient(self) -> str:
        data, addr = self.sock_.recvfrom(BUFFERSIZE)
        serData = data.decode(FORMAT)
        print("[CLIENT] " + " received data")
        return serData


def main():
    pass


if __name__ == '__main__':
    main()
