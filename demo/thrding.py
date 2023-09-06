import threading
import time

def worker(num):
    print("Starting")
    time.sleep(3)
    print("Done")
    print(num**2)


t1 = threading.Thread(target = worker, args= (1,),name="first")
t1.start()
t2 = threading.Thread(target=worker, args=(2,), name="t2")
t2.start()
t3 = threading.Thread(target=worker, name="t3")
t3.start()
t4 = threading.Thread(target=worker, name="t4")
t5 = threading.Thread(target=worker, name="t5")
t6 = threading.Thread(target=worker, name="t6")
t7 = threading.Thread(target=worker, name="t7")
t8 = threading.Thread(target=worker, name="t8")
t9 = threading.Thread(target=worker, name="t9")
t10 = threading.Thread(target=worker, name="t10")


time.sleep(3)

t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
t9.start()
t10.start()