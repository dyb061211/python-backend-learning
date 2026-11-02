# Python Backend Learning

本项目用于记录 Python 后端开发学习过程中的代码与实践。

目前主要包含 Python 异步与并发编程、Redis 基础、MySQL + Redis 缓存工程，以及 FastAPI + Celery 后台任务、消息队列和 FastAPI 进阶工程实验。

## 项目结构

```text
PythonProject/
├── week17-async/     # Python 异步与并发编程
├── week18-redis/     # Redis 与后端缓存工程
├── week19-background-jobs/  # Week19 后台任务与消息队列、Week20 FastAPI 进阶与服务集成
└── README.md
```

## Week17：Python Async & Concurrency

学习 Python 异步编程与并发处理的核心机制。

**主要学习内容：**

- Coroutine、Event Loop、async/await
- Task、gather、TaskGroup
- Timeout、Cancellation
- Semaphore、Queue
- Race Condition、asyncio.Lock
- asyncio.to_thread()
- FastAPI 同步与异步处理
- httpx.AsyncClient

**实践内容：**

- 顺序执行与异步并发性能对比
- Semaphore 并发限制
- Queue 生产者消费者模型
- 异常、超时与任务取消
- 异步批处理综合实验

## Week18：Redis & Backend Cache

学习 Redis 基础知识，并结合 MySQL 实现商品缓存 Demo。

**主要学习内容：**

- Redis 常见数据类型
- Cache Hit / Cache Miss
- TTL、Cache Aside
- 缓存穿透、击穿、雪崩
- INCR、SET NX、MULTI/EXEC、WATCH
- redis-py、redis.asyncio
- Connection Pool
- 缓存一致性与故障降级
- Redis 持久化与内存淘汰基础

**实践内容：**

使用 Python + MySQL + Redis 实现商品缓存系统，包含：

- 商品查询与缓存命中
- TTL 过期后重新加载
- MySQL 商品更新与 Redis 缓存失效
- Redis 故障时降级查询 MySQL
- 基本异常处理与资源管理

## Week19：Background Jobs & Message Queue

学习后台任务与消息队列机制，结合 FastAPI、Celery、Redis 和 MySQL 实现任务处理 Demo。

**主要学习内容：**

- 同步处理、FastAPI BackgroundTasks 与 Celery Worker
- Redis Broker 消息传递与 Result Backend 状态、结果存储
- 任务提交、task_id 与状态查询
- 异常分类、自动重试与退避
- request_id、Redis SET NX 与 MySQL 重复写入处理的幂等性实验
- Worker 并发、任务积压与单个 Worker 内的任务速率限制
- MySQL job_runs 任务状态与结果记录

**实践内容：**

- 对比同步请求、进程内后台任务与消息队列任务
- 通过 POST /jobs 提交任务，使用 GET /jobs/{task_id} 查询 Celery 状态与结果
- 在 MySQL job_runs 中记录 PENDING、STARTED、SUCCESS、FAILURE，通过 GET /job-runs 查询运行记录
- 独立实验验证连接异常重试、重复请求处理与结果等待超时
- 批量提交任务，观察 Worker 并发、队列积压与 rate_limit 限流

以上为学习实验；重试、幂等性与状态记录仍有故障边界，不保证 Exactly-once。

## Week20：FastAPI Advanced & Backend Service Integration

基于 Week19 的后台任务项目学习 FastAPI 进阶功能，对现有服务进行小范围工程整理，提高接口的可维护性、可验证性和错误处理能力。

**主要学习内容：**

- APIRouter 路由组织与职责划分
- Pydantic 请求模型、响应模型与接口契约
- Depends 依赖注入、子依赖与 yield 资源管理
- Settings、环境变量与敏感配置管理
- FastAPI Lifespan 与 app.state
- HTTP 状态、Celery 状态和业务状态的区别
- HTTPException、exception_handler 与安全错误响应
- Middleware、trace_id 与请求日志关联
- TestClient、Mock 与接口测试
- 同步 PyMySQL、数据库事务与资源生命周期

**实践内容：**

- 将三个核心业务接口整理到 `job_routes.py`，保持原有 URL
- 为任务提交、任务状态和历史查询定义响应模型
- 使用 `settings.py` 集中管理 MySQL 和 Redis 配置
- 增加任务存在性检查，区分 HTTP 404 与 Celery PENDING
- 处理 MySQL 连接异常、Celery 发布异常和 Result Backend 查询异常
- 增加 HTTP Middleware，记录请求状态、耗时和 trace_id，并在任务提交日志中关联 trace_id 和 task_id
- 通过独立 Demo 验证 Depends、yield、Lifespan 和异常处理
- 学习记录包括 3 项 Mock 接口测试及 FastAPI + Celery + Redis + MySQL 完整链路回归；当前仓库未保存对应的独立测试脚本，本次文档更新未重新执行验证

**运行与验证：**

在 `week19-background-jobs` 目录、项目 Python 虚拟环境中执行，并确保本地 MySQL 和 Redis 服务已经启动。

FastAPI：

```bash
python -m uvicorn main:app --reload
```

Celery Worker：

```bash
python -m celery -A tasks:app worker --loglevel=info --pool=solo
```

核心接口：

| 接口 | 用途 |
|---|---|
| `POST /jobs` | 提交任务，正常返回 HTTP 202 和 task_id |
| `GET /jobs/{task_id}` | 查询 Celery 任务状态与结果 |
| `GET /job-runs?limit=10` | 查询 MySQL 任务历史 |

配置由 `settings.py` 管理。实际密码放在 Git 忽略的 `.env` 中，具体读取位置以 `settings.py` 的 `env_file` 为准；`.env.example` 仅提供安全的配置模板。

**已知限制：**

- MySQL 任务登记与 Redis 消息发布不是原子操作
- 发布网络异常时，任务是否入队可能不确定
- Celery PENDING 不能单独证明任务正在排队
- Result Backend 的任务结果可能过期
- MySQL UNIQUE 不能保证外部操作 Exactly-once
- Mock 测试不等于真实 Worker 集成测试
- Depends、yield 和 Lifespan 的部分内容通过独立实验验证，未强制集成到正式业务
- 当前没有完整认证与访问控制，仅用于本地受控环境，不直接公开部署

本周以现有服务整理为主，没有引入新的核心业务或复杂架构。

## 技术栈

Python · asyncio · FastAPI · Celery · MySQL · Redis（Broker / Result Backend）· PyMySQL · redis-py

## 学习目标

通过独立实验掌握 Python 后端开发中的并发处理、数据库操作、缓存设计、后台任务、消息队列和异常处理，逐步提升实际工程开发能力。

本项目主要用于学习与实践，不作为生产级系统使用。

## Week21 — Docker 本地容器化部署

### 目标

使用 Docker Compose 运行现有后台任务项目：

- Web：FastAPI
- Worker：Celery
- Redis：Broker 和 Result Backend
- MySQL：任务历史与业务结果

Web 和 Worker 使用同一应用镜像，但运行不同命令。

### 已验证环境

- Mac：arm64（Apple Silicon）
- Docker Desktop：4.81.0
- Docker Engine：29.6.1
- Docker Compose：v5.2.0
- 应用基础镜像：python:3.13-slim
- Redis：redis:7.4.12-alpine3.21
- MySQL：mysql:8.4.13

### 构建镜像

从 PythonProject 根目录进入：

```bash
cd week19-background-jobs
```

构建应用镜像：

```bash
docker build -t week21-backend:day2 .
```

应用依赖保存在 `requirements.docker.txt` 中，不复制宿主机 `.venv`。

### 配置

在应用目录创建 `.env.week21`，填写独立测试密码：

```text
W21_ROOT_PASSWORD=<自行设置的测试密码>
W21_APP_PASSWORD=<另一组测试密码>
```

不要使用真实业务数据库密码。

`.env.week21` 不应提交到 Git，也不应复制进镜像。

### 启动服务

```bash
docker compose --env-file .env.week21 -p week21-fresh config -q
docker compose --env-file .env.week21 -p week21-fresh up -d
```

查看状态：

```bash
docker compose --env-file .env.week21 -p week21-fresh ps
```

访问：<http://127.0.0.1:18080/openapi.json>

注意：再次使用相同项目名会复用已有的命名卷，不代表每次都从空数据库开始。

### 数据库初始化

`sql/001_schema.sql` 包含本项目最小表结构：

- `job_runs`
- `listing_results`

MySQL 官方镜像在全新数据目录首次初始化时执行该脚本。

已有数据库数据卷不会在每次重启时重新执行初始化脚本。

### 网络与数据持久化

- Web 仅发布到宿主机 `127.0.0.1:18080`
- Redis 和 MySQL 不发布宿主机端口
- 容器之间通过 Compose 服务名通信
- MySQL 使用独立命名卷
- Redis 使用 AOF（appendfsync everysec）和独立命名卷

持久化不等于备份，也不能保证任务 Exactly-once。

### 日志和停止服务

查看日志：

```bash
docker compose --env-file .env.week21 -p week21-fresh logs --tail=40 web worker
```

停止服务并保留容器和数据：

```bash
docker compose --env-file .env.week21 -p week21-fresh stop
```

删除本项目服务容器及网络，但保留命名卷：

```bash
docker compose --env-file .env.week21 -p week21-fresh down
```

不要随意使用 `down -v`，它会删除本项目声明的命名卷。

### 已验证内容

- Docker 镜像构建和依赖导入成功
- Web 和 Worker 分别运行
- Redis、MySQL 容器间连接成功
- MySQL 自动初始化业务表
- Redis AOF 重建恢复成功
- 健康检查通过
- POST /jobs → Worker → MySQL 真实链路成功
- 容器删除重建后 MySQL 历史数据保留
- 新 Compose 项目和新数据卷可独立初始化
- Redis 错误连接与 MySQL 缺表故障排查

### 已知边界

- 只验证了本地 Docker 环境
- 未部署到云服务器
- 未完成公网认证与授权
- 未验证跨 CPU 架构
- 未证明 Exactly-once 或完整崩溃恢复
- 未进行正式生产性能测试
- 数据卷持久化不等于备份
