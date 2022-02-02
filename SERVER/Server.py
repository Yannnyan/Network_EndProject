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

    def runServer(self):
        while True:
            data, addr = self.socket_.recvfrom(BUFFERSIZE)
            print(data)
            message = bytes("server says helo").encode(FORMAT)
            self.socket_.sendto(message, addr)

        # self.socket_.bind(('', 5050))
        # self.socket_.listen(1)
        # while True:
        #     print('Ready to serve...')
        #     connectionSocket, addr = self.socket_.accept()
        #     try:
        #         message = connectionSocket.recv(1024)
        #         filename = message.split()[1]
        #         print(f"Opening File - {filename} . . . ")
        #         f = open(filename[1:])
        #         print("Reading File . . . ")
        #         outputdata = f.read()
        #         print('[HTTP OK] sending HTTP OK')
        #         connectionSocket.send('HTTP/1.0 200 OK\n\n'.encode())
        #         print('[SEND] sending contents of files')
        #         connectionSocket.send(outputdata.encode())
        #         connectionSocket.send("\r\n".encode(FORMAT))
        #         print('[CLOSE] closing connections\n')
        #         connectionSocket.close()
        #     except OSError:
        #         print("FAILED OPENING FILE DOESNT EXIST")
        #         connectionSocket.send('HTTP/1.1 404 Not Found\n\n'.encode())
        #         f = open("404eror.html")
        #         outputdata = f.read()
        #         connectionSocket.send(outputdata.encode())
        #         connectionSocket.send("\r\n".encode(FORMAT))
        #         print("\n")
        #         connectionSocket.close()
        # serverSocket.close()
        pass



def main():
    Server_().runServer()

if __name__ == '__main__':
    main()
