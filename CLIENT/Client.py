import json
import socket

import CLIENT.RDTClient
from Algorithms import portsManager

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
        self.RDTServerPort = None
        self.RDT = None
        self.RDTSock = None

    # '{"connect" : "Joseph"}
    def connect(self):
        global PORT, PORTSERVER
        PORT = portsManager.getPort()
        self.sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_.bind((self.SERVERIP, PORT))
        addr = (self.SERVERIP, PORTSERVER)
        self.sock_.connect(addr)
        self.portRDT = portsManager.getPort()
        self.RDTSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.RDTSock.bind((self.SERVERIP,self.portRDT))

        message = json.dumps({"connect": [self.name, self.portRDT]})
        self.sock_.sendall(message.encode(FORMAT))


    def updateOnline(self):
        mes = json.dumps({"updateOnline": ""})
        self.sock_.sendall(mes.encode(FORMAT))

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
        self.RDTSock.close()
        portsManager.disconnectPort(self.portRDT)
        portsManager.disconnectPort(PORT)
        print("[CLIENT] Disconnected!")

    # '{"msg" : "message text"}'
    def sendMessage(self, msg: str, receiver: str):
        message = json.dumps({"msg": [receiver, msg]})
        self.sock_.sendall(message.encode(FORMAT))

    # '{"msgall" : "message text"}'
    def send_msg_all(self, msg):
        message = json.dumps({"msgall": msg})
        self.sock_.sendall(message.encode(FORMAT))

    # '{"files" : ""}'
    def get_list_file(self):
        message = json.dumps({"files": ""})
        self.sock_.sendall(message.encode(FORMAT))

    # '{"download" : "name_of_file"}'
    def download_file(self, name_of_file):
        self.RDT.addFile(name_of_file)
        self.RDT.startReceiving()
        message = json.dumps({"download": name_of_file})
        self.sock_.sendall(message.encode(FORMAT))

    # '{"proceed" : ""}'
    # proceed to download file ?
    def proceed(self, name_of_file):
        message = json.dumps({"proceed": name_of_file})
        self.sock_.sendall(message.encode(FORMAT))

    def listenClient(self) -> []:
        try:
            data, addr = self.sock_.recvfrom(BUFFERSIZE)
            print("[CLIENT] " + " received data")
            listjsons = data.decode(FORMAT).split("}{")
            if len(listjsons) != 1:
                for i in range(len(listjsons)):
                    if i % 2 == 0:
                        listjsons[i] = listjsons[i] + "}"
                    else:
                        listjsons[i] = "{" + listjsons[i]
            return listjsons
        except (OSError, ValueError):
            return None


def main():
    pass


if __name__ == '__main__':
    main()
