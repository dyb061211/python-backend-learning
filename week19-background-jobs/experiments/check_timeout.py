from celery.exceptions import TimeoutError
from tasks import generate_listing

result = generate_listing.delay(201)

try:
    print(result.get(timeout=1))
except TimeoutError:
    print("客户端等待超时")

print("继续等待：", result.get(timeout=10))
print("最终状态：", result.state)