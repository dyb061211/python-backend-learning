import asyncio
import time
from batch_service import *

products = [
    {"id": 1, "name": "Keyboard", "delay": 1},
    {"id": 2, "name": "Mouse", "delay": 2},
    {"id": 3, "name": "Monitor", "delay": 1},
    {"id": 4, "name": "Laptop", "delay": 2, "should_fail": True},
    {"id": 5, "name": "Headphones", "delay": 5},
]

async def main():
    start=time.perf_counter()
    results=await run_concurrent(products,5,3)
    elapsed=time.perf_counter()-start
    print(elapsed)
    success_count=0
    failure_count=0
    for result in results:
        print(result)
        if result["status"]=="success":
            success_count+=1
        else:
            failure_count+=1
    print("success count:",success_count)
    print("failure count:",failure_count)

async def cancellation_demo():
    products1 = [
        {"id": 1, "name": "Keyboard", "delay": 10},
        {"id": 2, "name": "Mouse", "delay": 10},
    ]
    task = asyncio.create_task(
        run_concurrent(
            products1,
            max_concurrency=2,
            timeout=30
        )
    )
    await asyncio.sleep(0.5)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Batch cancelled")
    print(task.done())
    print(task.cancelled())


if __name__=="__main__":
    asyncio.run(cancellation_demo())