import time
from fastapi import FastAPI,BackgroundTasks,Query
from pydantic import BaseModel,Field
from tasks import listing_to_mysql,app as celery_app
from uuid import uuid4
from job_repository import insert_pending_job,get_job_runs

class JobRequest(BaseModel):
    product_id: int = Field(gt=0)
    request_id: str = Field(min_length=1,max_length=80)

app=FastAPI()

def generate_listing(product_id:int):
    print(f"Product {product_id}: started", flush=True)
    time.sleep(60)
    print(f"Product {product_id}: finished", flush=True)
    return {
        "product_id": product_id,
        "title": f"Generated Listing {product_id}"
    }

@app.post("/sync")
def sync_generate(product_id: int):
    response=generate_listing(product_id)
    return response

@app.post("/background",status_code=202)
def background(product_id:int,background_tasks:BackgroundTasks):
    background_tasks.add_task(generate_listing,product_id)
    return {"status": "accepted", "product_id": product_id}

@app.post("/jobs",status_code=202)
def create_job(data: JobRequest):
    task_id=str(uuid4())
    insert_pending_job(task_id,data.request_id,data.product_id)
    listing_to_mysql.apply_async(args=(data.product_id, data.request_id),task_id=task_id)
    return {
        "task_id": task_id,
        "status": "accepted",
        "request_id": data.request_id
    }

@app.get("/jobs/{task_id}")
def get_job(task_id: str):
    result=celery_app.AsyncResult(task_id)
    if result.state=="SUCCESS":
        return {
            "task_id": task_id,
            "state": result.state,
            "result": result.result
        }
    if result.state=="FAILURE":
        return {
            "task_id": task_id,
            "state": result.state,
            "error_type": type(result.result).__name__
        }
    return {
        "task_id": task_id,
        "state": result.state
    }

@app.get("/job-runs")
def list_job_runs(limit: int = Query(default=10, ge=1, le=100)):
    return get_job_runs(limit)