import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("连接数据库aiqt成功！")
    except Error as e:
        print(f"连接数据库aiqt失败：'{e}' ")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("执行查询成功！")
    except Error as e:
        print(f"执行查询错误： '{e}' 致命错误")