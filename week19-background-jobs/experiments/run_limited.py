import time
from tasks import limited_listing

start = time.perf_counter()

results = [
    limited_listing.delay(i)
    for i in range(401, 407)
]

for result in results:
    print(result.get(timeout=30))

print(f"总耗时: {time.perf_counter() - start:.2f}s")