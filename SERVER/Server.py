import socket


def main():
    Server_().runServer()


class Server_():

    def __init__(self):
        # The SOCK_STREAM represents UDP connection
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def runServer(self):
        pass


if __name__ == '__main__':
    main()
