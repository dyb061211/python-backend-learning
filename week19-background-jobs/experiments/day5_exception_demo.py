from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from fastapi import FastAPI,Request,HTTPException

app=FastAPI()

class DataBaseUnavailableError(Exception):
    pass

@app.exception_handler(DataBaseUnavailableError)
async def handle_database_error(request:Request,exc:DataBaseUnavailableError):
    print("服务器错误类型：",type(exc).__name__)
    return JSONResponse(
        status_code=503,
        content={
            "error": {
                "code": "DATABASE_UNAVAILABLE",
                "message": "Database temporarily unavailable"
            }
        }
    )

@app.get("/demo")
def demo():
    raise DataBaseUnavailableError("Simulated failure")

@app.get("/unexpected")
def unexpected():
    raise ValueError("Simulated programming error")

@app.get("/publish-demo")
def publish_demo():
    try:
        raise ConnectionError("Simulated broker network error")
    except ConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "PUBLISH_UNCONFIRMED",
                "message": "Task publication could not be confirmed"
            }
        ) from exc

if __name__=="__main__":
    with TestClient(app,raise_server_exceptions=False) as client:
        response = client.get("/publish-demo")

        print(response.status_code)
        print(response.json())