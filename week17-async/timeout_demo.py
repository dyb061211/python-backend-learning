import asyncio
import time
from datetime import datetime

async def request(request_id,delay,should_fail=False):
    print("request_id:",request_id)
    print("start:",datetime.now())
    await asyncio.sleep(delay)
    if should_fail:
        raise ValueError(f"Request {request_id} failed")
    print("end:",datetime.now())

async def main():
    start=time.perf_counter()
    try:
        async with asyncio.timeout(2):
            await request(2,5)
    except TimeoutError:
        print("Request 2 timeout")
    elapsed=time.perf_counter()-start
    print("elapsed:",elapsed)

if __name__ == "__main__":
    asyncio.run(main())