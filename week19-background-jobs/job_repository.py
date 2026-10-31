import os
import pymysql
from settings import settings


def insert_pending_job(task_id: str, request_id: str, product_id: int):
    conn = pymysql.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password.get_secret_value(),
        database=settings.mysql_database,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit = False
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO job_runs
                    (task_id, request_id, product_id, status)
                VALUES (%s, %s, %s, %s)
                """,
                (task_id, request_id, product_id, "PENDING")
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def update_job_status(task_id: str, status: str,result_status: str | None = None,error_message: str | None = None):
    conn = pymysql.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password.get_secret_value(),
        database=settings.mysql_database,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE job_runs
                SET status = %s,
                    result_status = %s,
                    error_message = %s
                WHERE task_id = %s
                """,
                (status, result_status, error_message, task_id)
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_job_runs(limit: int = 10):
    conn = pymysql.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password.get_secret_value(),
        database=settings.mysql_database,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id, request_id,product_id, status, result_status
                FROM job_runs
                ORDER BY created_at DESC,task_id DESC
                LIMIT %s
                """,
                (limit,)
            )
            return cursor.fetchall()
    finally:
        conn.close()

def get_job_by_task_id(task_id: str):
    conn=pymysql.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password.get_secret_value(),
        database=settings.mysql_database,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id FROM job_runs WHERE task_id=%s
                """,
                (task_id,)
            )
            return cursor.fetchone()
    finally:
        conn.close()