import os
import keyboard
import time
from threading import Thread, Event
from multiprocessing import Queue
from Model.cserver import CServer

#q = Queue()

def getAllIpOld(q: Queue):
    
    print("calling the function")
    inplist_arr = []
    with open("listIp.txt") as file:
        inplist = file.read()
        inplist_arr = inplist.splitlines()
    
    event = Event()
    st = time.time()
    ithrd = 0
    t = []
    for machineip in inplist_arr:
        ithrd = ithrd + 1
        print(f"start - {machineip}")
        cserver = CServer(machineip)
        t.append(Thread(target= pingSrvr, args=(q, event, cserver), name=f't[{ithrd}]'))
        print(machineip)
        #pingSrvr(machineip)
    for thrd in t:
            thrd.start()

    while True:
        if keyboard.is_pressed('q'):
            print("you press the keys")
            event.set()
            break
            
    for thrd in t:
        thrd.join()

    print(time.time() - st)
    

def pingSrvr(q, event, cserver):
    while True:
        if event.is_set():
            break
        res = os.popen(f"ping -n 1 {cserver.ipAddress}").read()
        #print(res.lower())
        if (("request timed out") in res.lower()) or (("unreachable") in res.lower()):
#            print(f"{ipaddr} - Not reachable")
            if cserver.lastStatus != "Inactive":
                q.put(dict({"ip": cserver.ipAddress, "status": "Inactive"}))
                cserver.lastStatus = "Inactive"
           # yield dict({"ipadd": ipaddr, "status": "Not reachable"})
        else:
            if cserver.lastStatus != "Active":
                q.put(dict({"ip": cserver.ipAddress, "status": "Active"}))
                cserver.lastStatus = "Active"
           # yield dict({"ipadd": ipaddr, "status": "Active"})
      

def getAllIp2():
    print("second function called")

if __name__ == "__main__":
    print("main called")
    q = Queue()
    getAllIp2()
    getAllIp()
    # pingSrvr("172.17.26.57")
