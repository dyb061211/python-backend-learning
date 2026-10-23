import asyncio
import time
from fastapi import FastAPI

app=FastAPI()
@app.get("/health")
def is_health():
    return {"status": "ok"}

@app.get("/sync-demo")
def sync_demo():
    time.sleep(2)
    return {"request":"ok"}

@app.get("/async-demo")
async def async_demo():
    await asyncio.sleep(2)
    return {"request":"ok"}

@app.get("/blocking-demo")
async def blocking_demo():
    time.sleep(2)
    return {"request": "ok"}