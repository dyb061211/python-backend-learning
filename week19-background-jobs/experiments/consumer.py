import json
import redis
import time

QUEUE_KEY='week19:jobs'

client=redis.Redis(
    host='127.0.0.1',
    port=6379,
    db=0,
    decode_responses=True,
    socket_timeout=None,
    socket_connect_timeout=3
)

while True:
    message=client.blpop(QUEUE_KEY,0)
    message=json.loads(message[1])
    print(message['task_id'])
    time.sleep(2)
    print(f'{message['task_id']} finished')

