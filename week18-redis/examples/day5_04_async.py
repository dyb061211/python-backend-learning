import asyncio
import redis.asyncio as redis

client=redis.Redis(
    host='127.0.0.1',
    port=6380,
    db=0,
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3
)

async def main():
    try:
        await client.set("test01", "Apple")
        await client.set("test02", "Orange")
        await client.set("test03", "Banana")
        results=await asyncio.gather(
            client.get("test01"),
            client.get("test02"),
            client.get("test03")
        )
        for res in results:
            print(res)
    finally:
        await client.aclose()


if __name__ == '__main__':
    asyncio.run(main())