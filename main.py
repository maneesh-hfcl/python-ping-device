import uvicorn
import asyncio
from fastapi import FastAPI, Request, Response, Form
from sse_starlette.sse import EventSourceResponse
from ping_server_pool import getAllIp
from ping_dev_pool import getPingAllIpPort
from multiprocessing import Queue
from threading import Thread
from Model.cserver import CServer
from fastapi.middleware.cors import CORSMiddleware
import json
from threading import Event
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Model.helper import  GetPingFromDBDevice,GetDBConfig, hlpr_GetDBInfo,hlpr_SaveDBConfig

app = FastAPI()

app.mount("/static", StaticFiles(directory="html/static"), name="static")

templates = Jinja2Templates(directory="html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

eventping = Event()
eventdevport = Event()
response_msg = ""


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/sse")
async def sse():
    generator = numbers(1,25)
    return EventSourceResponse(generator)

@app.get("/sse-ping")
async def pingdevice():
    q = Queue()
    pingthrd = Thread(target=getAllIp, args=(q,), name="sse-ping")
    pingthrd.start()
    print("calling sse-ping")
    generatePing = getPingData(q)
    return EventSourceResponse(generatePing)


@app.get("/sse-ping-db-device")
async def pingdevice():
    q = Queue()
    pingthrd = Thread(target=GetPingFromDBDevice, args=(q,), name="sse-ping-db-device")
    pingthrd.start()
    print("calling sse-ping")
    generatePing = getPingData(q)
    return EventSourceResponse(generatePing)


@app.get("/pobject")
def pingobject():
    cserver =  CServer("127.1.1.1")
    cserver.lastStatus = "Active"
    return cserver

@app.get("/default/ping", response_class=HTMLResponse)
async def read_htmlping(request: Request):
    global response_msg
    server, username, passwd, dbname  = GetDBConfig()
    response_data = {"server": server, "username": username, "passwd": passwd, "dbname": dbname}
    res = {"request": request, "response": response_data, "response_msg": response_msg}
    response_msg = ""
    return templates.TemplateResponse("pingdevice.html", res)


@app.get("/sse-ping-device")
async def pingdevice():
    qdev = Queue()
    pingthrd = Thread(target=getPingAllIpPort, args=(qdev, eventdevport), name="sse-ping-device")
    pingthrd.start()
    print("calling sse-ping-device")
    generatePing = getPingData(qdev)
    return EventSourceResponse(generatePing)


@app.get("/default/pingdevport", response_class=HTMLResponse)
async def read_htmlpingdevport(request: Request):
    res = {"request": request}
    return templates.TemplateResponse("pingdevport.html",res)

@app.get("/stoppingdev")
async def stoppingdev():
    print("calling stopping function")
    eventdevport.set()
    return "stopped event called"

@app.get("/dbinfo")
async def getdbinfo():
    return hlpr_GetDBInfo()

@app.post("/default/ping", response_class=RedirectResponse, status_code=302)
async def savedbconfig(request:Request):
    form_data = await request.form()
    dbserver = form_data["server"]
    dbusername = form_data["username"]
    dbpassword = form_data["passwd"] 
    dbname = form_data["dbname"]
    #print(form_data["server"] + " : " + form_data["username"] + " : " + form_data["passwd"] + " : " + form_data["dbname"])
    ret_val = hlpr_SaveDBConfig(dbserver, dbusername, dbpassword, dbname)
    print(ret_val)
    response = ""
    if ret_val == "success":
        response = "Database configuration successfully saved!"
    else:
        response = "Error! in saving the DB configuration"
 #   server, username, passwd, dbname  = GetDBConfig()
 #   response_data = {"server": server, "username": username, "passwd": passwd, "dbname": dbname}
 #   res = {"response": response_data, "respnose_msg":response}
    global response_msg
    response_msg = response
    return "/default/ping"



def getPingData(q: Queue):
#    return f"pinging data from server. qsize: {q.qsize()}"
    while True:
#        print(f"q: {q.qsize()}")
        if q.qsize() > 0:
            print("getting q data")
            data_recvd = json.dumps(q.get())
            yield dict(data = data_recvd)


async def numbers(minimum, maximum):
    for i in range(minimum, maximum + 1):
        await asyncio.sleep(1)
        yield dict(data = i)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088, log_level='info')