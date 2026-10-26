import json
import redis

QUEUE_KEY='week19:jobs'

client=redis.Redis(
    host='127.0.0.1',
    port=6379,
    db=0,
    decode_responses=True,
    socket_timeout=None,
    socket_connect_timeout=3
)

for product_id in [101, 102, 103]:
    message={
        'task_id':f'job-{product_id}',
        'product_id':product_id
    }
    message=json.dumps(message)
    client.rpush(QUEUE_KEY, message)
    print(f"Submitted job-{product_id}")