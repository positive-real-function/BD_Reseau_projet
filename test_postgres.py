import psycopg2
from psycopg2 import OperationalError

# 测试连接函数
def test_postgres_connection():
    # PostgreSQL 数据库连接信息
    db_host = "localhost"  # 数据库地址
    db_name = "test_tcp_db"  # 数据库名称
    db_user = "jinzhuoyuan"  # 数据库用户名
    db_password = "123456"  # 数据库密码

    try:
        # 尝试连接到 PostgreSQL 数据库
        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )

        # 创建一个游标来执行 SQL 查询
        cursor = connection.cursor()

        # 执行 SQL 语句来测试连接
        cursor.execute("SELECT version();")
        # 获取查询结果
        db_version = cursor.fetchone()
        print(f"数据库版本: {db_version}")

        # 查询tickets表的所有值
        cursor.execute("SELECT * FROM tickets WHERE ticket_code=123456789;")
        tickets = cursor.fetchall()  # 获取所有记录

        print("tickets表的所有记录:")
        for ticket in tickets:
            print(ticket)  # 打印每一条记录

        # 关闭游标和连接
        cursor.close()
        connection.close()

        print("连接成功，连接已关闭。")

    except OperationalError as e:
        print(f"连接失败: {e}")

# 调用测试函数
if __name__ == "__main__":
    test_postgres_connection()