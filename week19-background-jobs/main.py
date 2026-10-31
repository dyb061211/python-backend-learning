import time
from fastapi import FastAPI,BackgroundTasks,Request
from job_routes import router as job_router
import logging
from fastapi.responses import JSONResponse
from pymysql.err import OperationalError as MySQLOperationalError
from uuid import uuid4

logger=logging.getLogger(__name__)

app=FastAPI()
app.include_router(job_router)

@app.exception_handler(MySQLOperationalError)
async def handle_mysql_error(request: Request, exc: MySQLOperationalError):
    error_code=exc.args[0] if exc.args else None
    logger.error(
        "MySQL error: code=%s, path=%s",
        error_code,
        request.url.path
    )
    if error_code==2003:
        return JSONResponse(
            status_code=503,
            content={
                "error": {
                    "code": "DATABASE_UNAVAILABLE",
                    "message": "Database unavailable"
                }
            }
        )
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error"
            }
        }
    )
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

@app.middleware('http')
async def log_middleware(request:Request,call_next):
    trace_id=uuid4().hex
    request.state.trace_id=trace_id
    start=time.perf_counter()
    print("请求进入：",trace_id,request.method,request.url.path)
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print("请求结束：", response.status_code,elapsed_ms)
    response.headers["X-Trace-ID"] = trace_id
    return response