import asyncio

async def producer(queue):
    for i in range(1,11):
        await queue.put(i)
        print("Produced:",i)
        print("Queue Size:",queue.qsize())

async def consumer(work_id,queue):
    while True:
        item=await queue.get()
        try:
            if item is None:
                break
            print(f"Worker {work_id} processing {item}")
            await asyncio.sleep(0.5)
            print(f"Worker {work_id} finished {item}")
        finally:
            queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=3)
    async with asyncio.TaskGroup() as tg:
        task1=tg.create_task(consumer(1,queue))
        task2=tg.create_task(consumer(2,queue))
        await producer(queue)
        await queue.put(None)
        await queue.put(None)
        await queue.join()


if __name__ == "__main__":
    asyncio.run(main())