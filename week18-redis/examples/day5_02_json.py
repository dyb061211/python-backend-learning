import json
import redis

product = {
    "id": 1001,
    "name": "无线吸尘器",
    "price": 299,
    "tags": ["家电", "清洁"]
}

client=redis.Redis(
    host='127.0.0.1',
    port=6380,
    db=0,
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3
)

client.hset(
    "week18:python:hash:1002",
    mapping={
        "name": "无线吸尘器",
        "price": 299,
        "color": "black"
    }
)
client.expire("week18:python:hash:1002",30)
result=client.hgetall("week18:python:hash:1002")
print(result)
print(type(result))

client.set("week18:python:views:1002", 0)

for _ in range(3):
    client.incr("week18:python:views:1002")

print(client.get("week18:python:views:1002"))
