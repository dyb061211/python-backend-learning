import asyncio

counter=0
lock=asyncio.Lock()

async def increment():
    global counter
    async with lock:
        temp = counter
        await asyncio.sleep(0)
        counter = temp + 1

async def worker():
    for i in range(1000):
        await increment()

async def main():
    await asyncio.gather(
        worker(),
        worker(),
    )
    print("counter:", counter)


if __name__ == "__main__":
    asyncio.run(main())