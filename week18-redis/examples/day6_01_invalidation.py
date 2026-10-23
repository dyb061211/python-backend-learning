import redis

products = {
    "name": "Apple",
    "price": 299
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
    "week18:day6:product:1001",
    mapping=products
)
client.expire("week18:day6:product:1001",60)
products["price"]=259
result1=client.hget("week18:day6:product:1001","price")
print(result1)
client.delete("week18:day6:product:1001")
result2=client.hgetall("week18:day6:product:1001")
print(result2)
client.hset(
    "week18:day6:product:1001",
    mapping=products
)
client.expire("week18:day6:product:1001",60)
result3=client.hget("week18:day6:product:1001","price")
print(result3)