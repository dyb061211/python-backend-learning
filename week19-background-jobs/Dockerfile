FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.docker.txt ./

RUN python -m pip install --no-cache-dir -r requirements.docker.txt

COPY main.py tasks.py job_routes.py job_repository.py settings.py ./

USER 1001:1001

CMD ["python","-m","uvicorn","main:app","--host","0.0.0.0","--port","8000"]
