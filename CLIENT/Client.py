import json
import socket
import threading
PORT = 5050
IP = "127.0.0.1"
FORMAT = "utf - 8"
BUFFERSIZE = 1024


class Client_:

    def __init__(self):
        self.sock_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_Running = True
        self.name = "No name entered"
        self.listeningThread = threading.Thread(target=self.startClient)
        self.listeningThread.start()

    # loop that keeps the client listening to the server
    def startClient(self):
        while self.client_Running:
            print("[CLIENT]")
            data, addr = self.sock_.recvfrom(BUFFERSIZE)
            print("[CLIENT] " + data.decode(FORMAT))

    # '{"connect" : "Joseph"}
    def connect(self, name):
        self.name = name
        message = json.dumps({"connect": name})
        self.sock_.sendto(message.encode(FORMAT), (IP, PORT))

    # '{"whoOnline" : ""}'
    def get_users(self) -> []:
        message = json.dumps({"whoOnline": ""})
        self.sock_.sendto(message.encode(FORMAT), (IP, PORT))

    # '{"dc" : ""}'
    def disconnect(self):
        message = json.dumps({"dc": ""})
        self.sock_.sendto(message.encode(FORMAT), (IP, PORT))
        self.client_Running = False
        self.sock_.close()

    # '{"msg" : "message text"}'
    def sendMessage(self, msg: str):
        message = json.dumps({"mgs": msg})
        self.sock_.sendto(message.encode(FORMAT), (IP, PORT))

    # '{"msgall" : "message text"}'
    def set_msg_all(self, msg):
        message = json.dumps({"msgall": msg})
        self.sock_.sendto(message.encode(FORMAT),(IP, PORT))

    # '{"files" : ""}'
    def get_list_file(self):
        self.client_Running = False
        message = json.dumps({"files": ""})
        self.sock_.sendto(message.encode(FORMAT), (IP, PORT))

    # '{"download" : "name_of_file"}'
    def download_file(self, name_of_file):
        pass

    # '{"proceed" : ""}'
    # proceed to download file ?
    def proceed(self):
        pass


def main():
    Client_().sendMessage()


if __name__ == '__main__':
    main()
