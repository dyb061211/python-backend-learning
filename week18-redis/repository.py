import pymysql

def get_connection(password):
    return pymysql.connect(
        user='backend_user',
        password=password,
        host='127.0.0.1',
        port=3306,
        database="week18_catalog_demo",
        charset='utf8mb4',
        autocommit=False,
        cursorclass=pymysql.cursors.DictCursor
    )

def get_run_id(connection,product_id):
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM products WHERE id=%s',
            (product_id,)
        )
        return cursor.fetchone()

def update_run_id(connection,product_id,price):
    with connection.cursor() as cursor:
        cursor.execute(
            'UPDATE products SET price=%s WHERE id=%s',
            (price, product_id)
        )
        connection.commit()