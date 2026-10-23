import asyncio
import time
from datetime import datetime

async def request(request_id,delay):
    print("id:",request_id)
    print("start:",datetime.now())
    await asyncio.sleep(delay)
    print("end:",datetime.now(),request_id)
    return f"result-{request_id}"

async def main():
    print("start:",datetime.now())
    start=time.perf_counter()
    async with asyncio.TaskGroup() as tg:
        task1=tg.create_task(request(1,3))
        task2=tg.create_task(request(2,1))
        task3=tg.create_task(request(3,2))
    result=[task1.result(),task2.result(),task3.result()]
    print(result)
    elapsed=time.perf_counter()-start
    print("end:",datetime.now(),elapsed)

if __name__=="__main__":
    asyncio.run(main())