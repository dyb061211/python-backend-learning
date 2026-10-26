from celery import Celery
import time
import redis
import os
import pymysql
from job_repository import update_job_status

demo_redis=redis.Redis(
    host='127.0.0.1',
    port=6379,
    db=3,
    decode_responses=True
)

app=Celery(
    "week19",
    broker="redis://127.0.0.1:6379/1",
    backend="redis://127.0.0.1:6379/2"
)

@app.task(track_started=True)
def generate_listing(product_id:int):
    print(f"{product_id} started")
    time.sleep(3)
    return {
        "product_id": product_id,
        "title":"Apple"
    }

@app.task(
    bind=True,
    autoretry_for=(ConnectionError,),
    retry_kwargs={"max_retries":2},
    retry_backoff=True,
    retry_jitter=False
)
def unstable_listing(self,product_id:int):
    attempt=self.request.retries
    print(f"当前重试次数: {attempt}")
    if attempt<=2:
        raise ConnectionError("Connection error")
    else:
        return {
            "product_id": product_id,
            "title":"Apple"
        }

@app.task(
    bind=True,
    autoretry_for=(ConnectionError,),
    retry_kwargs={"max_retries": 2, "countdown": 2}
)
def validate_listing(self, product_id: int):
    print(f"当前重试次数：{self.request.retries}")
    if product_id<0:
        raise ValueError("Invalid product ID")
    else:
        return {
            "product_id": product_id,
            "title":"Apple"
        }

@app.task
def listing_without_idempotency(product_id:int,request_id:int):
    key = f"week19:demo:executions:{request_id}"
    count = demo_redis.incr(key)
    print(f"{request_id}: {count}")
    return {
        "product_id": product_id,
        "request_id": request_id,
        "count": count
    }

@app.task
def listing_with_idempotency(product_id:int,request_id:int):
    lock_key = f"week19:demo:claimed:{request_id}"
    count_key = f"week19:demo:executions:{request_id}"
    claimed = demo_redis.set(
        lock_key, "1", nx=True, ex=60
    )
    if not claimed:
        return {
            "status": "already_claimed",
            "request_id": request_id
        }
    count = demo_redis.incr(count_key)
    return {
        "status": "processed",
        "request_id": request_id,
        "count": count
    }

@app.task(bind=True)
def listing_to_mysql(self,product_id: int, request_id: str):
    task_id = self.request.id
    update_job_status(task_id, "STARTED")
    conn=pymysql.connect(
        host='127.0.01',
        port=3306,
        user='root',
        password=os.environ['MYSQL_PASSWORD'],
        database='week19_demo',
        autocommit=False
    )
    try:
        if product_id == 9999:
            raise RuntimeError("Simulated listing failure")
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO listing_results (request_id,product_id,title) VALUES (%s, %s,%s)',
                (request_id,product_id,'Apple')
            )
            conn.commit()
            update_job_status(
                task_id,
                "SUCCESS",
                "created"
            )
        return {
            "status": "created",
            "   request_id": request_id
        }
    except pymysql.err.IntegrityError as exc:
        conn.rollback()
        if exc.args[0] == 1062:
            update_job_status(
                task_id,
                "SUCCESS",
                "duplicate"
            )
            return {
                "status": "duplicate",
                "request_id": request_id
            }
        else :
            raise
    except Exception as exc:
        update_job_status(
        task_id,
        "FAILURE",
        error_message=f"{type(exc).__name__}: {exc}"
    )
        raise
    finally:
        conn.close()

@app.task
def batch_listing(product_id: int):
    print(f"Product {product_id} started", flush=True)

    time.sleep(2)

    print(f"Product {product_id} finished", flush=True)

    return {
        "product_id": product_id,
        "status": "completed"
    }

@app.task(rate_limit="1/s")
def limited_listing(product_id: int):
    print(f"Product {product_id} started", flush=True)
    time.sleep(0.2)
    return {
        "product_id": product_id,
        "status": "completed"
    }
