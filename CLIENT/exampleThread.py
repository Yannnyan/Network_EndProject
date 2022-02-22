import threading
import time


def threadfunc(a):
    while True:
        print("hello from thread " + str(a))
        time.sleep(1)


thread1 = threading.Thread(target=threadfunc, args=(1,))
thread2 = threading.Thread(target=threadfunc, args=(2,))
thread1.start()
thread2.start()
#threadfunc(2)
