import socket

clients = {}

serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.bind(("127.0.0.1", 55000))

data, addr = serversocket.recvfrom(1024)
if data.decode("utf - 8") == "connect":
    clients["client1"] = addr

with open("../FILES/baby_shark.txt") as file:
    while True:
        buffer = file.read(1024)
        if buffer == '':
            break
        serversocket.sendto(buffer.encode("utf - 8"), clients["client1"])

serversocket.sendto("finish".encode("utf - 8"), clients["client1"])
serversocket.close()
