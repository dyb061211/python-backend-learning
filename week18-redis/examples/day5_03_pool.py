import redis

client=redis.Redis(
    host='127.0.0.1',
    port=6380,
    db=0,
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3
)

print(client.ping())
print(type(client.connection_pool))

bad_client=redis.Redis(
    host='127.0.0.1',
    port=6389,
    db=0,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1
)

try:
    print(bad_client.ping())
except redis.exceptions.ConnectionError:
    print("Connection error")
except redis.exceptions.TimeoutError:
    print("Timeout error")
finally:
    bad_client.close()