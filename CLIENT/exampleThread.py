import json
import threading
import time
import CLIENT.Client

#
# def threadfunc():
#     while True:
#         client.listenClient()
#         print("got message")

#
# client = CLIENT.Client.Client_("127.0.0.0", 49153)
# thread1 = threading.Thread(target=threadfunc)
# thread1.start()
# client.get_users()
# threadfunc(2)

mes = json.dumps({"dt": "val"})
sage = json.dumps({"lol": "hs"})
message = mes + sage
lis = message.split('}{')
for i in range(len(lis)):
    if i % 2 == 0:
        lis[i] = lis[i] + '}'
    else:
        lis[i] = '{' + lis[i]
print(lis)