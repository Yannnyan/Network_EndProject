import socket

PORT = "5050"
IP = "127.0.0.1"
FORMAT = "utf - 8"
BUFFERSIZE = 1024


class Client_:

    def __init__(self):
        self.sock_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self):
        pass

    def get_users(self) -> []:
        pass

    def disconnect(self):
        self.sock_.close()

    def sendMessage(self):
        message = "client says hello"
        self.sock_.sendto(bytes(message).encode(FORMAT), IP)
        data, addr = self.sock_.recvfrom(BUFFERSIZE)
        print(data)
        self.disconnect()

    # sends message to everyone in the chat
    def set_msg_all(self):
        pass

    def get_list_file(self) -> []:
        pass

    def download_file(self, name_of_file):
        pass

    # proceed to download file ?
    def proceed(self):
        pass
