from fastapi import APIRouter,Query,HTTPException,Request
from pydantic import BaseModel,Field
from uuid import uuid4
from tasks import listing_to_mysql, app as celery_app
from job_repository import insert_pending_job, get_job_runs,get_job_by_task_id
from typing import Any
import logging
from kombu.exceptions import OperationalError as BrokerOperationalError
from redis.exceptions import(
    ConnectionError as RedisConnectionError,
    TimeoutError as RedisTimeoutError
)

logger=logging.getLogger("uvicorn.error")

router = APIRouter(tags=["jobs"])

class JobRequest(BaseModel):
    product_id: int = Field(gt=0)
    request_id: str = Field(min_length=1,max_length=80)

class JobSubmitResponse(BaseModel):
    task_id:str
    status: str
    request_id: str

class JobStatusResponse(BaseModel):
    task_id: str
    state: str
    result:dict[str,Any] | None = None
    error_type: str | None = None

class JobRunResponse(BaseModel):
    task_id: str
    request_id: str
    product_id: int
    status: str
    result_status: str | None = None

@router.post("/jobs",status_code=202,response_model=JobSubmitResponse)
def create_job(data: JobRequest,request: Request):
    task_id=str(uuid4())
    insert_pending_job(task_id,data.request_id,data.product_id)
    try:
        listing_to_mysql.apply_async(args=(data.product_id, data.request_id), task_id=task_id)
        logger.info(
            "Task submitted:trace_id=%s,task_id=%s",
            request.state.trace_id,
            task_id
        )
    except BrokerOperationalError as exc:
        logger.exception(
            "Task publication unconfirmed: task_id=%s",
            task_id
        )
        raise HTTPException(
            status_code=503,
            detail={
                "code": "PUBLISH_UNCONFIRMED",
                "message": "Task publication could not be confirmed",
                "task_id": task_id
            }
        ) from exc
    return {
        "task_id": task_id,
        "status": "accepted",
        "request_id": data.request_id
    }

@router.get("/jobs/{task_id}",response_model=JobStatusResponse,response_model_exclude_none=True)
def get_job(task_id: str):
    job=get_job_by_task_id(task_id)
    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    try:
        result=celery_app.AsyncResult(task_id)
        if result.state == "SUCCESS":
            return {
                "task_id": task_id,
                "state": result.state,
                "result": result.result
            }
        if result.state == "FAILURE":
            return {
                "task_id": task_id,
                "state": result.state,
                "error_type": type(result.result).__name__
            }
        return {
            "task_id": task_id,
            "state": result.state
        }
    except (RedisConnectionError, RedisTimeoutError) as exc:
        logger.exception(
            "Result backend unavailable: task_id=%s",
            task_id
        )
        raise HTTPException(
            status_code=503,
            detail={
                "code": "RESULT_BACKEND_UNAVAILABLE",
                "message": "Task status temporarily unavailable"
            }
        ) from exc


@router.get("/job-runs",response_model=list[JobRunResponse])
def list_job_runs(limit: int = Query(default=10, ge=1, le=100)):
    return get_job_runs(limit)

if __name__=="__main__":
    data = {
        "task_id": "abc-123",
        "status": "accepted",
        "request_id": "req-1",
        "internal_debug": "secret"
    }
    response=JobSubmitResponse.model_validate(data)
    print(response.model_dump())