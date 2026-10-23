import asyncio
import time

semaphore=asyncio.Semaphore(5)

active_count=0
max_active_count=0

async def request(request_id):
    global active_count, max_active_count
    async with semaphore:
        active_count += 1
        max_active_count = max(
            max_active_count,
            active_count
        )
        try:
            print(f"Request {request_id} started")
            print(f"Active: {active_count}")
            await asyncio.sleep(1)
        finally:
            active_count -= 1

async def main():
    start=time.perf_counter()
    tasks=[request(i) for i in range(1,21)]
    await asyncio.gather(*tasks)
    print("Max active:", max_active_count)
    elapsed=time.perf_counter()-start
    print(f"elapsed time:{elapsed}")


if __name__ =="__main__":
    asyncio.run(main())
