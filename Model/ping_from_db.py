import os
import keyboard
import time
from threading import Thread, Event
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
import datetime
from Model.clsdevice import ClsDevice

#q = Queue()

def getPingFrmDB(q: Queue, lstDevices: []):
    pool = ThreadPoolExecutor(15)    
    print("calling the function")
    #lstDev = GetDBDevice()
    inplist_arr = lstDevices
    # with open("listIp.txt") as file:
    #     inplist = file.read()
    #     inplist_arr = inplist.splitlines()
    print(inplist_arr)
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
        if q.qsize() > 0:
             print(q.get())
    print(time.time() - st)


def pingSrvr(pool, q, event, cdevice):
    #while True:
    if event.is_set():
        print("Event shutdown ")
        return
    res = os.popen(f"ping -n 1 {cdevice.ipAddress}").read()
    #print(res.lower())
    cdevice.datetime = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
#    if (("request timed out") in res.lower()) or (("unreachable") in res.lower()):
    if (("request timed out") in res.lower()) or (("unreachable") in res.lower()):
#            print(f"{ipaddr} - Not reachable")
        cdevice.status = "Inactive"
        cdevice.info = res.lower() 
         # yield dict({"ipadd": ipaddr, "status": "Not reachable"})
    else:
        cdevice.status = "Active"
        cdevice.info = "" 
    if cdevice.lastStatus != cdevice.status:
        q.put(dict({"ip": cdevice.ipAddress,"name": cdevice.name, "status": cdevice.status, 
                        "dt": cdevice.datetime, "info": cdevice.info, "type": cdevice.type}))
        cdevice.lastStatus = cdevice.status   
        # yield dict({"ipadd": ipaddr, "status": "Active"})
    #time.sleep(2)

def getAllIp2():
    print("second function called")


def itrIPList(pool, inplist_arr, q, event):
    while True:
        print("---------------------------------------------------------")
        for machineip in inplist_arr:
            print(f"start - {machineip}")
            print(machineip)
            cserver = ClsDevice(machineip)
    #        t.append(Thread(target= pingSrvr, args=(q, event, cserver), name=f't[{ithrd}]'))
            pool.submit(pingSrvr, pool, q, event, cserver)
        time.sleep(2)


if __name__ == "__main__":
    print("main called")
    q = Queue()
    getPingFrmDB(q)
#    getAllIp2()
#    getAllIp(q)
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
