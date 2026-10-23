import redis
import time

client=redis.Redis(
    host="127.0.0.1",
    port=6380,
    db=0,
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3,
)

client.set("week18:python:product:1001","Apple")
result = client.get("week18:python:product:1001")
print(result)
print(type(result));
client.expire("week18:python:product:1001",30)
time.sleep(2)
print(client.ttl("week18:python:product:1001"))
client.delete("week18:python:product:1001")
print(client.get("week18:python:product:1001"))

print(client.ping())

client.close()