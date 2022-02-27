import socket

clientsSeq = {}

serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.bind(("127.0.0.1", 55000))

data, addr = serversocket.recvfrom(1024)
clientsSeq[addr] = int(data.decode("tuf - 8"))  # sequence 3
serversocket.sendto("" + (clientsSeq[addr] + 1).encode("tuf - 8"), addr)
