# Python Backend Learning

本项目用于记录 Python 后端开发学习过程中的代码与实践。

目前主要包含 Python 异步与并发编程、Redis 基础以及 MySQL + Redis 缓存工程实验。

## 项目结构

```text
PythonProject/
├── week17-async/     # Python 异步与并发编程
├── week18-redis/     # Redis 与后端缓存工程
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

## 技术栈

Python · asyncio · FastAPI · MySQL · Redis · PyMySQL · redis-py

## 学习目标

通过独立实验掌握 Python 后端开发中的并发处理、数据库操作、缓存设计和异常处理，逐步提升实际工程开发能力。

本项目主要用于学习与实践，不作为生产级系统使用。