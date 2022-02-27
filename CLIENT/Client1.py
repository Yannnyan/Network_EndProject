import json
import socket
import threading
import time

addressServer = ("127.0.0.1", 49153)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 55000))
sock.connect(addressServer)

def listenClient():
    while True:
        data, addr = sock.recvfrom(1024)
        print(data.decode("utf - 8"))


def sendMessage(message):
    print("sending message")
    sock.sendall(message.encode("utf - 8"))


curtime = int(round(time.time() * 1000))
thread = threading.Thread(target=listenClient)
thread.start()

sendMessage(json.dumps({"connect": "yehazkel"}))
while True:
    if curtime < int(round(time.time() * 1000)) - 1000:
        sendMessage(json.dumps({"whoOnline": ""}))
        curtime = (time.time() * 1000)
