# Python Backend Learning

本项目用于记录 Python 后端开发学习过程中的代码与实践。

目前主要包含 Python 异步与并发编程、Redis 基础、MySQL + Redis 缓存工程，以及 FastAPI + Celery 后台任务与消息队列工程实验。

## 项目结构

```text
PythonProject/
├── week17-async/     # Python 异步与并发编程
├── week18-redis/     # Redis 与后端缓存工程
├── week19-background-jobs/  # 后台任务与消息队列工程
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

## 技术栈

Python · asyncio · FastAPI · Celery · MySQL · Redis（Broker / Result Backend）· PyMySQL · redis-py

## 学习目标

通过独立实验掌握 Python 后端开发中的并发处理、数据库操作、缓存设计、后台任务、消息队列和异常处理，逐步提升实际工程开发能力。

本项目主要用于学习与实践，不作为生产级系统使用。