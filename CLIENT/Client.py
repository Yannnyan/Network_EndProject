import json
import socket
import threading

PORT = 49152
PORTSERVER = 49153
FORMAT = "utf - 8"
BUFFERSIZE = 1024


class Client_:

    def __init__(self, IP, name):
        self.sock_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_.bind((IP, PORT))
        self.IP = IP
        self.name = name
        self.client_Running = True

    # '{"connect" : "Joseph"}
    def connect(self, name) -> str:
        self.name = name
        message = json.dumps({"connect": name})
        addr = (self.IP, PORTSERVER)
        print(addr)
        self.sock_.sendto(message.encode(FORMAT), addr)
        r , ad= self.sock_.recvfrom(BUFFERSIZE)
        return r.decode(FORMAT)

    # '{"whoOnline" : ""}'
    def get_users(self):
        message = json.dumps({"whoOnline": ""})
        self.sock_.sendto(message.encode(FORMAT), (self.IP, PORTSERVER))

    # '{"dc" : ""}'
    def disconnect(self):
        message = json.dumps({"dc": self.name})
        self.sock_.sendto(message.encode(FORMAT), (self.IP, PORTSERVER))
        self.client_Running = False
        self.sock_.close()
        print("[CLIENT] Disconnected!")

    # '{"msg" : "message text"}'
    def sendMessage(self, msg: str, reciever: str):
        message = json.dumps({"mgs": [reciever, msg]})
        self.sock_.sendto(message.encode(FORMAT), (self.IP, PORTSERVER))

    # '{"msgall" : "message text"}'
    def set_msg_all(self, msg):
        message = json.dumps({"msgall": msg})
        self.sock_.sendto(message.encode(FORMAT), (self.IP, PORTSERVER))

    # '{"files" : ""}'
    def get_list_file(self):
        self.client_Running = False
        message = json.dumps({"files": ""})
        self.sock_.sendto(message.encode(FORMAT), (self.IP, PORTSERVER))

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
