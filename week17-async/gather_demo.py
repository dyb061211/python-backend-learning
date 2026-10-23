import asyncio
import time
from datetime import datetime

async def request(request_id,delay):
    print("id:",request_id)
    print("start:",datetime.now())
    await asyncio.sleep(delay)
    print("end:",datetime.now(),request_id)
    return f"result-{request_id}"

async def main1():
    print("start:",datetime.now())
    start = time.perf_counter()
    result=await asyncio.gather(
        request(1,4),
        request(2,1),
        request(3,3),
        request(4,2),
        request(5,1)
    )
    print(result)
    elapsed = time.perf_counter() - start
    print("elapsed:",elapsed)

async def main2():
    task=asyncio.create_task(request(1,2))
    print(task.done())
    await task#
    print(task.done())
    print(task.result())

if __name__ == "__main__":
    asyncio.run(main1())