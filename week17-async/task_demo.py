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
    start=time.perf_counter()
    task_a = asyncio.create_task(request(1,3))
    task_b = asyncio.create_task(request(2, 1))
    task_c = asyncio.create_task(request(3, 2))
    result1 = await task_a
    result2 = await task_b
    result3 = await task_c
    print(result1)
    print(result2)
    print(result3)
    elapsed = time.perf_counter() - start
    print("elapsed:",elapsed)


if __name__ == "__main__":
    asyncio.run(main())
