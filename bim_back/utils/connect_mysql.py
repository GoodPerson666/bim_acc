# 连接 MySQL 数据库
import pymysql

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        database='bim',
        cursorclass=pymysql.cursors.DictCursor
    )
