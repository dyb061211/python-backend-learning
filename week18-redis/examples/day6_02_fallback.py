import redis
import json

client=redis.Redis(
    host='127.0.0.1',
    port=6380,
    db=0,
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3
)

bad_client=redis.Redis(
host='127.0.0.1',
    port=6399,
    db=0,
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3
)

products = {
    1001: {"name": "Apple", "price": 259}
}


def get_product(product_id,cache_client):
    key = f"week18:day6:product:{product_id}"
    try:
        res=cache_client.get(key)
        return json.loads(res)
    except (
        redis.exceptions.ConnectionError,
        redis.exceptions.TimeoutError,
    ):
        print("error")
        return products[product_id]

if __name__=="__main__":
    client.set("week18:day6:product:1001",json.dumps({"name": "Apple", "price": 259}))
    try:
        res1 = get_product(1001, client)
        res2 = get_product(1001, bad_client)

        print(res1)
        print(res2)
    finally:
        client.close()
        bad_client.close()