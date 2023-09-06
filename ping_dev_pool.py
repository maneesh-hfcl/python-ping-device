import os
import keyboard
import time
from threading import Thread, Event
from multiprocessing import Queue
from Model.cserver import CServer
from concurrent.futures import ThreadPoolExecutor
import datetime
import socket
import sys

#q = Queue()

def getPingAllIpPort(q: Queue):
    pool = ThreadPoolExecutor(5)    
    print("calling the function")
    str_file_list = []
    inplist_arr = []
    
    with open("listIpPort.txt") as file:
        inplist = file.read()
        str_file_list = inplist.splitlines()

    for machineip in str_file_list:
        print(f"start - {machineip}")
        cserver = CServer(machineip)
        inplist_arr.append(cserver)

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


def connSocket(pool, q, event, cserver):
    #while True:
    if event.is_set():
        print("Event shutdown ")
        pool.shutdown()
        return

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("socket successfully created")
        clientIpAddr = cserver.ipAddress
        port = int(cserver.port)
        cserver.datetime = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
        print(f"connecting to socket : {clientIpAddr},{port}")
        s.connect((clientIpAddr, port))
        cserver.status = "Active"
        print('connecting cserver status')
        #print(f"{cserver.status}/{cserver.lastStatus}" )
    except socket.error as err:
        print('socket Error!')
        print(err)
        cserver.status = "Inactive"
        #print(f"socket error :: status = {cserver.status}, laststatus = {cserver.lastStatus}" )
    except ex as ex:
        cserver.status = "Inactive"
        print('Error!')
        print(ex)
        #print(f"Error, status = {cserver.status} , laststatus = {cserver.lastStatus}" )

    print("after exception called")
    
    print(f"status = {cserver.status} , laststatus = {cserver.lastStatus}" )
    cserver.info = "" 
    if cserver.lastStatus != cserver.status:
        print('checking last status')
        q.put(dict({"ip": cserver.getIPAddressPort(), "status": cserver.status, 
                        "dt": cserver.datetime, "info": cserver.info}))
        cserver.lastStatus = cserver.status   
        # yield dict({"ipadd": ipaddr, "status": "Active"})
    #time.sleep(2)



def itrIPList(pool, inplist_arr, q, event):
    while True:
        print("---------------------------------------------------------")
        for clsip in inplist_arr:
    #        t.append(Thread(target= pingSrvr, args=(q, event, cserver), name=f't[{ithrd}]'))
            pool.submit(connSocket, pool, q, event, clsip)
        time.sleep(15)


if __name__ == "__main__":
    print("Started pinging device with port")
    q = Queue()
    getPingAllIpPort(q)

