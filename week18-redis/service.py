from cache import *
from repository import *

def get_product_message(product_id,client,connection):
    key = f"week18:catalog:product:{product_id}"
    cache_available=True
    try:
        res = get_run_id_redis(client, key)
        if not res:
            res=None
    except (redis.exceptions.ConnectionError,redis.exceptions.TimeoutError):
        print("Redis unavailable, fallback to MySQL")
        res=None
        cache_available=False
    if res is None:
        res = get_run_id(connection, product_id)
        if not res:
            print("没有相关产品")
            return None
        if cache_available:
            try:
                add_run_id_redis(client, res, key)
                add_ttl_redis(client, key, 30)
            except (
                    redis.exceptions.ConnectionError,
                    redis.exceptions.TimeoutError
            ) as e:
                print(f"Redis cache write failed: {e}")
    return res

def change_price(product_id,price,connection,client):
    update_run_id(connection,product_id,price)
    key = f"week18:catalog:product:{product_id}"
    try:
        delete_run_id_redis(client, key)
    except (
            redis.exceptions.ConnectionError,
            redis.exceptions.TimeoutError
    ) as e:
        print(f"MySQL 已更新，但 Redis 缓存删除失败: {e}")
        raise