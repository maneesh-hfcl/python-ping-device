import os
import keyboard
import time
from threading import Thread, Event
from multiprocessing import Queue
from Model.cserver import CServer
from concurrent.futures import ThreadPoolExecutor
import datetime

#q = Queue()

def getAllIp(q: Queue):
    pool = ThreadPoolExecutor(5)    
    print("calling the function")
    inplist_arr = []
    with open("listIp.txt") as file:
        inplist = file.read()
        inplist_arr = inplist.splitlines()
    
    event = Event()
    st = time.time()
    ithrd = 0
    t = Thread(target=itrIPList, args=(pool, inplist_arr, q, event,))
    t.start()    
    while True:
        if keyboard.is_pressed('q'):
            print("you press the keys")
            event.set()
            break
        # if q.qsize() > 0:
        #     print(q.get())
    print(time.time() - st)


def pingSrvr(pool, q, event, cserver):
    #while True:
    if event.is_set():
        print("Event shutdown ")
        pool.shutdown()
        return
    res = os.popen(f"ping -n 1 {cserver.ipAddress}").read()
    #print(res.lower())
    cserver.datetime = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
#    if (("request timed out") in res.lower()) or (("unreachable") in res.lower()):
    if (("request timed out") in res.lower()) or (("unreachable") in res.lower()):
#            print(f"{ipaddr} - Not reachable")
        cserver.status = "Inactive"
        cserver.info = res.lower() 
         # yield dict({"ipadd": ipaddr, "status": "Not reachable"})
    else:
        cserver.status = "Active"
        cserver.info = "" 
    if cserver.lastStatus != cserver.status:
        q.put(dict({"ip": cserver.ipAddress, "status": cserver.status, 
                        "dt": cserver.datetime, "info": cserver.info}))
        cserver.lastStatus = cserver.status   
        # yield dict({"ipadd": ipaddr, "status": "Active"})
    #time.sleep(2)

def getAllIp2():
    print("second function called")


def itrIPList(pool, inplist_arr, q, event):
    while True:
        print("---------------------------------------------------------")
        for machineip in inplist_arr:
#            print(f"start - {machineip}")
            cserver = CServer(machineip)
    #        t.append(Thread(target= pingSrvr, args=(q, event, cserver), name=f't[{ithrd}]'))
            pool.submit(pingSrvr, pool, q, event, cserver)
        time.sleep(15)


if __name__ == "__main__":
    print("main called")
    q = Queue()
    getAllIp2()
    getAllIp(q)
    # cserver = CServer(ipAdd="172.17.26.47")
    # pool = ThreadPoolExecutor(2)
    # event =Event()
    # pool.submit(pingSrvr, q, event, cserver)
    # while True:
    #     if keyboard.is_pressed('q'):
    #         print("you press the keys")
    #         event.set()
    #     if q.qsize() > 0:
    #         print(q.get())
