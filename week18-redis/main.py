from service import *
import redis
import os

password = os.environ["MYSQL_PASSWORD"]
connection=get_connection(password)
client=get_redis_client()

bad_client = redis.Redis(
    host="127.0.0.1",
    port=6399,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1
)

try:
    result = get_product_message(
        1001,
        bad_client,
        connection
    )

    print(result)
    assert result["price"] == 279

finally:
    client.close()
    connection.close()
    bad_client.close()

