import socket

# 创建TCP/IP套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP地址和端口
server_address = ('localhost', 8001)  # 替换为你的服务器IP
server_socket.bind(server_address)

# 开始监听连接
server_socket.listen(5)
print('Waiting for a client to connect...')

connection, client_address = server_socket.accept()
print('Connected to', client_address)

try:
    while True:
        # 接收数据
        data = connection.recv(1024)
        if not data or data.decode().lower() == 'exit':
            print("Client disconnected")
            break
        print('Client:', data.decode())

        # 服务器发送响应
        message = input("Server: ")
        if message.lower() == 'exit':
            connection.sendall(message.encode())
            print("Closing connection...")
            break
        connection.sendall(message.encode())
finally:
    connection.close()