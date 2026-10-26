from tasks import batch_listing

for product_id in range(301, 313):
    result = batch_listing.delay(product_id)
    print(f"Submitted {product_id}: {result.id}")

print("全部任务已经提交")