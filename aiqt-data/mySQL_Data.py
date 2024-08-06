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
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# 示例用法
connection = create_connection("35.175.245.164", "aiqt", "Aiqt@2024", "aiqt")

# 示例查询：创建一个表
create_table_query = """
CREATE TABLE IF NOT EXISTS test_table (
  id INT AUTO_INCREMENT, 
  name TEXT NOT NULL, 
  age INT, 
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""
execute_query(connection, create_table_query)

# 示例查询：插入数据
insert_data_query = """
INSERT INTO test_table (name, age) VALUES ('John Doe', 28)
"""
execute_query(connection, insert_data_query)

