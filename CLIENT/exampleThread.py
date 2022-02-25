import threading
import time
import CLIENT.Client


def threadfunc():
    while True:
        client.listenClient()
        print("got message")


client = CLIENT.Client.Client_("127.0.0.0", 49153)
thread1 = threading.Thread(target=threadfunc)
thread1.start()
client.get_users()
# threadfunc(2)
