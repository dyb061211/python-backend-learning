from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
from fastapi.testclient import TestClient

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("应用启动：创建资源")
    resource={
        "count":0,
        "closed":False
    }
    app.state.resource=resource
    try:
        yield
    finally:
        resource["closed"]=True
        print("应用关闭：释放资源")

app=FastAPI(lifespan=lifespan)

@app.get("/demo")
def demo(request:Request):
    resource=app.state.resource
    resource["count"]+=1
    return {"count": resource["count"]}

if __name__ == "__main__":
    with TestClient(app) as client:
        print("第一次请求：", client.get("/demo").json())
        print("第二次请求：", client.get("/demo").json())
    print("资源已关闭：", app.state.resource["closed"])
