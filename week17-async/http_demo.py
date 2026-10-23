import asyncio
import httpx
import time

async def endpoint(path):
    start=time.perf_counter()
    base_url="http://127.0.0.1:8000"
    url = base_url + path
    async with httpx.AsyncClient(timeout=15.0) as ac:
        responses=await asyncio.gather(
            ac.get(url),
            ac.get(url),
            ac.get(url)
        )
    elapse=time.perf_counter()-start
    print(elapse)
    for response in responses:
        print(response.status_code)
        print(response.json())

if __name__ == "__main__":
    asyncio.run(endpoint("/blocking-demo"))