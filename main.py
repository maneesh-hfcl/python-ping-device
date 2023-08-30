import uvicorn
import asyncio
from fastapi import FastAPI, Request, Response
from sse_starlette.sse import EventSourceResponse
from ping_server import getAllIp
from multiprocessing import Queue
from threading import Thread

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/sse")
async def sse():
    generator = numbers(1,1111125)
    return EventSourceResponse(generator)

@app.get("/sse-ping")
async def pingdevice():
    q = Queue()
    pingthrd = Thread(target=getAllIp, args=(q,), name="sse-ping")
    pingthrd.start()
    print("calling sse-ping")
    generatePing = getPingData(q)
    return EventSourceResponse(generatePing)

def getPingData(q: Queue):
#    return f"pinging data from server. qsize: {q.qsize()}"
    while True:
#        print(f"q: {q.qsize()}")
        yield(q.get())


async def numbers(minimum, maximum):
    for i in range(minimum, maximum + 1):
        await asyncio.sleep(1)
        yield dict(data = i)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088, log_level='info')