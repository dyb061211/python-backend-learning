import asyncio
import time
from datetime import datetime

async def request(request_id, delay):
    print("Request started")
    try:
        await asyncio.sleep(delay)
        print("Request success")
    finally:
        print("Request resource released")

async def main():
    start=time.perf_counter()
    task = asyncio.create_task(request(1, 10))
    await asyncio.sleep(1)
    task.cancel()
    try:
        await task
        print("Request success")
    except asyncio.CancelledError:
        print("task cancelled")
    print(task.done())
    print(task.cancelled())
    elapsed=time.perf_counter()-start
    print("elapsed:",elapsed)


if __name__ == "__main__":
    asyncio.run(main())