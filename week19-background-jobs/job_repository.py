import os
import pymysql


def insert_pending_job(task_id: str, request_id: str, product_id: int):
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=os.environ["MYSQL_PASSWORD"],
        database="week19_demo",
        autocommit=False
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
        host="127.0.0.1",
        port=3306,
        user="root",
        password=os.environ["MYSQL_PASSWORD"],
        database="week19_demo",
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
        host="127.0.0.1",
        port=3306,
        user="root",
        password=os.environ["MYSQL_PASSWORD"],
        database="week19_demo",
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id, request_id,product_id, status, result_status
                FROM job_runs
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (limit,)
            )
            return cursor.fetchall()
    finally:
        conn.close()