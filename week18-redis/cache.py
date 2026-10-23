import redis

def get_redis_client():
    return redis.Redis(
        host='127.0.0.1',
        port=6380,
        db=0,
        decode_responses=True,
        socket_connect_timeout=3,
        socket_timeout=3,
    )

def get_run_id_redis(client,key)->dict|None:
    res=client.hgetall(key)
    if not res:
        return None
    return {
        "id":int(res["id"]),
        "name":res["name"],
        "price":int(res["price"])
    }

def add_run_id_redis(client,product,key)->None:
    client.hset(
        key,
        mapping=product
    )

def add_ttl_redis(client,key,times)->None:
    client.expire(key, times)

def delete_run_id_redis(client,key)->None:
    client.delete(key)