import socket

serveraddr = ("127.0.0.1", 55000)
clientaddr = ("127.0.0.1",55001)

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
clientsocket.bind(("127.0.0.1", 55001))
clientsocket.sendto("connect".encode("utf - 8"), serveraddr)

keepgoing = True
with open("clientBaby_shark.txt","w") as file:
    while keepgoing:
        data, addr = clientsocket.recvfrom(1024)
        file.write(data.decode("utf - 8"))
        if data.decode("utf - 8") == "finish":
            keepgoing = False
    file.close()



