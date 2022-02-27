import socket
import threading
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 55010))
sock.listen(15)
connectionList = []
threadPool = []

def acceptConnections():
    global connectionList
    while len(connectionList) <= 15:
        print("listening to connections")
        connection, addr = sock.accept()
        connectionList.append(connection)
        thread = threading.Thread(target=recieveData, args= [connection])
        threadPool.append(thread)
        thread.start()

def recieveData(connection):
    while True:
        data, ad = connection.recvfrom(1024)
        print(data.decode("utf - 8"))
        connection.sendall("da from server".encode("utf - 8"))


thread1 = threading.Thread(target=acceptConnections)
thread1.start()

while True:
    pass

