import socket
import time
addressServer = ("127.0.0.1", 55010)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 55021))

def sendMessage():
    print("sending message1")
    try:
        sock.send("hello buddy".encode("utf - 8"))
    except:
        print("erorr")

curtime = int(round(time.time() * 1000))
sock.connect(addressServer)
while True:
    if curtime < int(round(time.time() * 1000)) - 1000:
        sendMessage()
        curtime = (time.time() * 1000) + 1000





