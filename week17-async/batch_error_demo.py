import asyncio
import time

async def request(request_id,delay,should_fail=False):
    try:
        await asyncio.sleep(delay)
        if should_fail:
            raise ValueError("Request failed")
        return f"Request {request_id}"
    finally:
        print("Request resource released")

async def request_time_out():
    async with asyncio.timeout(2):
        return await request(5, 10)


async def main():
    start=time.perf_counter()
    results=await asyncio.gather(
        request(1,0.5),
        request(2,1),
        request(3, 1.5),
        request(4, 0.8,True),
        request_time_out(),
        return_exceptions=True
    )
    for result in results:
        if isinstance(result, Exception):
            print("Failed:", type(result).__name__, str(result))
        else:
            print("Success:", result)
    elapsed=time.perf_counter()-start
    print("elapsed:",elapsed)

if __name__=="__main__":
    asyncio.run(main())

