from fastapi import FastAPI,Depends,HTTPException
from typing import Annotated
from fastapi.testclient import TestClient

app=FastAPI()
count=0

def get_value():
    global count
    count+=1
    print(f"依赖执行{count}次")
    return {"count": count}

def get_resource():
    print("创建资源")
    resource={"ready":True}
    try:
        yield resource
    finally:
        print("释放资源")

def get_context(
        resource:Annotated[dict,Depends(get_resource)]
):
    print("执行 get_context")
    return {"resource": resource}


@app.get("/demo")
def demo(
        a:Annotated[dict,Depends(get_value)],
        b:Annotated[dict,Depends(get_value)],
):
    print("Route执行")
    return {
        "a":a["count"],
        "b":b["count"],
        "same_object":a is b
    }

@app.get("/resource-ok")
def resource_ok(
        resource:Annotated[dict,Depends(get_resource)]
):
    print("正常执行 Route")
    return resource

@app.get("/resource-error")
def resource_error(
        resource:Annotated[dict,Depends(get_resource)]
):
    print("Route 出现异常")
    raise HTTPException(
        status_code=400,
        detail="Demo error"
    )

@app.get("/nested")
def nested(
        context:Annotated[dict,Depends(get_context)],
        resource:Annotated[dict,Depends(get_resource)]
):
    print("执行 nested Route")
    return {
        "ready": context["resource"]["ready"],
        "same_object": context["resource"] is resource
    }

if __name__ == "__main__":
    with TestClient(app) as client:
        print("子依赖实验：")
        print(client.get("/nested").json())