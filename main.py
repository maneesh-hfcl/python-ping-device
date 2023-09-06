import uvicorn
import asyncio
from fastapi import FastAPI, Request, Response
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
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


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

@app.get("/pobject")
def pingobject():
    cserver =  CServer("127.1.1.1")
    cserver.lastStatus = "Active"
    return cserver

@app.get("/default/ping", response_class=HTMLResponse)
async def read_htmlping(request: Request):
    res = {"request": request}
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