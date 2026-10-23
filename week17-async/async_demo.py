import time
from datetime import datetime
import asyncio

async def async_request(request_id):
    print("request_id:",request_id)
    print("start:", datetime.now())
    await asyncio.sleep(2)
    print("end:", datetime.now())

async def main():
    await asyncio.gather(
        async_request(1),
        async_request(2),
        async_request(3),
    )

if __name__ == "__main__":
    start=time.perf_counter()
    asyncio.run(main())
    elapsed=time.perf_counter()-start
    print(elapsed)