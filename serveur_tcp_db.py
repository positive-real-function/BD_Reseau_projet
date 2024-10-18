import socket
import psycopg2
from psycopg2 import OperationalError, ProgrammingError, InterfaceError

# PostgreSQL 连接信息
DB_HOST = "localhost"
DB_NAME = "test_tcp_db"
DB_USER = "jinzhuoyuan"  # 替换为你的数据库用户名
DB_PASSWORD = "123456"  # 替换为你的数据库密码

def get_ticket_info(qr_code):
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
        # cursor.execute("SELECT version();")
        # 获取查询结果
        # db_version = cursor.fetchone()
        # print(f"数据库版本: {db_version}")

        # 查询tickets表的所有值
        cursor.execute("SELECT * FROM tickets WHERE ticket_code=%s;", (qr_code,))
        tickets = cursor.fetchall()  # 获取记录

        print('information:')
        for ticket in tickets:
            print(ticket)  # 打印每一条记录

        # 关闭游标和连接
        cursor.close()
        connection.close()

        print("Connexion réussie, connexion fermée.")  # 输出连接成功信息

    except OperationalError as e:
        print(f"Échec de la connexion: {e}")  # 输出连接失败信息

# 服务器启动代码
def start_server():
    host = "localhost"  # 服务器地址
    port = 8001  # 服务器端口

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Serveur démarré, en attente de connexion client...")  # 输出服务器启动信息

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Client {addr} connecté")  # 输出客户端连接信息

        with client_socket:
            while True:
                qr_code = client_socket.recv(1024).decode('utf-8')
                if not qr_code or qr_code.lower() == "exit":
                    print(f"Client {addr} déconnecté")  # 输出客户端断开连接信息
                    break

                print(f"QR code reçu: {qr_code}")  # 输出收到的二维码

                # 测试数据库连接
                # test_postgres_connection()

                # 查询数据库并返回结果
                get_ticket_info(qr_code)


if __name__ == "__main__":
    start_server()