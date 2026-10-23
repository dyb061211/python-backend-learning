import time
import asyncio
from datetime import datetime

def blocking_work(elapsed):
    print("Blocking work started")
    time.sleep(elapsed)
    print("Blocking work finished")

async def ticker():
    for i in range(5):
        print("Now:",datetime.now())
        await asyncio.sleep(0.5)

async def main():
    task=asyncio.create_task(ticker())
    await asyncio.sleep(0)
    await asyncio.to_thread(blocking_work,2)
    await task

if __name__ == '__main__':
    asyncio.run(main())