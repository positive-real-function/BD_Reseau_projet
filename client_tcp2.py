import socket

# 创建TCP/IP套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务器
server_address = ('localhost', 8001)  # 替换为服务器的IP
client_socket.connect(server_address)

try:
    while True:
        # 客户端发送数据
        message = input("Client: ")
        client_socket.sendall(message.encode())
        if message.lower() == 'exit':
            print("Closing connection...")
            break

        # 接收服务器响应
        data = client_socket.recv(1024)
        if not data or data.decode().lower() == 'exit':
            print("Server disconnected")
            break
        print('Server:', data.decode())
finally:
    client_socket.close()