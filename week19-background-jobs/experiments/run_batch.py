import time
from tasks import batch_listing

start=time.perf_counter()
results=[]

for product_id in range(201,207):
    result=batch_listing.delay(product_id)
    results.append(result)

print("所有任务已经提交")

for result in results:
    print(result.get(timeout=60))

elapsed=time.perf_counter()-start
print("总耗时:",elapsed)
